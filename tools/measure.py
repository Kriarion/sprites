#!/usr/bin/env python3
"""measure.py — mede proporções de um corpo inteiro para controle de drift.

    python tools/measure.py body.png --report out.json --overlay out.png

Mede, em px: altura total, altura de cabeça (topo -> ponto mais estreito na região do
pescoço), número de cabeças, largura de ombros/quadril, comprimento de perna.
Converte para unidades de rig (u) assumindo body_height_u (default 200).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from key import border_color, build_alpha, despeckle


def silhouette(path: Path) -> np.ndarray:
    rgb = np.array(Image.open(path).convert("RGB"))
    key = border_color(rgb)
    a = build_alpha(rgb, key, 60, 110)
    a, _ = despeckle(a, 4000)
    return a.astype(bool)


def measure(mask: np.ndarray, body_height_u: float = 200.0) -> dict:
    ys, xs = np.where(mask)
    top, bottom = int(ys.min()), int(ys.max())
    h = bottom - top + 1
    widths = mask.sum(axis=1).astype(float)
    max_w = widths.max()
    # 1) região da cabeça: primeira linha com largura relevante
    head_rows = np.where(widths > max_w * 0.18)[0]
    head_start = int(head_rows[0]) if len(head_rows) else top
    # 2) pescoço: mínimo de largura entre 8% e 30% da altura, após a cabeça
    lo = head_start + int(h * 0.08)
    hi = min(top + int(h * 0.32), bottom)
    seg = widths[lo:hi]
    neck_y = lo + int(np.argmin(seg)) if len(seg) else head_start + int(h * 0.16)
    head_h = max(neck_y - head_start, 1)

    torso = slice(neck_y, neck_y + int(h * 0.18))
    shoulder_w = int(widths[torso].max())
    hip_band = slice(top + int(h * 0.48), top + int(h * 0.58))
    hip_w = int(widths[hip_band].max())
    leg_h = int(h * 0.50)

    scale = body_height_u / h
    return {
        "body_height_px": h,
        "head_height_px": head_h,
        "heads_tall": round(h / head_h, 2),
        "shoulder_width_px": shoulder_w,
        "hip_width_px": hip_w,
        "head_height_u": round(head_h * scale, 1),
        "shoulder_width_u": round(shoulder_w * scale, 1),
        "hip_width_u": round(hip_w * scale, 1),
        "leg_length_u_est": round(leg_h * scale, 1),
        "neck_y_px": neck_y,
        "bbox": [int(xs.min()), top, int(xs.max()), bottom],
        "px_per_u": round(h / body_height_u, 3),
    }


def overlay(path: Path, m: dict, out: Path):
    img = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = m["bbox"]
    d.rectangle([x0, y0, x1, y1], outline=(0, 255, 255, 200), width=2)
    d.line([(x0, m["neck_y_px"]), (x1, m["neck_y_px"])], fill=(255, 80, 80, 230), width=2)
    d.line([(x0, y0 + (m["neck_y_px"] - y0) * 2), (x1, y0 + (m["neck_y_px"] - y0) * 2)],
           fill=(255, 200, 80, 200), width=1)
    d.line([(x0, y1 - (m["neck_y_px"] - y0)), (x1, y1 - (m["neck_y_px"] - y0))],
           fill=(255, 200, 80, 200), width=1)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def components(mask: np.ndarray, min_area: int = 3000):
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        sub = lab == i
        if sub.sum() < min_area:
            continue
        ys, xs = np.where(sub)
        out.append((int(xs.min()), int(ys.min()), sub))
    out.sort(key=lambda t: (t[0], t[1]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--body-height-u", type=float, default=200)
    ap.add_argument("--report", default=None)
    ap.add_argument("--overlay", default=None)
    ap.add_argument("--per-component", action="store_true")
    a = ap.parse_args()
    mask = silhouette(Path(a.image))
    if a.per_component:
        figs = components(mask)
        res = []
        for i, (x0, y0, sub) in enumerate(figs):
            m = measure(sub, a.body_height_u)
            m["figure_index"] = i
            res.append(m)
            if a.overlay and i == 0:
                overlay(Path(a.image), m, Path(a.overlay))
        if a.report:
            Path(a.report).parent.mkdir(parents=True, exist_ok=True)
            Path(a.report).write_text(json.dumps({"figures": res}, indent=2))
        print(json.dumps({"figures": [{k: r[k] for k in
              ("figure_index", "body_height_px", "heads_tall", "head_height_u",
               "shoulder_width_u", "hip_width_u")} for r in res]}, indent=2))
        return 0
    m = measure(mask, a.body_height_u)
    if a.report:
        Path(a.report).parent.mkdir(parents=True, exist_ok=True)
        Path(a.report).write_text(json.dumps(m, indent=2))
    if a.overlay:
        overlay(Path(a.image), m, Path(a.overlay))
    print(json.dumps(m, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
