# enemies/

Inimigos, elites e bosses. **Nenhum asset aqui ainda** (Fase 0).

| Pasta | Escala típica | Exemplos |
|---|---|---|
| `common/` | 120–200 u | Saibaman, soldado Red Ribbon, soldado de Freeza |
| `elite/` | 200–260 u | Raditz, Nappa, Zarbon, Dodoria, Ginyu |
| `bosses/` | 400–900 u | Freeza, Cell, Majin Buu, Broly, Beerus, Jiren |

## Regras

- Inimigo comum pode usar rig simplificado; boss gigante **exige** segmentação e escala próprias.
- Animações mínimas: idle, walk, attack, hit, die. Boss: + ataques especiais e retrato.
- Hitbox por segmento em bosses (cabeça/tronco/cauda) com multiplicadores distintos.
- Boss nunca reduzido ao tamanho de personagem comum para "facilitar".
- Escala declarada em `scale.body_height_u` e validada contra o mapa de referência.
