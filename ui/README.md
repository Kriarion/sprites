# ui/

Kit de HUD e interfaces de MMO 2D. **Nenhum asset aqui ainda** (Fase 0).

| Pasta | Conteúdo |
|---|---|
| `hud/` | frames de jogador/alvo, barras HP/Ki/XP/classe, nível, status |
| `inventory/`, `equipment/` | painéis, slots, tooltips |
| `skills/` | action bar (5 slots), lista de skills, cooldown |
| `quests/`, `shop/` | listas, detalhes, moedas |
| `chat/`, `dialogs/` | input, log, balões de NPC, colunas de opção |
| `character_creation/` | raça, face, cabelo, cor, confirmação |
| `icons/` | ícones 128/64 de itens, skills, status, moedas |

## Regras

- Design em 1280×720; escalas 1×/2×/0,75× testadas.
- 9-slice com `slice_margins` declaradas; fonte mínima 512 px.
- 8 estados por componente interativo (ou justificativa de ausência).
- **Nenhum texto embutido** — tudo renderizado pela engine (localização).
- `preview_composed.png` sobre um mapa real do pacote.
