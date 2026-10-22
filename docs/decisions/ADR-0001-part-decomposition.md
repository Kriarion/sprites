# ADR-0001 — Decomposição de peças a partir de imagens geradas

- **Status:** Parcialmente substituída pelo `ADR-0006` (2026-10-22). O modo `grid` permanece como secundário.
- **Data:** 2026-10-22
- **Decisores:** Diretor de Arte + Technical Artist + Engenheiro de Pipeline
- **Afeta:** Fases 1–13, orçamento de gerações, gate G2, `tools/decompose.py`

## 1. Contexto

O projeto exige **peças realmente separadas** (21 por personagem), com alpha verdadeiro e pivôs corretos
(master §7.2, §7.3, §19.3). A ferramenta de geração disponível:

- produz **1 imagem por chamada**;
- não garante alpha real (tende a desenhar xadrez ou fundo branco);
- não obedece grades com precisão milimétrica;
- está limitada a **10 chamadas por sessão**.

Gerar "uma peça por chamada" é inviável: 21 peças × ~3 formas = 63 chamadas > orçamento de uma fase.
Gerar um personagem inteiro em uma chamada e "cortar os membros" também não funciona: as peças se tocam,
o corte é arbitrário e o pivô vira adivinhação.

## 2. Decisão

**Adotar geração em grade determinística com fundo chroma-key e pivô derivado de template.**

### 2.1 Template de folha de peças (`PART_SHEET`)

| Parâmetro | Valor |
|---|---|
| Canvas | **1024 × 1024** |
| Grade | **4 × 4** células |
| Célula | **256 × 256 px** |
| Área útil por célula | 224 × 224 px, centralizada (gutter de 16 px em cada lado) |
| Cor de fundo | `#FF00FF` chapado (ou `#00FF00` quando o objeto contiver magenta) |
| Ordem das peças | declarada no prompt e no template, posicional (célula 1 → peça 1) |
| Células não usadas | vazias, apenas fundo |
| Proibições no prompt | texto, rótulos, linhas de grade, sombra no chão, cenário, xadrez |

Um personagem completo usa **4 folhas** por forma:

| Folha | Peças | Células usadas |
|---|---|---|
| `PART_SHEET_A` | tronco, pelve, coxas (2), canelas (2), pés (2), braços superiores (2), antebraços (2), mãos (2) | 13 de 16 |
| `PART_SHEET_B` | cabeça base, cabelo frontal, cabelo traseiro, helm, olhos (2 estados), boca (2) | 8 de 16 |
| `PART_SHEET_C` | peças de roupa/armadura (até 16) | até 16 |
| `PART_SHEET_D` | arma(s) + acessórios grandes (2–4 objetos) | 2–4 |

### 2.2 Pipeline de extração

```text
1. cor de fundo = mediana das bordas
2. alpha = distância de cor > tolerância (default 70/255), com fechamento morfológico
3. erode 1 px + remoção de componentes < 24 px
4. despill: reduzir canal dominante do key nas bordas (Raio 2 px)
5. para cada célula (i,j) da grade: bbox da alpha dentro da área útil
6. cell-fit check: bbox deve caber em 224² e não tocar o gutter
7. corte com 2 px de respiro
8. nome = peça declarada na ordem do template
9. pivô = ponto nomeado do template, expresso em fração da bbox (ex.: forearm: 0.18, 0.06)
10. downscale LANCZOS do mestre (1024) para a escala de entrega
```

O **pivô vem do template**, não do desenho. Exemplo de entrada do template:

```json
{
  "template": "PART_SHEET_A",
  "cell_px": 256,
  "content_px": 224,
  "background": "#FF00FF",
  "cells": [
    { "index": 0,  "part": "torso",         "anchor": "spine_low",   "layer": 11, "pivot": [0.50, 0.92] },
    { "index": 1,  "part": "pelvis",        "anchor": "root",        "layer": 10, "pivot": [0.50, 0.10] },
    { "index": 2,  "part": "thigh_front",   "anchor": "hip.front",   "layer": 12, "pivot": [0.50, 0.06] },
    { "index": 3,  "part": "thigh_back",    "anchor": "hip.back",    "layer": 7,  "pivot": [0.50, 0.06] }
  ]
}
```

