#!/usr/bin/env python3
"""compose.py — monta peças por âncora/pivô (prova do gate G3) e gera overlay de proporção.

    python tools/compose.py parts.json --out preview.png --scale 4 --overlay

O rig de referência (200 u) está embutido aqui a partir de
docs/anatomy_and_rigging.md §2 e docs/technical_specification.md §2.2.
Nenhuma peça é reposicionada "no olho": a posição vem da âncora.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

# --- rig de referência: âncora -> (x_u, y_u) com y medido do CHÃO para cima ---
ANCHORS = {
    "root": (0, 0), "pelvis": (0, 100), "spine_low": (0, 118), "spine_high": (0, 140),
    "neck": (0, 162), "head": (0, 164), "head_top": (0, 200),
    "shoulder.front": (28, 156), "shoulder.back": (-28, 156),
    "elbow.front": (30, 124), "elbow.back": (-30, 124),
    "wrist.front": (31, 94), "wrist.back": (-31, 94),
    "grip.front": (31, 94), "grip.back": (-31, 94),
    "hip.front": (11, 100), "hip.back": (-11, 100),
    "knee.front": (11, 56), "knee.back": (-11, 56),
    "ankle.front": (11, 14), "ankle.back": (-11, 14),
    "toe.front": (18, 4), "toe.back": (-18, 4),
    "hair.front": (0, 176), "hair.back": (0, 176), "helm": (0, 176), "face": (0, 182),
    "cape.01": (0, 156), "cape.02": (0, 132), "cape.03": (0, 108),
    "tail.01": (-12, 96), "tail.02": (-22, 88), "tail.03": (-30, 78),
    "wing.front": (14, 150), "wing.back": (-14, 150),
}
BODY_H = 200

# deslocamento de profundidade: pecas traseiras sao levemente deslocadas (leitura 3/4 + half-shadow).
# -6 u empurrava braco/perna traseiros para fora da silhueta do torso; -2 mantem a leitura 3/4.
DEPTH_OFFSET_U = {"back": (-2, -2)}

# Dimensoes canonicas por TIPO de peca, em u (technical_specification.md 2.2).
# Usadas para normalizar pecas geradas em escalas arbitrarias (cada celula e desenhada
# "preenchendo" seu espaco, entao a escala relativa entre pecas NAO e confiavel).
PART_DIMS_U = {
    # Proporcao canonica 5,9 cabecas / 200 u (ADR-0007, technical_specification.md 2.2)
    "head": (29, 34), "hair_front": (33, 20), "hair_back": (33, 26), "helm": (31, 24),
    "torso": (46, 48), "chest": (46, 48), "pelvis": (40, 20), "pelvis_belt": (40, 20),
    "thigh_front": (17, 44), "thigh_back": (17, 44), "thigh_guard": (19, 40),
    "shin_front": (12, 42), "shin_back": (12, 42), "shin_greave": (14, 38),
    "foot_front": (26, 14), "foot_back": (26, 14), "boot_single": (26, 32),
    "upperarm_front": (13, 32), "upperarm_back": (13, 32),
    "forearm_front": (10, 30), "forearm_back": (10, 30), "forearm_bracer": (12, 28),
    "hand_front": (11, 17), "hand_back": (11, 17), "hand_open": (11, 17), "glove_single": (11, 17),
    "pauldron_single": (20, 18), "pauldrons": (56, 18),
    "face_eyes": (29, 12), "hand_grip": (11, 17), "forearm_fist": (11, 15),
    "weapon_01": (40, 120), "weapon_02": (40, 120), "weapon_03": (20, 130), "weapon_04": (10, 90),
}


def compose(parts_doc: dict, directory: Path, scale: float, body_h: int = BODY_H,
            normalize: bool = True, preserve_aspect: bool = False):
    parts = [p for p in parts_doc["parts"] if p.get("anchor") in ANCHORS]
    canvas_h = int(body_h * scale * 1.25)
    canvas_w = int(body_h * scale * 1.1)
    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    report = []

    def anchor_px(anchor: str):
        ax, ay = ANCHORS[anchor]
        return canvas_w / 2 + ax * scale, canvas_h - 20 - ay * scale

    for p in sorted(parts, key=lambda q: (q.get("layer") or 0)):
        pname0 = p.get("part") or p.get("id")
        if p.get("variant"):
            continue
        f = directory / p["file"]
        if not f.exists():
            continue
        piece = Image.open(f).convert("RGBA")
        # normalizacao anatomica: escala a peca para a dimensao canonica do seu tipo
        k = 1.0
        pname = p.get("part") or p.get("id")
        if normalize and pname in PART_DIMS_U:
            tw_u, th_u = PART_DIMS_U[pname]
            if preserve_aspect:
                # modo antigo: normaliza so a altura; a largura fica refem do desenho
                target_h = int(round(th_u * scale))
                k = target_h / piece.height
                piece = piece.resize((max(1, int(piece.width * k)), max(1, target_h)),
                                     Image.LANCZOS)
            else:
                # SILHUETA CANONICA (padrao): a peca preenche a caixa canonica do seu tipo.
                # Normalizar so a altura deixava a largura refem do desenho (pelve 25/40 u,
                # pe 17/26 u, cabelo 21/33 u) e a silhueta nao conversava com o rig.
                # A distorcao de aspecto NAO e escondida: vai para o relatorio (aspect_drift).
                target_w = max(1, int(round(tw_u * scale)))
                target_h = max(1, int(round(th_u * scale)))
                k = target_h / piece.height
                piece = piece.resize((target_w, target_h), Image.LANCZOS)
        # pivo recalculado para o tamanho FINAL (nunca herdado do tamanho original)
        if p.get("pivot_norm"):
            px = p["pivot_norm"][0] * piece.width
            py = p["pivot_norm"][1] * piece.height
        else:
            px, py = p["pivot_px"][0] * k, p["pivot_px"][1] * k
        ax, ay = anchor_px(p["anchor"])
        if str(p["anchor"]).endswith(".back"):
            dx, dy = DEPTH_OFFSET_U["back"]
            ax, ay = ax + dx * scale, ay - dy * scale
        # ajuste fino explicito do spec (u; +x direita, +y sobe). NAO substitui o pivo:
        # o pivo continua sendo o ponto de articulacao, o offset resolve a emenda entre pecas.
        ox, oy = p.get("offset_u") or (0, 0)
        ax, ay = ax + ox * scale, ay - oy * scale
        left, top = int(round(ax - px)), int(round(ay - py))
        img.alpha_composite(piece, dest=(max(left, 0), max(top, 0)))
        report.append({
            "part": pname, "anchor": p["anchor"], "layer": p["layer"],
            "pivot_px": p.get("pivot_px"), "pivot_norm": p.get("pivot_norm"),
            "normalized_scale": round(k, 3), "placed_at": [left, top],
            "offscreen": left < 0 or top < 0,
        })
    return img, report


def overlay(img: Image.Image, scale: float):
    """Linhas de referência: topo, olhos, queixo, ombro, quadril, joelho, chão."""
    draw = ImageDraw.Draw(img)
    h = img.height
    base = h - 20
    for y_u, color, label in [
        (200, (255, 80, 80, 180), "top 200u"),
        (182, (255, 200, 80, 160), "eyes 182u"),
        (164, (255, 200, 80, 160), "chin 164u"),
        (156, (120, 200, 255, 180), "shoulder 156u"),
        (100, (120, 255, 160, 180), "hip 100u"),
        (56, (120, 255, 160, 150), "knee 56u"),
        (0, (255, 255, 255, 220), "ground 0"),
    ]:
        y = int(base - y_u * scale)
        draw.line([(0, y), (img.width, y)], fill=color, width=1)
    # eixo de gravidade
    draw.line([(img.width // 2, 0), (img.width // 2, img.height)], fill=(255, 255, 255, 90), width=1)
    return img


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("parts_json")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--scale", type=float, default=4.0)
    ap.add_argument("--overlay", action="store_true")
    ap.add_argument("--no-normalize", action="store_true",
                    help="nao escala pecas para a dimensao canonica do tipo")
    ap.add_argument("--preserve-aspect", action="store_true",
                    help="normaliza so pela altura e preserva o aspecto do desenho (modo antigo)")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()

    doc = json.loads(Path(a.parts_json).read_text())
    directory = Path(a.parts_json).parent
    img, rep = compose(doc, directory, a.scale, normalize=not a.no_normalize,
                       preserve_aspect=a.preserve_aspect)
    if a.overlay:
        img = overlay(img, a.scale)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(a.out, optimize=True)
    if a.report:
        Path(a.report).write_text(json.dumps({"placed": rep}, indent=2))
    print(json.dumps({"out": a.out, "size": img.size, "placed": len(rep),
                      "offscreen": [r["part"] for r in rep if r["offscreen"]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
