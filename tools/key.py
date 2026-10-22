#!/usr/bin/env python3
"""key.py — chroma-key removal com alpha real, despill e limpeza.

Entrada: PNG com fundo chapado (magenta/verde/branco).
Saída:   PNG RGBA com alpha real, bordas tratadas, bbox aparado (trim).

Não aprova nada: apenas processa. Uso:
    python tools/key.py in.png -o out.png --report report.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def border_color(rgb: np.ndarray) -> np.ndarray:
    """Cor dominante da moldura de 2 px — a cor de fundo presumida."""
    band = 2
    edges = np.concatenate([
        rgb[:band, :, :].reshape(-1, 3),
        rgb[-band:, :, :].reshape(-1, 3),
        rgb[:, :band, :].reshape(-1, 3),
        rgb[:, -band:, :].reshape(-1, 3),
    ])
    return np.median(edges, axis=0)


def build_alpha(rgb: np.ndarray, key: np.ndarray, t_low: float, t_high: float) -> np.ndarray:
    """Distância de cor -> alpha suave, depois binarizado com 1 px de matte."""
    dist = np.sqrt(((rgb - key[None, None, :]) ** 2).sum(axis=2))
    alpha = np.clip((dist - t_low) / max(t_high - t_low, 1e-6), 0.0, 1.0)
    hard = (alpha > 0.5).astype(np.uint8)
    # remove poeira de keying (abertura) e fecha furos de anti-aliasing
    hard = ndimage.binary_opening(hard, np.ones((2, 2)))
    hard = ndimage.binary_closing(hard, np.ones((3, 3)))
    hard = ndimage.binary_fill_holes(hard)
    return hard


def despeckle(alpha: np.ndarray, min_area: int) -> tuple[np.ndarray, int]:
    lab, n = ndimage.label(alpha)
    if n == 0:
        return alpha, 0
    sizes = ndimage.sum(alpha, lab, range(1, n + 1))
    keep = np.zeros(n + 1, dtype=bool)
    keep[1:] = sizes >= min_area
    removed = int((~keep[1:]).sum())
    return keep[lab].astype(np.uint8), removed


def despill(rgb: np.ndarray, alpha: np.ndarray, key: np.ndarray, radius: int) -> np.ndarray:
    """Neutraliza a cor-chave que vazou nas bordas (halo)."""
    edge = alpha.astype(bool) & ~ndimage.binary_erosion(alpha.astype(bool), iterations=radius)
    if not edge.any():
        return rgb
    out = rgb.astype(np.float32).copy()
    k = np.argmax(key)  # canal dominante do key (ex.: G do magenta? magenta = R+B)
    others = [c for c in range(3) if c != k]
    # tonelada de key: reduzir os dois canais fortes do key nas bordas
    key_chan = [c for c in range(3) if key[c] > 128]
    for c in key_chan:
        out[..., c] = np.where(edge, out[..., c] * 0.55 + out[..., others].mean(axis=-1) * 0.45, out[..., c])
    return np.clip(out, 0, 255).astype(np.uint8)


def trim(rgb: np.ndarray, alpha: np.ndarray, pad: int):
    ys, xs = np.where(alpha > 0)
    if len(ys) == 0:
        return None, None, None
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, alpha.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, alpha.shape[1])
    return rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1], (int(x0), int(y0), int(x1), int(y1))


def key_image(path: Path, out: Path, bg: str | None, t_low: float, t_high: float,
              min_area: int, pad: int, despill_radius: int, keep_canvas: bool):
    img = Image.open(path)
    mode = img.mode
    rgb = np.array(img.convert("RGB"))
    key = border_color(rgb)
    if bg and bg.lower() != "auto":
        key = np.array([int(bg[i:i + 2], 16) for i in (1, 3, 5)], dtype=float)

    alpha = build_alpha(rgb, key, t_low, t_high)
    alpha, removed = despeckle(alpha, min_area)
    rgb2 = despill(rgb, alpha, key, despill_radius)

    coverage = alpha.mean()
    # halo = pixel de PEÇA (alpha>0) cuja cor ainda está perto do key
    dist = np.sqrt(((rgb - key[None, None, :]) ** 2).sum(axis=2))
    on_part = alpha > 0
    residue = float(((dist < 40) & on_part).sum() / max(int(on_part.sum()), 1))

    if keep_canvas:
        out_rgb, out_a, box = rgb2, alpha, (0, 0, rgb.shape[1], rgb.shape[0])
    else:
        out_rgb, out_a, box = trim(rgb2, alpha, pad)
        if out_rgb is None:
            raise SystemExit(f"ERRO: alpha vazio em {path} (key={key.tolist()})")

    rgba = np.dstack([out_rgb, (out_a * 255).astype(np.uint8)])
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(out, optimize=True)

    return {
        "input": str(path),
        "output": str(out),
        "input_mode": mode,
        "size_in": [int(rgb.shape[1]), int(rgb.shape[0])],
        "size_out": [int(rgba.shape[1]), int(rgba.shape[0])],
        "key_color": [int(c) for c in key],
        "alpha_coverage": round(float(coverage), 4),
        "key_halo_ratio": round(float(residue), 4),
        "speckles_removed": removed,
        "trim_box": [int(v) for v in box],
        "alpha_real": bool(alpha.min() == 0 and alpha.max() == 1),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--bg", default="auto", help="auto | #RRGGBB")
    ap.add_argument("--t-low", type=float, default=60.0)
    ap.add_argument("--t-high", type=float, default=110.0)
    ap.add_argument("--min-area", type=int, default=600)
    ap.add_argument("--pad", type=int, default=2)
    ap.add_argument("--despill-radius", type=int, default=2)
    ap.add_argument("--keep-canvas", action="store_true")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()

    rep = key_image(Path(a.input), Path(a.output), a.bg, a.t_low, a.t_high,
                    a.min_area, a.pad, a.despill_radius, a.keep_canvas)
    if a.report:
        Path(a.report).parent.mkdir(parents=True, exist_ok=True)
        Path(a.report).write_text(json.dumps(rep, indent=2))
    print(json.dumps(rep, indent=2))
    if rep["alpha_coverage"] < 0.005:
        print("FALHA: alpha praticamente vazio", flush=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
