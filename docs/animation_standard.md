# PADRÃO DE ANIMAÇÃO (normativo)

**Versão:** 1.0.0 · **Base:** guia1 §3, guia2 §2, master §11 · **Contrato de dados:** `technical_specification.md` §9

Animações são entregues como **timelines JSON sobre rig** (primário) e, quando necessário,
**spritesheets** (secundário, para engines sem skeletal). A referência estética é o tweening do Flash:
poucos desenhos, interpolação bem escolhida, silhueta sempre legível.

---

## 1. Convenções

| Item | Valor |
|---|---|
| FPS de referência | **24 fps** (estética Flash) |
| Reprodução em runtime | 30/60 fps com interpolação — FPS de desenho ≠ FPS de jogo |
| Unidade de tempo | milissegundos, absolutos dentro da animação |
| Loop | obrigatoriamente sem "pop": primeiro e último key idênticos (ou último = primeiro − 1 frame) |
| Espelhamento | toda animação é definida para facing **direita**; esquerda = flip horizontal |
| Interpolação padrão | linear com `ease` por key (`in`, `out`, `inout`) |
| Frames desenhados | 4–12 por loop; 4–8 por ataque (não usar 24 desenhos) |
| Origem | `root` nunca sai do chão, exceto em jump/fall/knockback |
| Personagem no chão | `root.y = 0`; nunca "flutuar" sem motivo declarado |

## 2. Catálogo de animações obrigatórias (personagens jogáveis)

| # | `id` | Duração | Loop | Keys | Eventos | Observações |
|---:|---|---:|---|---:|---|---|
| 1 | `idle` | 2400 ms | ✅ | 5 | `blink` (aleatório), `breathe` | torso achata em Y e expande em X ~2%; braços ±3° |
| 2 | `idle_combat` | 1600 ms | ✅ | 4 | — | guarda, arma erguida, respiração curta |
| 3 | `blink` | 160 ms | ❌ | 3 | — | troca `face_eyes`, nunca redesenha a cabeça |
| 4 | `walk` | 800 ms | ✅ | 8 | `footstep` ×2 | passada curta, tronco +3° |
| 5 | `run` | 600 ms | ✅ | 8 | `footstep` ×2, `dust` | tronco +15°, braços opostos, cabelo/capa com atraso |
| 6 | `jump` | 500 ms | ❌ | 5 | `leave_ground` | antecipação 120 ms, subida 200 ms, apex 80 ms |
| 7 | `fall` | 600 ms | ✅ | 3 | — | loop de queda, capa/cabelo para cima |
| 8 | `land` | 250 ms | ❌ | 4 | `land_impact` | absorção, `root.y` −6 u e retorno |
| 9 | `attack01` | 500 ms | ❌ | 5 | `hit_frame` @ 55% | windup 120 → impacto → recover |
| 10 | `attack02` | 550 ms | ❌ | 5 | `hit_frame` @ 55% | variação de golpe (não reciclar pose 1) |
| 11 | `heavy` | 800 ms | ❌ | 6 | `hit_frame` @ 60%, `camera_shake` | step à frente de 10 u |
| 12 | `ki_cast` | 900 ms | ❌ | 6 | `projectile_spawn` @ 65%, `muzzle_flash` | mão frontal, concentração visível |
| 13 | `ki_charge` | 1200 ms | ✅ | 4 | `charge_tick` @ 200 ms | aura crescente, partículas |
| 14 | `hit` | 300 ms | ❌ | 3 | `flash` | reação curta, sem perder a pose de leitura |
| 15 | `knockback` | 600 ms | ❌ | 4 | `land_impact` | deslocamento em X, `root.y` com arco |
| 16 | `death` | 1200 ms | ❌ | 6 | `death_end` | queda + dissolve/poof (guia2 §2) |
| 17 | `revive` | 1500 ms | ❌ | 6 | `revive_end` | subida + aura |
| 18 | `transform` | 1800 ms | ❌ | 8 | `form_swap` @ 70%, `aura_burst` | troca de peças: cabelo, olhos, sobrancelhas |
| 19 | `emote_wave` | 1600 ms | ❌ | 5 | — | emotes são cosméticos |

Extras por categoria (não obrigatórios em todo personagem): `emote_dance`, `emote_laugh`, `sit`,
`fly` (transformações voadoras), `aura_idle` (transformado).

## 3. Estrutura de combate (obrigatória)

Todo ataque tem **cinco fases** com durações declaradas:

```text
preparação → antecipação → execução → impacto → recuperação
```

| Fase | % do total | Regra |
|---|---:|---|
| Preparação | 10–15% | sair da pose de descanso, sem mudar silhueta de leitura |
| Antecipação | 15–25% | movimento **contra** a direção do golpe (recuo de braço/tronco) |
| Execução | 15–20% | trajetória rápida; 1–2 keys, `ease: in` |
| Impacto | 5–10% | frame de contato **segurável** (2–3 frames), VFX e hitbox ativos |
| Recuperação | 30–40% | retorno com overlapping, nunca "teleporte" para o idle |

