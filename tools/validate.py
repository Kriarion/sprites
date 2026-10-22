#!/usr/bin/env python3
"""validate.py — validador do pacote (quality_checklist.md §7).

    python tools/validate.py            # valida registry, arquivos, schemas e ledger
    python tools/validate.py --png FILE # valida um PNG isolado (alpha real etc.)

Exit code != 0 se qualquer teste falhar. Não corrige nada.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ID_RE = re.compile(r"^DB_[A-Z]{3,8}_[A-Z]{2,12}_[A-Z0-9_]+$")
LAYERS = set(range(-10, 31))
STATUSES = {"PLANNED", "GENERATED", "PROCESSING", "QA_PENDING", "APPROVED",
            "REWORK_REQUIRED", "BLOCKED", "DEPRECATED"}

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    results.append((name, ok, detail))
    return ok


def png_report(path: Path) -> dict:
    img = Image.open(path)
    rgba = np.array(img.convert("RGBA"))
    a = rgba[..., 3]
    return {
        "mode": img.mode,
        "size": img.size,
        "has_transparent": bool((a == 0).any()),
        "has_opaque": bool((a == 255).any()),
        "alpha_coverage": round(float((a > 0).mean()), 4),
    }


def validate_png(path: Path) -> list[tuple[str, bool, str]]:
    out = []
    try:
        r = png_report(path)
    except Exception as exc:  # noqa: BLE001
        return [("png_opens", False, f"{path}: {exc}")]
    out.append((f"png_opens:{path.name}", True, str(r["size"])))
    out.append((f"alpha_real:{path.name}", r["has_transparent"] and r["has_opaque"], str(r)))
    out.append((f"alpha_coverage:{path.name}", r["alpha_coverage"] > 0.002,
                f"{r['alpha_coverage']:.4f}"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="append", default=[])
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if a.png:
        for p in a.png:
            for n, ok, d in validate_png(Path(p)):
                check(n, ok, d)
        return report(a.quiet)

    # ---- 1. registry ----
    reg_path = ROOT / "production/asset_registry.json"
    reg = json.loads(reg_path.read_text())
    ids, dup = set(), []
    for asset in reg["assets"]:
        aid = asset.get("asset_id", "")
        check(f"id_pattern:{aid}", bool(ID_RE.match(aid)), aid)
        if aid in ids:
            dup.append(aid)
        ids.add(aid)
        check(f"status_enum:{aid}", asset.get("status") in STATUSES, asset.get("status", ""))
        if asset.get("status") == "APPROVED":
            qa = asset.get("qa", {}).get("report")
            check(f"approved_has_qa:{aid}", bool(qa) and (ROOT / qa).exists(), str(qa))
            for f in asset.get("files", []):
                check(f"file_exists:{f}", (ROOT / f).exists(), f)
        for part in asset.get("parts", []):
            f = part.get("file")
            if f:
                check(f"part_exists:{f}", (ROOT / f).exists(), f)
            check(f"part_layer:{aid}:{part.get('id')}", part.get("layer") in LAYERS,
                  str(part.get("layer")))
    check("no_duplicate_ids", not dup, ",".join(dup))

    # ---- 2. contadores coerentes ----
    counts = {s: 0 for s in STATUSES}
    for asset in reg["assets"]:
        counts[asset.get("status", "PLANNED")] = counts.get(asset.get("status", "PLANNED"), 0) + 1
    declared = reg.get("counters", {}).get("by_status", {})
    check("registry_counters", all(declared.get(k, 0) == v for k, v in counts.items()),
          f"declared={declared} real={counts}")

    # ---- 3. ledger ----
    led = json.loads((ROOT / "production/generation_ledger.json").read_text())
    total = 0
    for s in led["sessions"]:
        sid = s["session_id"]
        calc = s["executed_new"] + s["executed_corrections"]
        check(f"ledger_sum:{sid}", calc == s["total_executed"],
              f"{s['executed_new']}+{s['executed_corrections']} vs {s['total_executed']}")
        check(f"ledger_cap:{sid}", s["total_executed"] <= 10, str(s["total_executed"]))
        total += s["total_executed"]
    check("ledger_totals_match", led["totals"]["generations_executed"] == total,
          f"{led['totals']['generations_executed']} vs {total}")

    # ---- 4. manifest × registry ----
    man = json.loads((ROOT / "asset_manifest.json").read_text())
    approved = [x["asset_id"] for x in reg["assets"] if x.get("status") == "APPROVED"]
    listed = [x["asset_id"] for x in man.get("assets", [])]
    check("manifest_matches_registry", sorted(approved) == sorted(listed),
          f"registry={len(approved)} manifest={len(listed)}")
    check("manifest_counts", man.get("counts", {}).get("total_approved", -1) == len(approved),
          str(man.get("counts", {}).get("total_approved")))

    # ---- 5. schemas parseáveis ----
    for s in (ROOT / "production/schemas").glob("*.json"):
        try:
            json.loads(s.read_text())
            check(f"schema_json:{s.name}", True)
        except Exception as exc:  # noqa: BLE001
            check(f"schema_json:{s.name}", False, str(exc))

    # ---- 6. templates ----
    for t in (ROOT / "tools/templates").glob("*.json"):
        tpl = json.loads(t.read_text())
        n = len([c for c in tpl["cells"] if c.get("part")])
        check(f"template_cells:{t.name}", n <= tpl["grid"]["cols"] * tpl["grid"]["rows"], str(n))
        for c in tpl["cells"]:
            if c.get("part") and c.get("layer") is not None:
                check(f"template_layer:{t.name}:{c['part']}", c["layer"] in LAYERS, str(c["layer"]))

    # ---- 7. continuity ----
    cont = json.loads((ROOT / "production/continuity_state.json").read_text())
    check("continuity_sessions_order",
          cont["last_completed_session"] < cont["next_session"],
          f"{cont['last_completed_session']} -> {cont['next_session']}")
    check("continuity_budget_cap", cont["gen_budget"]["max_per_session"] == 10,
          str(cont["gen_budget"]["max_per_session"]))

    return report(a.quiet)


def report(quiet: bool) -> int:
    fails = [r for r in results if not r[1]]
    if not quiet:
        for n, ok, d in results:
            if not ok:
                print(f"FAIL  {n}  {d}")
        print(f"\n{len(results)} testes, {len(results) - len(fails)} PASS, {len(fails)} FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
