# PADRÃO DE VFX E HABILIDADES (normativo)

**Versão:** 1.0.0 · **Base:** guia1 §6, guia2 §4, master §12

A magia do estilo AQW não é simulação de partículas: é **sprite animado com blending aditivo**.
O que define qualidade é a **componentização** — um Kamehameha não é uma imagem, é um sistema.

---

## 1. Anatomia obrigatória de uma habilidade

```text
skills/beams/kamehameha/
├── DB_SKILL_KAMEHAMEHA.asset.json
├── icon_128.png  icon_64.png
├── cast_start/       pose_prep.png, chi_sphere_01..04.png
├── charging/         orbit_01..06.png, core_*.png
├── projectile/       core.png, segment.png, tip.png, trail_01..04.png
├── impact/           flash.png, ring.png
├── explosion/        frame_01..08.png
├── particles/        spark_01..06.png, dust_01..04.png
├── preview/          preview_sequence.png, preview.apng
└── metadata.json
```

Regras:
- **Nunca** entregar personagem + feixe + explosão numa única imagem inseparável (master §12.3).
- Segmento de feixe é **extensível** (tileable ao longo do eixo) com `core` e `tip` separados.
- Cada componente tem pivô (ponto de origem/emissão) documentado.
- Nome de arquivo indica a função, nunca "vfx1.png".

## 2. Categorias

| Categoria | Pasta | Exemplos |
|---|---|---|
| Ataque físico | `melee/` | soco, chute, combo, sword slash |
| Rajada de Ki | `projectiles/` | ki blast, Death Beam, Kienzan (disco) |
| Feixe contínuo | `beams/` | Kamehameha, Galick Gun, Final Flash, Makankosappo |
| Explosão / AoE | `explosions/` | Big Bang Attack, Death Ball, Final Explosion |
| Onda de choque | `explosions/` | shockwave de impacto |
| Aura / buff | `auras/`, `buffs/` | Kaioken, SSJ aura, escudo, cura |
| Debuff | `buffs/` | marca de Babidi, congelamento |
| Transformação | `transformations/` | burst de ativação, desativação |
| Utilidade | `buffs/` | Instant Transmission, Solar Flare |
| Invocação | `summons/` | Genki Dama (esfera + feixe), dragões |

## 3. Blending (contrato com a engine)

| Tipo de efeito | Blend | Observação |
|---|---|---|
| Núcleo de energia, flash, spark | **Aditivo (Add)** | núcleo sempre branco; satura sem escurecer |
| Aura, glow suave | **Screen** | não "lava" o personagem (alpha ≤ 60%) |
| Sombra de energia, fumaça, poeira | **Multiply / Normal** | poeira com alpha 40–70% |
| Rastro (trail) | **Add** com fade de alpha | 4 frames, alpha 100→0 |
| Impacto de corte (slash) | **Screen** ou **Add** | arco branco-amarelo com borda colorida |
| Escudo | **Screen** com borda Normal | deve ler como "película", não opaco |

Regras:
- Todo componente declara `blend: "add" | "screen" | "normal" | "multiply"` nos metadados.
- Efeito luminoso **nunca** em PNG com fundo opaco.
- Alpha > 0 obrigatório em toda a imagem (não existe "glow preto").
- Cor de núcleo: `#FFFFFF` a `#FFF4CC`; saturação só nas bordas.

## 4. Paleta por elemento

| Elemento | Núcleo | Meio | Borda (glow) |
|---|---|---|---|
| Ki padrão | `#FFFFFF` | `#8FE3FF` | `#2E9BFF` |
| Kamehameha | `#FFFFFF` | `#9FE8FF` | `#1F6FE0` |
| Energia maligna / vilão | `#FFFFFF` | `#E8B4FF` | `#8A2BE2` |
| Fogo | `#FFF8D0` | `#FFC24B` | `#E0411B` |
| Elétrico (SSJ2, Thunder) | `#FFFFFF` | `#C8F0FF` | `#4FD2FF` |
| Divino (SSG/SSB/UI) | `#FFFFFF` | `#FFD9A0` / `#A0E4FF` | `#C77BFF` / `#2E6BFF` |
| Destruição (Hakai) | `#FFFFFF` | `#C9A0FF` | `#5B1FA8` |
| Cura / buff | `#FFFFFF` | `#B8FFD0` | `#2FD07A` |
| Sombra / drenagem | `#E9D8FF` | `#6E4B9E` | `#1A0F2B` |

Cores exatas em `references/palettes/core_palettes.json`.

## 5. Timing (regra dos 100 ms)

| Fase | Duração alvo | Frames @24fps |
|---|---:|---:|
| Cast start / concentração | 300–600 ms | 8–14 |
| Carga (loop) | 1200 ms | 4 (loop) |
| Disparo / travel | 200–500 ms | 5–12 |
| Impacto (flash + ring) | 100–200 ms | 3–5 |
| Explosão | 400–800 ms | 10–19 |
| Dissipação | 300–500 ms | 7–12 |

- Frame de impacto **deve** existir e ser legível em 1–2 frames (é o "hit stop" visual).
- Efeito total de skill comum: ≤ 1,8 s até dissipar (combate casual, guia2 §3).
- Nada bloqueia a tela por mais de 400 ms (legibilidade de combate).

## 6. Legibilidade

- Efeito não pode cobrir o personagem por completo, exceto Ultimate/boss declarado.
- Contraste do efeito contra o cenário deve ser testado nos 3 temas mais comuns
  (claro, escuro, saturado).
- Máximo de **20** sistemas de VFX simultâneos na tela (orçamento §7 de `technical_specification.md`).
- Partículas: no máximo 6 sprites distintos por efeito; reutilização obrigatória.

## 7. Metadados de uma skill

```json
{
  "asset_id": "DB_SKILL_KAMEHAMEHA",
  "category": "skill",
  "subcategory": "beam",
  "owner_character": "goku",
  "components": [
    { "id": "core", "file": "projectile/core.png", "blend": "add", "pivot": [0, 32], "tileable_axis": null },
    { "id": "segment", "file": "projectile/segment.png", "blend": "add", "tileable_axis": "x", "stretch_min_px": 128 },
    { "id": "tip", "file": "projectile/tip.png", "blend": "add", "anchor": "head" },
    { "id": "impact_ring", "file": "impact/ring.png", "blend": "add", "scale_from": 0.4, "scale_to": 2.2 }
  ],
  "timing_ms": { "cast_start": 400, "charge_loop": 1200, "fire": 300, "impact": 150, "explosion": 600, "fade": 400 },
  "socket": "hand.front",
  "events": [{ "t": 0, "type": "charge" }, { "t": 400, "type": "fire" }, { "t": 700, "type": "impact" }],
  "icon": "icon_128.png",
  "preview": "preview/preview.apng",
  "damage_profile_hint": { "type": "beam", "max_targets": 3, "ticks": 4 }
}
```

`damage_profile_hint` é **sugestão de design**, não balanceamento final.

## 8. Checklist de aprovação

- [ ] Componentes separados em arquivos distintos.
- [ ] `blend` declarado por componente.
- [ ] Alpha real; núcleo branco; nenhum fundo opaco.
- [ ] Segmento testado em 2 comprimentos (curto/longo) sem esticar borda.
- [ ] Impacto e explosão legíveis isoladamente.
- [ ] Ícone 128/64 entregue, legível e coerente com a paleta.
- [ ] Timing dentro das faixas da §5.
- [ ] Preview APNG com a sequência completa.
- [ ] Não cobre o personagem além do permitido.
- [ ] Reutiliza partículas existentes quando possível.
