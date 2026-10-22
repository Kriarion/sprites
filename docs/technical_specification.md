# ESPECIFICAÇÃO TÉCNICA (normativa)

**Versão:** 1.0.0 · **Base:** master §18, guia1 §2/§7, guia2 §2/§10
**Escopo:** unidades, escala, resoluções, coordenadas, pivôs, alpha, atlas, performance, metadados.

---

## 1. Sistema de coordenadas

| Item | Definição |
|---|---|
| Espaço de imagem | Origem no **canto superior esquerdo**, `x` para a direita, `y` para **baixo** |
| Unidade | **Pixel** (px) na escala declarada do arquivo |
| Unidade de rig | `1 u = 1 px na escala 1x` |
| Rotação | **Graus**, sentido **horário positivo** (consistente com y↓) |
| Origem do personagem (root) | Interseção entre a **linha do chão** e o **eixo de gravidade** (entre os pés) |
| Eixo de gravidade | `x` do centro da pelve, `y` no chão |
| Facing canônico | 3/4 voltado para a **direita da tela** (espelhável por flip horizontal) |
| Profundidade | Eixo `z` inteiro; **não** há eixo z fractional. Convenção de camadas em `anatomy_and_rigging.md` §5 |
| Pivô | Coordenada no espaço **da própria peça** (top-left da peça = 0,0) |
| Âncora | Posição do osso/encaixe no espaço **do rig**, em u |

Arquivos que usam coordenadas mistas **devem** declarar `coordinate_system: "top_left_y_down"` nos metadados.

## 2. Escala canônica e proporções

### 2.1 Escalas de exportação

| Escala | Altura do corpo | Uso |
|---|---|---|
| **4x (mestre)** | 800 px | Fonte de trabalho para redução; detalhe de cabeça, rosto, arma, ícone |
| **2x** | 400 px | Entrega de alta qualidade; base de atlas de personagem |
| **1x (jogo)** | 200 px | Entrega padrão para jogo 2D em 1280×720 |
| (0,5x) | 100 px | Previews de UI, mapa, retrato pequeno |

Regra de ouro: **reduzir sempre, nunca ampliar**. Se um asset só existe em 1x, ele é a versão final — não se
"recupera" resolução depois.

### 2.2 Tabela de medidas do humanoide padrão (em u, origem no chão)

| Ponto | y | x (relativo ao centro) | Observação |
|---|---|---|---|
| Topo do crânio | 200 | 0 | sem cabelo volumoso |
| Linha dos olhos | 182 | ±7 | |
| Base do queixo | 164 | 0 | |
| **Pescoço (pivô da cabeça)** | **162** | 0 | âncora `neck` |
| **Ombro (pivô do braço)** | **156** | ±28 | âncora `shoulder.front/back` |
| Peitoral (linha do mamilo) | 142 | — | |
| **Cotovelo** | **124** | ±30 | `elbow.*` |
| Cintura (estreitamento) | 120 | — | |
| **Quadril (pivô da perna)** | **100** | ±11 | `hip.*` |
| **Punho** | **94** | ±31 | `wrist.*` |
| Ponta dos dedos | 80 | — | |
| **Pelve / root (topo)** | **118** | 0 | |
| **Joelho** | **56** | ±11 | `knee.*` |
| **Tornozelo** | **14** | ±11 | `ankle.*` |
| Planta do pé | 0 | — | |

Medidas transversais:

| Medida | Valor (u) |
|---|---|
| Largura dos ombros (externo a externo) | 56 |
| Largura do tórax | 46 |
| Largura da cintura | 34 |
| Largura do quadril | 40 |
| Altura da cabeça (crânio+mandíbula) | 36 |
| Largura da cabeça | 30 |
| Comprimento do braço (ombro→punho) | 62 |
| Comprimento da perna (quadril→tornozelo) | 86 |
| Comprimento do pé | 26 |
| Largura da mão | 12 · altura 18 |
| Espessura do braço (superior/antebraço) | 13 / 10 |
| Espessura da coxa / canela | 17 / 12 |

