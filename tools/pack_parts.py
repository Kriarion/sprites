#!/usr/bin/env python3
"""pack_parts.py — transforma folhas brutas + spec em biblioteca de peças do corpo.

    python tools/pack_parts.py production/specs/body_m_v1.json -o exports/individual_png/body_m_v1

Etapas por peça:
  key (magenta) -> componentes conexos -> seleção por índice -> merge -> rotação ->
  trim -> normalização anatômica (PART_DIMS_U) -> pivô por tipo -> PNG + parts.json

Não aprova nada: monta a biblioteca e delega a medição a measure.py / coherence.py.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

import key as keymod
from compose import PART_DIMS_U

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "production/raw"

# pivo canonico por TIPO de peca, em fracao da bbox final (proximal = topo na orientacao vertical)
PIVOT_BY_TYPE = {
    "torso": (0.50, 0.79), "pelvis": (0.50, 0.30),
    "head": (0.50, 0.95), "hair_front": (0.50, 0.92), "hair_back": (0.50, 0.15),
    "face_eyes": (0.50, 0.50),
    "upperarm_front": (0.50, 0.06), "upperarm_back": (0.50, 0.06),
    "forearm_front": (0.50, 0.06), "forearm_back": (0.50, 0.06), "forearm_fist": (0.50, 0.06),
    "thigh_front": (0.50, 0.05), "thigh_back": (0.50, 0.05),
    "shin_front": (0.50, 0.05), "shin_back": (0.50, 0.05),
    "foot_front": (0.42, 0.22), "foot_back": (0.42, 0.22),
    "hand_front": (0.50, 0.10), "hand_back": (0.50, 0.10), "hand_grip": (0.50, 0.10),
}


def sheet_components(sheet_png: Path) -> tuple[list[dict], np.ndarray]:
    """keya a folha e devolve os componentes conexos ordenados em leitura."""
    rgb = np.array(Image.open(sheet_png).convert("RGB"))
    kc = keymod.border_color(rgb)
    alpha = keymod.build_alpha(rgb, kc, 60, 110)
    alpha, _ = keymod.despeckle(alpha, 3000)
    rgb2 = keymod.despill(rgb, alpha, kc, 2)
    rgba = np.dstack([rgb2, (alpha * 255).astype(np.uint8)])

    lab, n = ndimage.label(alpha > 0)
    comps = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 3000:
            continue
        ys, xs = np.where(m)
        comps.append({"id": i, "mask": m,
                      "bbox": (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1),
                      "area": int(m.sum())})
    comps.sort(key=lambda c: (c["bbox"][1] // 64, c["bbox"][0]))
    return comps, rgba


def cut(rgba: np.ndarray, comp: dict, others: list[dict] | None = None) -> Image.Image:
    masks = [comp] + (others or [])
    # bbox = UNIAO de todos os componentes (critical for merged pieces like the two eyes)
    x0 = min(c["bbox"][0] for c in masks)
    y0 = min(c["bbox"][1] for c in masks)
    x1 = max(c["bbox"][2] for c in masks)
    y1 = max(c["bbox"][3] for c in masks)
    keep = np.zeros(rgba.shape[:2], dtype=bool)
    for c in masks:
        keep |= c["mask"]
    sub = rgba[y0:y1, x0:x1].copy()
    sub[..., 3] = np.where(keep[y0:y1, x0:x1], sub[..., 3], 0)
    return Image.fromarray(sub, "RGBA")


def normalize(piece: Image.Image, part: str, target_h_px: int) -> tuple[Image.Image, float]:
    if part not in PART_DIMS_U:
        return piece, 1.0
    w_u, h_u = PART_DIMS_U[part]
    k = target_h_px / piece.height
    return piece.resize((max(1, round(piece.width * k)), target_h_px), Image.LANCZOS), round(k, 3)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--target-height-u", type=int, default=None,
                    help="altura alvo da peca em u (default: a do PART_DIMS_U)")
    ap.add_argument("--scale", type=float, default=2.0, help="px por u na saída")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()

    spec = json.loads(Path(a.spec).read_text())
    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    parts, issues, log = [], [], []

    for sheet in spec["sheets"]:
        png = next(iter(sorted(RAW.glob(f"*/{sheet['sheet']}.png"))), None)
        if png is None:
            issues.append({"sheet": sheet["sheet"], "issue": "raw_not_found"})
            continue
        comps, rgba = sheet_components(png)
        for entry in sheet["components"]:
            idx = entry["index"]
            merge = entry.get("merge", [idx])
            try:
                main_c = comps[idx]
                extra = [comps[i] for i in merge if i != idx]
            except IndexError:
                issues.append({"sheet": sheet["sheet"], "part": entry["part"],
                               "issue": "index_out_of_range", "index": idx, "found": len(comps)})
                continue
            piece = cut(rgba, main_c, extra)

            rot = entry.get("rotate_deg", 0)
            if rot:
                piece = piece.rotate(rot, expand=True, resample=Image.BICUBIC)

            if entry["part"] not in PART_DIMS_U:
                issues.append({"sheet": sheet["sheet"], "part": entry["part"],
                               "issue": "no_canonical_dims",
                               "detail": "peca salva na escala bruta: adicione o tipo em PART_DIMS_U"})
            target_h = (a.target_height_u or PART_DIMS_U.get(entry["part"], (0, piece.height))[1])
            target_h_px = int(round(target_h * a.scale))
            piece, k = normalize(piece, entry["part"], target_h_px)

            pv = PIVOT_BY_TYPE.get(entry["part"], (0.5, 0.1))
            pivot_px = [round(pv[0] * piece.width, 1), round(pv[1] * piece.height, 1)]

            fname = f"{entry['part']}.png"
            piece.save(outdir / fname, optimize=True)
            parts.append({
                "id": entry["part"], "file": fname, "layer": entry["layer"],
                "anchor": entry["anchor"], "shaded": entry.get("shaded", False),
                "variant": entry.get("variant", False),
                "source_sheet": sheet["sheet"], "component_index": idx,
                "merge": merge if len(merge) > 1 else None,
                "rotated_deg": rot, "normalized_scale": k,
                "size_px": [piece.width, piece.height],
                "pivot_px": pivot_px, "pivot_norm": [pv[0], pv[1]],
                "offset_u": entry.get("offset_u", [0, 0]),
            })
            log.append({"sheet": sheet["sheet"], "part": entry["part"],
                        "bbox_src": list(main_c["bbox"]), "out": fname})

    parts.sort(key=lambda p: p["layer"])
    doc = {"spec": spec["spec_id"], "session": spec["session"], "rig": spec["rig"],
           "body_height_u": spec["body_height_u"], "scale_px_per_u": a.scale,
           "proportional_system": spec["proportion"],
           "parts_count": len(parts), "parts": parts, "issues": issues}
    (outdir / "parts.json").write_text(json.dumps(doc, indent=2))
    if a.report:
        Path(a.report).parent.mkdir(parents=True, exist_ok=True)
        Path(a.report).write_text(json.dumps({"log": log, "issues": issues}, indent=2))
    print(json.dumps({"parts": len(parts), "issues": len(issues),
                      "ids": [p["id"] for p in parts]}, indent=2))
    return 0 if parts else 1


if __name__ == "__main__":
    raise SystemExit(main())
