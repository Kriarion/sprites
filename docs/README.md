# docs/ — Índice documental

Este diretório contém três camadas de documentos:

1. **Fonte (imutável)** — os três documentos originais do projeto.
2. **Padrões (normativos)** — derivados dos fontes, são a autoridade operacional do dia a dia.
3. **Decisões (ADRs)** — registro do *porquê* de cada escolha técnica, com alternativas descartadas.

## 1. Documentos-fonte (não editar)

| Arquivo | Origem | Conteúdo | Uso |
|---|---|---|---|
| `asset_guide1.md` | Guia 1 | Paper-doll de 21 camadas, pivôs, animação esqueletal, VFX, cenários, HUD, templates de prompt, esquema JSON | Referência técnica primária |
| `asset_guide2.md` | Guia 2 | Estética detalhada, luz superior-frontal, half-shadow, materiais, UI clássica, mapas multicamada, mecânicas de MMO | Referência artística primária |
| `master-prompt.md` | Master Prompt | Missão, hierarquia, orçamento de 10 gerações/sessão, estrutura de pastas, IDs, fases, metas, QA, autonomia, direitos | **Autoridade máxima** |

Qualquer edição nesses arquivos exige ADR e bump de versão em `VERSION.md`.

## 2. Documentos normativos (derivados)

| Documento | Deriva de | Responde a |
|---|---|---|
| `project_plan.md` | master §0, §2, §21, §26, §28 | Como o projeto se organiza, o que está dentro/fora do escopo, riscos |
| `roadmap.md` | master §21, §22, §29 | Em que ordem, em quantas sessões, com quais critérios de saída |
| `tooling_audit.md` | master §29 PASSO 2 | O que as ferramentas disponíveis realmente fazem |
| `production_pipeline.md` | master §3, §19, §20, §25 | O ciclo de sessão e a promoção de asset |
| `art_style_guide.md` | guia1 §1, guia2 §1, master §6 | **Visual Bible**: contorno, cor, luz, proporção, material |
| `technical_specification.md` | guia1 §2, §7; guia2 §10; master §18 | Escala, resolução, coordenadas, pivôs, atlas, performance |
| `anatomy_and_rigging.md` | guia1 §2, guia2 §2, master §7 | Rigs, bones, pivôs, ordem de camadas |
| `animation_standard.md` | guia1 §3, guia2 §2, master §11 | Animações, durações, eventos, hitboxes |
| `equipment_standard.md` | guia1 §4, guia2 §6, master §10 | Slots, ancoragem, compatibilidade, máscaras |
| `environments_standard.md` | guia1 §7, guia2 §8, master §15 | Camadas, tiles, colisão, parallax |
| `vfx_standard.md` | guia1 §6, guia2 §4, master §12 | Componentização, blending, legibilidade |
| `ui_standard.md` | guia1 §8, guia2 §7, master §16 | HUD, 9-slice, estados |
| `naming_conventions.md` | master §5, §18.4 | IDs, arquivos, versões, migração |
| `integration_guide.md` | master §18.5 | Uso em engines |
| `quality_checklist.md` | master §23 | Gates, checklists, testes |
| `character_catalog.md` | master §8, §9 | Catálogo canônico priorizado |

## 3. ADRs

| ADR | Decisão |
|---|---|
| `decisions/ADR-0001-part-decomposition.md` | Como obter peças **realmente separadas** a partir de geração de imagem |
| `decisions/ADR-0002-canonical-scale.md` | Escala canônica, unidades de rig e resoluções de export |
| `decisions/ADR-0003-data-format.md` | Formato de dados engine-agnostic (PNG + JSON, sem proprietário) |
| `decisions/ADR-0004-generation-budget.md` | Política de orçamento de gerações e ledger |
| `decisions/ADR-0005-content-waves.md` | Waves de conteúdo e critérios de promoção |

---

## 4. Glossário (termos usados em todos os documentos)

| Termo | Definição |
|---|---|
| **Asset** | Unidade entregável identificada por ID, com PNG + metadados + status. Não é "uma imagem". |
| **Peça (part)** | Fragmento modular de um asset (ex.: `front_forearm`). Tem PNG próprio e pivô. |
| **Paper-doll** | Sistema em que o corpo é composto por peças sobrepostas com pivôs, em vez de desenhos inteiros. |
| **Rig** | Hierarquia de bones + limites articulares + âncoras que recebe as peças. |
| **Pivô** | Ponto de rotação de uma peça, em px, coordenadas top-left/y↓, mais versão normalizada. |
| **Âncora** | Nome semântico do encaixe (`neck`, `shoulder.front`). Pivô é o valor; âncora é o significado. |
| **u (unidade de rig)** | 1 u = 1 px na escala 1x. Corpo adulto = 200 u. |
| **1x / 2x / 4x** | Multiplicadores da escala canônica (200 / 400 / 800 px de altura). |
| **Sessão** | Unidade de produção com orçamento próprio de ≤10 gerações, ID `DB-SESSION-XXXX`. |
| **Geração** | Uma chamada à ferramenta de geração de imagem. Variações/edições contam separadamente. |
| **Lote (batch)** | Conjunto coeso de assets gerados na mesma sessão (mesmo personagem/paleta/rig). |
| **Promoção** | Passagem de um asset por gates G0→G5 até `APPROVED`. |
| **VAZIO/alfa real** | Canal alpha verdadeiro, sem fundo branco/preto/xadrez simulado. |
| **Chroma-key** | Remoção de fundo por cor de contraste (magenta/verde), seguida de despill. |
| **Half-shadow** | Convenção AQW de escurecer membros traseiros para criar profundidade com economia. |
| **9-slice** | Técnica de UI: painel escalável por 9 regiões com margens fixas. |
| **Occluder** | Elemento de primeiro plano que esconde parcialmente o personagem. |
| **Dummy** | Corpo neutro cinza/branco usado para testar peças e máscaras de cor. |
| **Wave** | Agrupamento de sessões com objetivo de fase comum. |
| **Gate** | Ponto de controle obrigatório; sem ele o asset não avança de status. |
