#!/usr/bin/env python3
"""contactsheet.py — folha de contato rotulada de um lote de pecas (fecha BL-016).

    python tools/contactsheet.py exports/individual_png/body_m_v1/parts.json -o out.png

Motivo: indice de componente NAO e identidade semantica. Na DB-SESSION-0002 duas trocas
(mao<->pe, cabelo<->face) so apareceram quando as pecas foram olhadas lado a lado.
A folha e, portanto, etapa obrigatoria do processamento, nao extra.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw

CELL, PAD, LABEL = 150, 8, 16


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("parts_json")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--bg", default="28,28,32")
    a = ap.parse_args()
    doc = json.loads(Path(a.parts_json).read_text())
    d = Path(a.parts_json).parent
    parts = doc["parts"]
    rows = (len(parts) + a.cols - 1) // a.cols
    W = a.cols * (CELL + PAD) + PAD
    H = rows * (CELL + LABEL + PAD) + PAD
    img = Image.new("RGB", (W, H), tuple(int(x) for x in a.bg.split(",")))
    dr = ImageDraw.Draw(img)
    for i, p in enumerate(parts):
        cx = PAD + (i % a.cols) * (CELL + PAD)
        cy = PAD + (i // a.cols) * (CELL + LABEL + PAD)
        f = d / p["file"]
        if not f.exists():
            continue
        piece = Image.open(f).convert("RGBA")
        k = min((CELL - 8) / piece.width, (CELL - 8) / piece.height)
        piece = piece.resize((max(1, int(piece.width * k)), max(1, int(piece.height * k))), Image.NEAREST)
        img.paste(piece, (cx + (CELL - piece.width) // 2, cy + (CELL - piece.height) // 2), piece)
        name = p.get("part") or p.get("id")
        tag = f"L{p['layer']} {name}" + (" *" if p.get("shaded") else "") + (" v" if p.get("variant") else "")
        dr.text((cx + 2, cy + CELL + 2), tag[:26], fill=(230, 230, 235))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(a.out)
    print(json.dumps({"out": a.out, "parts": len(parts), "size": img.size,
                      "note": "* = camada traseira (half-shadow) · v = variante de pose"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