Ataques de Ki substituem execução/impacto por: concentração → acúmulo → disparo → recuo → retorno.

## 4. Movimento

### 4.1 Corrida (ciclo de 8 keys, 600 ms)

| Key | t (ms) | Perna frontal | Perna traseira | Braço frontal | Braço traseiro | Tronco |
|---:|---:|---|---|---|---|---|
| 1 | 0 | contato à frente | estendida atrás | atrás | à frente | 15° |
| 2 | 75 | apoio | elevação | atrás | à frente | 14° |
| 3 | 150 | passagem | passagem | neutro | neutro | 13° |
| 4 | 225 | empurra | à frente | à frente | atrás | 14° |
| 5 | 300 | contato atrás | contato à frente | à frente | atrás | 15° |
| 6–8 | 375–525 | espelho de 2–4 | | | | 13–15° |

- `root` oscila em Y entre 0 e −4 u (bounce).
- Cabelo, capa e arma frontal têm atraso de **2 keys** em relação ao corpo (overlapping).
- Arma frontal rotaciona levemente para trás por gravidade (guia1 §3).

### 4.2 Idle

- Respiração: `spine_low` escala 1.02 em X e 0.98 em Y, ciclo de 2400 ms.
- Braços: ±3°; cabeça: ±1,5°; cabelo/capa: ±2° com atraso.
- Piscar: evento aleatório com intervalo de 2,5–5 s (não faz parte do loop de idle).

## 5. Eventos (contrato com a engine)

| `type` | Payload | Consumo |
|---|---|---|
| `hit_frame` | `{ "hitbox": "id", "damage_mult": 1.0 }` | ativa hitbox |
| `projectile_spawn` | `{ "socket": "hand.front", "projectile": "DB_SKILL_…" }` | instancia projétil |
| `muzzle_flash` | `{ "socket": "hand.front", "vfx": "id" }` | VFX filho |
| `footstep` | `{ "foot": "front" \| "back" }` | som/poeira |
| `land_impact` | `{ "power": 0.0–1.0 }` | poeira/shake |
| `camera_shake` | `{ "strength": 0–1, "ms": 200 }` | câmera |
| `flash` | `{ "color": "#ffffff", "ms": 80 }` | flash de dano |
| `form_swap` | `{ "form": "ssj", "assets": [...] }` | troca de peças |
| `sfx` | `{ "id": "step_dirt_01" }` | áudio (sugestão, não produzido) |
| `spawn` | `{ "ref": "asset_id", "offset": [x,y] }` | invocação |
| `death_end` | `{}` | libera o corpo |

Nenhum evento implícito: se a engine precisa saber, está no JSON.

## 6. Hitboxes e hurtboxes

- Coordenadas em **u**, relativas a `root`, `y` para cima positivo **nos eventos** (conversão explícita
  para a convenção y↓ na exportação; o validador checa o sinal).
- Formato: retângulo (`x, y, w, h`) ou cápsula (`x1,y1,x2,y2,r`).
- Toda animação de ataque declara hitbox no `hit_frame` e **hurtbox** no corpo (uma por animação).
- Boss: hitboxes por segmento (cabeça, tronco, cauda) com multiplicadores distintos.

## 7. Requisitos de entrega por animação

| Item | Obrigatório |
|---|---|
| Timeline JSON | ✅ |
| Preview APNG/GIF | ✅ |
| Folha de poses (PNG) | ✅ para animações de combate |
| Duração e loop declarados | ✅ |
| Eventos | ✅ quando aplicável |
| Hitbox/hurtbox | ✅ em combate |
| Notas de implementação (1 parágrafo) | ✅ |

## 8. Consistência (checks automáticos)

- [ ] Nenhum bone fora do ROM da §4 de `anatomy_and_rigging.md` (com 10% de margem).
- [ ] `root` não muda de `x` em animações de loop (exceto run, com retorno exato).
- [ ] Primeiro e último key idênticos em loops.
- [ ] Peças não trocam de escala entre keys (mão não "cresce").
- [ ] Equipamento não some nem troca de forma entre frames.
- [ ] Pivôs não se deslocam (só rotacionam; translação só em `root`/`pelvis`).
- [ ] Nenhuma key a menos de 33 ms de outra (evita tremor a 24 fps).
- [ ] `hit_frame` existe e cai antes de 70% da duração.

## 9. Animações especiais

- **Transformação:** aura sobe, partículas orbitam, cabelo muda, olhos mudam, roupas ajustam.
  O `form_swap` ocorre a 70% — antes disso o personagem é a forma base.
- **Voo (`fly`):** tronco inclinado 20°, pernas para trás, aura contínua; `root.y` livre.
- **Boss gigante:** passos com `camera_shake` automático; idle com peso (nunca "respiração fofa").
- **Pets:** ciclo curto (idle 1200 ms, follow 800 ms), sem ataque complexo.
- **Morte:** nunca remover o asset da cena sem `death_end` (evita corpo "vivo" invisível).
