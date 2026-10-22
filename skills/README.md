# skills/

Habilidades, VFX e ícones de skill. **Nenhum asset aqui ainda** (Fase 0).

| Pasta | Conteúdo |
|---|---|
| `icons/` | ícones 128/64 de habilidades e transformações |
| `projectiles/` | ki blasts, Death Beam, Kienzan |
| `beams/` | Kamehameha, Galick Gun, Final Flash, Makankosappo |
| `melee/` | socos, chutes, cortes de espada |
| `explosions/` | Big Bang Attack, Death Ball, ondas de choque |
| `auras/` | Kaioken, SSJ, escudos |
| `buffs/` | cura, buff, debuff, utilidade (Solar Flare, Instant Transmission) |
| `transformations/` | bursts de ativação e desativação |

## Regras

- Skill é **sistema de componentes**, nunca imagem única (ver `vfx_standard.md` §1).
- Cada componente declara `blend` (add/screen/normal/multiply) e pivô de emissão.
- Feixe tem `core` + `segment` (tileável) + `tip` separados.
- Timing dentro das faixas de `vfx_standard.md` §5; impacto legível em 1–2 frames.
- Ícone obrigatório; preview APNG obrigatório.
