# DB-SESSION-NNNN — Relatório de sessão

Copie este arquivo para `production/session_reports/DB-SESSION-NNNN.md` **ao fim** da sessão.
Formato baseado no master §25. Nada aqui pode ser inventado: se não foi feito, escreva "não executado".

```text
SESSION ID:        DB-SESSION-NNNN
DATE:              AAAA-MM-DD
PHASE / WAVE:      Fn / Wn
TYPE:              REFERENCE | ANATOMY | CHARACTER | EQUIPMENT | ANIMATION | VFX | ENVIRONMENT | UI | CORRECTION
OBJECTIVE:         <uma frase objetiva>

IMAGE GENERATIONS
- Planned new:        N
- Executed new:       N
- Reserved corrections: N
- Executed corrections: N
- Total executed:     N        (deve ser <= 10 e igual a executed_new + executed_corrections)

ASSETS CREATED:      <IDs separados por vírgula, ou "nenhum">
ASSETS APPROVED:     <IDs>
ASSETS REJECTED:     <IDs + motivo curto>
ASSETS PENDING:      <IDs + o que falta>

FILES EXPORTED:      <diretórios/arquivos reais>
METADATA UPDATED:    <registry / manifest / ledger / continuity>

QUALITY ISSUES:      <defeito, asset, gate, decisão>
CORRECTIONS PERFORMED: <chamada → resultado>
PIPELINE CHANGES:    <ferramenta/template alterado e por quê>

CURRENT PROJECT STATUS: <fase, marco, o que está aprovado>
NEXT SESSION OBJECTIVE: <objetivo + orçamento planejado>
OPEN RISKS:          <riscos novos ou agravados>
```

## Checklist de fechamento

- [ ] `generation_ledger.json` atualizado e conciliado.
- [ ] `asset_registry.json` reflete os status reais.
- [ ] `asset_manifest.json` regenerado (`tools/build_manifest.py`).
- [ ] `continuity_state.json` atualizado (`last_completed_session`, `next_session`, prioridades).
- [ ] `production_backlog.json` atualizado (itens concluídos/bloqueados).
- [ ] QA reports criados para cada asset avaliado.
- [ ] Nenhum arquivo listado aqui está ausente em disco.
