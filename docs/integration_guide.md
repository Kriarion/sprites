# GUIA DE INTEGRAÇÃO (engine-agnostic)

**Versão:** 1.0.0 · **Base:** master §18.5

O pacote entrega **PNG + JSON**. Nada essencial depende de engine. Este guia descreve o modelo mental mínimo
para montar o personagem em qualquer runtime 2D.

---

## 1. Modelo de montagem

```text
Personagem = RIG (hierarquia de bones + âncoras)
           + SLOTS (peças por camada)
           + TRANSFORMS (pose por animação)
           + TIMELINE (keys + eventos)

Para cada bone, em ordem de profundidade (layer):
    sprite.position  = bone.world_position - pivot_px   (ajustado por pixels_per_unit)
    sprite.rotation  = bone.world_rotation
    sprite.scale     = 1 (nunca escalar peças de corpo)
```

Passo a passo:

1. Carregar `*.rig.json` → criar nós na hierarquia de bones.
2. Para cada *slot*, carregar o PNG indicado em `parts[]` e ancorar em `parts[].anchor`,
   deslocando pelo `pivot_px` dividido por `pixels_per_unit`.
3. Aplicar `layer` como `z_index` (ou ordem de filhos).
4. Tocar `*.anim.json`: interpolar rotação/posição por key; disparar `events` nos tempos declarados.
5. Espelhar para a esquerda por **flip horizontal do nó raiz** (nunca flip peça a peça).

Escala de mundo: `1 u = 1 px` em 1x. Em 1280×720, personagem = 200 px. Escolha um `ppu` (pixels por
unidade de mundo) e mantenha consistente em toda a cena.

## 2. Ordem de renderização

Use `layer` (0–21) para o corpo e as camadas de efeito (−10, 22, 23). Nunca confie na ordem de carregamento
de arquivos. `ground shadow` (layer 0) é desenhado **no chão**, não como filho do personagem.

## 3. Godot 4 (exemplo de referência)

```gdscript
# montagem mínima (Node2D hierárquico, sem plugin)
func build(rig: Dictionary, parts: Array) -> Node2D:
    var bones := {}
    for b in rig.bones:
        var n := Node2D.new()
        n.name = b.id
        n.position = Vector2(b.x, -b.y)   # JSON usa y↓, Godot usa y↑
        bones[b.id] = n
        if b.parent != null:
            bones[b.parent].add_child(n)
    for p in parts:
        var s := Sprite2D.new()
        s.texture = load(p.file)
        s.centered = false
        s.offset = -Vector2(p.pivot_px[0], p.pivot_px[1])
        s.z_index = p.layer
        bones[p.anchor].add_child(s)
    return bones[rig.bones[0].id]
```

Conversões importantes:
- **Y invertido** (JSON y↓ → Godot y↑): negar `y` ao criar nós.
- **Rotação**: JSON é graus, horário positivo. Em Godot, `rotation_degrees` é anti-horário positivo →
  negar o valor.
- `filter` da textura: **linear** com *mipmaps off* para estilo Flash; `nearest` só se o jogo for pixel art
  (não é o caso).

## 4. Unity 2D (exemplo de referência)

- Hierarquia de `Transform` espelhando o rig; `SpriteRenderer` por peça com `sortingOrder = layer`.
- `Sprite.Create` com `pivot` normalizado (`pivot_norm`) para respeitar a rotação.
- Animação por `AnimationClip` gerada a partir do `*.anim.json` (curvas de `localEulerAngles.z`
  com sinal invertido) ou por runtime customizado lendo o JSON.
- `TextureImporter`: `Sprite (2D and UI)`, `Filter Mode: Bilinear`, `Compression: None`
  (para preservar contorno), `sRGB: on`.

## 5. GameMaker / Construct / engine própria

- `layer` → `depth` (invertido: GameMaker desenha menor depth na frente).
- Timeline JSON é agnóstico: qualquer tween engine serve (`t` em ms, `rot` em graus).
- Uso de spritesheet: as mesmas peças empacotadas em atlas — o JSON do atlas dá `frame` e `pivot`.

## 6. Exemplo de arquivos opcionais por engine

`examples/` pode conter:

- `examples/godot_minimal/` — projeto Godot 4 demonstrativo (opcional).
- `examples/unity_minimal/` — cena e scripts demonstrativos (opcional).
- `examples/web_preview/` — visualizador HTML/JS de montagem e timeline (opcional; requer servir localmente).

Esses exemplos são **conveniência**, nunca o entregável. Se um exemplo quebrar, o pacote continua válido.

## 7. Configurações de importação recomendadas

| Engine | Filtro | Compressão | Mipmap | Notes |
|---|---|---|---|---|
| Godot | Linear | Lossless | Off | `fix_alpha_border` on (evita bleeding) |
| Unity | Bilinear | None | Off | `Sprite Mode: Single`, `Mesh Type: Full Rect` |
| WebGL | Linear | — | Off | `premultipliedAlpha: false` |
| GameMaker | Linear | Lossless | Off | — |

## 8. Espelhamento e facing

- Um único conjunto de arte, facing direita. Esquerda = flip horizontal do nó raiz.
- Atenção: textos/emblemas dentro da arte devem ser **neutros** (ou ausentes) para não ficarem invertidos.
  Regra do projeto: nenhum texto legível em equipamento; kanji estilizado só quando simétrico ou aceitável
  espelhado (declarar em `readability.mirror_safe: true`).

## 9. Escala e câmera

- Cena de 1280×720 com personagem de 200 px: câmera ortográfica, `zoom = 1`.
- Para telas maiores, escalar a câmera por fator inteiro quando possível (evita serrilhado de contorno).
- HUD em camada separada, escalado independentemente (ver `ui_standard.md` §1).

## 10. Áudio e eventos

`events[].type` inclui `sfx` com um `id` sugerido. O pacote **não** entrega áudio; a engine mapeia
`id` → arquivo próprio. Não invente dependência de áudio no pacote.

## 11. Checklist de integração

- [ ] Personagem montado a partir do JSON, sem ajuste manual de peça.
- [ ] Pivôs corretos após conversão de eixo (y↓ → y↑).
- [ ] Ordem de camadas correta em idle, corrida e ataque.
- [ ] Animação interpola sem "pop" em loop.
- [ ] Eventos disparam (`projectile_spawn` cria o Kamehameha no `hand.front`).
- [ ] Flip horizontal funciona e não revela texto espelhado.
- [ ] Nenhum asset proprietário obrigatório para rodar.
- [ ] Escala consistente com o cenário (`reference_scale.png` do mapa).
