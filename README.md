# DRAGON BALL — AQW-STYLE COMPLETE GAME ASSET PACK

Biblioteca modular de assets 2D para jogos, com **identidade Dragon Ball** (DB, DBZ, DBS, DBGT e filmes) e
**linguagem gráfica inspirada em AdventureQuest Worlds** (Flash/cartoon vetorial, cel-shading chapado,
personagens paper-doll, cenários 2.5D em camadas e HUD de MMO).

O projeto **não é uma coleção de ilustrações**. É um pipeline de produção de recursos gráficos:
peças separadas com pivôs, rigs documentados, animações, metadados JSON, atlases, camadas de cenário,
kit de UI e documentação de integração — utilizável em Godot, Unity, GameMaker, Construct ou engine própria.

> **Battle on!** — mas com orçamento controlado: no máximo **10 gerações de imagem por sessão**.

---

## 1. Estado atual

| Item | Estado |
|---|---|
| Fase | **FASE 0 — Auditoria e Planejamento** (documentação) |
| Versão do pacote | `0.1.0` (documentação e infraestrutura, sem assets) |
| Assets registrados | `0` |
| Sessões de produção executadas | `0` |
| Gerações de imagem consumidas | `0` |
| Padrão visual | Definido em prosa (`docs/art_style_guide.md`), **ainda não validado em imagem** |

Nada foi declarado pronto. Este repositório contém, por enquanto, **planejamento, padrões e infraestrutura**.
O primeiro asset real só existirá após a Sessão `DB-SESSION-0001`.

Leia `docs/project_plan.md` para a visão completa e `docs/roadmap.md` para a sequência de execução.

---

## 2. Documentos-fonte (autoridade)

Os três documentos originais que originaram este projeto estão preservados em `docs/` e são **imutáveis**:

| Arquivo | Papel |
|---|---|
| `docs/asset_guide1.md` | Guia técnico/artístico v1 — paper-doll, 21 camadas, prompting, metadados |
| `docs/asset_guide2.md` | Guia v2 — estética detalhada, luz, half-shadow, UI, mapas, mecânicas |
| `docs/master-prompt.md` | Master Prompt — missão, autoridade, orçamento de gerações, estrutura, fases, critérios de aceitação |

**Hierarquia de decisão** (do `master-prompt`, §1), aplicada em todo o projeto:

1. Regras explícitas do Master Prompt.
2. Requisitos técnicos dos dois guides.
3. Continuidade visual/técnica dos assets já aprovados.
4. Referências canônicas de Dragon Ball.
5. Boas práticas de produção gráfica 2D.
6. Decisões criativas próprias do agente.

Os documentos derivados em `docs/` (este conjunto) **operacionalizam** essa hierarquia: não a substituem.

---

## 3. Mapa da documentação

| Documento | Conteúdo |
|---|---|
| `docs/README.md` | Índice, glossário e relação fonte → documento derivado |
| `docs/project_plan.md` | Planejamento: escopo, princípios, arquitetura de produção, riscos, governança |
| `docs/roadmap.md` | Roadmap por ondas/fases, marcos M0–M6, critérios de saída e estimativa de sessões |
| `docs/tooling_audit.md` | Auditoria real de capacidades e limitações das ferramentas disponíveis |
| `docs/production_pipeline.md` | Ciclo de sessão, orçamento de gerações, ledger, QA e promoção de assets |
| `docs/art_style_guide.md` | **Visual Bible** — contorno, cel-shading, luz, cor, proporção, material |
| `docs/technical_specification.md` | Escala canônica, resoluções, coordenadas, pivôs, atlas, performance |
| `docs/anatomy_and_rigging.md` | Rigs por arquétipo, hierarquia de bones, tabela de pivôs, ordem de camadas |
| `docs/animation_standard.md` | Animações obrigatórias, durações, eventos, hitboxes, timelines |
| `docs/equipment_standard.md` | Slots, ancoragem, compatibilidade, máscaras de cor, clipping |
| `docs/environments_standard.md` | Camadas parallax, tiles, escala, colisão, occluders, portais |
| `docs/vfx_standard.md` | Componentização de habilidades, blend modes, timing, legibilidade |
| `docs/ui_standard.md` | HUD, 9-slice, estados, resoluções, atlas, localização |
| `docs/naming_conventions.md` | IDs, nomes de arquivo, pastas, versionamento, migração |
| `docs/integration_guide.md` | Integração engine-agnostic (Godot/Unity/GameMaker/exemplos) |
| `docs/quality_checklist.md` | Máquina de estados, checklists, testes automáticos e gates |
| `docs/character_catalog.md` | Catálogo canônico priorizado por saga/continuidade (tiers P0–P2) |
| `docs/decisions/` | ADRs — decisões arquiteturais registradas |

