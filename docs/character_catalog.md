# CATÁLOGO CANÔNICO DE CONTEÚDO

**Versão:** 1.0.0 · **Base:** master §8, §9, §10, §13, §14, §15 · **Backlog executável:**
`production/production_backlog.json`

Catálogo **expansível**, organizado por continuidade, com prioridade em três tiers:

| Tier | Significado | Consequência |
|---|---|---|
| **P0** | bloqueia o vertical slice / demo jogável | entra nas waves W1–W3 |
| **P1** | necessário para o roster e o mundo inicial | waves W4–W11 |
| **P2** | expansão por saga | wave W12 em diante |

**Continuidade** é obrigatória nos metadados (`continuity: db | dbz | dbs | gt | movie`) e **nunca** se
mistura versões de continuidades diferentes no mesmo design (master §8.5).

---

## 1. Corpos base e rigs

| Prioridade | Item | Rig | Observação |
|---|---|---|---|
| P0 | Humano masculino padrão (dummy) | `DB_RIG_HUMAN_M_001` | base de tudo |
| P0 | Humano feminino padrão (dummy) | `DB_RIG_HUMAN_F_001` | mesma topologia |
| P0 | Musculoso / infantil | `DB_RIG_HUMAN_MUSC_001` / `CHILD_001` | variantes de escala |
| P1 | Saiyajin M/F (com cauda) | `SAIYAN_*` | cauda animável |
| P1 | Namekuseijin | `NAMEK_001` | antenas, orelhas |
| P1 | Majin | `MAJIN_001` | membros elásticos |
| P1 | Androide humanoide | `ANDROID_001` | juntas mecânicas |
| P1 | Raça de Freeza | `FRIEZA_001` | crânio alongado, cauda, 3 dedos |
| P2 | Criatura pequena / quadrúpede / boss XL / com asas | `CREATURE_*`, `BOSS_XL_001` | rigs não humanoides |

## 2. Dragon Ball (clássico) — `continuity: db`

| Tier | Personagem | Forma/Notas |
|---|---|---|
| P1 | Goku criança | base; reusa `CHILD_001` |
| P1 | Bulma | várias roupas (P2) |
| P1 | Kuririn criança | |
| P1 | Mestre Kame | NPC + jogável tardio |
| P1 | Piccolo Daimaoh | boss (W8) |
| P1 | Piccolo Jr. (jovem) | |
| P2 | Yamcha, Tenshinhan, Chaotzu, Chi-Chi, Lunch, Tao Pai Pai | |
| P2 | Pilaf, Shu, Mai | NPCs/vilões cômicos |
| P2 | Oolong, Puar | pets (W9) |
| P2 | Yajirobe, Karin, Kami-Sama, Mr. Popo, Android 8, Rei Cutelo | NPCs |

## 3. Dragon Ball Z — `continuity: dbz`

| Tier | Personagem | Observação |
|---|---|---|
| **P0** | **Goku adulto (base)** | vertical slice obrigatório |
| **P0** | **Vegeta (Saga Saiyajin / armadura)** | rig musculoso |
| **P0** | **Piccolo** | rig namek |
| P1 | Gohan criança / adolescente / adulto | 3 corpos distintos |
| P1 | Kuririn adulto | |
| P1 | Trunks do Futuro / Trunks criança | |
| P1 | Goten, Gotenks, Vegito | fusões |
| P1 | Bulma (várias), Chi-Chi, Videl, Mr. Satan, Dende | NPCs + jogáveis |
| P1 | Freeza (formas 1–4 + 100%) | boss |
| P1 | Cell (imperfeito, sem-perfeito, perfeito) | boss |
| P1 | Majin Buu (gordo, mal, Super, Kid) | boss |
| P2 | Raditz, Nappa, Zarbon, Dodoria, Força Ginyu (5) | elites |
| P2 | Androides 16, 17, 18, 19, 20 | |
| P2 | Dabura, Babidi, Bardock, Rei Kaiô | |
| P2 | Cell Juniors, Saibaman | inimigos comuns |

## 4. Dragon Ball Super — `continuity: dbs`

| Tier | Personagem | Observação |
|---|---|---|
| P1 | Beerus, Whis | NPCs divinos |
| P1 | Goku Black, Zamasu, Fusão Zamasu | vilões |
| P1 | Jiren, Toppo, Dyspo | Universo 11 |
| P2 | Hit, Cabba, Caulifla, Kale, Kefla | Universo 6 |
| P2 | Champa, Vados, Zen'oh, Grande Sacerdote | |
| P2 | Broly (DBS), Gogeta (DBS) | |
| P2 | Moro, Granolah | só se o escopo de mangá for confirmado |

## 5. Dragon Ball GT — `continuity: gt`

| Tier | Personagem | Observação |
|---|---|---|
| P2 | Goku GT (criança) | reusa `CHILD_001` |
| P2 | Pan, Trunks GT, Vegeta GT | |
| P2 | Giru | pet |
| P2 | Baby, Super Baby Vegeta, Super Androide 17 | bosses |
| P2 | Omega Shenron + Dragões Malignos | bosses |
| P2 | Gogeta SSJ4 | |

## 6. Filmes — `continuity: movie`

| Tier | Personagem | Continuidade declarada |
|---|---|---|
| P2 | Cooler, Metal Cooler | `movie` (DBZ films) |
| P2 | Turles, Lord Slug, Garlic Jr. | `movie` |
| P2 | Janemba, Tapion, Hirudegarn | `movie` |
| P2 | Bojack | `movie` |
| P2 | Broly (trilogia de filmes DBZ) | `movie` — **não** confundir com Broly de DBS |
| P2 | Androides 13, 14, 15 | `movie` |

