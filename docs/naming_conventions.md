# CONVENÇÕES DE NOMENCLATURA (normativo)

**Versão:** 1.0.0 · **Base:** master §5, §18.4

ID é **contrato permanente**. Renomear quebra animações, prefabs, saves e documentação. Por isso o padrão é
fechado e versionado.

---

## 1. Formato do ID

```text
DB_[CATEGORY]_[SUBCATEGORY]_[NAME]_[VARIANT]_[STATE]
```

- `DB` = prefixo fixo do projeto.
- `CATEGORY` = 3–8 letras maiúsculas (tabela §2).
- `SUBCATEGORY` = 2–12 letras maiúsculas (tabela §3).
- `NAME` = identificador curto em maiúsculas, sem acento, sem espaço (`GOKU`, `SAIYAN_ARMOR`, `KAME_HOUSE`).
- `VARIANT` = forma/cor/gênero/versão de continuidade (`BASE`, `SSJ`, `SSB`, `M`, `F`, `GOLD`, `DBZ`).
- `STATE` = estado de animação/uso (`IDLE`, `RUN`, `ATTACK01`, `CAST`, `ICON`, `SHEET`).

Sufixos `VARIANT` e `STATE` são **omitidos** quando não se aplicam — nunca preenchidos com `NONE`.

Exemplos válidos:

```text
DB_CHAR_HERO_GOKU_BASE_IDLE
DB_CHAR_HERO_GOKU_SSJ_ATTACK01
DB_CHAR_VILLAIN_FRIEZA_FINAL_IDLE
DB_ENEMY_COMMON_SAIBAMAN_GREEN_ATTACK
DB_PET_COMPANION_PUAR_DEFAULT_FOLLOW
DB_SKILL_BEAM_KAMEHAMEHA_BLUE_PROJECTILE
DB_VFX_KI_EXPLOSION_BLUE_01
DB_ENV_MAP_KAME_HOUSE          (mapa: STATE omitido)
DB_UI_HUD_PLAYER_FRAME
DB_EQUIP_ARMOR_SAIYAN_M_BASE
DB_ICON_SKILL_KAMEHAMEHA
```

## 2. Categorias (`CATEGORY`)

| Código | Uso | Diretório |
|---|---|---|
| `CHAR` | personagem (jogável, NPC, herói, vilão) | `characters/` |
| `EQUIP` | equipamento vestível | `equipment/` |
| `ENEMY` | inimigo não jogável | `enemies/` |
| `PET` | mascote/companheiro/invocação | `pets/` |
| `SKILL` | habilidade (conjunto de componentes) | `skills/` |
| `VFX` | efeito avulso (slash, impacto, aura genérica) | `skills/` |
| `ENV` | cenário, mapa, tile, prop | `environments/` |
| `UI` | componente de interface | `ui/` |
| `ICON` | ícone de item/skill/transformação | `ui/icons/` ou junto do asset |
| `RIG` | rig (dado, não imagem) | `characters/rigs/` |
| `ANIM` | timeline de animação | junto do asset |

## 3. Subcategorias (`SUBCATEGORY`)

| Categoria | Subcategorias válidas |
|---|---|
| `CHAR` | `HERO`, `VILLAIN`, `NPC`, `BASE` (corpo base), `FORM` (transformação) |
| `EQUIP` | `ARMOR`, `HELM`, `HAIR`, `CAPE`, `GLOVES`, `BOOTS`, `BELT`, `ACC`, `WEAPON` |
| `ENEMY` | `COMMON`, `ELITE`, `BOSS` |
| `PET` | `COMPANION`, `CREATURE`, `SUMMON` |
| `SKILL` | `MELEE`, `BEAM`, `PROJ`, `AOE`, `BUFF`, `DEBUFF`, `UTIL`, `TRANSFORM`, `SUMMON` |
| `VFX` | `SLASH`, `IMPACT`, `AURA`, `EXPLOSION`, `PARTICLE`, `SHOCKWAVE` |
| `ENV` | `MAP`, `SKY`, `MID`, `FG`, `TILE`, `PROP`, `BUILDING`, `PORTAL` |
| `UI` | `HUD`, `ICON`, `PANEL`, `BUTTON`, `BAR`, `CHAT`, `SHOP`, `QUEST`, `DIALOG`, `CREATION` |
| `ICON` | `SKILL`, `ITEM`, `EQUIP`, `FORM`, `CURRENCY`, `STATUS` |
| `RIG` | arquétipo (`HUMAN`, `SAIYAN`, `NAMEK`, `MAJIN`, `ANDROID`, `FRIEZA`, `CREATURE`, `BOSS`) |

