#!/usr/bin/env python3
"""coherence.py — audita os seis invariantes de coerência do pacote (ADR-0007).

    python tools/coherence.py --registry production/asset_registry.json \
        --parts exports/individual_png/parts_body_v1 \
        --out production/coherence_report.json

C1 escala · C2 proporção · C3 contorno · C4 paleta · C5 half-shadow · C6 estrutura
Não corrige nada: mede e reprova.
"""
from __future__ import annotations

import argparse
import colorsys
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent

BACK_LAYERS = {2, 3, 4, 5, 6, 7, 8, 9}
FRONT_LAYERS = {1, 12, 13, 14, 18, 19, 20}

TOL = {
    "c1_height_u": 0.05,
    "c2_heads": (5.60, 6.20),
    "c2_joint_u": 4.0,
    "c3_line_ratio": (0.008, 0.014),
    "c4_dh": 8.0, "c4_ds": 0.10, "c4_dv": 0.10,
    "c5_half_shadow": 0.80,
}


def rgba(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGBA"))


def silhouette_metrics(path: Path) -> dict:
    a = rgba(path)[..., 3] > 127
    ys, xs = np.where(a)
    if len(ys) == 0:
        return {}
    top, bottom = int(ys.min()), int(ys.max())
    h = bottom - top + 1
    widths = a.sum(axis=1).astype(float)
    mx = widths.max()
    rel = np.where(widths > mx * 0.18)[0]
    head_start = int(rel[0]) if len(rel) else top
    lo = head_start + int(h * 0.08)
    hi = min(top + int(h * 0.34), bottom)
    seg = widths[lo:hi]
    neck_y = lo + int(np.argmin(seg)) if len(seg) else head_start + int(h * 0.17)
    head_h = max(neck_y - head_start, 1)
    return {
        "height_px": h,
        "head_px": head_h,
        "heads_tall": round(h / head_h, 2),
        "bbox": [int(xs.min()), top, int(xs.max()), bottom],
    }


def outline_ratio(path: Path, ref_height_px: int | None = None) -> float:
    """espessura media da linha escura / altura de referencia.

    A referencia e a ALTURA DO CORPO canonico (200 u * ppu), nao a altura da peca:
    uma peca de armadura de 300 px nao tem contorno 8x mais grosso que um corpo de 200 px.
    """
    rgba_arr = rgba(path)
    rgb = rgba_arr[..., :3].astype(float)
    a = rgba_arr[..., 3] > 127
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    dark = (lum < 60) & a
    if dark.sum() < 50:
        return 0.0
    # espessura media = area de linha / perimetro da silhueta  (estavel, sem ridge detection)
    perim = a & ~ndimage.binary_erosion(a, iterations=1)
    perim_n = int(perim.sum())
    if perim_n == 0:
        return 0.0
    thick = float(dark.sum()) / perim_n
    ys, _ = np.where(a)
    height = ref_height_px or int(ys.max() - ys.min() + 1)
    return round(thick / max(height, 1), 5)


def dominant_colors(path: Path, k: int = 5) -> list[tuple[float, float, float]]:
    arr = rgba(path)
    mask = arr[..., 3] > 200
    px = arr[mask][:, :3].astype(float)
    if len(px) < k * 10:
        return []
    # k-means leve determinístico
    rng = np.random.default_rng(7)
    cent = px[rng.choice(len(px), k, replace=False)]
    for _ in range(12):
        d = ((px[:, None, :] - cent[None, :, :]) ** 2).sum(axis=2)
        lab = d.argmin(axis=1)
        for i in range(k):
            if (lab == i).any():
                cent[i] = px[lab == i].mean(axis=0)
    out = []
    for c in cent:
        r, g, b = c / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        out.append((round(h * 360, 1), round(s, 3), round(v, 3)))
    return out


def palette_drift(cols, palette: dict, group: str | None = None) -> dict:
    """menor distancia HSV de cada cor amostrada a qualquer cor da paleta aprovada.

    Se `group` for informado (ex.: "body_neutral"), compara APENAS com aquele grupo:
    um corpo base cinza nao deve ser comparado com a paleta do Goku.
    """
    ref = []
    groups = [palette[group]] if group and group in palette else list(palette.values())
    for gr in groups:
        if isinstance(gr, dict):
            for v in gr.values():
                if isinstance(v, str) and v.startswith("#") and len(v) == 7:
                    r, g, b = (int(v[i:i + 2], 16) / 255 for i in (1, 3, 5))
                    h, ss, vv = colorsys.rgb_to_hsv(r, g, b)
                    ref.append((h * 360, ss, vv))
    for group in []:
        if isinstance(group, dict):
            for v in group.values():
                if isinstance(v, str) and v.startswith("#") and len(v) == 7:
                    r, g, b = (int(v[i:i + 2], 16) / 255 for i in (1, 3, 5))
                    h, s, vv = colorsys.rgb_to_hsv(r, g, b)
                    ref.append((h * 360, s, vv))
    if not ref or not cols:
        return {"evaluated": False}
    worst = {"dh": 0.0, "ds": 0.0, "dv": 0.0}
    for h, s, v in cols:
        achromatic = s < 0.12  # cinza/preto/branco: matiz e ruido, so o valor importa
        best, bd = None, 1e9
        for rh, rs, rv in ref:
            dh = min(abs(h - rh), 360 - abs(h - rh))
            d = dh / 360 * 3 + abs(s - rs) + abs(v - rv)
            if d < bd:
                bd, best = d, (dh, abs(s - rs), abs(v - rv))
        # cinza (S<0.12) ou tom escuro (V<0.25): matiz e saturacao sao perceptualmente ruido.
        # Nesses casos so o VALOR (luminosidade) participa da comparacao.
        low_perception = achromatic or v < 0.25
        if not low_perception:
            worst["dh"] = max(worst["dh"], best[0])
            worst["ds"] = max(worst["ds"], best[1])
        worst["dv"] = max(worst["dv"], best[2])
    return {"evaluated": True, "worst_dh": round(float(worst["dh"]), 1),
            "worst_ds": round(float(worst["ds"]), 2), "worst_dv": round(float(worst["dv"]), 2),
            "achromatic_colors_ignored": bool(any(s < 0.12 for _, s, _ in cols))}


def mean_lum(path: Path) -> float:
    arr = rgba(path)
    m = arr[..., 3] > 200
    if m.sum() < 50:
        return None
    px = arr[..., :3][m].astype(float)
    lum = 0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]
    return float(lum.mean())