## 7. Transformações — `form`

| Tier | Forma | Componentes obrigatórios |
|---|---|---|
| P1 | Base | — |
| P1 | Super Saiyan | cabelo, sobrancelhas, olhos, aura, ativação |
| P1 | Super Saiyan 2 | idem + faísca elétrica |
| P1 | Super Saiyan 3 | cabelo longo, sem sobrancelhas, aura densa |
| P1 | Super Saiyan God / Blue | cabelo+aura; pele/olhos |
| P2 | Super Saiyan Blue Evolution / Rosé | variações de aura |
| P2 | Ultra Instinct Sign / Ultra Instinct | olhos prateados, aura, cabelo |
| P2 | Ultra Ego, Beast, Orange Piccolo, Potencial Liberado | |
| P2 | Golden Freeza / Black Freeza | |
| P2 | Majin (possessão) | marca M, veias |
| P2 | Oozaru | **rig próprio** (não humanoide) |
| P2 | Super Saiyan 4 | corpo peludo, rig adaptado |
| P2 | Fusões (Gogeta, Vegito, Gotenks, Kefla) | rig próprio quando anatomia difere |

## 8. Equipamentos canônicos

| Tier | Item | Slot |
|---|---|---|
| P0 | Gi de Goku (laranja/azul, kanji, faixa, pulseiras, botas) | chest, arms, legs, boots, belt |
| P1 | Armadura Saiyajin (com/sem ombreiras) | chest, shoulders, legs, boots |
| P1 | Roupa de Piccolo (cape, turbante, ombreiras) | chest, cape, helm, shoulders |
| P1 | Uniforme da Força Ginyu | full set |
| P1 | Uniforme Red Ribbon | full set |
| P1 | Roupas da Capsule Corporation | full set |
| P1 | Roupa de fusão (Gotenks/Vegito) | chest, belt |
| P1 | Great Saiyaman (capacete + capa) | helm, cape, chest |
| P2 | Roupas de treino de Kuririn, roupas de Trunks, coletes de treino | |
| P1 | Armas: espada de Trunks, bastão mágico, cajados, lanças, machados | `weapon_main` |
| P1 | Acessórios: Scouter, Brincos Potara, Radar do Dragão, Cápsulas Hoi-Poi, pesos, mochilas | `accessory` |

Meta do master §22: **20+** conjuntos de armadura, **50+** armas, **30+** helms/cabelos/acessórios.

## 9. Habilidades prioritárias

| Tier | Técnica | Componentização |
|---|---|---|
| **P0** | Kamehameha | 8+ componentes (referência do padrão) |
| P1 | Galick Gun, Final Flash, Big Bang Attack | feixe/explosão |
| P1 | Masenko, Makankosappo | feixe |
| P1 | Genki Dama, Kienzan, Death Beam, Death Ball, Special Beam Cannon | projétil/AoE |
| P1 | Solar Flare, Kaioken, Instant Transmission | util/buff |
| P2 | Burning Attack, Final Kamehameha, Stardust Breaker, Hakai | |
| P0/P1 | Genéricos: slash, impacto, escudo, cura, debuff, aura, explosão | reutilizáveis |

Meta: **40+** habilidades/VFX; **100+** ícones.

## 10. Inimigos, bosses e pets

| Categoria | Tier P1 | Tier P2 |
|---|---|---|
| Comuns | Saibaman, soldado Red Ribbon, soldado de Freeza | criaturas de Namek, Cell Juniors, capangas de Babidi, robôs |
| Elites | Raditz, Nappa, Ginyu | Zarbon, Dodoria, Androides, Dabura |
| Bosses | Freeza, Cell, Majin Buu | Piccolo Daimaoh, Broly, Beerus, Goku Black, Jiren, Baby, Omega Shenron, Cooler, Janemba |
| Pets | Puar, Oolong, Icarus | Giru, criaturas de Namek, robôs auxiliares |

Meta: **20+** comuns, **10+** bosses, **20–50** pets.

## 11. Locais prioritários

| Tier | Local | Continuidade |
|---|---|---|
| **P0** | Kame House (mapa-piloto, mais simples) | dbz |
| P1 | Monte Paozu, Casa de Goku, Cidade do Oeste | dbz |
| P1 | Torneio de Artes Marciais (arena) | db |
| P1 | Namekusei (exterior) | dbz |
| P1 | Planeta de Beerus | dbs |
| P1 | Arena do Torneio do Poder | dbs |
| P2 | Planeta Vegeta, Nave de Freeza, Planeta do Rei Kaiô, Sala do Tempo, Arena de Cell, Mundo dos Kaioshins | dbz |
| P2 | Torre Karin, Plataforma de Kami-Sama, Capsule Corp, bases Red Ribbon, desertos, florestas | db/dbz |
| P2 | Universo 6, locais de Zamasu/Goku Black, planetas de GT, cenários de filmes | dbs/gt/movie |

Meta: **5–10** mapas demonstrativos completos.

## 12. Regras de catálogo

1. Todo item deste catálogo entra no backlog com `tier`, `continuity` e dependências (rig, base, mapa).
2. Nenhum item P2 começa antes de M3 (vertical slice) estar atingido.
3. Personagens com **anatomia incompatível** (Oozaru, Shenron, Hirudegarn) declaram rig próprio na primeira
   linha do backlog — não são "espremidos" em rig humanoide.
4. Designs **originais** (equipamentos/criaturas inventados) são permitidos, mas marcados
   `ownership: original_design` e nunca apresentados como canônicos.
5. Broly de DBZ (filmes) e Broly de DBS são **assets diferentes**, com `continuity` distinta.
