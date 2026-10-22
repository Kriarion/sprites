# RELATÓRIO DE CALIBRAÇÃO — DB-SESSION-0001

**Sessão:** `DB-SESSION-0001` · **Data:** 2026-10-22 · **Tipo:** `REFERENCE` + spike de pipeline
**Orçamento:** 10/10 gerações consumidas (7 novas + 3 de correção) — teto respeitado, divisão planejada excedida em 1 nova
**Veredito do spike:** **PARCIAL — arquitetura revisada** (ver `ADR-0006`)

Este documento substitui suposições por medições. Todos os números abaixo foram gerados por
`tools/cellstats.py`, `tools/key.py`, `tools/measure.py` e `tools/compose.py`, com log em
`production/qa_reports/logs/`.

---

## 1. Sumário executivo

| Hipótese do plano | Resultado medido | Consequência |
|---|---|---|
| O gerador respeita grade 4×4 imposta por prompt | ❌ **Falso** — 13/16 células a 4,79 px da borda, 6 células com fragmentos múltiplos | Grade rígida não é contrato |
| Peças simétricas saem como objeto único | ❌ **Falso** — o modelo desenha **pares espelhados L/R** na mesma célula | Cada célula pode conter 2 objetos |
| Chroma-key magenta produz alpha limpo | ✅ **Verdadeiro** — halo 0,0% em 5 de 6 folhas; 2,06% na folha de dummy (borda suave) | Keying aprovado |
| Pivô pode ser derivado só do template | ⚠️ **Parcial** — pivô por *tipo* funciona, mas âncora errada desmonta o boneco | Pivô por tipo **+ validação de montagem obrigatória** |
| Escala relativa entre peças da mesma folha é consistente | ❌ **Falso** — cada célula é desenhada "preenchendo" seu espaço | **Normalização anatômica obrigatória** |
| Proporção pode ser dirigida por descrição | ✅ **Verdadeiro, com controle numérico explícito** | Usar percentual, não "heroic proportions" |
| 1 objeto por célula é extraível por componentes conexos | ✅ **Verdadeiro** — 9/9 objetos isolados, 1 componente cada | Nova arquitetura (ADR-0006) |

## 2. Experimento A — grade 4×4 com 12 peças (G3, falhou)

Prompt pedia 12 peças em 4×4, "não tocar vizinhas". Resultado (`cellstats_g3.json`):

```text
covered_cells: 16/16      multi_fragment_cells: 6      gutter_violations: 13
```

- O modelo **desenhou 2 figuras por linha**, ignorando a divisão em 4 colunas.
- Pares L/R (coxas, canelas, pés, braços) apareceram como **dois objetos espelhados** dentro da mesma célula.
- Células 2, 4, 5, 6, 7, 10 continham 2–4 fragmentos: impossível atribuir um nome a cada um.

**Diagnóstico:** "peça simétrica" para o modelo significa "desenhe as duas". Pedir "uma coxa" produziu
"as duas coxas". O layout também foi colapsado para 2 colunas por convenção interna do gerador.

## 3. Experimento B — grade 3×3 com peças singulares explícitas (G4, falhou)

Prompt reescrito: "exactly NINE separate objects", "never draw a mirrored pair", "no object is repeated".
Resultado (`cellstats_g4.json`):

```text
covered_cells: 9/9        multi_fragment_cells: 5       gutter_violations: 7
```

- O modelo **duplicou** o pelvis (duas cópias na mesma faixa) e manteve pares espelhados nas coxas.
- A célula do pé recebeu **duas botas** desalinhadas verticalmente, atravessando a fronteira entre linhas.

**Diagnóstico:** instruções negativas ("never", "no") não são obedecidas de forma confiável. O modelo
completa simetria por conta própria e reorganiza o layout conforme a composição que considera agradável.

## 4. Experimento C — 9 objetos nomeados, um por célula (G8, **aprovado**)

Prompt: lista numerada de 9 objetos **diferentes por natureza** (peitoral, cinto, ombreira, coxa, canela,
braçadeira, bota, mão, luva), cada um descrito com sua função, mais a regra de margem.

