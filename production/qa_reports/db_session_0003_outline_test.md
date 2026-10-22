# QA — DB-SESSION-0003 (teste de peso de contorno · PENDING-004 opção A)

**Sessão:** DB-SESSION-0003 · **Data:** 2026-10-22 · **Orçamento:** 2 de 10 (2 novas, 0 correções)
**Objetivo:** validar se pedir contorno grosso no prompt resolve C3 **antes** de regenerar o corpo inteiro.

## 1. Antes de testar: a métrica estava errada

Duas implementações anteriores de C3 mediam a coisa errada e foram **descartadas**:

| Método | Problema | Evidência |
|---|---|---|
| `2 × média(EDT)` na faixa de contorno | devolve ~metade da largura real | retângulo sintético de 6 px → 2,67 px |
| faixa recortada por dilatação de 2 px | **satura em 2,67 px** para qualquer linha ≥3 px | teste de 2 a 12 px → 2,67 constante |
| área escura total ÷ perímetro | somava sombreado interno ao contorno | `hair_back` dava 14,4 px "de linha" |

Método adotado (`tools/measure_outline.py`): contorno = linha escura **conectada à borda** da silhueta;
espessura = área(contorno) ÷ perímetro da silhueta. Calibração em retângulos de 1 a 12 px:

| Largura real | 1 | 2 | 3 | 4 | 6 | 8 | 10 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Medido | 1,0 | 1,98 | 2,95 | 3,9 | 5,75 | 7,53 | 9,25 | 10,9 |

Erro < 8% em toda a faixa. **O número anterior (1,12 px @1x) estava inflado em ~20%**; o valor correto
do lote de 2026-10-22 é **0,94 px @1x (0,47% da altura)**.

## 2. Teste A: prompt com espessura explícita (2 gerações)

| Lote | Folhas | Mediana do contorno no mestre | % da altura da peça | @1x |
|---|---:|---:|---:|---:|
| Sessão 0002 (referência) | g2, g3 | 2,78 px | 0,88% | 0,94 px |
| Sessão 0003 (pedido de 3%) | t1, t2 | 2,71 px | 0,88% | 0,93 px |

**Resultado: A não funciona.** O modelo entrega ~0,9% da altura da peça independentemente do número
pedido (pedi 3%, ele deu 0,88% duas vezes). A espessura do traço é propriedade fixa do estilo do gerador.

Artefatos: `production/raw/DB-SESSION-0003/t1_outline_front4.png`, `t2_outline_back4.png`;
peças `exports/individual_png/outline_test_v1/` (8 peças, 0 issues); métricas
`logs/outline_master_comparison.json`, `logs/outline_test_v1.json`.

## 3. Por que o prompt não poderia funcionar (causa real)

A cadeia de escala consome a linha: uma peça de ~330 px no mestre vira ~96 px no tamanho canônico
(redução de ~3,5×). Como a linha é desenhada com largura **em pixels do mestre**, ela encolhe junto.
Manter 0,88% da altura da peça no mestre significa **0,94 px @1x** no corpo de 200 px. Para chegar a
1,6–2,8 px @1x seria preciso desenhar ~3% da altura da peça — e o modelo não faz isso.

## 4. Opção B testada (0 gerações): recontorno determinístico

`tools/restroke.py`: separa a linha **conectada à borda** (contorno) do sombreado interno, dilata só o
contorno, em supersampling ×3, com alfa pré-multiplicado, *despill* de magenta e extensão de borda.

| `--add-px` | Contorno @2 px/u | @1x | % da altura | C3 |
|---:|---:|---:|---:|---|
| 0 (original) | 1,88 px | 0,94 px | 0,47% | FAIL |
| 1,0 | 2,95 px | 1,47 px | 0,74% | FAIL |
| 2,0 | 3,27 px | 1,64 px | 0,82% | PASS (no piso) |
| **2,5** | **3,62 px** | **1,81 px** | **0,91%** | **PASS** |

No lote completo (18 peças): mediana **1,81 px @1x (0,91%)**, `coherence` = **6/6 invariantes PASS**.
Comparação visual a 1x: `logs/assembly_body_m_v1_restroke_compare.png`.

## 5. Achados colaterais

- **C4 estava cega:** amostrava a paleta incluindo a cor do contorno; engrossar a linha mudava o
  histograma e reprovava paleta sem nenhuma cor ter mudado (ΔV 13%). Corrigido: C4 amostra só cor de
  material (contorno excluído).
- **C3 estava com a escala trocada:** usava a escala da montagem (4 px/u) como referência das peças
  (2 px/u), errando por 2×. Corrigido com `--parts-ppu`.
- **Despill de borda:** as peças exportadas carregam resíduo magenta (max chroma 57 em pixel de borda);
  visível só fora de fundo magenta. `restroke.py` já corrige o que toca; o `pack_parts.py` **não** —
  registrar como ISSUE.

## 6. Veredito

- Opção **A: reprovada por medição** (2 gerações, diferença de −1%).
- Opção **B: aprovada tecnicamente** (0 gerações, C3 PASS, 6/6, verificado a 1x).
- O corpo base passa de 83,3% para **100%** de coerência **de pacote** — o que não significa arte
  aprovada: D1/D2/D3/D6/D10 continuam abertos e são de geração.
