# equipment/

Equipamentos modulares. **Nenhum asset aqui ainda** (Fase 0).

| Pasta | Slot | Camadas |
|---|---|---|
| `armor/` | `chest`, `belt`, `shoulders` | 10, 11, 17 |
| `helmets/` | `helm` | 16 |
| `hairstyles/` | `hair` | 2, 16 |
| `capes/` | `cape`, `back` | 1, 3 |
| `gloves/` | `gloves` | 6, 20 |
| `boots/` | `boots` | 8, 9, 13, 14 |
| `accessories/` | `accessory` | 16 ou 23 |
| `weapons/` | `weapon_main`, `weapon_off` | 21, 3 |

## Regras

- Pivô e âncora **idênticos** à peça-base correspondente (`equipment_standard.md` §2).
- Toda peça testada em 3 bases (M/F/musculoso) e 3 poses antes de `APPROVED`.
- Ícone 128/64 e `preview_assembly.png` obrigatórios.
- Armas: cabo no eixo vertical/horizontal, pivô em `grip.front` (centro do cabo).
- `conflicts_with` declarado (capa × asas, mochila × capa).
- Conjunto canônico declara `ownership: canonical_ip`; design inventado declara `original_design`.