Resultado (`cellstats_g8.json` + `decompose_armor_test.json`):

```text
componentes conexos: 9/9          fragmentos por objeto: 1         área: 18.900–36.777 px
keying: halo 0,0%   alpha real: sim   alpha_coverage: 0,207
```

**Conclusão:** o contrato que funciona não é "grade", é **"9 objetos distintos, um por região"**. Peças
singulares nomeadas por função → extração perfeita por componentes conexos.

## 5. Experimento D — proporção (G1, G9, G10) — 3 tentativas

| Geração | Instrução de proporção | Medido | Alvo |
|---|---|---|---|
| G1 | "heroic 5.5-head proportions, head slightly large" | **7,52 / 6,93 / 6,70 / 6,46** cabeças | 5,5 |
| G9 | "exactly 6 heads tall, oversized head, do not draw 7 or 8" | **4,16 / 4,09 / 3,75 / 3,74** | 6,0 |
| G10 | "head = 18% da altura total; ombros = 28%; cintura a 60%; joelhos a 28%" | **5,89** (frontal) | 5,5 |

**Achados:**
1. Adjetivos ("heroic", "slightly large") **não controlam** proporção: o modelo entrega anatomia realista (7,5).
2. Pedir um número de cabeças **supercorrige**: "6 heads" → 4,1.
3. **Percentual explícito por segmento** é o único controle preciso: 18% → 5,89 cabeças (erro de 7%).
4. A distribuição é bimodal: ou realista, ou cartoon grosseiro. Não há meio-termo por adjetivo.

**Regra adotada (Visual Bible 1.1.0):** toda ficha de personagem declara percentuais medidos
(cabeça, ombro, cintura, joelho, quadril) e é **medida por `tools/measure.py`** antes de aprovar.
Tolerância ±5%. O alvo canônico permanece **5,5 cabeças (cabeça = 18,2% da altura)**.

## 6. Experimento E — montagem (G3 do gate)

Montagem de `DB_EQUIP_ARMOR_TESTPLATE_M` com 9 peças, pivô por tipo, normalização anatômica
(`exports/previews/assembly_armor_test.png`):

| Iteração | Defeito | Correção aplicada |
|---|---|---|
| 1 | Peças em escalas incompatíveis (mão maior que o torso) | **normalização anatômica** por `PART_DIMS_U` em `compose.py` |
| 2 | Pivô herdado do tamanho original → peças deslocadas | pivô **recalculado** a partir de `pivot_norm` após o resize |
| 3 | `pelvis` ancorado em `root` (chão) e `pauldron` em `spine_high` (âncora de par) | âncoras corrigidas para `pelvis` e `shoulder.front` |

**Estado final:** G3 **FAIL** — legítimo, não cosmético. Motivos:
1. O conjunto tem **9 de 21 peças**: sem braços superiores, mãos traseiras, cabeça e capa.
2. A ordem de camadas de um conjunto **incompleto** não pode ser validada (não há com o que sobrepor).
3. Pivôs por tipo ainda não passaram pelo teste de rotação ±35°.

Nenhum ajuste foi feito "para parecer montado". O asset permanece `QA_PENDING` com G3 reprovado.

## 7. Experimentos acessórios (aprovados no G1)

| Geração | Conteúdo | Resultado | Registro |
|---|---|---|---|
| G2 | 4 materiais × 2 versões (lit / half-shadow) | ✅ 8 objetos, 3 tons, half-shadow correto, metal com rim light | `DB_REF_MATERIALS_V1` |
| G5 | 4 armas oversized, cabo vertical | ✅ 4/4, cabos alinhados ao eixo vertical, prontos para pivô | `DB_REF_WEAPONS_V1` |
| G6 | 4 cabeças (M, F, infantil, musculosa) | ✅ 4/4, mesmo estilo de olho, mesmo peso de linha, corte de pescoço limpo | `DB_REF_HEADS_V1` |
| G7 | Kit de UI (painel, HP, Ki, slot, 6 botões) | ✅ 5/5, magenta visível pelos soquetes vazios, sem texto | `DB_REF_UI_PROBE_V1` |

