#!/usr/bin/env python3
"""measure_outline.py — mede a ESPESSURA DO CONTORNO separado do sombreado interno.

Método: contorno = linha escura conectada à borda da silhueta; espessura = área do contorno ÷
perímetro da silhueta (para uma faixa fechada de largura w em volta da forma, área = w × perímetro).
Validado contra retângulos sintéticos de 1 a 12 px: erro < 8%.

Histórico do método (importa): duas tentativas anteriores mediram errado —
  1) `2 × média(EDT)` na faixa: devolve ~w/2 (subestima pela metade);
  2) faixa recortada por dilatação de 2 px: satura em 2,67 px para QUALQUER linha ≥ 3 px.
Com o método atual, o mesmo lote de 18 peças é reavaliado do zero.

    python tools/measure_outline.py exports/individual_png/body_m_v1 -o report.json --ppu 2
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

LUM_LINE = 90


def measure(path: Path) -> dict | None:
    a = np.array(Image.open(path).convert("RGBA"))
    alpha = a[..., 3] > 127
    if alpha.sum() < 400:
        return None
    lum = a[..., :3].astype(float) @ [0.299, 0.587, 0.114]
    dark = alpha & (lum < LUM_LINE)
    inner = ndimage.binary_erosion(alpha, np.ones((3, 3), bool))
    border = alpha & ~inner
    seed = dark & border
    if seed.sum() < 20 or border.sum() < 20:
        return None
    lab, _ = ndimage.label(dark)
    ids = [i for i in set(np.unique(lab[seed]).tolist()) if i != 0]
    contour = np.isin(lab, ids)
    c_area, p_len = int(contour.sum()), int(border.sum())
    shade_area = int(dark.sum()) - c_area
    return {"file": path.name,
            "contour_px": round(c_area / p_len, 2),
            "contour_area": c_area, "silhouette_perimeter": p_len,
            "shade_area_frac_of_dark": round(shade_area / max(int(dark.sum()), 1), 2),
            "piece_h_px": int(a.shape[0])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--ppu", type=float, default=2.0)
    ap.add_argument("--ref-height-u", type=float, default=200.0)
    ap.add_argument("--glob", default="*.png")
    ap.add_argument("--target-lohi", nargs=2, type=float, default=[1.6, 2.8],
                    help="faixa alvo em px @1x (coherence_standard C3)")
    a = ap.parse_args()
    rows, missing = [], []
    for f in sorted(Path(a.dir).glob(a.glob)):
        m = measure(f)
        (rows.append(m) if m else missing.append(f.name))
    vals = [r["contour_px"] for r in rows]
    med = float(np.median(vals)) if vals else None
    med1x = med / a.ppu if med else None
    lo, hi = a.target_lohi
    rep = {"parts_measured": len(rows), "parts_skipped": missing,
           "unit": "px na escala das peças",
           "contour_median_px": round(med, 2) if med else None,
           "contour_median_px_1x": round(med1x, 2) if med1x else None,
           "contour_pct_of_height_1x": round(med1x / a.ref_height_u * 100, 2) if med1x else None,
           "target_px_1x": [lo, hi],
           "pass": bool(med1x and lo <= med1x <= hi),
           "verdict": ("dentro do padrao" if med1x and lo <= med1x <= hi else
                       "abaixo do piso" if med1x and med1x < lo else
                       "acima do teto" if med1x else "sem dados"),
           "detail": rows}
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(rep, indent=2))
    print(json.dumps({k: rep[k] for k in ("parts_measured", "contour_median_px",
                                          "contour_median_px_1x", "contour_pct_of_height_1x",
                                          "verdict")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
