# ANATOMIA E RIGGING (normativo)

**Versão:** 1.0.0 · **Base:** guia1 §2, guia2 §2, master §7 · **Schema:** `production/schemas/rig.schema.json`

O corpo é um **paper-doll**: 21 peças independentes, cada uma presa a uma âncora por um pivô. O rig é
**dado** (JSON), não binário de software — essa é a decisão `ADR-0003`.

---

## 1. Ordem de camadas (vocabulário fechado, `layer`)

Do fundo para a frente. Os números são **valores absolutos** usados em todos os metadados.

| layer | id | Peça | Âncora | Notas |
|---:|---|---|---|---|
| 0 | `shadow_ground` | Sombra no chão | `root` | elipse, alpha 25–35%, **não** faz parte da folha do personagem |
| 1 | `cape` | Capa / asas traseiras | `spine_high` | animação de sway própria |
| 2 | `hair_back` | Cabelo traseiro | `head` | escurecido (half-shadow) |
| 3 | `weapon_back` | Arma traseira | `grip.back` | só em empunhadura dupla |
| 4 | `upperarm_back` | Braço superior traseiro | `shoulder.back` | escurecido |
| 5 | `forearm_back` | Antebraço traseiro | `elbow.back` | escurecido |
| 6 | `hand_back` | Mão traseira | `wrist.back` | escurecida |
| 7 | `thigh_back` | Coxa traseira | `hip.back` | escurecida |
| 8 | `shin_back` | Canela/bota traseira | `knee.back` | escurecida |
| 9 | `foot_back` | Pé traseiro | `ankle.back` | escurecido |
| 10 | `pelvis` | Pelve / cintura | `root` | raiz visual |
| 11 | `torso` | Tronco / peitoral | `spine_low` | conecta à pelve |
| 12 | `thigh_front` | Coxa frontal | `hip.front` | detalhado |
| 13 | `shin_front` | Canela/bota frontal | `knee.front` | detalhado |
| 14 | `foot_front` | Pé frontal | `ankle.front` | detalhado |
| 15 | `head` | Cabeça base / face | `neck` | contém `face_eyes` (piscar) e `face_mouth` |
| 16 | `helm` | Capacete / cabelo frontal | `head` | sobrepõe a cabeça |
| 17 | `pauldrons` | Ombreiras | `spine_high` | cobre as juntas dos ombros |
| 18 | `upperarm_front` | Braço superior frontal | `shoulder.front` | detalhado |
| 19 | `forearm_front` | Antebraço frontal | `elbow.front` | detalhado |
| 20 | `hand_front` | Mão frontal | `wrist.front` | pose de grip |
| 21 | `weapon_main` | Arma principal | `grip.front` | filha da mão frontal |

Camadas de efeito (fora do corpo, não contam nas 21):

| layer | id | Uso |
|---:|---|---|
| −10 | `aura_back` | aura atrás do personagem |
| 22 | `aura_front` | aura à frente do corpo |
| 23 | `vfx_attach` | VFX presos a mãos/pés (carga de Ki) |
| 30 | `nameplate` | nome/guilda (engine, não arte) |

**Regra:** `layer` é inteiro e único dentro de um mesmo personagem. Exceções exigem ADR.

## 2. Hierarquia de bones

```text
root                         (0,0 no chão, eixo de gravidade)
├── pelvis                   (+0, +100 u)
│   ├── spine_low            (+0, +118 u)
│   │   └── spine_high       (+0, +140 u)
│   │       ├── neck         (+0, +162 u)
│   │       │   └── head     (+0, +164 u)
│   │       │       ├── face_eyes
│   │       │       ├── face_mouth
│   │       │       ├── hair_front
│   │       │       ├── hair_back
│   │       │       └── helm
│   │       ├── shoulder.front  (+28, +156 u)
│   │       │   └── upperarm.front
│   │       │       └── forearm.front
│   │       │           └── hand.front
│   │       │               └── grip.front → weapon_main
│   │       ├── shoulder.back   (−28, +156 u)
│   │       │   └── … (espelho) → weapon_back
│   │       ├── pauldron.front / pauldron.back
│   │       └── cape.01 → cape.02 → cape.03
│   ├── hip.front  (+11, +100 u)
│   │   └── thigh.front → knee.front → shin.front → ankle.front → foot.front
│   └── hip.back   (−11, +100 u)
│       └── thigh.back → knee.back → shin.back → ankle.back → foot.back
└── (opcional) tail.01 → tail.02 → tail.03      (raça de Freeza, Oozaru, bosses)
    (opcional) wing.front / wing.back            (pets, bosses)
```

