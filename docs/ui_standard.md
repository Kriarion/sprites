# PADRÃO DE UI E HUD (normativo)

**Versão:** 1.0.0 · **Base:** guia1 §8, guia2 §7, master §16

UI de MMO 2D utilitária com estética Dragon Ball: **moldura escura + ouro velho + detalhe tecnológico**
(scouter, circuitos, cápsulas). Legibilidade acima de ornamento. Nenhum texto embutido.

---

## 1. Resolução e grade

| Item | Valor |
|---|---|
| Resolução de design | 1280 × 720 |
| Escalas de UI | 1× (1280×720), 2× (2560×1440), 0,75× (960×540) |
| Unidade de grade | 8 px |
| Margem de tela | 24 px |
| Altura do slot de skill | 64 px (1×) |
| Tamanho de ícone de skill | 64 px (1×) · 128 fonte |
| Barra de HP/Ki | altura 18 px, largura 220 px (jogador) |
| Alvo de clique mínimo | 40 × 40 px |
| Fonte (quando renderizada) | sem serifa, condensada, com contorno 1 px escuro |

## 2. Layout canônico do HUD

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ┌──────────────┐                              ┌──────────────────┐   │
│ │ RETRATO   Nv │                              │  RETRATO ALVO    │   │
│ │ Nome          │                              │  Nome / HP       │   │
│ │ HP ████████   │                              │  ████████████    │   │
│ │ Ki ██████     │                              └──────────────────┘   │
│ │ XP ██   Classe│                                                     │
│ └──────────────┘                                                     │
│                                                                       │
│                        (área de jogo)                                 │
│                                                                       │
│        ┌──────────────────────────────────────────────┐               │
│        │ [1][2][3][4][5]   chat / log                 │               │
│        └──────────────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
```

- **Canto superior esquerdo:** retrato circular, nome, classe/rank, nível, HP (vermelho), Ki (azul),
  XP (roxo) e progressão de classe (verde) — cores herdadas da convenção AQW (guia2 §7).
- **Canto superior direito:** alvo (retrato, nome, HP, ícone de tipo).
- **Centro-inferior:** 5 slots de habilidade + barra de recurso + log de chat recolhível.
- **Canto inferior direito:** botões (inventário, equipamento, skills, quests, loja, opções).
- Layout é **dado** (`hud.json`), não estático: a engine reposiciona por âncora.

## 3. Componentes obrigatórios

| Grupo | Componentes |
|---|---|
| HUD | frame de jogador, retrato, barras HP/Ki/XP/classe, nível, nome, status icons, frame de alvo |
| Action bar | 5 slots, moldura, tecla, cooldown radial, estado vazio, indicador de transformação |
| Inventário | painel, grade de slots, abas, botão de ordenar, scrollbar, tooltip |
| Equipamento | boneco paper-doll com 17 slots, botão desequipar, comparador |
| Skills | lista, árvore/rank, detalhe de skill, botão aprender |
| Quests | lista, detalhe, recompensa, indicador "!" e "?" |
| Loja | lista, preço, moedas (Zeni/AC), botão comprar/vender |
| Crafting | receita, ingredientes, resultado, progresso |
| Chat | input, log, canais (cores), emotes |
| Diálogos | balão de NPC, colunas de opções (Quest/Shop/Talk), retrato |
| Personagem | criação (raça, face, cabelo, cor), seleção, confirmação |
| Sistema | modal de confirmação, notificação/toast, loading, tooltip, cursor |

## 4. Estados (obrigatórios por componente interativo)

`normal` · `hover` · `pressed` · `selected` · `disabled` · `cooldown` · `locked` · `notification`

- Todo botão entrega **8 estados** ou declara explicitamente quais não se aplicam.
- Cooldown é **overlay radial** (máscara), não uma imagem por frame.
- `disabled` nunca é só "mais escuro": reduzir saturação e adicionar padrão de hachura sutil.

## 5. 9-slice

- Todo painel/moldura escalável é entregue com `slice_margins` em px (top, right, bottom, left).
- Fonte mínima do 9-slice: **512 px** de lado (para reduzir com qualidade).
- Cantos ornamentados: margem ≥ 48 px em 1× para não esticar ornamento.
- Nenhum painel entregue em tamanho único quando deve ser redimensionável.
- Bordas: 2 px de contorno escuro + 1 px de ouro interno (padrão visual do kit).

## 6. Paleta de UI

| Uso | Cor |
|---|---|
| Fundo de painel | `#14121A` a 88% |
| Borda externa | `#0B0A0F` |
| Ouro velho (trim) | `#C9A227` |
| Ouro claro (highlight) | `#F1DC8A` |
| Pedra/mármore escuro | `#2A2733` |
| HP | `#D92B2B` (base) / `#7A1010` (fundo) |
| Ki | `#2E7BFF` / `#12285C` |
| XP | `#8A4BFF` / `#2C1653` |
| Classe | `#37C46B` / `#123A23` |
| Texto | `#F2EFE6` · texto secundário `#B9B2A4` |
| Alerta | `#FF5A3C` |

## 7. Ícones

- Base **128 px**, entrega em 128 e 64 (e 256 para loja/quando justificar).
- Enquadramento: objeto centralizado, ocupando 70–80% da área, margem interna de 12 px (em 128).
- Fundo transparente; moldura entregue **separada** (para reuso por raridade).
- Contorno 3 px em 128 (proporcional à regra de 2 px @1x de personagem).
- 1 ideia por ícone; sem texto; legível em 64 px e em 32 px (teste).
- Variações de estado entregues como overlay, não como ícone novo.

## 8. Localização e dados dinâmicos

- **Nenhum texto permanente embutido em imagem** (master §16.4). Nome, número, preço, descrição e tempo
  são renderizados pela engine.
- Números em fonte tabular (largura fixa) para não "tremer" durante atualização.
- Componentes que exibem valores entregues com área segura declarada (`safe_text_area`).

## 9. Entrega

```text
ui/hud/
├── DB_UI_HUD_PLAYER_FRAME.asset.json
├── player_frame_512.png
├── portrait_mask_circle.png
├── bar_hp_fill.png  bar_hp_bg.png  bar_ki_fill.png  bar_ki_bg.png
├── states/{normal.png, hover.png, ...}
├── slice_margins.json
└── preview_composed.png
```

- `preview_composed.png` mostra o HUD sobre um mapa real do pacote (evidência do gate G3).
- Atlas de UI: 2048², com padding 2 px e `slice_margins` no JSON.

## 10. Checklist de aprovação

- [ ] Escalas 1×/2×/0,75× testadas (nada quebra, nada fica ilegível).
- [ ] Todos os estados presentes ou justificados.
- [ ] 9-slice com margens declaradas e ornamento preservado.
- [ ] Nenhum texto embutido.
- [ ] Contraste de texto ≥ 4,5:1 sobre o painel.
- [ ] Ícones legíveis em 64 e 32 px.
- [ ] HUD não cobre a área jogável central (banda y 440–700 na horizontal central).
- [ ] Paleta de UI respeitada.
- [ ] Componentes com atlas e metadados.
- [ ] `preview_composed.png` anexado.