def audit_parts(parts_dir: Path, palette_path: Path, ref_h: int = 200) -> dict:
    palette = json.loads(Path(palette_path).read_text())
    pal = {k: v for k, v in palette.items() if k not in ("global", "note", "palette_schema_version")}
    # achatado: todas as cores hex do arquivo
    flat = {"all": {}}
    for k, v in pal.items():
        if isinstance(v, dict):
            flat["all"].update({kk: vv for kk, vv in v.items() if isinstance(vv, str) and vv.startswith("#")})

    results = []
    for p in sorted(parts_dir.glob("*.png")):
        m = silhouette_metrics(p)
        results.append({
            "file": p.name,
            "heads_tall": m.get("heads_tall"),
            "outline_ratio": outline_ratio(p, ref_h),
            "dominant_hsv": dominant_colors(p, 4),
            "mean_lum": round(mean_lum(p), 1) if mean_lum(p) else None,
        })
    return {"palette_source": str(palette_path), "parts": results, "palette_flat": flat}


def evaluate(full_body_png: Path | None, parts_dir: Path | None, palette_path: Path,
             declared: dict | None = None, ref_h: int = 200,
             palette_group: str | None = None, parts_json: str | None = None) -> dict:
    inv = {}

    # C1 escala (por declaracao + medicao do corpo inteiro, se houver)
    if full_body_png and Path(full_body_png).exists():
        m = silhouette_metrics(Path(full_body_png))
        ppu = (declared or {}).get("pixels_per_unit", 1)
        body_u = m["height_px"] / ppu
        ok = bool(abs(body_u - 200) / 200 <= TOL["c1_height_u"])
        inv["C1_scale"] = {"pass": ok, "body_height_u": round(body_u, 1), "ppu": ppu,
                           "tolerance": "200 u ±5%"}
    else:
        inv["C1_scale"] = {"pass": None, "reason": "sem corpo inteiro para medir"}

    # C2 proporcao
    if full_body_png and Path(full_body_png).exists():
        m = silhouette_metrics(Path(full_body_png))
        lo, hi = TOL["c2_heads"]
        inv["C2_proportion"] = {"pass": bool(lo <= m["heads_tall"] <= hi),
                                "heads_tall": m["heads_tall"], "tolerance": f"{lo}–{hi}"}
    else:
        inv["C2_proportion"] = {"pass": None, "reason": "sem corpo inteiro"}

    # C3 contorno
    if parts_dir:
        ratios = [outline_ratio(p, ref_h) for p in sorted(Path(parts_dir).glob("*.png"))]
        ratios = [r for r in ratios if r > 0]
        if ratios:
            med = float(np.median(ratios))
            lo, hi = TOL["c3_line_ratio"]
            inv["C3_outline_weight"] = {"pass": bool(lo <= med <= hi), "median_ratio": round(med, 5),
                                        "tolerance": f"{lo}–{hi}", "samples": len(ratios)}
        else:
            inv["C3_outline_weight"] = {"pass": None, "reason": "sem pecas"}

    # C4 paleta
    if parts_dir:
        palette = json.loads(Path(palette_path).read_text())
        drift = palette_drift(dominant_colors(next(iter(sorted(Path(parts_dir).glob("*.png")))), 3)
                              if list(Path(parts_dir).glob("*.png")) else [], palette, palette_group)
        if drift.get("evaluated"):
            ok = (drift["worst_dh"] <= TOL["c4_dh"] and
                  drift["worst_ds"] <= TOL["c4_ds"] and
                  drift["worst_dv"] <= TOL["c4_dv"])
            inv["C4_palette"] = {"pass": bool(ok), **drift,
                                 "tolerance": "ΔH<=8° ΔS<=10% ΔV<=10%"}
        else:
            inv["C4_palette"] = {"pass": None, "reason": "paleta ou pecas ausentes"}

    # C5 half-shadow: luminancia media das pecas traseiras / frontais
    if parts_json:
        pj = json.loads(Path(parts_json).read_text())
        d = Path(parts_dir) if parts_dir else None
        if d:
            back = [p for p in pj["parts"] if p.get("shaded")]
            front = [p for p in pj["parts"] if not p.get("shaded") and not p.get("variant")]
            lb = [mean_lum(d / p["file"]) for p in back if (d / p["file"]).exists()]
            lf = [mean_lum(d / p["file"]) for p in front if (d / p["file"]).exists()]
            lb = [x for x in lb if x is not None]
            lf = [x for x in lf if x is not None]
            if lb and lf:
                ratio = (sum(lb) / len(lb)) / (sum(lf) / len(lf))
                inv["C5_half_shadow"] = {"pass": bool(ratio <= TOL["c5_half_shadow"]),
                                         "ratio": round(ratio, 3),
                                         "tolerance": f"<= {TOL['c5_half_shadow']}",
                                         "back_samples": len(lb), "front_samples": len(lf)}
            else:
                inv["C5_half_shadow"] = {"pass": None, "reason": "sem amostras front/back"}

    # C6 estrutura: ancoras, camadas, pivos
    if parts_json:
        pj = json.loads(Path(parts_json).read_text())
        ANCHORS = {"root", "pelvis", "spine_low", "spine_high", "neck", "head", "head_top",
                   "shoulder.front", "shoulder.back", "elbow.front", "elbow.back",
                   "wrist.front", "wrist.back", "grip.front", "grip.back",
                   "hip.front", "hip.back", "knee.front", "knee.back",
                   "ankle.front", "ankle.back", "toe.front", "toe.back",
                   "hair.front", "hair.back", "helm", "face"}
        bad_anchor, bad_layer, dup_layer, bad_pivot = [], [], [], []
        seen = {}
        for part in pj["parts"]:
            if part.get("variant"):
                continue
            if part["anchor"] not in ANCHORS:
                bad_anchor.append(part["id"])
            if not (-10 <= part["layer"] <= 30):
                bad_layer.append(part["id"])
            fl = part.get("file")
            if fl:
                try:
                    w, h = Image.open(Path(parts_dir) / fl).size
                    px, py = part["pivot_px"]
                    if not (0 <= px <= w and 0 <= py <= h):
                        bad_pivot.append(part["id"])
                except Exception:
                    bad_pivot.append(part["id"])
            if part["layer"] in seen and seen[part["layer"]] != part["id"]:
                dup_layer.append(f"{part['id']}@{part['layer']} vs {seen[part['layer']]}")
            seen[part["layer"]] = part["id"]
        ok = not (bad_anchor or bad_layer or bad_pivot)
        inv["C6_structure"] = {"pass": bool(ok), "bad_anchor": bad_anchor,
                               "bad_layer": bad_layer, "bad_pivot": bad_pivot,
                               "layer_collisions": dup_layer,
                               "note": "colisao de camada nao reprova: pecas alternativas (fist/grip) compartilham camada"}

    return inv


