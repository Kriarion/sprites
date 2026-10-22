# PADRÃO DE EQUIPAMENTOS (normativo)

**Versão:** 1.0.0 · **Base:** guia1 §4, guia2 §6, master §10

Equipamento é a razão de existir do paper-doll: **trocar sem redesenhar**. Este documento define como.

---

## 1. Slots (vocabulário fechado)

| Slot | `slot_id` | Camada(s) que ocupa | Peças | Substitui corpo? |
|---|---|---|---|---|
| Cabeça | `head` | 15 | 1 | sim (morph) |
| Rosto/face | `face` | 15.5 (sub-camada da cabeça) | olhos, boca, marca | não |
| Cabelo | `hair` | 2 + 16 | 2 (frente/trás) | parcial |
| Capacete | `helm` | 16 | 1–2 | parcial ou total |
| Tronco | `chest` | 11 | 1 | sim |
| Ombros | `shoulders` | 17 | 2 (ou 1 par) | não |
| Braços | `arms` | 4, 5, 18, 19 | 4 | sim |
| Luvas | `gloves` | 6, 20 | 2 | sim |
| Cintura | `belt` | 10.5 | 1 | parcial |
| Pernas | `legs` | 7, 8, 12, 13 | 4 | sim |
| Botas | `boots` | 8, 9, 13, 14 | 4 | sim |
| Costas | `back` | 3 | 1 | não |
| Capa | `cape` | 1 | 1–3 segmentos | não |
| Arma principal | `weapon_main` | 21 | 1 | não |
| Arma secundária | `weapon_off` | 3 | 1 | não |
| Acessório | `accessory` | 16 ou 23 | 1 | não |
| Aura cosmética | `aura` | −10 / 22 | 2 | não |

Regra: um slot aceita **uma** peça por vez; peças podem ocupar múltiplas camadas (ex.: bota cobre canela e pé).

## 2. Ancoragem

- Toda peça declara `anchor` (vocabulário de `anatomy_and_rigging.md` §2) e `pivot_px`.
- **Armaduras que substituem corpo** devem copiar o pivô da peça-base correspondente (mesma âncora,
  mesmo pivô em u, ajustado só pela bbox do novo arquivo).
- Armas: `grip.front` no **cabo**, com o eixo do cabo alinhado vertical ou horizontalmente no arquivo,
  para que a rotação seja previsível.
- Capas: pivô em `spine_high` e cadeia de 2–3 segmentos com pivôs no topo de cada segmento.
- Nenhuma peça é ancorada em "coordenada mágica" fora do vocabário.

## 3. Compatibilidade

Matriz obrigatória por peça (`compatibility` nos metadados):

```json
"compatibility": {
  "rigs": ["DB_RIG_HUMAN_M_001", "DB_RIG_HUMAN_MUSC_001"],
  "genders": ["m", "f"],
  "body_scales": ["standard", "muscular"],
  "conflicts_with": ["cape", "back"],
  "requires": []
}
```

- Teste obrigatório em **3 bases** (masculino, feminino, musculoso) e **3 poses** (idle, run, attack).
- `conflicts_with` resolve sobreposição (ex.: asas × capa; mochila × capa).
- Peças exclusivas de corpo (ex.: cauda de Oozaru) declaram `rigs` específicos.
- Personagem canônico veste o conjunto canônico por padrão (não é slot aleatório).

## 4. Variantes e máscaras

| Tipo de variante | Sufixo no ID | Exemplo |
|---|---|---|
| Gênero | `_M` / `_F` | `DB_EQUIP_ARMOR_SAIYAN_M_...` |
| Cor/tinta | `_RED`, `_BLK`, `_GOLD` | `DB_EQUIP_ARMOR_GINYU_WHT` |
| Forma do personagem | `_SSJ`, `_BASE` | — (vem do corpo, não do equipamento) |
| Nível de detalhe | `_PRESTIGE` | conjuntos de prestígio (guia2 §6) |

Máscaras de cor por peça (opcionais, obrigatórias em sets cosméticos): `mask_cloth`, `mask_metal`,
`mask_glow`. Ver `anatomy_and_rigging.md` §6.

## 5. Poses de empunhadura (grip poses)

- `grip.front` e `grip.back` têm **poses de mão** dedicadas: `hand_grip_vertical`, `hand_grip_horizontal`,
  `hand_relaxed`, `hand_open` (para ki cast), `hand_fist`.
- A mão frontal troca de pose por **troca de sprite** (mesma âncora/pivô), nunca por deformação.
- Armas de duas mãos: arma principal em `hand.front`, arma secundária opcional em `hand.back`.

## 6. Clipping e ordem

- Sobreposição mínima de **4 u** nas juntas; 0 gap visível.
- Itens volumosos (ombreiras gigantes, capas longas) recebem camada própria declarada — e **não** podem
  ocultar a mão frontal nem a arma principal.
- Regra de leitura: em idle, 3 pontos de referência do corpo (rosto, mão frontal, linha do quadril)
  devem permanecer visíveis, salvo sets "prestige" que ocupam toda a silhueta (declarar em `readability`).

## 7. Entrega por conjunto

```text
equipment/armor/saiyan_armor/
├── DB_EQUIP_ARMOR_SAIYAN_M.asset.json
├── chest.png  shoulders.png  arms_f.png  arms_b.png
├── belt.png  legs_f.png  legs_b.png  boots_f.png  boots_b.png
├── masks/ (opcional)
├── icon_128.png  icon_64.png
├── preview_assembly.png
└── changelog.md
```

- Ícone sempre presente para qualquer item equipável (master §17).
- `preview_assembly.png` mostra o set vestido no dummy (evidência do gate G3).

## 8. Checklist de aprovação

- [ ] Pivô/âncora idênticos aos da peça-base correspondente.
- [ ] Testado em 3 bases e 3 poses, sem gap > 0 e sem clipping crítico.
- [ ] `conflicts_with` coerente (testado contra capa/back).
- [ ] Escala consistente: a peça não "cresce" entre bases.
- [ ] Paleta do personagem/set respeitada.
- [ ] Ícone 128/64 legível.
- [ ] Preview de montagem anexado.
- [ ] Metadados completos e ID único.