### 2.3 Critério de sucesso do spike (Sessão 0001)

| Métrica | Meta | Se falhar |
|---|---|---|
| Peças separadas corretamente | ≥ 10 de 12 | revisar prompt/template (1 rodada de correção) |
| Peças dentro da célula (`cell-fit`) | ≥ 90% | reduzir densidade da grade (3×3) |
| Resíduo de fundo | < 0,5% da área | ajustar tolerância/despill |
| Pivô alinhado (teste de rotação 8 ângulos) | 100% sem gap > 2 px | revisar fração do template |

Duas falhas consecutivas → acionar plano B (§6) e registrar `BLOCKED` para o formato de folha única.

## 3. Alternativas consideradas

| Alternativa | Prós | Contras | Veredito |
|---|---|---|---|
| **A. Uma peça por chamada** | qualidade e pivô triviais | 21+ chamadas por personagem; estoura o orçamento por 3× | rejeitada |
| **B. Personagem inteiro + corte por componentes conexos** | 1 chamada | peças se tocam; corte arbitrário; pivô adivinhado; membros traseiros somem no escuro | rejeitada como principal (mantida como fallback §6) |
| **C. Poses completas e "desmontagem" manual** | parece arte final | não é peça independente; viola master §19.3 | rejeitada |
| **D. Grade determinística + chroma-key + pivô de template** | 4–5 chamadas por personagem; pivô determinístico; auditável | depende de o gerador respeitar o layout; exige ferramenta de keying | **aceita** |
| **E. Geração vetorial / edição em Illustrator** | qualidade ideal | ferramenta inexistente no ambiente | rejeitada por impossibilidade |

## 4. Consequências

**Positivas**
- Personagem completo em **4–5 chamadas** (dentro do orçamento de 10).
- Pivô auditável e repetível (mesma fração para todos os personagens do mesmo rig).
- Segmentação scriptável → cada peça é um arquivo, atendendo ao master §19.3.
- Custo de correção baixo: refaz-se **uma folha**, não o personagem.

**Negativas / custos**
- Exige `tools/key.py` e `tools/decompose.py` antes de qualquer asset aprovado (bloqueia W1).
- O gerador pode desrespeitar a grade → taxa de reprovação maior nas primeiras sessões.
- Peças grandes (asas, cabelo longo, cauda) não cabem em 224 px → precisam de folha própria (1 chamada extra).
- Fundo magenta pode vazar em objetos magenta (ex.: Majin Buu) → usar verde nesses casos e registrar no prompt.

## 5. Riscos residuais

| Risco | Mitigação |
|---|---|
| Peças adjacentes se fundem | gutter 16 px + prompt proibitivo + `cell-fit` check |
| Contorno é comido pelo erode | erode máx. 1 px; validar espessura no G1 |
| Escala inconsistente entre peças da mesma folha | manter mesmo tamanho aparente no prompt + overlay de proporção |
| Peça "genérica" (ex.: pulso sem mão) | nomear função na ordem do prompt e validar semanticamente no G1 |

## 6. Plano B (se o spike falhar)

1. **Reduzir densidade:** grades 2×2 / 3×3 com peças maiores (menos peças por chamada).
2. **Folhas por membro:** 1 chamada para "perna completa desmembrada" (3 peças) etc.
3. **Recorte assistido por componente conexo** dentro da célula, quando houver toque leve.
4. Se nada funcionar de forma consistente: os resultados passam a ser classificados como
   **`REFERENCE_ONLY`** (referência visual pendente de produção técnica, master §19.3) e o projeto precisa
   de revisão de escopo — nunca de "aprovação por conveniência".

## 7. Quando revisitar

- Ao final da `DB-SESSION-0001` (obrigatório, com números medidos).
- Sempre que a taxa de aprovação de folhas cair abaixo de 60% em uma sessão.
- Se a plataforma passar a oferecer geração com alpha nativo ou controle de layout.
