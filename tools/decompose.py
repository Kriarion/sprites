#!/usr/bin/env python3
"""decompose.py — extrai peças de uma folha keyed usando template de grade.

Modos:
  grid        — corte por células declaradas no template (ADR-0001, modo primário)
  components  — segmentação por componentes conexos (modo de diagnóstico/fallback)

Saída: PNGs por peça + parts.json + relatório com cell-fit e métricas.

    python tools/decompose.py sheet.png --template tools/templates/PART_SHEET_A.json \
        -o out/parts --report out/decompose_report.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def load_rgba(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGBA")
    return np.array(img)


def bbox_of(mask: np.ndarray):
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def split_grid(rgba: np.ndarray, tpl: dict, outdir: Path, min_px: int):
    h, w = rgba.shape[:2]
    cols, rows = tpl["grid"]["cols"], tpl["grid"]["rows"]
    cell_w, cell_h = w / cols, h / rows
    content = tpl["content_px"]
    trim_pad = tpl.get("trim_px", 2)
    alpha = rgba[..., 3]

    parts, issues = [], []
    for cell in tpl["cells"]:
        part = cell.get("part")
        if not part:
            continue
        i = cell["index"]
        cx, cy = i % cols, i // cols
        x0, y0 = int(round(cx * cell_w)), int(round(cy * cell_h))
        x1, y1 = int(round((cx + 1) * cell_w)), int(round((cy + 1) * cell_h))
        sub = alpha[y0:y1, x0:x1] > 127
        bb = bbox_of(sub)
        if bb is None or sub.sum() < min_px:
            issues.append({"part": part, "issue": "cell_empty", "cell": i})
            continue

        pw, ph = bb[2] - bb[0], bb[3] - bb[1]
        # proximidade das bordas da célula (gutter): se toca, provável fusão entre peças
        gutter = tpl.get("gutter_px", 16) / 2
        touches = (bb[0] <= gutter) or (bb[1] <= gutter) or \
                  (bb[2] >= cell_w - gutter) or (bb[3] >= cell_h - gutter)
        fits = (pw <= content and ph <= content)
        if not fits:
            issues.append({"part": part, "issue": "content_overflow", "size": [pw, ph], "limit": content})
        if touches:
            issues.append({"part": part, "issue": "near_gutter", "bbox": list(bb)})

        # recorte com respiro e alpha preservado
        rx0, ry0 = max(bb[0] - trim_pad, 0), max(bb[1] - trim_pad, 0)
        rx1, ry1 = min(bb[2] + trim_pad, cell_w), min(bb[3] + trim_pad, cell_h)
        piece = rgba[y0 + ry0:y0 + ry1, x0 + rx0:x0 + rx1].copy()

        # zera qualquer resíduo fora da peça principal desta célula
        pm = piece[..., 3] > 127
        lab, n = ndimage.label(pm)
        if n > 1:
            sizes = ndimage.sum(pm, lab, range(1, n + 1))
            biggest = int(np.argmax(sizes)) + 1
            piece[..., 3] = np.where(lab == biggest, piece[..., 3], 0)

        name = f"{part}.png"
        Image.fromarray(piece, "RGBA").save(outdir / name, optimize=True)

        pv = cell.get("pivot") or [0.5, 0.5]
        pivot_px = [round(pv[0] * piece.shape[1], 2), round(pv[1] * piece.shape[0], 2)]
        parts.append({
            "part": part,
            "file": name,
            "cell": i,
            "layer": cell.get("layer"),
            "anchor": cell.get("anchor"),
            "shaded": cell.get("shaded", False),
            "size_px": [int(piece.shape[1]), int(piece.shape[0])],
            "bbox_in_cell": [int(v) for v in bb],
            "cell_fit": bool(fits and not touches),
            "pivot_px": pivot_px,
            "pivot_norm": [round(pivot_px[0] / piece.shape[1], 4), round(pivot_px[1] / piece.shape[0], 4)],
        })
    return parts, issues


def split_components(rgba: np.ndarray, outdir: Path, min_px: int, max_parts: int = 24):
    """Fallback: componentes conexos do alpha, ordenados em leitura (linha, coluna)."""
    mask = rgba[..., 3] > 127
    lab, n = ndimage.label(mask)
    comps = []
    for i in range(1, n + 1):
        sub = lab == i
        if sub.sum() < min_px:
            continue
        bb = bbox_of(sub)
        comps.append((bb, int(sub.sum()), i))
    comps.sort(key=lambda c: (c[0][1] // 64, c[0][0]))
    comps = comps[:max_parts]

    parts, issues = [], []
    for idx, (bb, area, lid) in enumerate(comps):
        x0, y0, x1, y1 = bb
        piece = rgba[y0:y1, x0:x1].copy()
        piece[..., 3] = np.where(lab[y0:y1, x0:x1] == lid, piece[..., 3], 0)
        name = f"component_{idx:02d}.png"
        Image.fromarray(piece, "RGBA").save(outdir / name, optimize=True)
        parts.append({
            "part": f"unlabeled_{idx:02d}",
            "file": name,
            "cell": None,
            "layer": None,
            "anchor": None,
            "size_px": [int(piece.shape[1]), int(piece.shape[0])],
            "bbox": [int(v) for v in bb],
            "area_px": area,
            "cell_fit": None,
            "pivot_px": [round(piece.shape[1] / 2, 2), round(piece.shape[0] / 2, 2)],
            "pivot_norm": [0.5, 0.5],
        })
    if len(comps) < 8:
        issues.append({"issue": "few_components", "count": len(comps)})
    return parts, issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sheet")
    ap.add_argument("--template", default=None)
    ap.add_argument("--mode", choices=["grid", "components", "auto"], default="auto")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--report", default=None)
    ap.add_argument("--min-px", type=int, default=2500)
    a = ap.parse_args()

    rgba = load_rgba(Path(a.sheet))
    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    issues: list[dict] = []
    mode = a.mode

    if mode in ("grid", "auto") and a.template:
        tpl = json.loads(Path(a.template).read_text())
        parts, issues = split_grid(rgba, tpl, outdir, a.min_px)
        expected = len([c for c in tpl["cells"] if c.get("part")])
        if mode == "auto" and len(parts) < max(3, expected * 0.5):
            issues.append({"issue": "grid_failed_fallback_to_components",
                           "found": len(parts), "expected": expected})
            for f in outdir.glob("*.png"):
                f.unlink()
            parts, more = split_components(rgba, outdir, a.min_px)
            issues += more
            mode = "components"
        tpl_name = tpl["template"]
    else:
        parts, issues = split_components(rgba, outdir, a.min_px)
        tpl_name, mode = None, "components"

    ok = [p for p in parts if p.get("cell_fit") is True]
    rep = {
        "sheet": str(a.sheet),
        "template": tpl_name,
        "mode_used": mode,
        "parts_found": len(parts),
        "parts_cell_fit": len(ok),
        "issues": issues,
        "parts": parts,
    }
    if a.report:
        Path(a.report).parent.mkdir(parents=True, exist_ok=True)
        Path(a.report).write_text(json.dumps(rep, indent=2, ensure_ascii=False))
        (outdir / "parts.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False))
    print(json.dumps({k: rep[k] for k in ("template", "mode_used", "parts_found", "parts_cell_fit")}, indent=2))
    return 0 if parts else 1


if __name__ == "__main__":
    raise SystemExit(main())