Convenções:
- `front` = lado **mais próximo do observador** (o lado da tela em 3/4). `back` = lado oposto, escurecido.
- Nome de bone = nome da âncora correspondente. Sem sinônimos.
- Cadeias (cauda, capa, cabelo) usam índices de 2 dígitos (`tail.01`).

## 3. Rigs por arquétipo (master §7.4)

| ID de rig | Arquétipo | Bones | Reutiliza | Particularidades |
|---|---|---:|---|---|
| `DB_RIG_HUMAN_M_001` | Humano masculino padrão | 27 | — | base de Goku, Kuririn, Yamcha, Trunks |
| `DB_RIG_HUMAN_F_001` | Humano feminino padrão | 27 | M_001 (mesma topologia) | quadril +2 u, ombro −8 u, altura 192 u |
| `DB_RIG_HUMAN_MUSC_001` | Musculoso | 29 | M_001 + bones de trapézio | ombros 68 u, braço mais grosso |
| `DB_RIG_HUMAN_CHILD_001` | Infantil | 27 | M_001 | altura 128 u, cabeça 40 u |
| `DB_RIG_SAIYAN_M_001` | Saiyajin masculino | 30 | M_001 + `tail.01–03` | cauda animável, cabelo com 3 bones |
| `DB_RIG_SAIYAN_F_001` | Saiyajin feminino | 30 | F_001 + cauda | |
| `DB_RIG_NAMEK_001` | Namekuseijin | 30 | M_001 + `antenna.01–02` | 5 dedos não obrigatórios; orelhas pontudas |
| `DB_RIG_MAJIN_001` | Majin | 28 | M_001 | membros elásticos (escala de bone) |
| `DB_RIG_ANDROID_001` | Androide humanoide | 28 | M_001 | juntas mecânicas visíveis, sem `face_mouth` obrigatório |
| `DB_RIG_FRIEZA_001` | Raça de Freeza | 30 | M_001 + `tail.01–03` | crânio alongado, 3 dedos por mão |
| `DB_RIG_CREATURE_S_001` | Criatura pequena (pet) | 8 | — | 4–8 bones, sem dedos |
| `DB_RIG_CREATURE_QUAD_001` | Quadrúpede | 18 | — | 4 cadeias de perna |
| `DB_RIG_BOSS_XL_001` | Boss gigante | 34+ | varia | escala 4x–9x, segmentação de cauda/asa |
| `DB_RIG_CREATURE_TAIL_001` | Criatura com cauda | 26 | M_001 | cauda de 3–5 segmentos |
| `DB_RIG_CREATURE_WING_001` | Criatura com asas | 24 | CREATURE_S_001 | asa frontal/traseira com 2 segments |

**Regra:** novas espécies só ganham rig próprio se a anatomia **não** puder ser acomodada por um rig
existente com escala/offset. Criaturas não são forçadas em rigs humanoides (master §7.4).

## 4. Limites articulares (ROM canônico)

Valores em graus, para a pose de descanso (idle). O rig declara `min`/`max`; animações fora da faixa
**falham** na validação.

| Junta | min | max | Observação |
|---|---:|---:|---|
| `neck` | −25 | 30 | |
| `head` | −35 | 35 | inclinação; rotação de 3/4 só para cutscene |
| `spine_low` | −20 | 25 | |
| `spine_high` | −25 | 25 | |
| `shoulder.*` | −15 | 20 | elevar/abaixar |
| `upperarm.*` | −150 | 90 | braço para trás/frente |
| `forearm.*` | −150 | 0 | cotovelo só dobra para dentro |
| `wrist.*` | −60 | 60 | |
| `hip.*` | −120 | 45 | |
| `knee.*` | 0 | 145 | joelho só dobra para trás |
| `ankle.*` | −35 | 40 | |
| `tail.01–0n` | −60 | 60 | por segmento |
| `cape.01–03` | −30 | 45 | soma máxima 60 (evitar auto-interseção) |

Envelopes de animação: **nenhuma** pose de combate pode exceder 90% do ROM — o excedente é onde nasce o
"encaixe estourado".

