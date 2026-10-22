# characters/

Personagens, corpos base e rigs. **Nenhum asset aqui ainda** (Fase 0).

## Subpastas (criadas quando o primeiro asset chegar)

| Pasta | Conteúdo |
|---|---|
| `base_bodies/` | corpos neutros/dummies utilizáveis por qualquer personagem |
| `canonical_heroes/` | Goku, Vegeta, Gohan, Piccolo, Trunks, Kuririn, Bulma… |
| `canonical_villains/` | Freeza, Cell, Majin Buu, Goku Black, Jiren… |
| `npcs/` | não combatentes (Mestre Kame, Dende, Mr. Satan, Videl…) |
| `transformations/` | peças de substituição por forma (cabelo, olhos, sobrancelhas, aura) |
| `rigs/` | `*.rig.json` (dado, sem imagem) |

## Estrutura por personagem

```text
canonical_heroes/goku/
├── goku_base.asset.json          metadados (parts, pivôs, camadas, animações)
├── parts/                        PNGs por peça (fonte)
│   ├── goku_base_head.png
│   ├── goku_base_torso.png
│   └── ...
├── anim/                         *.anim.json
├── masks/                        máscaras de cor (opcional)
├── icons/                        retrato 128/64
├── preview/                      montagem + APNG
└── changelog.md
```

## Regras

- 21 peças por personagem, camadas `0–21` de `anatomy_and_rigging.md` §1.
- Toda peça tem pivô de template + âncora nomeada; sem pivô "ajustado no olho".
- Personagem canônico declara `continuity` (`db|dbz|dbs|gt|movie`) e `ownership: canonical_ip`.
- Transformação **não** é recolor da imagem inteira: é substituição de peças + aura + VFX.
- Não criar pasta de personagem sem asset registrado e aprovado em G1–G4.
