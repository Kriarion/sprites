# ROADMAP DE PRODUÇÃO

**Versão:** 1.0.0 · **Data:** 2026-10-22 · **Base:** master §21–§22, §29

O roadmap é organizado em **waves** (agrupamentos de fases) e **sessões** com orçamento fechado.
Não há datas: a unidade de progresso é a **sessão** (`DB-SESSION-XXXX`), limitada a 10 gerações de imagem.
Estimar em calendário só é honesto depois que a primeira wave medir a taxa real (ver §8).

---

## 1. Visão geral

| Wave | Fase | Objetivo | Sessões | Gerações (máx.) | Marco |
|---|---|---|---|---|---|
| **W0** | F0 | Auditoria, planejamento, infraestrutura, padrões | 1 (esta) | 0 | **M0** |
| **W1** | F1 | Visual Bible validada em imagem + pipeline de peças provado | 2 | 16 | **M1** |
| **W2** | F2 | Corpos base, rigs, montagem e máscaras | 3 | 27 | **M2** |
| **W3** | F3 | Vertical slice Goku completo | 6 | 51 | **M3** |
| **W4** | F4 | Roster de personagens principais | 9 | 80 | **M4** |
| **W5** | F5 | Transformações e auras | 5 | 42 | — |
| **W6** | F6 | Equipamentos, armas, helms, capas | 7 | 62 | — |
| **W7** | F7 | Habilidades e VFX | 7 | 60 | **M5** |
| **W8** | F8 | Inimigos, elites e bosses | 7 | 60 | — |
| **W9** | F9 | Pets e companheiros | 4 | 32 | — |
| **W10** | F10 | Ambientes e mapas | 6 | 50 | — |
| **W11** | F11 | HUD e UI completa | 6 | 48 | — |
| **W12** | F12 | Expansão por saga (contínua) | 12+ | 100+ | — |
| **W13** | F13 | Integração, QA final, release | 4 | 20 | **M6** |

**Total estimado até `1.0.0`: ~79 sessões, ~648 gerações** (com 2.500–3.500 peças/assets resultantes).

> As estimativas de gerações são **tetos**, não metas. Sessão que termina com 6 gerações e 3 peças
> aprovadas é melhor que sessão que gasta 10 e reprova 6.

---

## 2. Marcos (milestones)

| Marco | Nome | Critério objetivo de atingimento |
|---|---|---|
| **M0** | Base documental | Planejamento, roadmap, Visual Bible, especificações, ADRs e registros criados; 0 assets |
| **M1** | Estilo e pipeline provados | Existe **1 prancha de estilo aprovada** e **1 conjunto de peças recortadas de uma grade**, com alpha real, > pivô derivado e montagem de teste. Pipeline de recorte é script, não manual |
| **M2** | Rig funcional | Corpo masculino e feminino montados a partir de 21 peças independentes; rotação de ±35° em cada junta sem abertura; rig JSON valida no schema |
| **M3** | Goku jogável | Desenvolvedor externo monta e anima Goku (idle, run, attack, kimehameha) apenas com os arquivos entregues, sem redesenhar nada |
| **M4** | Roster inicial | 8 personagens jogáveis aprovados com rig compartilhado e preview de montagem |
| **M5** | Combate e magia | Kamehameha, Galick Gun, Final Flash e ≥12 VFX genéricos componentizados + ícones |
| **M6** | Pack 1.0.0 | Metas do master §22 atingidas, QA final aprovado, integração demonstrada em pelo menos 1 engine |

---

## 3. W0 — Fase 0: Auditoria e Planejamento *(concluída na entrega de documentação)*

**Sessão:** `DB-SESSION-0000` (sem gerações).

Entregáveis:

- `README.md`, `VERSION.md`, `LICENSE_NOTES.md`, `asset_manifest.json`.
- `docs/`: planejamento, roadmap, auditoria de ferramentas, pipeline, Visual Bible, especificação técnica,
  anatomia/rigging, animação, equipamentos, ambientes, VFX, UI, nomenclatura, integração, qualidade, catálogo.
- `docs/decisions/ADR-0001..0005`.
- `production/`: ledger, backlog, registry, continuity, schemas, templates de relatório.
- `references/palettes/core_palettes.json` (paletas canônicas iniciais).
- `tools/README.md` (contrato das ferramentas a construir na W1).

**Critério de saída:** ✅ pipeline definido, padrões escritos, backlog inicial registrado, zero asset declarado.

---

## 4. W1 — Fase 1: Visual Bible validada + spike de pipeline

**Objetivo:** provar, com imagem, que (a) o estilo é reproduzível e (b) peças podem ser extraídas de uma
grade determinística com alpha real e pivô correto. **Nada canônico é produzido ainda** — o alvo é um
*dummy* neutro, para separar "acertar o estilo" de "acertar o personagem".

### DB-SESSION-0001 — Calibração de estilo e spike de decomposição

