# DB-SESSION-0002 — Relatório de sessão

```text
SESSION ID:        DB-SESSION-0002
DATE:              2026-10-22
PHASE / WAVE:      F2 / W2
TYPE:              ANATOMY
OBJECTIVE:         Corpo humano base montavel (ADR-0006) + rig JSON + teste de montagem

IMAGE GENERATIONS
- Planned new:          6
- Executed new:         5
- Reserved corrections: 4
- Executed corrections: 0
- Total executed:       5        (= 5 + 0; teto de 10 respeitado com folga de 5)

ASSETS CREATED:    DB_CHAR_BASE_HUMAN_M (corpo base masculino, 18 pecas + 2 variantes)
                   DB_RIG_HUMAN_M_001 (rig, 27 bones, 19 slots)
ASSETS APPROVED:   nenhum
ASSETS REJECTED:   g1_body_parts_front (folha 9 objetos: modelo misturou corpo inteiro com pecas)
ASSETS PENDING:    DB_CHAR_BASE_HUMAN_M (G3 PARTIAL: folga punho, decal de olhos, cabelo sobre face, contorno fino)

FILES EXPORTED:    exports/individual_png/body_m_v1/ (18 pecas + 2 variantes + parts.json)
                   exports/previews/assembly_body_m_v1.png
                   exports/metadata/db_char_base_human_m.asset.json
                   characters/rigs/db_rig_human_m_001.rig.json
                   production/coherence_report.json
                   production/qa_reports/logs/contact_sheet_body_m_v1.png
METADATA UPDATED:  registry, manifest, ledger, continuity, backlog, standards 1.2.0/1.1.0

QUALITY ISSUES:
- D1 folga antebraco->mao (pivo de tipo nao medido na peca)
- D2 face_eyes esmagado: normalizacao por altura em decal largo
- D3 hair_front cobre a face
- D4 contorno ~1,1 px em 1x (C3) - sistemico; dilatacao 1 px testada e DESCARTADA (engrossa linha interna)
- D6 juntas com taper (cotovelo/punho/joelho encostam em 0,1 u; falta cap de sobreposicao 2-3 u na arte)
- D7 largura refem do desenho (resolvido por silhueta canonica; drift residual medido em 6 pecas)
- D8 braco traseiro fora do torso (resolvido) | D9 hand_back horizontal (resolvido) | D10 cabelo traseiro cobre o pescoco
- 2 trocas de identidade indice->peca detectadas por contact sheet e corrigidas no spec

CORRECTIONS PERFORMED: nenhuma geracao de correcao (0 de 4 reservadas usadas).
  Corrigido por spec/codigo, com medicao antes e depois:
  - hand_back desenhada na horizontal -> rotate_deg 270 (escolhido por strip de rotacao)
  - cintura aberta 13,2 u -> pivo de torso/pelvis recalculado (0,95->0,79 e 0,12->0,30) => folga 1,9 u
  - braco traseiro fora do torso -> DEPTH_OFFSET -6 -> -2 u + offset_u por peca => sobreposicao 3,3 u
  - larguras erradas -> politica de SILHUETA CANONICA no compose.py (peca preenche a caixa do tipo)
  - altura do corpo 193,5 u -> 200,2 u
  - bbox de merge dos olhos, troca mao/pe em g3, variantes de pose, dims canonicas
  - novo tools/audit_geometry.py: 15 juntas + 20 aspectos medidos (JSON)

PIPELINE CHANGES:
- tools/pack_parts.py (novo): folhas -> pecas nomeadas via spec, merge, rotacao, normalizacao, pivo por tipo
- tools/compose.py: depth offset para camadas traseiras; tolera id/part; dims para face/hand_grip/forearm_fist
- tools/coherence.py (novo): 6 invariantes; C2 por rig; C4 por grupo de paleta; C5/C6 implementados
- tools/measure.py e key.py: metricas corrigidas por evidencia
- docs/coherence_standard.md: faixa C3 revisada por medicao (0,009-0,013 -> 0,008-0,014)

MEASUREMENTS (antes -> depois, mesma sessao):
  altura do corpo 193,5 u -> 200,2 u | folga de cintura 13,2 u -> 1,9 u | ombro traseiro folga 3,7 u -> sobreposicao 3,3 u
  half-shadow back/front 0,69 -> 0,52 | C3 0,00488 -> 0,00461 (segue reprovado: ~1,12 px @1x)
  contorno medido por EDT: mediana 2,24 px @2 px/u = 1,12 px @1x = 0,56% da altura (padrao pede 0,8-1,4%)

CURRENT PROJECT STATUS: F2 parcialmente cumprida. Corpo base montavel por dados, rig JSON valido no schema,
  coerencia 83,3% (5/6). Nenhum asset APPROVED. M1 nao fechado (falta corrigir D1-D4 e teste de rotacao).
NEXT SESSION OBJECTIVE: DB-SESSION-0003 — correcao (6-8 geracoes):
  1) folha de corpo com contorno 3-4 px no mestre (D4)
  2) cabelo com recorte de face (D3) + decal de olhos com aspecto correto (D2)
  3) par antebraco+mao para eliminar folga (D1)
  4) teste de rotacao +-35 em 8 angulos nas 12 juntas -> assembly_report.json
OPEN RISKS: nenhuma rotacao testada; nenhuma animacao; nenhuma mascara de cor;
  C3 pode exigir pos-processamento de linha (dilatar 1 px) se o gerador nao obedecer.
```
