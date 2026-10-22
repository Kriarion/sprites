# ADR-0007 — Proporção canônica 5,9 cabeças + coerência auditável do pacote

- **Status:** Aceita (decisão do usuário, 2026-10-22)
- **Data:** 2026-10-22
- **Contexto:** evidência da `DB-SESSION-0001` (`docs/calibration_report.md` §5)
- **Relaciona-se com:** ADR-0002 (escala), ADR-0006 (decomposição), Visual Bible 1.2.0

## 1. Contexto

A calibração mediu três regimes do gerador para proporção humana:

| Instrução | Resultado medido |
|---|---|
| "heroic 5.5-head proportions" | 7,52 / 6,93 / 6,70 / 6,46 cabeças |
| "exactly 6 heads tall" | 4,16 / 4,09 / 3,75 / 3,74 cabeças |
| "head = 18% da altura total" | **5,89 cabeças** |

Existe um ponto estável: **percentual explícito de 17–18%** produz ≈ 5,9 cabeças de forma reprodutível.
Insistir em 5,5 exigiria correção por personagem, gastando reserva de orçamento em toda ficha.

## 2. Decisão

1. **Proporção canônica do pacote: 5,9 cabeças** (arredondado de 5,88).
2. **Cabeça = 34 u = 17,0% da altura de 200 u** (queixo → topo do crânio).
3. **Tolerância de aceitação: ±5%** na razão cabeça/altura (32,3–35,7 u) e **±4 u** por articulação.
4. **A instrução de prompt é percentual, nunca adjetivo:** `head = 17% of total height`,
   `shoulders = 28%`, `waist = 60%`, `hips = 50%`, `knees = 28%`.
5. O alvo 5,5 do guia original é **abandonado como padrão** e mantido apenas como referência histórica.

Tabela canônica (base 200 u, origem no chão):

| Ponto | y (u) | % da altura |
|---|---:|---:|
| Topo do crânio | 200 | 100% |
| Linha dos olhos | 184 | 92% |
| Queixo | 166 | 83% |
| Pivô do pescoço (`neck`) | 164 | 82% |
| Pivô do ombro (`shoulder.*`) | 156 | 78% |
| Esterno | 144 | 72% |
| Cintura | 118 | 59% |
| Pivô do quadril (`hip.*`) | 100 | 50% |
| Punho (`wrist.*`) | 94 | 47% |
| Ponta dos dedos | 80 | 40% |
| Joelho (`knee.*`) | 56 | 28% |
| Tornozelo (`ankle.*`) | 14 | 7% |
| Chão | 0 | 0% |

Larguras: cabeça 29 u · ombros 56 u · tórax 46 u · cintura 34 u · quadril 40 u · mão 11×17 u · pé 26 u.
Comprimentos: braço superior 32 u · antebraço 30 u · coxa 44 u · canela 42 u.

## 3. Coerência obrigatória ("o pacote conversa entre si")

Estabilizar a proporção resolve **um** eixo de coerência. Um pacote que "conversa entre si" precisa de
**seis invariantes medidos**, não de boa vontade. Fica instituído `docs/coherence_standard.md` e a ferramenta
`tools/coherence.py`, que audita todo asset registrado e emite um **score de coerência do pacote**.

| # | Invariante | Métrica | Tolerância |
|---|---|---|---|
| C1 | Escala | `pixels_per_unit` e altura em u | 1, 2 ou 4; corpo 200 u ±5% |
| C2 | Proporção | razão cabeça/altura, posição de ombro/quadril/joelho | ±5% / ±4 u |
| C3 | Contorno | espessura média da linha escura / altura | 0,9–1,3% (≈2 px em 1x) |
| C4 | Paleta | ΔH, ΔS, ΔV dos 5 pontos canônicos vs paleta aprovada | ΔH ≤ 8°, ΔS ≤ 10%, ΔV ≤ 10% |
| C5 | Half-shadow | luminância média das peças traseiras / frontais | ≤ 0,80 (traseira ao menos 20% mais escura) |
| C6 | Estrutura | âncora e camada no vocabulário; sem camada duplicada; pivô dentro da peça | 100% |

Regra: um asset **não pode** ser `APPROVED` com qualquer invariante fora de tolerância.
Se um invariante falhar para **todos** os assets, a culpa é do padrão — e o padrão é revisto por ADR,
nunca "ajustado por asset".

## 4. Alternativas consideradas

| Alternativa | Problema |
|---|---|
| Insistir em 5,5 cabeças | exige correção por personagem; queima 1–2 gerações de reserva por ficha |
| Adotar 7,5 (realista) | perde o "charme Flash" exigido pelo master §2 |
| Sem tolerância numérica | volta ao "ficou bom" — não é auditável |
| Coerência só por revisão visual | não escala para 60+ sessões; drift invisível |

## 5. Consequências

- `technical_specification.md` §2.2 e `anatomy_and_rigging.md` §2/§4 atualizados para 5,9 cabeças.
- `tools/compose.py` `PART_DIMS_U` recalibrado (cabeça 29×34).
- Toda ficha de personagem passa por `tools/measure.py` **antes** de gerar peças.
- O `coherence_report.json` entra no fechamento de cada sessão, junto do ledger.
- Mudar qualquer tolerância exige novo ADR + bump MAJOR do Technical Standard.