> Desvio máximo aceito em montagem: **±5%** na altura total e **±4 u** em qualquer articulação.

### 2.3 Conversão

```text
px = u × escala
u  = px ÷ escala
```

`pixels_per_unit` nos metadados = escala do arquivo (1, 2 ou 4). Toda engine deve ser capaz de reproduzir a
montagem a partir de `u` + `pixels_per_unit` sem consultar o PNG.

## 3. Resoluções por categoria

| Categoria | Mestre (geração/processo) | Entrega | Formato | Atlas |
|---|---|---|---|---|
| Peça de personagem | 512 px no maior lado | 2x (400 u de corpo) | PNG RGBA | 2048² (por personagem) |
| Corpo completo (referência) | 1024 px de altura | 4x | PNG RGBA | — |
| Cabeça / rosto | 512–1024 px | 4x | PNG RGBA | 1024² |
| Arma | 1024 px no maior lado | 2x–4x | PNG RGBA | 2048² (por conjunto) |
| Armadura / set | 512 px por peça | 2x | PNG RGBA | 2048² |
| VFX (frame) | 512 px por célula | 2x | PNG RGBA | 2048² (grade 4×4 ou 8×8) |
| Ícone de item/skill | 256 px | 128 e 64 | PNG RGBA | 1024² |
| Retrato de HUD | 256×256 | 128 e 64 | PNG RGBA | 1024² |
| UI painel (9-slice) | 512 px de lado | 1x da UI (ver §3.1) | PNG RGBA | 2048² |
| Cenário — camada | 2048–4096 px de largura | 1x da cena | PNG RGBA ou WebP lossless | — |
| Tile de chão | 512 px | 256 px | PNG RGBA | 2048² |
| Prop de cenário | 512 px | 2x do prop | PNG RGBA | 2048² |

### 3.1 Resolução de tela e HUD

| Item | Valor |
|---|---|
| Resolução de design do jogo | **1280 × 720** (escala 16:9) |
| Área jogável vertical | y `440–700` (banda de caminhada) |
| Linha do chão de referência | y `620` |
| Personagem 1x | 200 px → ocupa ~28% da altura da tela |
| HUD base | desenhado para 1280×720, escalável por 9-slice e por fator inteiro/half |
| Margem de segurança | 24 px em todas as bordas |
| Tamanho mínimo de alvo de clique | 40×40 px em 1280×720 |

Cenário em camadas usa largura de 1536 px (1,2×) para permitir parallax horizontal sem emenda visível.

## 4. Pivôs e âncoras

### 4.1 Regras

1. Todo pivô é registrado em **px** (`pivot_px`, relativo ao top-left do PNG) **e** normalizado
   (`pivot_norm` = `pivot_px / [w,h]`), com **âncora nomeada**.
2. O pivô é escolhido para que a **rotação não abra a articulação**: ele fica no centro geométrico da
   junta, não no centro da peça.
3. Peças que se sobrepõem devem ter sobreposição de **≥ 4 u** além do pivô (margem de "sangria de junta")
   para cobrir a abertura durante rotações.
4. Faixa de teste obrigatória: **−35° a +35°** em toda junta, mais as poses de `animation_standard.md`.
5. Nenhum pivô pode estar fora dos limites da imagem (`0 ≤ x ≤ w`, `0 ≤ y ≤ h`) — salvo declaração
   explícita `pivot_outside: true` com justificativa (ex.: cabo de arma).

### 4.2 Nomes de âncora (vocabulário fechado)

```text
root, pelvis, spine_low, spine_high, neck, head, head_top
shoulder.front, shoulder.back, elbow.front, elbow.back
wrist.front, wrist.back, grip.front, grip.back
hip.front, hip.back, knee.front, knee.back, ankle.front, ankle.back
toe.front, toe.back, tail.01…tail.0n, wing.front, wing.back
cape.01…cape.0n, hair.back, hair.front, helm, face
```

