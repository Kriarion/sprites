#!/usr/bin/env python3
"""audit_geometry.py — mede emendas (juntas) e drift de aspecto da montagem, em unidades do rig.

    python tools/audit_geometry.py exports/individual_png/body_m_v1/parts.json -o audit.json

Nao julga por olho: reconstroi o retangulo de cada peca com a MESMA regra do compose.py
(escala canonica por tipo, pivo normalizado, offset de profundidade, offset_u do spec)
e reporta sobreposicao/folga por junta e o erro de aspecto arte-vs-canonico.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from compose import ANCHORS, PART_DIMS_U, DEPTH_OFFSET_U

PAIRS = [('torso', 'pelvis', 'waist'), ('pelvis', 'thigh_front', 'hip F'), ('pelvis', 'thigh_back', 'hip B'),
         ('upperarm_front', 'forearm_front', 'elbow F'), ('forearm_front', 'hand_front', 'wrist F'),
         ('upperarm_back', 'forearm_back', 'elbow B'), ('forearm_back', 'hand_back', 'wrist B'),
         ('thigh_front', 'shin_front', 'knee F'), ('shin_front', 'foot_front', 'ankle F'),
         ('thigh_back', 'shin_back', 'knee B'), ('shin_back', 'foot_back', 'ankle B'),
         ('head', 'torso', 'neck'), ('torso', 'upperarm_front', 'shoulder F'),
         ('torso', 'upperarm_back', 'shoulder B'), ('head', 'face_eyes', 'eyes')]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("parts_json")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    doc = json.loads(Path(a.parts_json).read_text())
    d = Path(a.parts_json).parent
    rects = {}
    for p in doc["parts"]:
        if p.get("variant"):
            continue
        name = p.get("part") or p.get("id")
        im = Image.open(d / p["file"]); w, h = im.size
        if name in PART_DIMS_U:
            tw, th = PART_DIMS_U[name]; k = th / h; w, h = w * k, th
        ax, ay = ANCHORS[p["anchor"]]
        if str(p["anchor"]).endswith(".back"):
            dx, dy = DEPTH_OFFSET_U["back"]; ax += dx; ay += dy
        ox, oy = p.get("offset_u") or (0, 0)
        ax += ox; ay -= oy
        pn = p["pivot_norm"]
        rects[name] = {"left": round(ax - pn[0] * w, 1), "right": round(ax - pn[0] * w + w, 1),
                       "top": round(ay + pn[1] * h, 1), "bottom": round(ay + pn[1] * h - h, 1),
                       "w": round(w, 1), "h": round(h, 1), "anchor": p["anchor"], "layer": p["layer"],
                       "art_aspect": round(im.width / im.height, 3),
                       "canon_aspect": round(PART_DIMS_U[name][0] / PART_DIMS_U[name][1], 3)
                       if name in PART_DIMS_U else None}
    joints = []
    for a_, b_, label in PAIRS:
        A, B = rects[a_], rects[b_]
        joints.append({"pair": f"{a_}->{b_}", "label": label,
                       "x_overlap_u": round(min(A["right"], B["right"]) - max(A["left"], B["left"]), 1),
                       "y_overlap_u": round(min(A["top"], B["top"]) - max(A["bottom"], B["bottom"]), 1)})
    drift = [{"part": n, "art_aspect": r["art_aspect"], "canon_aspect": r["canon_aspect"],
              "error_pct": round((r["art_aspect"] / r["canon_aspect"] - 1) * 100, 1),
              "placed_w_u": r["w"], "canon_w_u": PART_DIMS_U[n][0]}
             for n, r in rects.items() if r["canon_aspect"]]
    out = {"unit": "u (1 u = 1/200 da altura)", "sign": "+ = sobreposicao, - = folga",
           "joints": joints, "aspect_drift": sorted(drift, key=lambda z: -abs(z["error_pct"])), "rects": rects}
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(out, indent=2))
    gaps = [j for j in joints if j["y_overlap_u"] < 0 or j["x_overlap_u"] < -1]
    print(json.dumps({"joints": len(joints), "com_folga": len(gaps),
                      "piores": [j["pair"] for j in sorted(joints, key=lambda z: z["y_overlap_u"])[:4]],
                      "maior_drift_aspecto_pct": drift[0]["error_pct"] if drift else 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