## 5. Sobreposição e sangria de junta

- Cada peça tem **sangria de junta** de **≥ 4 u** além do pivô (na direção distal e proximal).
- Ombreiras e pelve cobrem as juntas críticas (ombro, quadril) por desenho — se a peça base não cobrir,
  a armadura deve cobrir.
- Teste de rotação: 8 ângulos por junta (−35, −25, −15, −5, 5, 15, 25, 35) × 2 eixos visuais.
  Qualquer "gap" de fundo ou "dobra" visível = reprovado.
- Pivô da cabeça fica **dentro** do tronco (2 u abaixo do queixo), nunca na borda externa.

## 6. Máscaras de recoloração (`color_masks`)

Cada personagem/armadura pode entregar máscaras em **canal único (grayscale)**, mesmo tamanho da peça-alvo:

| Máscara | Escopo |
|---|---|
| `mask_skin` | pele (todas as peças de corpo) |
| `mask_hair` | cabelo (frontal/traseiro) |
| `mask_eyes` | íris e esclera (separadas: `mask_iris`, `mask_sclera`) |
| `mask_cloth` | tecido da roupa |
| `mask_metal` | metais e trims |
| `mask_energy` | aura/glow (para tint por habilidade) |

Regras:
- Máscara é **opcional** por asset, mas se existir deve ser listada em `dependencies`.
- Recoloração aplicada em runtime multiplicando a máscara pela cor — o PNG original permanece intacto.
- **Nunca** recolorir personagem canônico de forma que destrua a identidade (master §7.5).
- Personagens canônicos têm `recolor_allowed: false` para skins/cabelo canônicos, e `true` para
  acessórios cosméticos explicitamente marcados.

## 7. Ritual de montagem (obrigatório para aprovar um rig)

1. Montar o dummy neutro a partir das 21 peças, apenas com os dados do JSON (sem "ajuste manual").
2. Renderizar 3 poses: idle, corrida (frame de contato), ataque (frame de impacto).
3. Sobrepor o overlay de proporção (`references/proportion_charts/`) e medir desvio.
4. Rotacionar cada junta em 8 ângulos e procurar gaps/dobras.
5. Gerar `examples/sample_character/assembly_report.json` com: peças usadas, desvio medido, gaps
   encontrados, resultado (`PASS`/`FAIL` por junta).
6. Somente com `PASS` em todas as juntas o rig entra em `APPROVED`.

Se qualquer item falhar, o rig é `REWORK_REQUIRED` — **não** se "ajusta no olho" e segue.

## 8. Extensões (asas, caudas, bosses)

- Cauda: mínimo 3 segmentos, cada um com peça própria e pivô na base; animação em chicote.
- Asas: `wing.front` e `wing.back` com 2 segmentos cada (base e ponta) para flap convincente.
- Boss gigante: segmentação adicional de pescoço (2), mandíbula (1), braços (3 por lado)
  e cauda (5) quando couber; escala declarada em `scale.body_height_u`.
- Todas as extensões entram como `optional_bones` no rig, para que o mesmo rig sirva a variantes
  com e sem cauda.

## 9. Rigs como dado: contrato mínimo

```json
{
  "rig_id": "DB_RIG_HUMAN_M_001",
  "archetype": "human_male_standard",
  "version": "1.0.0",
  "body_height_u": 200,
  "bones": [
    { "id": "root",   "parent": null,      "x": 0,  "y": 0,   "length": 0, "rot": 0 },
    { "id": "pelvis", "parent": "root",    "x": 0,  "y": 100, "length": 18 },
    { "id": "neck",   "parent": "spine_high", "x": 0, "y": 162, "length": 2,
      "min": -25, "max": 30 }
  ],
  "slots": [
    { "layer": 15, "anchor": "neck", "allowed_categories": ["head", "hair", "helm", "face"] }
  ],
  "optional_bones": ["tail.01", "tail.02", "tail.03", "cape.01", "cape.02", "cape.03"],
  "recolor_masks": ["mask_skin", "mask_hair", "mask_eyes", "mask_cloth", "mask_metal", "mask_energy"],
  "compatible_bodies": ["DB_CHAR_BASE_HUMAN_M"],
  "approval": { "session": "DB-SESSION-0005", "report": "production/qa_reports/rig_m_001.md" }
}
```
