# ADR-0006 — Decomposição por componentes conexos + normalização anatômica

- **Status:** Aceita
- **Data:** 2026-10-22
- **Substitui parcialmente:** ADR-0001 §2 (grade determinística como modo primário)
- **Evidência:** `docs/calibration_report.md` §2–§6, logs em `production/qa_reports/logs/`

## 1. Contexto

A `DB-SESSION-0001` testou a arquitetura do ADR-0001 (grade 4×4 rígida + corte por célula) e ela **falhou
de forma reprodutível**:

| Teste | Resultado |
|---|---|
| Grade 4×4 com 12 peças | 16/16 células ocupadas, 13 violações de gutter, 6 células multi-fragmento |
| Grade 3×3 com peças singulares | 9/9 ocupadas, ainda com pares espelhados e peça atravessando linha |
| 9 objetos **distintos por função** | 9/9 componentes isolados, 1 fragmento por objeto |

Duas causas ficaram claras:
1. **O gerador não trata grade como contrato.** Ele recompõe o layout (colapsa colunas, duplica simetria).
2. **Escala relativa entre peças não existe.** Cada célula é preenchida individualmente; a mão pode sair
   maior que o torso. Montagem direta resultou em boneco desmontado (ver `assembly_armor_test.png`, iteração 1).

## 2. Decisão

### 2.1 Modo primário: componentes conexos sobre objetos distintos

Abandonar a grade como contrato de extração. O prompt passa a especificar **N objetos distintos por função**
em regiões separadas (sem gutter numérico, sem coordenadas de célula). A extração é feita por
**rotulagem de componentes conexos** do alpha, com binarização e remoção de ruído.

Consequências:
- O nome da peça **não** vem da posição — vem de **ordem de leitura validada visualmente** (curadoria humana
  ou do agente no gate G1) e registrada em `parts.json`.
- Peças simétricas (par L/R) que vierem no mesmo objeto são **um único PNG** e devem ser declaradas
  `mirrored_pair: true` — a engine as usa como duas instâncias espelhadas. Isso é aceitável e reduz trabalho.
- O modo `grid` do `decompose.py` permanece disponível como **secundário**, para folhas que por acaso
  respeitem grade (ex.: frames de VFX em matriz regular, que o gerador tende a respeitar melhor).

### 2.2 Normalização anatômica obrigatória

Toda peça é **redimensionada para a dimensão canônica do seu tipo** (tabela `PART_DIMS_U` em
`tools/compose.py`, derivada de `technical_specification.md` §2.2) antes de qualquer montagem ou export.

- A escala é uniforme (mesmo fator em X e Y) para não deformar a arte.
- O fator aplicado é registrado (`normalized_scale` no relatório de montagem) e auditável.
- Sem normalização, a montagem é **proibida** — o resultado não é evidência de nada.

### 2.3 Pivô por tipo + validação de montagem

O pivô continua vindo de template (ADR-0001 §2.2), mas agora indexado por **tipo de peça**, não por célula.
Um pivô só é aceito após o **teste de montagem** e o **teste de rotação ±35°** em 8 ângulos.

Âncoras corrigidas por evidência:
- `pelvis` → âncora `pelvis` (**não** `root`: `root` é a origem no chão, usada pela sombra e pelo hitbox).
- ombreira única → `shoulder.front` (e não `spine_high`, que é a âncora **de pares** de ombreira).

## 3. Alternativas consideradas

| Alternativa | Problema |
|---|---|
| Insistir na grade 4×4 com prompt mais rígido | 2 tentativas já falharam; modelo trata layout como sugestão |
| Uma peça por geração | 21+ chamadas por personagem; estoura o orçamento em 3× |
| Aceitar escalas arbitrárias e "ajustar no olho" | não é pipeline; não é reproduzível; viola o gate G3 |
| Cortar peças manualmente por bbox fixa | volta a depender de layout que não existe |

## 4. Consequências

**Positivas**
- Extração **funcional e comprovada**: 9/9 objetos isolados, alpha limpo, 1 componente cada.
- A normalização transforma peças de escalas arbitrárias em um boneco montável — resolve o defeito da iteração 1.
- Menos chamadas por personagem do que "uma peça por imagem".
- Pares espelhados passam a ser **vantagem** (metade do trabalho para metade das peças).

**Negativas / custos**
- Nomear peças exige **validação visual** (não é posicional). Custo humano/agente por folha, não por imagem.
- `mirrored_pair` precisa ser respeitado pela engine (ou desmembrado por script de espelhamento, que preserva
  a peça original).
- A normalização pode gerar diferença de proporção **dentro** da peça (ex.: canela mais curta que o canônico):
  isso é detectado no G1, não corrigido por escala.

## 5. Critérios de sucesso para a próxima sessão

| Métrica | Meta | Se falhar |
|---|---|---|
| Componentes por folha de corpo | 9–12, 1 fragmento cada | reduzir para 6 objetos por folha |
| Normalização + montagem de corpo completo (21 peças) | membros encaixam sem gap > 4 u | revisar `PART_DIMS_U` com medição real |
| Rotação ±35° nas 12 juntas | sem abertura visível | ajustar pivô do tipo + sangria de junta |
| Proporção medida (`measure.py`) | 5,5 cabeças ± 5% | recalibrar percentuais do prompt |

## 6. O que NÃO muda

- Orçamento de 10 gerações por sessão (ADR-0004).
- Chroma-key magenta e alpha real (funcionou: halo 0,0%).
- Contorno, cel-shading, luz e paleta (Visual Bible 1.1.0).
- Entrega neutra PNG + JSON (ADR-0003).
- Regra de honestidade: peça incompleta não é asset aprovado.