Nenhum nome novo entra sem atualização deste vocabulário + bump de versão.

## 5. Alpha, cor e compressão

| Item | Regra |
|---|---|
| Alpha | **Real**, 8 bits (RGBA8888) em todos os sprites. Alpha binário após o keying, com 1 px de matte suave apenas nas bordas anti-aliasing |
| Fundo | Proibido: branco, preto, xadrez desenhado, "transparência" cinza, sombra retangular |
| Cor | sRGB; sem perfil ICC embutido; sem EXIF |
| Padding interno | Peças **sem** margem vazia excessiva: `trim` na bbox + 2 px de respiro |
| Nominal | Arquivo PNG otimizado (`optimize=True`, `compress_level=9`); WebP lossless permitido só em camadas de cenário > 2048 px |
| Peso | Nenhum arquivo > 5 MB no Git (ver `.gitignore` e ADR-0003) |
| Premultiplicação | **Não** premultiplicar alpha nos PNGs entregues (convenção neutra) |

## 6. Atlas e spritesheets

- Dimensões **potência de 2** (512, 1024, 2048, 4096 quando justificado).
- **Padding de 2 px** entre sprites; **extrude de 1 px** nas bordas de cada sprite para evitar bleeding
  em filtragem bilinear.
- Atlas de personagem: máximo **2048²** por personagem (todas as peças + todas as poses de uma forma).
- Spritesheet de animação: grade regular (ex.: 8×4), ordem de frames documentada, sem reordenar.
- O JSON do atlas segue o formato de `production/schemas/` (campos `frames[].frame x/y/w/h`,
  `pivot`, `rotated: false`, `trimmed: true`, `sourceSize`).
- Nenhum atlas com coordenadas "calculadas de cabeça": sempre gerado por `tools/atlas.py`.

## 7. Orçamento de performance (por personagem em jogo)

| Recurso | Teto | Motivo |
|---|---|---|
| Peças visíveis simultâneas | 21 (+3 de VFX) | limite do paper-doll (guia1 §2.1) |
| Texturas distintas por personagem | 2 (2048²) | 1 para corpo/equip, 1 para a forma alternativa |
| Memória de textura por personagem | ≤ 32 MB RGBA (2048² ×2) | alvo de 8 personagens simultâneos em 512 MB |
| Camadas de cenário | 10 | guia1 §7 |
| Camadas com alpha sobreposto na tela | ≤ 6 | custo de fill-rate |
| Frames por animação | 4–12 (loop) / 4–8 (ataque) | estilo Flash + economia |
| VFX simultâneos por tela | ≤ 20 sistemas | legibilidade |
| Tamanho do pacote por personagem completo | ≤ 6 MB | entrega prática |

## 8. Metadados (contrato)

Schema: `production/schemas/asset_metadata.schema.json`. Exemplo canônico:

```json
{
  "asset_id": "DB_CHAR_HERO_GOKU_BASE",
  "version": "1.0.0",
  "status": "APPROVED",
  "category": "character",
  "subcategory": "canonical_hero",
  "character": "goku",
  "continuity": "dbz",
  "form": "base",
  "ownership": "canonical_ip",
  "restrictions": ["non_commercial_study_only"],
  "standards": { "visual_bible": "1.1.0", "technical": "1.0.0", "rig": "1.0.0" },
  "scale": { "rig_unit_px_1x": 1, "pixels_per_unit": 2, "body_height_u": 200 },
  "canvas": { "width": 2048, "height": 2048, "coordinate_system": "top_left_y_down" },
  "rig": "DB_RIG_HUMAN_M_001",
  "parts": [
    {
      "id": "head",
      "file": "exports/individual_png/goku/base/head.png",
      "layer": 15,
      "pivot_px": [64, 92],
      "pivot_norm": [0.5, 0.719],
      "anchor": "neck",
      "size_px": [128, 128],
      "origin_session": "DB-SESSION-0008"
    }
  ],
  "animations": {
    "idle": { "timeline": "idle.json", "duration_ms": 2400, "loop": true, "fps": 24 }
  },
  "dependencies": ["DB_RIG_HUMAN_M_001"],
  "files": ["..."],
  "provenance": {
    "session": "DB-SESSION-0007",
    "method": "generated_grid_keyed",
    "canonical_reference": "Goku DBZ base, gi laranja/azul, faixa e pulseiras",
    "aqw_reference": "ordem de camadas paper-doll, half-shadow"
  },
  "changelog": [{ "version": "1.0.0", "date": "2026-10-xx", "note": "primeira aprovação" }]
}
```

Regras: `parts[].file` deve existir; `layer` deve estar no vocabulário; `pivot_px` dentro da imagem;
`dependencies` devem existir no registry; `status` deve ser um dos 8 estados de `quality_checklist.md`.

## 9. Timelines de animação (contrato)

```json
{
  "animation": "run",
  "rig": "DB_RIG_HUMAN_M_001",
  "fps": 24,
  "duration_ms": 600,
  "loop": true,
  "tracks": {
    "root":        [{ "t": 0, "x": 0, "y": 0, "rot": 0 }, { "t": 300, "y": -6 }],
    "spine_high":  [{ "t": 0, "rot": 15 }, { "t": 150, "rot": 12 }, { "t": 300, "rot": 15 }],
    "thigh.front": [{ "t": 0, "rot": -25 }, { "t": 300, "rot": 25 }, { "t": 600, "rot": -25 }]
  },
  "events": [
    { "t": 300, "type": "footstep", "value": "front" },
    { "t": 300, "type": "sfx", "value": "step_dirt_01" }
  ],
  "hitbox_events": []
}
```

- `t` em milissegundos, absoluto dentro da animação.
- Rotação em graus, horário positivo; `x`/`y` em u, relativos à pose de descanso.
- Interpolação padrão: **linear** com `ease` declarado por key (`"ease": "in"|"out"|"inout"`).
- Toda timeline tem `preview` (APNG/GIF) e é validável pelo schema.

## 10. Validações técnicas obrigatórias (gate G2)

Implementadas em `tools/validate.py` e exigidas para `APPROVED`:

- [ ] PNG abre e é RGBA; existe ≥1 pixel com `alpha = 0` **e** ≥1 com `alpha = 255` (prova de alpha real).
- [ ] Nenhum pixel com cor de fundo-chave remanescente acima de 0.5% da área.
- [ ] Dimensões dentro da faixa da categoria (§3).
- [ ] `pivot_px` dentro da imagem (ou `pivot_outside` justificado).
- [ ] `asset_id` único no registry e aderente ao padrão de `naming_conventions.md`.
- [ ] Metadados validam no schema; todos os arquivos referenciados existem.
- [ ] Camada (`layer`) no vocabulário; ordem sem empate dentro do mesmo personagem.
- [ ] Atlases: coordenadas dentro dos limites, sem sobreposição, padding ≥2 px.
- [ ] Dependências existentes; nenhuma referência quebrada.
- [ ] Tamanho de arquivo e de atlas dentro do orçamento (§7).

## 11. Compatibilidade

Os entregáveis neutros são **PNG + JSON**. Qualquer arquivo específico de engine (`.tscn`, `.prefab`,
`.tres`) é **exemplo opcional** e nunca substitui os neutros (master §18.5).
Adapters previstos (não obrigatórios): Spine/DragonBones (mapear bones 1:1), Godot `Sprite2D` + `Node2D`
hierárquico, Unity `SpriteRenderer` hierárquico. Detalhes em `integration_guide.md`.
