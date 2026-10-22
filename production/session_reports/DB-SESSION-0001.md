# DB-SESSION-0001 — Relatório de sessão

```text
SESSION ID:        DB-SESSION-0001
DATE:              2026-10-22
PHASE / WAVE:      F1 / W1
TYPE:              REFERENCE + spike de pipeline
OBJECTIVE:         Calibrar o estilo em imagem e provar a decomposição de peças em grade

IMAGE GENERATIONS
- Planned new:          6
- Executed new:         7
- Reserved corrections: 4
- Executed corrections: 3
- Total executed:       10        (= 7 + 3, teto respeitado)

ASSETS CREATED:    DB_REF_STYLE_DUMMY_V1, DB_REF_STYLE_DUMMY_V2, DB_REF_MATERIALS_V1,
                   DB_REF_WEAPONS_V1, DB_REF_HEADS_V1, DB_REF_UI_PROBE_V1,
                   DB_EQUIP_ARMOR_TESTPLATE_M
ASSETS APPROVED:   DB_REF_MATERIALS_V1, DB_REF_WEAPONS_V1, DB_REF_HEADS_V1,
                   DB_REF_UI_PROBE_V1, DB_REF_STYLE_DUMMY_V1
ASSETS REJECTED:   DB_REF_STYLE_DUMMY_V2 (proporção 4,1 cabeças — supercorreção)
ASSETS PENDING:    DB_EQUIP_ARMOR_TESTPLATE_M (G3 FAIL: conjunto incompleto, pivôs sem teste de rotação)

FILES EXPORTED:    exports/individual_png/ref/ (6 folhas keyed)
                   exports/individual_png/parts_armor_test/ (9 peças isoladas)
                   exports/metadata/db_equip_armor_testplate_m.asset.json
                   exports/previews/assembly_armor_test.png
                   production/raw/DB-SESSION-0001/ (10 originais preservados)
METADATA UPDATED:  asset_registry, asset_manifest, generation_ledger, continuity_state,
                   production_backlog, VERSION, art_style_guide 1.1.0

QUALITY ISSUES:
- Grade rígida não é contrato: 13/16 violações de gutter e 6 células multi-fragmento (G3).
- Modelo desenha pares espelhados L/R quando a peça é simétrica (G4).
- Escala relativa entre peças da mesma folha é arbitrária (montagem desmontada na iteração 1).
- Proporção não obedece adjetivo; obedece percentual explícito (G1 → 7,5; G10 → 5,89 cabeças).
- Âncora `root` usada onde cabia `pelvis`; `spine_high` usada para ombreira única.

CORRECTIONS PERFORMED:
- G4 (correção de G3): grade 3×3 com peças singulares → ainda falhou em simetria e linha.
- G9 (correção de G1): "exactly 6 heads" → supercorrigiu para 4,1 cabeças.
- G10 (correção de G1): percentual por segmento → 5,89 cabeças (aceitável, ±7%).
- G8 (nova, não planejada): 9 objetos distintos por função → 9/9 componentes isolados. Virou o modo primário.

PIPELINE CHANGES:
- tools/key.py, decompose.py, compose.py, validate.py, measure.py, cellstats.py implementados e usados.
- compose.py: normalização anatômica por tipo + pivô recalculado pós-resize (2 bugs reais corrigidos por evidência).
- decompose.py: modo `components` promovido a primário; `grid` rebaixado a secundário (ADR-0006).
- ADR-0006 criado; ADR-0001 marcado como parcialmente substituído.

CURRENT PROJECT STATUS: F1 parcialmente cumprida. Estilo validado; pipeline de peças provado em 9 objetos;
corpo completo e rig ainda não. Marco M1 NÃO atingido (falta montagem de corpo montável).
NEXT SESSION OBJECTIVE: DB-SESSION-0002 — corpo humano completo (21 peças) com ADR-0006:
  folha A (torso/pelve/pernas), folha B (braços/mãos), folha C (cabeça/cabelo/face), + montagem e rotação.
  Orçamento: 6 novas / 4 reserva.
OPEN RISKS: peças articuladas (com curva de junta) podem sair como um objeto único com o membro vizinho;
  o teste de rotação ±35° continua não executado; nenhuma máscara de cor produzida.
```

## Conciliação de orçamento

| # | Geração | Tipo | Resultado |
|---:|---|---|---|
| 1 | `g1_style_dummy` | nova (planejada) | aprovada como referência de estilo; proporção 7,5 cabeças (fora do alvo) |
| 2 | `g2_shading_materials` | nova (planejada) | aprovada |
| 3 | `g3_part_sheet_a` | nova (planejada) | **reprovada** — grade ignorada |
| 4 | `g4_part_sheet_a_v2` | correção | **reprovada** — simetria e linha ainda quebradas |
| 5 | `g5_weapon_sheet` | nova (planejada) | aprovada |
| 6 | `g6_head_sheet` | nova (planejada) | aprovada |
| 7 | `g7_ui_probe` | nova (planejada) | aprovada |
| 8 | `g8_product_sheet` | nova (**não planejada**) | aprovada — mudou a arquitetura |
| 9 | `g9_style_dummy_v2` | correção | **reprovada** — supercorreção de proporção |
| 10 | `g10_canonical_dummy` | correção | aceitável (5,89 cabeças), base da regra de percentual |

**Desvio de plano registrado:** 1 geração nova além das 6 planejadas (a #8). Ela consumiu parte da reserva
de correção, que ficou em 3 de 4. O teto de 10 foi respeitado; a divisão planejada não. Registrado aqui em
vez de "ajustado" no ledger.
