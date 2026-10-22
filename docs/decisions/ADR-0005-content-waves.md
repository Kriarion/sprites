# ADR-0005 — Waves de conteúdo, tiers e critérios de promoção

- **Status:** Aceita
- **Data:** 2026-10-22
- **Afeta:** `roadmap.md`, `character_catalog.md`, `production/production_backlog.json`

## 1. Contexto

Dragon Ball tem centenas de personagens; o master lista metas ambiciosas (§22) e proíbe "produzir o
universo inteiro simultaneamente" (§21). Sem um mecanismo de priorização explícito, o projeto tende a
produzir o personagem mais divertido da semana em vez do que destrava o pipeline.

## 2. Decisão

1. **Tiers P0/P1/P2** aplicados a todo conteúdo:
   - **P0** destrava o vertical slice (Goku, corpos base, Kamehameha, Kame House, HUD mínimo).
   - **P1** compõe o roster inicial, o mundo inicial e o combate.
   - **P2** expansão por saga.
2. **Waves fechadas** (W0–W13). Cada wave tem objetivo, orçamento total e critério de saída binário.
3. **Gate de avanço:** nenhuma wave de produção de conteúdo (W4+) começa antes de **M3** (vertical slice
   de Goku aprovado e montável por terceiro).
4. **Um lote coeso por sessão** (mesmo personagem/paleta/rig/tema) — nunca misturar bosses com ícones.
5. **Reuso obrigatório:** antes de criar rig/base novo, verificar se um rig aprovado acomoda a anatomia.
   Criar rig novo exige justificativa no backlog.
6. **Backlog é a única porta de entrada.** Personagem "legal" que não está no backlog não é gerado.
7. **Meta de volume só vale com qualidade:** nenhuma meta numérica (ex.: "50 armas") autoriza aprovar
   asset reprovado em G1–G4.

## 3. Critério de saída de wave (template)

Um wave só fecha quando:

- [ ] todos os entregáveis P0 da wave estão `APPROVED`;
- [ ] nenhum asset da wave está `REWORK_REQUIRED` sem plano;
- [ ] relatórios de sessão do wave existem e estão conciliados com o ledger;
- [ ] `continuity_state.json` reflete o estado real;
- [ ] retro do wave registrada (o que funcionou, o que reprovou e por quê);
- [ ] ajuste de roadmap aplicado ao próximo wave.

## 4. Alternativas consideradas

| Alternativa | Problema |
|---|---|
| Ordem por popularidade de personagem | gera assets bonitos e não montáveis; quebra o pipeline |
| Paralelismo total (vários tipos por sessão) | mistura de estilo, ledger confuso, retrabalho |
| Sem tiers, decidir "no momento" | escopo infinito; nenhuma fase fecha |
| Fazer todos os rigs antes de qualquer personagem | meses sem nada jogável; risco alto sem feedback |

## 5. Consequências

- O projeto demora mais para mostrar "muitos personagens" e muito menos para mostrar **um jogo possível**.
- W1–W3 concentram risco: se falharem, o resto do roadmap é revisto (e isso é saudável).
- A reutilização de rig reduz custo marginal por personagem nas waves seguintes.
- Metas do §22 são perseguidas como consequência de waves fechadas, não como corrida.
