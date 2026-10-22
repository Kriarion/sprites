# exports/

Material de **consumo**, gerado por script a partir da fonte (`characters/`, `equipment/`, …).
**Nenhum arquivo aqui ainda** (Fase 0).

| Pasta | Conteúdo | Gerado por |
|---|---|---|
| `individual_png/` | peças normalizadas | `tools/decompose.py` |
| `spritesheets/` | animações em grade regular | `tools/compose.py` |
| `atlases/` | atlas 2048² + `.atlas.json` | `tools/atlas.py` |
| `metadata/` | JSONs prontos para engine | pipeline |
| `previews/` | montagens, APNGs, overlays | `tools/compose.py` |

## Regras

- **Nunca editar `exports/` à mão.** Regenerar sempre que a fonte mudar.
- `exports/` pode ser apagado e reconstruído — a fonte de verdade é o diretório da categoria.
- Nada em `exports/` é versionado além do necessário para consumo: manter apenas o último estado válido.
- Todo export é rastreável ao `asset_id` e à sessão que o produziu.