## 8. Números de controle para as próximas sessões

| Métrica | Valor medido nesta sessão | Uso |
|---|---|---|
| Halo de keying aceitável | ≤ 2,1% (borda suave) | gate G2 |
| Cobertura de alpha em folha de peças | 0,17–0,45 | detectar folha vazia/estourada |
| Área mínima de peça real | 18.900 px | filtro de ruído |
| Fragmentos por célula | 1 (aprovado) / ≥2 (reprovado) | `cellstats.py` |
| Razão cabeça/altura aprovada | 18,2% ± 5% | `measure.py` |
| Escala relativa entre peças | **não confiável** — sempre normalizar | `compose.py` |

## 9. O que NÃO foi provado

Sejamos explícitos, para não repetir o erro de declarar mais do que existe:

- Nenhuma peça de **corpo humano** (tronco, membros com articulação) foi extraída e montada com sucesso.
- Nenhum **rig JSON** foi validado em rotação real (só existe o rig de referência embutido no compositor).
- Nenhuma **animação** foi gerada (sem corpo completo, não há o que animar).
- O **teste de rotação ±35°** por junta continua não executado.
- Nenhuma **máscara de cor** foi produzida.
- Nada aqui é canônico de Dragon Ball: tudo é referência de estilo ou design original de teste.

Esses itens migram para `DB-SESSION-0002` e para a Fase 2, com a arquitetura revisada.

---

# ADENDO — DB-SESSION-0002 (corpo base)

**Orçamento:** 5 de 10 (5 novas, 0 correções) · **Resultado:** corpo montável, **0 assets aprovados**

## 10. Formato de folha: 9 objetos falha, 4 objetos funciona

| Folha | Objetos pedidos | Componentes isolados | Problema |
|---|---:|---:|---|
| `g1_body_parts_front` | 9 (3×3) | 10 | o modelo desenhou **um corpo inteiro** + 6 peças; torso, pernas e pelve fundiram |
| `g2_core4` | 4 (2×2) | 4 | limpo |
| `g3_limbs4` | 4 (2×2) | 4 | limpo |
| `g4_head4` | 4 (2×2) | 5 | olhos saíram como **dois objetos** (resolvido por `merge` no spec) |
| `g5_back4` | 4 (2×2) | 4 | peças desenhadas **horizontais** → correção por `rotate_deg` |
| `g6_back_hands_feet` | 4 (2×2) | 4 | limpo |

**Regra adotada:** **4 objetos por folha** (2×2), cada um descrito por função. Acima disso o modelo
começa a "compor uma figura" em vez de listar peças. Custo: ~5 folhas por corpo completo — ainda dentro
do orçamento de 10 por sessão.

## 11. O que o corpo base provou e o que não provou

**Provou:**
- 18 peças isoladas, nomeadas e montadas **apenas por dados** (`parts.json` + rig JSON).
- Proporção **5,88 cabeças** por construção (cabeça 34 u / corpo 200 u), dentro de 5,6–6,2.
- Half-shadow medido: traseiras/frontais = **0,69** (limite 0,80).
- Escala: 193,5 u medidos (alvo 200 ±5%).

**Não provou:**
- **Contorno:** ~1,0 px em 1x, contra o padrão de 1,6–2,8 px → **C3 reprovado**, score 83,3%.
- **Rotação:** nenhuma junta foi testada em ±35°. M1 continua aberto.
- **Articulação:** folga visível entre antebraço e mão (pivô de tipo ≠ punho real da peça).
- **Decais:** olhos e cabelo frontal precisam de normalização por largura e recorte de rosto.

## 12. Lição de processo

Duas trocas de identidade (`mão↔pé`, `cabelo↔face`) passaram despercebidas pelo pipeline e só apareceram
na **folha de contato** (`production/qa_reports/logs/contact_sheet_body_m_v1.png`).
Índice de componente **não** é identidade semântica: a conferência visual por folha de contato passa a ser
etapa obrigatória do processamento (`BL-016`).
