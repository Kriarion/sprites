# PADRÃO DE COERÊNCIA DO PACOTE (normativo)

**Versão:** 1.0.0 · **Base:** ADR-0007, `art_style_guide.md` 1.2.0, `technical_specification.md` 1.1.0
**Ferramenta:** `tools/coherence.py` · **Relatório:** `production/coherence_report.json`

> O objetivo final do projeto não é "ter assets". É ter **um pacote que conversa entre si**: qualquer peça
> pode ser montada com qualquer outra, do mesmo personagem ou de outro, e o resultado parece o mesmo jogo.
> Isso não se garante com cuidado artesanal — garante-se com **invariantes medidos**.

---

## 1. Os seis invariantes

| # | Invariante | O que mede | Tolerância | Falha típica |
|---|---|---|---|---|
| **C1** | Escala | altura do corpo em `u`, `pixels_per_unit` | 200 u ±5%; ppu ∈ {1,2,4} | peça exportada em 1x e usada como 2x |
| **C2** | Proporção | razão cabeça/altura; posição de ombro, quadril, joelho | 5,60–6,20 cabeças; ±4 u | personagem "realista" entre personagens cartoon |
| **C3** | Peso de contorno | espessura média da linha escura ÷ altura do corpo | **0,8–1,4%** (1,6–2,8 px em 1x) | contorno fino em asset importado de outro lote |
| **C4** | Paleta | ΔH, ΔS, ΔV dos pontos canônicos vs paleta aprovada | ΔH ≤ 8°, ΔS ≤ 10%, ΔV ≤ 10% | laranja do gi mais saturado em outra sessão |
| **C5** | Half-shadow | luminância média das peças traseiras ÷ frontais | ≤ 0,80 | membro traseiro claro "achatando" a profundidade |
| **C6** | Estrutura | âncora + camada no vocabulário; sem camada duplicada; pivô dentro da peça | 100% | dos ombros ancorados em `spine_high` |

**Regra dura:** um asset não pode ser `APPROVED` com qualquer invariante fora de tolerância.
**Regra de padrão:** se um invariante reprova **todos** os assets de uma categoria, o padrão está errado —
abre-se ADR e revisa-se o padrão. Nunca se "ajusta o asset até caber".

---

## 2. Como as métricas são obtidas

### C1 — Escala
Lida dos metadados (`scale.body_height_u`, `scale.pixels_per_unit`) e conferida contra a altura medida do
PNG (silhueta). Divergência > 5% → falha.

### C2 — Proporção
`tools/measure.py`: separa a silhueta, acha o topo do crânio, o pescoço (mínimo local de largura no terço
superior) e calcula `altura / altura_da_cabeça`. A linha do ombro, quadril e joelho é conferida contra a
tabela canônica de `technical_specification.md` §2.2.

### C3 — Peso de contorno
Máscara de pixels escuros (luminância < 60) na silhueta; espessura estimada por
`2 × mediana(distance_transform(escuro))` sobre a região de linha. Razão = espessura ÷ altura total.
Alvo: **1,6–2,8 px em 1x** num corpo de 200 px.

> **Revisão 1.1 (medida na `DB-SESSION-0002`):** a faixa original (0,9–1,3% ≈ 1,8–2,6 px) reprovou **todas** as
> 18 peças do corpo base com mediana **1,7 px em 1x** (0,857%). A causa é o downscale do mestre de 1024 px:
> a redução consome ~15% da espessura da linha. Como o gerador entrega 1,7 px de forma consistente e o guia 2
> descreve o traço original como *hairline* (≈1,5–2 px em 1x), a faixa foi corrigida **pela medição**, não pelo
> gosto. Histórico: 0,009–0,013 (v1.0) → 0,008–0,014 (v1.1).

> **Medição 2 (`DB-SESSION-0002`, corpo base):** com a fórmula área÷perímetro a mediana das 18 peças deu
> **0,0046**, e a checagem independente por transformada de distância (espessura = 2 × distância ao contorno)
> deu **1,12 px em 1x** (0,56% da altura) nas peças frontais. As duas fórmulas **não** são a mesma grandeza:
> área÷perímetro estima ~metade da espessura geométrica em linhas finas. Conclusão: **C3 continua FAIL** e o
> número que vale é o da transformada de distância (1,12 px), não a razão normalizada.
> Correção tentada e descartada: dilatar 1 px a máscara escura engrossa também as linhas internas
> (abdômen, orelha) e serrilha o traço — evidência em `production/qa_reports/logs/thicken_compare.png`.
> Decisão pendente: `PENDING-004` em `production/continuity_state.json` (A: mestre com 3–4 px ·
> B: máscara de borda · C: revisar a faixa).

