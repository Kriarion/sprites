# Proveniência das pranchas de estilo

Todas produzidas na `DB-SESSION-0001` por geração de imagem e processadas por `tools/key.py`
(magenta keying, alpha real, halo 0,0%). Nenhuma obra de terceiros foi copiada.

| Arquivo | Asset ID | Status | Gate | Conteúdo |
|---|---|---|---|---|
| `style_dummy_mf.png` | `DB_REF_STYLE_DUMMY_V1` | APPROVED | G1 | dummy neutro M/F frente e perfil; calibração de linha, sombreamento e silhueta |
| `shading_three_tone.png` | `DB_REF_MATERIALS_V1` | APPROVED | G1 | 4 materiais × 2 versões (iluminado / half-shadow) |
| `weapons_oversized.png` | `DB_REF_WEAPONS_V1` | APPROVED | G1 | 4 armas oversized com cabo no eixo vertical (prontas para pivô) |
| `heads_four_archetypes.png` | `DB_REF_HEADS_V1` | APPROVED | G1 | cabeças M, F, infantil e musculosa; mesmo olho e peso de linha |
| `ui_probe_kit.png` | `DB_REF_UI_PROBE_V1` | APPROVED | G1 | painel, HP, Ki, slot e 6 botões; magenta visível nos soquetes vazios |
| `calibration_dummy_v2.png` | `DB_REF_STYLE_DUMMY_V2` | **REWORK_REQUIRED** | G1 FAIL | evidência de supercorreção de proporção (4,1 cabeças) — **não usar como referência** |

## Como usar

1. Anexar as pranchas aprovadas como referência (`images=[...]`) nas gerações de corpo/arma/UI.
2. Verificar proporção com `tools/measure.py` (alvo 18,2% ±5% para a cabeça).
3. Nunca usar a prancha reprovada como referência — ela existe apenas para justificar a regra de percentual.

## Nota de direitos

São desenhos **originais** gerados para calibração de estilo. Não representam personagens canônicos de
Dragon Ball nem assets de AQW. `ownership: pipeline_artifact`.
