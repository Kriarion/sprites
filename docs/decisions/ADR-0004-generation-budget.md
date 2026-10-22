# ADR-0004 — Política de orçamento de gerações e ledger

- **Status:** Aceita
- **Data:** 2026-10-22
- **Afeta:** todas as sessões; `production/generation_ledger.json`; `production_pipeline.md` §2

## 1. Contexto

O master (§3) impõe teto de **10 gerações de imagem por sessão**, com meta de 6–8 novas e 2–4 de reserva.
A plataforma não impõe esse contador: nada impede tecnicamente ultrapassar. Portanto o controle precisa ser
**documental e verificável**, com parada dura e evidência.

Além disso, a ferramenta oferece um modo interativo (`offer_options`) que pausa a execução esperando escolha
humana — incompatível com autonomia de produção e com contabilidade de chamadas.

## 2. Decisão

1. **Teto de 10 chamadas por sessão**, contadas por chamada (não por imagem retornada).
2. Meta padrão: **6–8 novas + 2–4 reservadas**. A reserva não consumida **não** vira novas gerações.
3. O ledger é a fonte de verdade: consultado **antes** de cada chamada e atualizado **ao fim** da sessão.
4. `total_executed = executed_new + executed_corrections` é invariante verificada pelo validador.
5. **`offer_options` é proibido em sessão de produção.** Motivos: pausa a sessão, move as opções não
   escolhidas para fora do pacote e torna a contagem de chamadas ambígua.
6. Ao atingir 10 chamadas, a sessão **para** — mesmo com lote incompleto. O restante vira próxima sessão.
7. Sessão sem entrada no ledger é considerada **não realizada** (não pode ter assets `APPROVED`).
8. Estouro de orçamento (acidente) é registrado como incidente em `continuity_state.json.known_issues`
   e a próxima sessão tem orçamento reduzido em quantidade equivalente.

## 3. Orçamento por tipo de sessão (referência)

| Tipo | Novas | Reserva | Observação |
|---|---:|---:|---|
| `REFERENCE` | 3–4 | 3 | referência não é asset; gastar pouco |
| `ANATOMY` | 4–5 | 3 | folhas de peças são densas |
| `CHARACTER` | 5–7 | 3 | 1–2 folhas de corpo + 1 de roupa |
| `EQUIPMENT` | 6–8 | 2 | uma folha por conjunto |
| `VFX` | 6–8 | 2 | folhas de frames |
| `ENVIRONMENT` | 4–6 | 3 | camadas + tiles |
| `UI` | 5–7 | 3 | painéis + ícones |
| `CORRECTION` | 0 | 10 | só correção |

## 4. Alternativas consideradas

| Alternativa | Problema |
|---|---|
| Contar só no fim da sessão | estouro descoberto tarde; retrabalho |
| "Usar o que precisar" | viola regra do master e destrói sustentabilidade |
| Contar por imagem retornada | a ferramenta retorna 1; incentiva lotes densos ilegíveis |
| Deixar o usuário aprovar cada chamada | anula a autonomia prevista no §26 |

## 5. Consequências

- Cada chamada precisa ser **planejada** (lote coeso, grade definida, prompt revisado).
- Reserva obriga a não "tentar de novo" no improviso — correção é decidida, não reflexa.
- O ledger permite calcular custo real por asset aprovado (métrica de eficiência do pipeline).
- Sessões curtas e densas > sessões longas e dispersas.
