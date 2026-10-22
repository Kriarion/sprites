# production/ — Registros de produção

Aqui vive a **memória operacional** do projeto. Se a documentação em `docs/` diz *como fazer*, esta pasta diz
*o que foi feito, com qual custo, e o que vem a seguir*.

| Arquivo | Papel | Atualizado quando |
|---|---|---|
| `generation_ledger.json` | Orçamento de gerações por sessão (fonte da verdade) | Antes e depois de cada chamada/sessão |
| `production_backlog.json` | Fila priorizada e executável (tiers P0–P2) | Início e fim de cada sessão |
| `asset_registry.json` | IDs, status, arquivos, dependências, versões | A cada promoção/reprovação |
| `continuity_state.json` | Estado para retomada sem perda de contexto | Fim de cada sessão |
| `schemas/` | JSON Schemas de asset, rig e animação | Quando um contrato muda (bump de versão) |
| `session_reports/` | Relatório obrigatório por sessão (master §25) | Fim de cada sessão |
| `qa_reports/` | Evidência de gates G1–G4 | A cada promoção |
| `rejected/` | Imagens e lotes reprovados (auditoria) | A cada reprovação |

## Ordem de leitura para retomar

1. `continuity_state.json`
2. último arquivo de `session_reports/`
3. `asset_registry.json`
4. `production_backlog.json`
5. `generation_ledger.json` (orçamento)

## Regras

- Nada aqui é "cosmético": todos os arquivos são lidos por `tools/validate.py`.
- Nunca editar `totals` do ledger sem sessão correspondente.
- Nunca apagar uma reprovação: mover para `rejected/` com o motivo.
- `asset_registry.json` só cresce; remoção de ID exige `migrations[]`.