Orçamento: **6 novas + 4 reservadas = 10**

| # | Chamada | Conteúdo | Uso |
|---|---|---|---|
| G1 | `REF_STYLE_DUMMY` | Dummy neutro masculino M/F, frente e perfil, corpo inteiro | Calibrar proporção, linha, cel-shading |
| G2 | `REF_SHADING_MATERIALS` | Estudo de 3 tons + half-shadow + 4 materiais (metal, couro, tecido, energia) | Calibrar cor e luz |
| G3 | `PART_SHEET_A` | **Grade 3×4, 12 peças** do corpo (torso, pelve, coxas, canelas, pés, braços, antebraços, mãos) em fundo magenta uniforme | Spike do pipeline de split |
| G4 | `HEAD_SHEET` | Grade 2×2: cabeça neutra M, F, infantil, musculosa — com pivô de pescoço visível | Spike de âncoras de cabeça |
| G5 | `WEAPON_SHEET` | Grade 2×2: 4 armas oversized, cabo alinhado ao eixo vertical | Referência de arma + spike de grip |
| G6 | `UI_PROBE` | Moldura de painel + barra HP/Ki + 6 ícones em grade | Referência de UI |

Reserva (4): correção de G3/G4 (as duas chamadas de maior risco), re-key de alpha, refazer grade.

**Processamento obrigatório:** `tools/decompose.py` (keying → alpha → bbox → split por célula),
`tools/validate_assets.py` (alpha, dimensões, pivô), montagem de teste em `examples/sample_character/`.

**Critério de saída da sessão:** G3 produz ≥10 peças com alpha real e bbox dentro da célula esperada.

### DB-SESSION-0002 — Fechamento da Visual Bible v1.1

Orçamento: **0–2 novas + 4 de correção**

- Consolidar o que as imagens reprovaram/confirmaram na Visual Bible (linha, cor, proporção).
- Validar/completar `tools/` (decompose, validate, compose, atlas).
- Atualizar ADR-0001 com o resultado real do spike (funcionou? qual tolerância? fallback?).
- Congelar `art_style_guide.md` em `1.1.0` e `references/visual_bible/` com as pranchas aprovadas.
- Criar `references/proportion_charts/body_200u.png` (overlay de proporção a partir do rig, gerado por script).

**Critério de saída da fase (M1):** estilo aprovado em imagem + pipeline de peças provado + ADR-0001
atualizado com evidência. Se o spike falhar, **a fase não avança** e o plano B (ADR-0001 §6) entra em vigor.

---

## 5. W2 — Fase 2: Corpos e rigs

| Sessão | Objetivo | Novas | Reserva |
|---|---|---|---|
| `DB-SESSION-0003` | Corpo base masculino + feminino: grade completa de 21 peças cada, pivôs | 7 | 3 |
| `DB-SESSION-0004` | Corpo musculoso + infantil + base Namekuseijin | 7 | 3 |
| `DB-SESSION-0005` | Bases Majin, androide humanoide, raça de Freeza, criatura pequena; rigs JSON | 7 | 3 |

Entregáveis da wave: 10 rigs base (master §7.4), tabela de pivôs, `dummies` neutros, máscaras de cor
(skin/hair/cloth/metal), teste de montagem em 3 poses (idle, corrida, ataque), preview de proporção.

**Critério de saída (M2):** masculino e feminino montados a partir de peças independentes, rotação ±35°
sem abertura visível em todas as juntas, rig valida no schema.

---

## 6. W3 — Fase 3: Vertical slice Goku

| Sessão | Objetivo | Novas | Reserva |
|---|---|---|---|
| `DB-SESSION-0006` | Ficha canônica Goku (frente/perfil/costas, gi, botas, faixa, kanji) + extração de paleta | 6 | 4 |
| `DB-SESSION-0007` | Corpo e membros de Goku (2 grades) + pivôs | 7 | 3 |
| `DB-SESSION-0008` | Cabeça, cabelo, expressões (blink, dano, grito) + gi modular (torso, faixa, botas, pulseiras) | 7 | 3 |
| `DB-SESSION-0009` | Poses e timelines: idle, run, attack01/02, heavy, ki_cast, hit, death | 7 | 3 |
| `DB-SESSION-0010` | Kamehameha componentizada (cast_start, charging, core, segmento, ponta, impacto, explosão, partículas, ícone) + retrato HUD | 8 | 2 |
| `DB-SESSION-0011` | Montagem final, previews, QA completo, release do pacote `0.4.0` | 0 | 3 |

**Critério de saída (M3):** um desenvolvedor externo, só com os entregáveis, monta e anima Goku.
Nenhuma peça redesenhada por ele. Kamehameha remontável com peças distintas.

> Regra de parada: **não** avançar para W4 antes de M3. É aqui que os padrões provam seu valor ou falham.

---

## 7. W4–W13

