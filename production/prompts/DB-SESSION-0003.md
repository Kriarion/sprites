# Prompts — DB-SESSION-0003 (teste de peso de contorno)

Objetivo: validar se instrução explícita de espessura no prompt (PENDING-004, opção A) muda o
contorno que chega ao pipeline. 2 gerações, nenhuma correção.

## G1 — `t1_outline_front4` (frente)

> Character sprite sheet on a flat solid magenta background (#FF00FF), arranged as a clean 2×2 grid
> with exactly FOUR separate, fully isolated body parts and generous empty margins between them:
> top-left: a male torso piece, front view, from base of neck to hips, with short sleeves ending
> mid-deltoid · top-right: a male pelvis piece in plain underwear, front view, with the top of both
> thighs cut off flat · bottom-left: a single upper arm piece, front view, deltoid at top and elbow
> cut flat at bottom · bottom-right: a single thigh piece, front view, hip cut flat at top and knee
> cut flat at bottom.
> Style: neutral gray "clay" sculpt material, monochrome gray only, no colors, no patterns, no logos,
> no text, no labels, no numbers, no arrows, no shadow cast on the background.
> Cel-shaded cartoon / Flash-animation look with a VERY THICK BOLD BLACK OUTLINE. The outline must be
> approximately 10 pixels wide on this 1408×768 canvas — that is about 3% of each part's height — with
> uniform thickness all the way around every part, never tapering to a hairline. Internal anatomical
> shading lines (pecs, abs, oblique, knee) are thinner, about 3 pixels. Crisp anti-aliased edges, clean
> solid flat fills, simple two-tone shading.
> Lighting: hard flat frontal light, subtle soft shadow only on the outer left edge of each part, no
> gradients in the background, no vignette.

## G2 — `t2_outline_back4` (costas, half-shadow)

Mesma estrutura, 4 peças traseiras (upper arm, forearm, thigh, shin), com:
> ... darkened to roughly 60% brightness because these are the shaded back-side pieces of a sprite set ...
> ... outline approximately 10 pixels wide on this 1408×768 canvas — about 3% of each part's height ...

## Resultado (medido)

| | Mediana do contorno | % da altura da peça | @1x (corpo de 200 px) |
|---|---:|---:|---:|
| Lote da sessão 0002 (referência) | 2,78 px no mestre | 0,88% | 0,94 px |
| **G1 + G2 (prompt com 3%)** | 2,71 px no mestre | 0,88% | 0,93 px |
| Pedido no prompt | ~10 px | ~3% | ~3,2 px |

**O gerador ignorou a instrução numérica**: entregou 0,88% da altura da peça nas duas folhas, igual ao
lote antigo. Diferença entre lotes: −1%. A instrução de espessura de contorno **não é executável por prompt**
neste modelo; o traço é uma característica fixa do estilo dele.
