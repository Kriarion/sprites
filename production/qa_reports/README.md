# qa_reports/

Evidência de qualidade por asset e por sessão. Um asset `APPROVED` **exige** um relatório aqui.

## Nomenclatura

```text
<asset_id>_<AAAAMMDD>.md        ex.: db_char_hero_goku_base_20261029.md
rig_<rig_id>_<AAAAMMDD>.md      ex.: rig_db_rig_human_m_001_20261105.md
session_<NNNN>_<AAAAMMDD>.md    ex.: session_0007_20261105.md
```

## Conteúdo mínimo

Ver `docs/quality_checklist.md` §9. Em resumo: gates G0–G4 com PASS/FAIL, motivo em caso de falha,
saída do validador colada (não parafraseada) e próxima ação.

## Regras

- Relatório não pode ser criado "só para aprovar": o log do validador é obrigatório.
- Reprovação também é registrada — inclusive com o motivo específico (não "ficou estranho").
- Nenhum arquivo aqui é apagado; correções geram novo relatório com data nova.