## 4. Nomes de arquivo

**Padrão:** `snake_case` minúsculo, derivado do ID, com a parte semântica da peça.

```text
<name>_<variant>_<part>.png

goku_base_head.png
goku_base_front_forearm.png
goku_ssj_front_hair.png
saiyan_armor_m_chest.png
kamehameha_blue_projectile_segment.png
ui_hud_player_frame_512.png
kame_house_layer_02_bg_far.png
```

Regras:
- Sempre minúsculo, sem acento, sem espaço, sem caractere especial (`-` proibido).
- Peças do corpo usam o vocabulário de `anatomy_and_rigging.md` (`front_forearm`, não `arm2`).
- Resolução no nome **somente** quando há mais de uma versão do mesmo arquivo (`_512`, `_128`).
- Versão de asset **não** entra no nome do arquivo (vai nos metadados) — evita duplicação infinita.
- Arquivos temporários/de trabalho nunca ficam no diretório de entrega.

## 5. Metadados e JSON

| Tipo | Nome |
|---|---|
| Asset composto (personagem, mapa, skill) | `<id_minusculo>.asset.json` |
| Animação | `<anim_id>.anim.json` |
| Rig | `<rig_id_minusculo>.rig.json` |
| Atlas | `<atlas_name>.atlas.json` |
| Mapa | `map.json` (dentro do diretório do mapa) |
| Relatório de QA | `production/qa_reports/<escopo>_<data>.md` |

## 6. Sessões, relatórios e promoções

| Item | Formato | Exemplo |
|---|---|---|
| Sessão | `DB-SESSION-NNNN` | `DB-SESSION-0007` |
| Relatório | `production/session_reports/DB-SESSION-NNNN.md` | — |
| Lote | `DB-BATCH-<escopo>-NN` | `DB-BATCH-GOKU-PARTS-01` |
| Promoção/QA | `production/qa_reports/<asset_id>_<AAAMMDD>.md` | — |
| Rejeitado | `production/rejected/DB-SESSION-NNNN/<arquivo>` | — |

## 7. Versionamento em nome de diretório

- Diretórios **não** têm versão (`characters/canonical_heroes/goku/`, nunca `goku_v2/`).
- Versão vive nos metadados (`version`) e no `changelog`.
- Assets substituídos vão para `production/rejected/` com nota — não são apagados (auditoria).

## 8. Migração e aliases

Se um ID precisar mudar:

1. Abrir ADR com justificativa.
2. Adicionar entrada em `production/asset_registry.json` → `migrations[]`:
   `{ "from": "ID_ANTIGO", "to": "ID_NOVO", "since": "0.5.0", "session": "DB-SESSION-00XX" }`.
3. Manter alias por **pelo menos 1 versão MINOR**.
4. Atualizar todos os assets dependentes e o `asset_manifest.json`.

Nenhuma renomeação silenciosa. `tools/validate.py` falha se encontrar ID órfão ou duplicado.

## 9. Checklist de conformidade

- [ ] ID casa com a regex `^DB_[A-Z]{3,8}_[A-Z]{2,12}_[A-Z0-9_]+$`.
- [ ] Categoria/subcategoria nas tabelas §2/§3.
- [ ] Arquivos em `snake_case` derivados do ID.
- [ ] Nenhum ID duplicado no registry.
- [ ] Nenhuma renomeação sem `migrations[]`.
- [ ] Pastas sem versão no nome.
