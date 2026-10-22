#!/usr/bin/env python3
"""cellstats.py — auditoria de folha em grade (cell-fit, fragmentos, ocupação).

Não recorta nada: mede. Serve para decidir, com número, se uma folha gerada pode ser
decomposta (gate G2 / ADR-0001 §2.3) ou se precisa de correção.

    python tools/cellstats.py sheet.png --cols 4 --rows 4 -o report.json --overlay out.png
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

from key import border_color, build_alpha, despeckle


def analyze(path: Path, cols: int, rows: int, t_low: float, t_high: float, min_area: int):
    rgb = np.array(Image.open(path).convert("RGB"))
    key = border_color(rgb)
    alpha = build_alpha(rgb, key, t_low, t_high)
    alpha, _ = despeckle(alpha, min_area)
    h, w = alpha.shape
    cw, ch = w // cols, h // rows

    cells = []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = c * cw, r * ch
            sub = alpha[y0:y0 + ch, x0:x0 + cw] > 0
            idx = r * cols + c
            area = int(sub.sum())
            if area == 0:
                cells.append({"index": idx, "row": r, "col": c, "empty": True,
                              "coverage": 0.0, "fragments": 0})
                continue
            ys, xs = np.where(sub)
            bb = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
            lab, n = ndimage.label(sub)
            sizes = ndimage.sum(sub, lab, range(1, n + 1)) if n else np.array([])
            frag = int((sizes > cw * ch * 0.004).sum())
            cells.append({
                "index": idx, "row": r, "col": c, "empty": False,
                "coverage": round(area / (cw * ch), 3),
                "bbox": bb,
                "size": [bb[2] - bb[0], bb[3] - bb[1]],
                "fragments": frag,
                "touches_gutter": bool(bb[0] < 4 or bb[1] < 4 or
                                       bb[2] > cw - 4 or bb[3] > ch - 4),
            })
    return {"file": str(path), "image_size": [w, h], "grid": [cols, rows],
            "cell_px": [cw, ch], "key_color": [int(v) for v in key],
            "covered_cells": sum(1 for c in cells if not c["empty"]),
            "multi_fragment_cells": sum(1 for c in cells if c.get("fragments", 0) > 1),
            "gutter_violations": sum(1 for c in cells if c.get("touches_gutter")),
            "cells": cells}


def overlay(path: Path, rep: dict, out: Path):
    img = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    font = ImageFont.load_default()
    cw, ch = rep["cell_px"]
    for c in rep["cells"]:
        x0, y0 = c["col"] * cw, c["row"] * ch
        color = (0, 200, 0, 170) if not c["empty"] else (120, 120, 120, 120)
        if c.get("fragments", 0) > 1:
            color = (255, 160, 0, 220)
        if c.get("touches_gutter"):
            color = (255, 0, 0, 220)
        d.rectangle([x0, y0, x0 + cw - 1, y0 + ch - 1], outline=color, width=2)
        label = f"{c['index']}"
        if not c["empty"]:
            label += f" f{c['fragments']}"
        d.text((x0 + 6, y0 + 5), label, fill=color, font=font)
        if not c["empty"]:
            bb = c["bbox"]
            d.rectangle([x0 + bb[0], y0 + bb[1], x0 + bb[2], y0 + bb[3]],
                        outline=(0, 160, 255, 200), width=1)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--rows", type=int, default=4)
    ap.add_argument("--t-low", type=float, default=60)
    ap.add_argument("--t-high", type=float, default=110)
    ap.add_argument("--min-area", type=int, default=600)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--overlay", default=None)
    a = ap.parse_args()

    rep = analyze(Path(a.image), a.cols, a.rows, a.t_low, a.t_high, a.min_area)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=2))
    if a.overlay:
        overlay(Path(a.image), rep, Path(a.overlay))
    print(json.dumps({k: rep[k] for k in ("covered_cells", "multi_fragment_cells",
                                          "gutter_violations", "cell_px")}, indent=2))
    for c in rep["cells"]:
        if not c["empty"]:
            print(f"  cell {c['index']:2d} r{c['row']}c{c['col']}: cov={c['coverage']:.2f} "
                  f"size={c['size']} frags={c['fragments']} gutter={c['touches_gutter']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