### W4 — Fase 4: Personagens principais (9 sessões)

Ordem por reutilização de rig (do mais próximo ao mais distante do corpo masculino aprovado):
Vegeta → Piccolo → Gohan (adolescente/adulto) → Kuririn → Trunks → Gohan criança → Bulma → Freeza → Cell.

Cada personagem: 1 sessão de ficha canônica (compartilhável entre 2 personagens quando da mesma saga) +
1–2 sessões de partes. Meta: 8 jogáveis + 10 NPCs (Kame, Chi-Chi, Dende, Mr. Satan, Videl, Rei Kaiô, Kaiohshin…).

### W5 — Fase 5: Transformações (5 sessões)

SSJ → SSJ2 → SSJ3 → SSG/SSB → SSJ4/UI/Ultra Ego/Beast → Golden Freeza/Potencial Liberado/Majin.
Cada transformação: cabelo, sobrancelhas, olhos, pele, aura (2 camadas + partículas), ativação/desativação,
idle específico, ícone, retrato (master §9.2). Oozaru recebe rig próprio.

### W6 — Fase 6: Equipamentos (7 sessões)

Armaduras (Saiyajin, Ginyu, Freeza, Red Ribbon, Capsule Corp, fusão, Great Saiyaman, Piccolo) →
armas (≥50) → helms/capas/cabelos → acessórios (scouters, Potara, Radar, cápsulas, pesos).
Cada peça precisa passar pelo teste de montagem em 3 bases (M/F/musculoso) e 3 poses.

### W7 — Fase 7: Habilidades e VFX (7 sessões)

Kamehameha refinada → Galick Gun, Final Flash, Big Bang, Masenko, Makankosappo → Genki Dama, Kienzan,
Solar Flare, Kaioken, Death Beam/Ball → Instant Transmission, Hakai → pacote genérico (slash, impacto,
escudo, cura, buff/debuff, aura, explosão) → ícones (≥100 ao final da fase 7+11).

### W8 — Fase 8: Inimigos e bosses (7 sessões)

Comuns (Saibaman, Red Ribbon, soldados de Freeza, Cell Juniors, capangas de Babidi) → elites (Raditz,
Nappa, Zarbon, Dodoria, Ginyu) → bosses (Freeza, Cell, Majin Buu, Broly, Janemba, Beerus, Jiren, Baby,
Omega Shenron). Boss gigante com segmentação própria e escala própria.

### W9 — Fase 9: Pets (4 sessões)

Puar, Oolong, Giru, Icarus, criaturas de Namekusei, robôs auxiliares (20–50 no total).
Escala 25–33% do padrão, rig ultrassimplificado, animações idle/follow/attack/hit/celebrate.

### W10 — Fase 10: Ambientes (6 sessões)

Kame House → Monte Paozu → Torneio de Artes Marciais → Namekusei → Planeta de Beerus → Arena do Torneio do
Poder → Sala do Tempo → Cidade do Oeste. Cada mapa: 10 camadas, tiles, props, portais, spawns, colisão,
occluders, metadados, preview composto.

### W11 — Fase 11: UI (6 sessões)

HUD (retrato, HP, Ki, XP, classe, nível, alvo) → action bar (5 slots + estados) → inventário/equipamento →
loja/craft/quests → chat/diálogos/cutscene → criação/seleção de personagem + atlas + 9-slice.

### W12 — Fase 12: Expansão por saga (contínua)

Preenchimento de lacunas: DB clássico, filmes, GT, personagens secundários, variações sazonais.
Entra por backlog, sempre em lotes coesos, respeitando os padrões congelados.

### W13 — Fase 13: Integração e QA final (4 sessões)

Validação de integridade, alpha, metadados, pivôs, atlas, compatibilidade cruzada, consistência visual,
documentação, organização; demonstração de integração (Godot 2D e/ou Unity 2D) e release `1.0.0`.

---

## 8. Ritmo e replanejamento

- **Sem datas no plano.** A primeira medição honesta vem ao fim de W1: gerações por asset aprovado,
  taxa de reprovação, tempo por sessão. Só então se projeta calendário.
- **Replanejamento obrigatório** ao fim de cada wave: comparar previsto × executado, ajustar tetos de
  gerações e reordenar o backlog.
- **Critério de replanejamento de escopo:** se a taxa de aprovação em W2–W3 ficar abaixo de 50%,
  o problema é de padrão/pipeline — parar produção e voltar a W1, não acelerar.

## 9. Caminho crítico

```text
M0 docs ─► M1 estilo+pipeline ─► M2 rig ─► M3 Goku jogável ─┬─► M4 roster ─► M5 combate ─► M6 pack 1.0.0
                                                            └─► W6 equip ─► W10 mapas ─► W11 UI
```

Nada em W4–W13 é iniciado antes de M3. Se M3 atrasar, o cronograma inteiro atrasa — de propósito.
