# environments/

Cenários 2.5D em camadas. **Nenhum asset aqui ainda** (Fase 0).

| Pasta | Conteúdo |
|---|---|
| `backgrounds/` | céu, horizonte, bg_far (camadas 0–2) |
| `midgrounds/` | bg_mid, decor (camadas 3–4) |
| `foregrounds/` | fg, occluders (camadas 8–9) |
| `ground_tiles/` | tiles 256×256 costurados |
| `props/` | objetos interativos e decorativos |
| `buildings/` | casas, templos, naves |
| `portals/` | setas/portais de transição (dourado = avançar, prata = voltar) |
| `maps/` | mapas montados com `map.json` + preview |

## Regras

- Mapa = 10 camadas + colisão + spawns + portais (`environments_standard.md` §1 e §4).
- Nada entregue como wallpaper achatado.
- Contorno sutil/ausente em fundo; mais forte apenas em props e primeiro plano.
- Personagem é o maior contraste da cena; escala de referência 200 u sempre anexada.
- Tiles: costura verificada nos 4 lados, mínimo 3 variações por material.
