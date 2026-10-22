#!/usr/bin/env python3
"""restroke.py — engrossa o CONTORNO (e só ele) por um número controlado de pixels de exportação.

Por que existe: o gerador entrega contorno de ~0,9% da altura da peça independentemente do que o
prompt pede (medido na DB-SESSION-0003: 2 folhas, 8 peças, mesma espessura do lote antigo). Como as
peças são reduzidas ~3,5x do mestre para o tamanho canônico, a linha chega ao 1x com ~1 px.

O que faz: separa a linha escura CONECTADA À BORDA (contorno) do sombreado interno, dilata **só o
contorno** e recompõe em supersampling para não serrilhar. O sombreado interno não é tocado.

    python tools/restroke.py exports/individual_png/body_m_v1 -o out_dir --add-px 1.0 --ss 3
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

LUM_LINE = 90


def _resize_premul(img: Image.Image, size: tuple[int, int], resample=Image.LANCZOS) -> Image.Image:
    """Redimensiona RGBA com alfa PREMULTIPLICADO.

    Sem isso, o RGB dos pixels transparentes (que num recorte por chroma key ainda guarda a cor
    do fundo, magenta) vaza para a borda no reamostragem e a peça ganha halo rosa.
    """
    a = np.array(img).astype(np.float32)
    al = a[..., 3:4] / 255.0
    pm = np.dstack([a[..., :3] * al, a[..., 3:4]])
    pm_img = Image.fromarray(np.clip(pm, 0, 255).astype(np.uint8), "RGBA").resize(size, resample)
    b = np.array(pm_img).astype(np.float32)
    al2 = np.clip(b[..., 3:4] / 255.0, 1e-6, 1.0)
    rgb = np.where(b[..., 3:4] > 0, b[..., :3] / al2, 0)
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), b[..., 3:4]]).astype(np.uint8), "RGBA")


def _despill(img: Image.Image, tol: int = 25) -> Image.Image:
    """Troca por cor limpa qualquer pixel com tingimento de key (magenta: R e B acima de G).

    O recorte por chroma key deixa esse resíduo nas bordas; ele só aparece quando a peça é
    composta sobre fundo que não seja magenta.
    """
    a = np.array(img).astype(np.int16)
    rgb, al = a[..., :3], a[..., 3]
    dirty = (al > 0) & ((rgb[..., 0] - rgb[..., 1] > tol) & (rgb[..., 2] - rgb[..., 1] > tol))
    if not dirty.any():
        return img
    clean = (al == 255) & ~dirty
    if clean.sum() == 0:
        return img
    _, idx = ndimage.distance_transform_edt(~clean, return_indices=True)
    ys, xs = idx[0], idx[1]
    out_rgb = rgb.copy()
    out_rgb[dirty] = rgb[ys[dirty], xs[dirty]]
    return Image.fromarray(np.dstack([np.clip(out_rgb,0,255).astype(np.uint8), a[...,3:4].astype(np.uint8)]), "RGBA")


def _edge_extend(img: Image.Image) -> Image.Image:
    """Copia a cor do pixel opaco mais próximo para os pixels de borda (alfa < 255).

    Elimina o halo do fundo (magenta do chroma key) que o reamostragem arrasta para a borda.
    """
    a = np.array(img)
    rgb = a[..., :3].astype(np.int16)
    al = a[..., 3]
    opaque = al >= 255
    if opaque.sum() == 0:
        return img
    _, idx = ndimage.distance_transform_edt(~opaque, return_indices=True)
    fixed = rgb.copy()
    ys, xs = idx[0], idx[1]
    fixed[~opaque] = rgb[ys[~opaque], xs[~opaque]]
    out = np.dstack([np.clip(fixed, 0, 255).astype(np.uint8), a[..., 3:4]])
    return Image.fromarray(out, "RGBA")


def restroke(img: Image.Image, add_px: float, ss: int = 3) -> tuple[Image.Image, dict]:
    img = _despill(img)
    big = _resize_premul(img, (img.width * ss, img.height * ss))
    a = np.array(big).astype(np.uint8)
    alpha = a[..., 3] > 127
    lum = a[..., :3].astype(float) @ [0.299, 0.587, 0.114]
    dark = alpha & (lum < LUM_LINE)
    inner = ndimage.binary_erosion(alpha, np.ones((3, 3), bool))
    border = alpha & ~inner
    seed = dark & border
    if seed.sum() < 20:
        return img, {"skipped": "sem contorno"}
    lab, _ = ndimage.label(dark)
    ids = [i for i in set(np.unique(lab[seed]).tolist()) if i != 0]
    contour = np.isin(lab, ids)
    r = max(1, int(round(add_px * ss / 2)))          # dilatação radial
    grown = ndimage.binary_dilation(contour, ndimage.generate_binary_structure(2, 2), iterations=r) & alpha
    ring = grown & ~contour
    col = np.median(a[contour][:, :3], axis=0).astype(np.uint8)
    out = a.copy()
    out[ring, 0:3] = col
    out[ring, 3] = 255
    res = _despill(_edge_extend(_resize_premul(Image.fromarray(out, "RGBA"), img.size)))
    return res, {"added_px_export": add_px, "ring_px": int(ring.sum()), "supersample": ss,
                 "line_color": col.tolist()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir_or_file")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--add-px", type=float, default=1.0, help="px somados à espessura (escala de exportação)")
    ap.add_argument("--ss", type=int, default=3)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    src = Path(a.dir_or_file)
    files = sorted(src.glob("*.png")) if src.is_dir() else [src]
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    log = []
    for f in files:
        im = Image.open(f).convert("RGBA")
        res, info = restroke(im, a.add_px, a.ss)
        res.save(out / f.name)
        log.append({"file": f.name, **info})
    if a.report:
        Path(a.report).write_text(json.dumps(log, indent=2))
    print(json.dumps({"out": str(out), "files": len(files), "add_px": a.add_px}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