Registros de produção (máquina):

| Arquivo | Papel |
|---|---|
| `production/generation_ledger.json` | Livro de controle de gerações por sessão |
| `production/production_backlog.json` | Backlog priorizado, executável |
| `production/asset_registry.json` | Catálogo técnico de assets (fonte da verdade dos IDs) |
| `production/continuity_state.json` | Estado do projeto para retomada sem perda de contexto |
| `production/schemas/*.json` | JSON Schemas de metadados de asset e de rig |
| `asset_manifest.json` | Manifesto público do pacote (o que existe, com hash e status) |

---

## 4. Estrutura de diretórios

Repositório raiz **é** a raiz do projeto (`dragonball-aqw-asset-pack`). A árvore-alvo vem do Master Prompt §4.

```text
.
├── README.md                 VERSION.md              LICENSE_NOTES.md
├── asset_manifest.json
├── docs/                     padrões, planejamento, ADRs, guides-fonte
├── references/               paletas, proporções, folhas de referência
│   ├── visual_bible/  palettes/  proportion_charts/  character_sheets/
├── characters/               base_bodies/ canonical_heroes/ canonical_villains/
│                             npcs/ transformations/ rigs/
├── equipment/                armor/ helmets/ hairstyles/ capes/ gloves/
│                             boots/ accessories/ weapons/
├── enemies/                  common/ elite/ bosses/
├── pets/                     companions/ creatures/ summons/
├── skills/                   icons/ projectiles/ auras/ melee/ beams/
│                             explosions/ buffs/ transformations/
├── environments/             backgrounds/ midgrounds/ foregrounds/ ground_tiles/
│                             props/ buildings/ portals/ maps/
├── ui/                       hud/ inventory/ equipment/ skills/ quests/ shop/
│                             chat/ dialogs/ character_creation/ icons/
├── exports/                  individual_png/ spritesheets/ atlases/ metadata/ previews/
├── production/               ledger, backlog, registry, continuity, reports, schemas, rejected
├── tools/                    validadores e utilitários de pipeline (Python + Pillow)
└── examples/                 sample_character/ sample_equipment/ sample_animation/
                              sample_map/ sample_ui/
```

**Regra de materialização de pastas:** nenhuma pasta é criada vazia para "parecer completa".
Cada raiz de categoria existe com um `README.md` que declara propósito, subpastas previstas e regras.
As subpastas nascem quando o primeiro asset daquela categoria é registrado.

---

## 5. Anatomia de um asset aprovado

Um asset só conta como entregue quando tem **todos** os itens aplicáveis:

```text
<asset_id>            ID único e permanente (ver docs/naming_conventions.md)
├── PNG(s)            RGBA, alpha real, sem resíduo de fundo
├── pivô(s)           em px (top-left, y↓) e normalizados, com nome de âncora
├── metadados JSON    valida o schema production/schemas/asset_metadata.schema.json
├── registro           entrada em production/asset_registry.json (status APPROVED)
├── preview           composição/imagem de verificação em exports/previews/
├── origem            sessão, prompt, referências canônicas usadas
└── dependências      rig, máscara de cor, atlas, animação que o consome
```

Imagem gerada **não é** asset aprovado. Somente `APPROVED` conta (ver `docs/quality_checklist.md`).

---

## 6. Como retomar o projeto (protocolo de retomada)

Qualquer agente ou pessoa que abrir este repositório deve, nesta ordem:

1. Ler `README.md` (este arquivo).
2. Ler `docs/art_style_guide.md` (Visual Bible).
3. Ler `docs/technical_specification.md` (especificações técnicas).
4. Ler `production/continuity_state.json` (estado real).
5. Ler o último relatório em `production/session_reports/`.
6. Consultar `production/asset_registry.json` (o que está aprovado).
7. Consultar `production/production_backlog.json` (próxima prioridade).
8. Conferir `production/generation_ledger.json` (orçamento da sessão corrente).
9. Retomar da próxima prioridade registrada — **nunca reiniciar do zero**.

Nunca regenere um asset `APPROVED` sem motivo técnico e decisão documentada.

---

## 7. Regras inegociáveis

- **Máximo de 10 gerações de imagem por sessão.** Meta operacional: 6–8 novas + 2–4 reservadas para correção.
- Não inventar arquivos, validações, rigs ou exports inexistentes.
- Não declarar fase concluída sem cumprir o critério de saída da fase.
- Não substituir asset completo por concept art.
- Não copiar, extrair ou redistribuir assets oficiais de AQW.
- Não apresentar o pacote como produto oficial ou licenciado de Dragon Ball.
- Preservar continuidade: IDs, escala, contornos, paleta e proporções não mudam sem ADR.

Direitos e limitações: ver `LICENSE_NOTES.md`.
