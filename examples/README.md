# examples/

Demonstrações funcionais e provas de montagem. **Nada aqui ainda** (Fase 0).

| Pasta | Conteúdo | Depende de |
|---|---|---|
| `sample_character/` | montagem de teste + `assembly_report.json` | W1/W2 |
| `sample_equipment/` | troca de slot em 3 bases | W2/W6 |
| `sample_animation/` | idle/run em APNG + timeline | W3 |
| `sample_map/` | mapa composto + escala de referência | W10 |
| `sample_ui/` | HUD composto sobre mapa | W11 |

## Regras

- Exemplo **não** é entregável essencial: se quebrar, o pacote continua válido.
- Exemplo precisa rodar com os arquivos do próprio pacote (sem asset externo).
- Arquivos específicos de engine (`.tscn`, `.prefab`) só existem aqui — nunca fora de `examples/`.
- `assembly_report.json` é evidência do gate G3, não ornamento.