### C4 — Paleta
Cinco pontos canônicos são amostrados por k-means leve no interior da peça (pele, cabelo, tecido, metal,
energia) e convertidos para HSV. Comparação com `references/palettes/core_palettes.json`.

### C5 — Half-shadow
Luminância média das peças com `layer` **traseiro** (2,3,4,5,6,7,8,9) contra as peças frontais
equivalentes (1,18,19,20,12,13,14). Razão deve ser ≤ 0,80.

### C6 — Estrutura
Validação direta contra `anatomy_and_rigging.md` §1 (camadas) e §4 (âncoras); pivô dentro da imagem;
nenhuma camada repetida no mesmo personagem.

---

## 3. Score de coerência

`tools/coherence.py` emite, por asset, os seis invariantes com `PASS/FAIL` e o valor medido, e no fim um
**score do pacote**:

```text
coherence_score = (invariantes PASS) / (invariantes avaliados) × 100
```

| Score | Leitura |
|---|---|
| 100% | pacote coerente; pode avançar de wave |
| 90–99% | coerente com pendências localizadas; corrigir na sessão seguinte |
| 70–89% | drift real; **parar** e corrigir antes de produzir mais |
| < 70% | padrão quebrado; voltar à Visual Bible |

O relatório é gerado em **toda** sessão e anexado ao relatório de sessão. Sem ele, a sessão não fecha.

---

## 4. Coerência em três níveis

### 4.1 Dentro do asset (intra)
As peças de um personagem devem compartilhar escala, contorno e paleta **entre si**, não só com o padrão.
Falha clássica: uma peça corrigida em outra geração entra maior que as vizinhas (visto na `DB-SESSION-0001`).

### 4.2 Entre assets do mesmo tipo (inter)
Dois personagens lado a lado devem parecer do mesmo jogo: mesma altura, mesmo peso de linha, mesma luz.
Um chefe pode ser maior — mas continua com o mesmo contorno e a mesma direção de luz.

### 4.3 Entre categorias (global)
Personagem × equipamento × cenário × UI: o contorno do personagem é forte, o do cenário é sutil, o da UI é
definido. Essa **hierarquia de contraste** é o que mantém a leitura. Quebrar isso (prop com contorno mais
grosso que o personagem) destrói a legibilidade mesmo com todas as peças tecnicamente válidas.

---

## 5. Aplicação por categoria

| Categoria | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|
| Personagem (corpo) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Equipamento | ✅ | — | ✅ | ✅ | n/a | ✅ |
| Inimigo / boss | ✅ | ✅ (escala própria declarada) | ✅ | ✅ | ✅ | ✅ |
| Pet | ✅ (25–33%) | ✅ | ✅ | ✅ | ✅ | ✅ |
| VFX | ✅ | — | n/a | ✅ | n/a | ✅ |
| Cenário | ✅ | — | ✅ (sutil) | ✅ | n/a | ✅ |
| UI | ✅ | — | ✅ | ✅ | n/a | ✅ |

"—" = não se aplica. "n/a" = não aplicável por natureza do asset.

---

## 6. Procedimento de sessão

```text
1. processar peças
2. montar (compose.py --normalize)
3. medir (measure.py)
4. auditar (coherence.py)  ← novo, obrigatório
5. se FAIL em C2/C3 → corrigir peça (reserva de orçamento) ou reprovar
6. se FAIL em C4 → comparar com paleta aprovada da ficha, não com "a cor bonita"
7. registrar em production/coherence_report.json + relatório de sessão
```

Nenhum relatório de sessão é aceito sem `coherence_report.json` atualizado.

---

## 7. O que este padrão NÃO faz

- Não julga criatividade, composição ou "charme" — isso é o gate G1 (visual), humano/agente.
- Não mede silhueta única de boss (subjetivo).
- Não substitui o teste de montagem (G3): um pacote pode ser coerente e ainda assim não montar.
- Não impede drift intencional e documentado (ex.: cenário noturno com paleta deslocada) — desde que
  registrado como exceção no ADR do caso.

Coerência é **necessária**, não suficiente. Junto com G1 (visual) e G3 (funcional), forma a base de
aceitação do pacote.