def score(inv: dict) -> dict:
    ev = [v for v in inv.values() if v.get("pass") is not None]
    ok = [v for v in ev if v["pass"] is True]
    pct = round(100 * len(ok) / len(ev), 1) if ev else None
    return {"evaluated": len(ev), "passed": len(ok), "coherence_score": pct}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-body", default=None)
    ap.add_argument("--parts", default=None)
    ap.add_argument("--palette", default="references/palettes/core_palettes.json")
    ap.add_argument("--ppu", type=int, default=1)
    ap.add_argument("--out", default="production/coherence_report.json")
    ap.add_argument("--measure-parts", action="store_true")
    ap.add_argument("--palette-group", default=None,
                    help="grupo da paleta do asset (ex.: body_neutral, characters/goku_base)")
    ap.add_argument("--parts-json", default=None,
                    help="parts.json do pack_parts: avalia proporcao pelo rig (confiavel) e nao pela silhueta")
    ap.add_argument("--ref-height-px", type=int, default=200,
                    help="altura do corpo canonico em px na escala das pecas (200 * ppu)")
    a = ap.parse_args()

    inv = evaluate(a.full_body, a.parts, Path(a.palette), {"pixels_per_unit": a.ppu},
                   a.ref_height_px, a.palette_group, a.parts_json)

    # C2 por rig (preferencial): proporcao = altura canonica da cabeca / altura do corpo
    if a.parts_json and Path(a.parts_json).exists():
        pj = json.loads(Path(a.parts_json).read_text())
        dims = json.loads(Path("tools/templates/part_dims.json").read_text()) \
            if Path("tools/templates/part_dims.json").exists() else {}
        head = next((p for p in pj["parts"] if p["id"] == "head"), None)
        body_u = pj.get("body_height_u", 200)
        if head and head["size_px"][1]:
            ppu = pj.get("scale_px_per_u", 2)
            head_u = head["size_px"][1] / ppu
            heads = body_u / head_u
            lo, hi = TOL["c2_heads"]
            inv["C2_proportion"] = {
                "pass": bool(lo <= heads <= hi),
                "method": "rig_defined",
                "head_u": round(head_u, 1), "body_u": body_u,
                "heads_tall": round(heads, 2), "tolerance": f"{lo}–{hi}",
                "note": "medido pelo rig (tamanho canonico da peca), nao pela silhueta" if a.full_body
                        else "medido pelo rig",
            }
    rep = {"standard": "docs/coherence_standard.md v1.0.0",
           "tolerances": TOL, "invariants": inv, **score(inv)}
    if a.measure_parts and a.parts:
        rep["part_metrics"] = audit_parts(Path(a.parts), Path(a.palette), a.ref_height_px)["parts"]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=2))
    print(json.dumps({"score": rep["coherence_score"], "evaluated": rep["evaluated"],
                      "invariants": {k: v.get("pass") for k, v in inv.items()}}, indent=2))
    return 0 if rep["coherence_score"] in (None, 100.0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
