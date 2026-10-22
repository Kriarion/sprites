# PADRÃO DE CENÁRIOS E MAPAS (normativo)

**Versão:** 1.0.0 · **Base:** guia1 §7, guia2 §8, master §15

Cenário não é wallpaper: é **conjunto de camadas montáveis** com chão caminhável, colisão e leitura de
profundidade. Nenhum mapa é entregue como imagem única achatada.

---

## 1. Camadas (vocabulário fechado)

Ordem de renderização, do fundo para a frente:

| `layer` | id | Parallax | Conteúdo | Contorno |
|---:|---|---:|---|---|
| 0 | `sky` | 0.02–0.05 | céu, sol/lua, nuvens distantes | nenhum |
| 1 | `horizon` | 0.10–0.20 | montanhas, silhuetas distantes | nenhum |
| 2 | `bg_far` | 0.25–0.40 | florestas, castelos, planetas | sutil |
| 3 | `bg_mid` | 0.45–0.60 | estruturas grandes, ruínas | sutil (0.5–1 px) |
| 4 | `decor` | 0.70 | postes, placas, vasos, detalhes | 1 px |
| 5 | `ground` | 1.00 | solo caminhável (base) | nenhum |
| 6 | `ground_detail` | 1.00 | pedras, grama, rachaduras sobre o solo | 0.5 px |
| 7 | `props` | 1.00–1.05 | props interativos (baús, portais, NPCs estáticos) | 1–1.5 px |
| 8 | `fg` | 1.15–1.35 | árvores, colunas, folhagem à frente | 1–2 px |
| 9 | `occluder` | 1.15–1.35 | máscaras que escondem o personagem | — |
| 10 | `overlay` | 0 | clima/luz (chuva, névoa, tint) | — |

Regras:
- `ground` é **sempre tileável** e define a banda caminhável.
- `occluder` é um PNG com alpha que a engine usa para mascarar personagens atrás de `fg`
  (ou o `fg` já é desenhado depois do personagem — a escolha é da engine; entregamos ambos).
- `overlay` nunca é obrigatório: o mapa funciona sem ele.

## 2. Escala e enquadramento

| Item | Valor |
|---|---|
| Resolução de design | 1280 × 720 |
| Largura da camada (sem tiling) | 1536 px (1,2×) |
| Banda caminhável | y 440–700 |
| Linha do chão de referência | y 620 |
| Personagem de referência | 200 px de altura |
| Personagem mínimo legível (distante) | 140 px (zoom out) |
| Escala de props | props grandes 1,5–3× o personagem; pequenos 0,2–0,5× |
| Tiles de chão | 256 × 256 px, costura verificada nos 4 lados |
| Grid de montagem | declarado no `map.json` (âncora top-left, y↓) |

Profundidade: **mais distante = menos contraste, menos saturação, menos detalhe**. O personagem deve ser o
elemento de maior contraste da cena.

## 3. Perspetiva

- Apresentação **2.5D de plano XY**, com leve inclinação isométrica do chão (guia1 §7).
- Personagem se desloca em X e Y dentro da banda caminhável (não é plataforma lateral pura).
- Escala do personagem **não** muda com Y (sem escala por profundidade) — evita inconsistência de rig.
- Oclusão dá a sensação de profundidade, não a escala.

## 4. Entrega por mapa

```text
environments/maps/kame_house/
├── map.json                  metadados (camadas, colisão, spawns, portais, escala)
├── layers/
│   ├── 00_sky.png
│   ├── 01_horizon.png
│   ├── 02_bg_far.png
│   ├── 03_bg_mid.png
│   ├── 04_decor.png
│   ├── 05_ground.png
│   ├── 06_ground_detail.png
│   ├── 07_props.png
│   ├── 08_fg.png
│   └── 09_occluder.png
├── tiles/ground_256/{tile_xx_yy.png}
├── props/{palm_tree.png, rock.png, mailbox.png}
├── collision.png             máscara binária (branco = bloqueado)
├── portals.json
├── preview_composed.png      evidência do gate G3
└── reference_scale.png       personagem 200 u sobreposto à cena
```

### `map.json` (mínimo)

```json
{
  "map_id": "DB_ENV_MAP_KAME_HOUSE",
  "theme": "tropical_island",
  "continuity": "dbz",
  "design_resolution": [1280, 720],
  "world_size": [1536, 720],
  "walkable_band": [440, 700],
  "ground_line_y": 620,
  "layers": [{ "id": "sky", "file": "layers/00_sky.png", "parallax": 0.03, "z": 0 }],
  "tiles": { "size": [256, 256], "grid": [6, 1], "origin": [0, 564] },
  "collision": { "file": "collision.png", "blocked_value": 1 },
  "spawns": [{ "id": "player_default", "x": 320, "y": 620 }],
  "portals": [{ "id": "to_beach", "x": 1500, "y": 620, "target": "DB_ENV_MAP_BEACH", "arrow": "gold" }],
  "npcs": [], "props": [],
  "reference_character_height": 200,
  "preview": "preview_composed.png"
}
```

## 5. Tiles

- 256×256, alinhados em grade, costura verificada nos 4 lados (teste automático de diferença de borda).
- Variações: no mínimo 3 por material (base, com detalhe, com variação de cor) para quebrar repetição.
- Nada de bordas "desenhadas" que denunciem o tile — o chão deve parecer contínuo.
- Transições (grama→areia, pedra→lama) entregues como tiles de borda ou máscaras de mistura.

## 6. Props e portais

- Props interativos têm pivô na base (`y` = linha do chão) e camada declarada.
- Portais entregues com: base desenhada, ícone de seta (dourada = avançar, prata = voltar, como em AQW),
  estado `idle` e `hover` opcional.
- Zonas de interação e spawns em `map.json`, nunca "implícitas na imagem".

## 7. Iluminação e clima

- Luz coerente com a Visual Bible (cima/frente).
- Cenários noturnos: paleta dessaturada + fontes de luz locais (tochas, ki, lua).
- `overlay` de clima pode ser animado (chuva em loop de 12 frames) e reutilizado entre mapas.

## 8. Checklist de aprovação

- [ ] 10 camadas presentes ou explicitamente justificadas.
- [ ] `ground` tileável, costura testada nos 4 lados.
- [ ] `collision.png` coerente com o desenho (nada de parede invisível sem desenho).
- [ ] `preview_composed.png` com personagem de referência em 3 posições da banda.
- [ ] Banda caminhável respeitada; personagem não "flutua".
- [ ] Contorno dos props conforme tabela §1 (fundo quase sem contorno).
- [ ] Perspetiva coerente entre camadas (linha do horizonte única).
- [ ] Legibilidade: personagem é o maior contraste da cena.
- [ ] Metadados completos (`map.json` + `asset_metadata.json`).
- [ ] Nenhum mapa entregue como imagem achatada única.
