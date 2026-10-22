# VISUAL BIBLE — Guia de Estilo (normativo)

**Versão:** 1.2.0 — **proporção estabilizada em 5,9 cabeças** (ADR-0007)
**Status:** `VIGENTE` (estilo validado em imagem; proporção decidida e mensurável; coerência auditada por `tools/coherence.py`)
**Base:** `asset_guide1.md` §1, `asset_guide2.md` §1 e §10, `master-prompt.md` §6,
evidência em `docs/calibration_report.md`

> Este documento é a **lei visual** do projeto. Nenhum asset entra em produção sem poder ser descrito por
> estas regras. Toda exceção exige ADR.
> Enquanto a versão for `1.0.0`, os números aqui são **alvos a validar**; a `1.1.0` incorporará o que as
> imagens reais confirmarem ou corrigirem.

---

## 1. Identidade visual em uma frase

**Cartoon de fantasia heroico, vetorial na alma e raster na entrega:** contorno preto forte e limpo,
preenchimento chapado, cel-shading de blocos duros, luz consistentemente de cima-frente, silhueta
exagerada e legível, proporção heroica estilizada com cabeça e mãos expressivas.

Não é anime detalhado, não é pixel art, não é pintura, não é 3D renderizado.

## 2. Cinco regras que não se negociam

1. **Contorno externo sempre presente e escuro** nos personagens, equipamentos e ícones. Cenários de fundo
   são a exceção (contorno sutil ou ausente).
2. **Uma fonte de luz para todo o pacote:** cima, à frente e à esquerda do observador. Sem exceções por asset.
3. **Sombreamento em blocos**, nunca gradiente suave — exceto energia/magia (aura, feixe, fogo), que pode
   usar gradiente e blending.
4. **Paleta limitada por design:** 5–8 cores principais, 1 base por material, 1–2 sombras chapadas,
   1–3 destaques.
5. **Legibilidade primeiro:** se ao reduzir para 1x o asset vira mancha, o design está errado.

## 3. Contorno (lineart)

### 3.1 Espessura canônica

A espessura é **proporcional à altura do corpo (200 u)**, não ao tamanho da imagem:

| Tipo de linha | 1x (200 u) | 2x (400 u) | 4x (800 u) | Uso |
|---|---|---|---|---|
| Contorno externo | `2.0 px` (min 1.5) | 4.0 px | 8.0 px | Silhueta de personagem, arma, ícone |
| Linha interna estrutural | `1.2 px` | 2.4 px | 4.8 px | Separação de placas de armadura, dobras grandes |
| Detalhe / textura | `0.8 px` (min 1) | 1.6 px | 3.2 px | Costuras, runas, escamas, vincos pequenos |
| Cenário interativo (prop) | `1.0–1.5 px` | 2–3 px | 4–6 px | Props em primeiro plano |
| Cenário de fundo | `0–1.0 px` | 0–2 px | 0–4 px | Fundo/midground (contorno sutil ou nenhum) |

Regra prática: **contorno externo ≈ 1% da altura do corpo**. Nunca inferior a 1 px em 1x (senão some).

### 3.2 Cor do contorno

- Personagem/equipamento: `#100D14` (preto levemente violeta), **não** preto puro `#000000`, para não
  "furar" a leitura em telas escuras.
- Nunca colorir o contorno externo com a cor local do objeto (isso descaracteriza o estilo Flash).
- Linhas internas podem ser uma versão escurecida da cor local (mistura 60–75% com o contorno).

### 3.3 Qualidade

- Curvas limpas, sem tremor; nenhum "cabelo" de linha solta.
- Linhas que terminam em junta devem terminar **sob** a peça vizinha, não no ar.
- Nenhum contorno borrado ou semi-transparente (exceto VFX).

## 4. Pintura e sombreamento (cel-shading)

### 4.1 Os três tons (obrigatório por material)

| Camada | Regra | Implementação |
|---|---|---|
| **1. Cor base** | Cor sólida e plana | 100% opacidade, sem textura |
| **2. Sombra dura** | Recorte seco, borda definida | Preto a **22–30%** em Multiply **ou** base escurecida 35–45% |
| **3. Brilho duro** | Recorte nítido nas faces voltadas à luz | Branco a **40–55%** em Screen **ou** base clareada 25–35% |
| (opcional) **Sombra profunda** | Oclusão em dobras internas e sob peças sobrepostas | Preto a **40–50%** |
| (opcional) **Rim light** | Só em metal, energia, bosses | Branco 60–80%, 1–2 px no lado da luz |

**Proibido como padrão:** gradiente radial/linear de preenchimento, brush com opacidade, textura
fotográfica, "blur" de sombra, Ambient Occlusion pintada suave.

### 4.2 Half-shadow (assinatura AQW)

Membros **traseiros** (braço/perna de trás, cabelo de trás, arma traseira) recebem uma versão
escurecida e dessaturada da sua cor — tipicamente **base × 0.55 + dessaturar 15%**, chegando a silhueta
quase preta em peças muito traseiras. Benefícios: profundidade imediata, leitura de "lado" e economia de
detalhe (herança da otimização Flash).

Regra: membro traseiro **nunca** tem brilho próprio; membro frontal concentra os detalhes.

### 4.3 Luz canônica

```text
                 LUZ (elevação ~55°, azimute ~30° à esquerda do observador)
                        ↘
        ┌───────────────────────────────┐
        │  · face superior/claridade    │
        │  · sombra cai para baixo/dir. │
        │  · brilho na borda de cima    │
        └───────────────────────────────┘
                    PERSONAGEM (3/4, olhando à direita)
```

- Direção fixa: **cima + frente + esquerda do observador**.
- Sombra projetada no chão: elipse, preto 25–35%, sem blur pesado.
- Em cenas noturnas ou de energia, a **cor** da luz pode mudar (azul, roxo, laranja), a **direção não**.

### 4.4 Materiais

| Material | Base | Sombra | Brilho | Detalhe obrigatório |
|---|---|---|---|---|
| Metal polido | cinza-azulado médio | borda dura 45% | faixa branca alongada + rim light | rebites/trims de ouro |
| Metal escuro/ferro | grafite | preto 40% | brilho estreito e curto | arranhões em 0.8 px |
| Couro | marrom/mosto | 35%, forma arredondada | brilho pequeno e alto contraste | costura 0.8 px |
| Tecido (gi) | cor viva plana | dobras em "V" largos, 2 blocos | ausente ou 1 bloco suave | barra reforçada, costura |
| Pele | tom canônico | 1 bloco em baixo/atrás | 1 bloco pequeno testa/nariz/ombro | sombra de pálpebra |
| Cabelo | cor canônica | 1 bloco por mecha | 1 faixa por mecha, no topo | mechas com ponta afiada |
| Energia/Ki | cor saturada | núcleo claro, borda escura | branco no núcleo + glow aditivo | anel de choque, partículas |
| Pedra/rocha | cinza terroso | 2 blocos angulares | quase nenhum | lascas, faces planas |
| Madeira | ocre | bloco de veio | risco claro | veio em 1–2 linhas |
| Ouro (trims, Dragon Ball) | amarelo quente | 40% + marrom | brilho branco curto e forte | 4–6 estrelas (Esferas) |

## 5. Proporção e anatomia estilizada

### 5.1 Cânone de proporção (humanoide adulto)

Referência completa e medidas em `docs/technical_specification.md` §2.

> **DECISÃO 1.2.0 (ADR-0007):** a proporção canônica do pacote é **5,9 cabeças** — a faixa em que o gerador
> é estável e reproduzível. Adjetivos **não controlam** proporção ("heroic 5.5-head" → 7,5; "exactly 6 heads"
> → 4,1); só **percentual explícito** funciona ("head = 17%" → 5,88). Portanto: **todo prompt de corpo declara
> percentuais medidos**, e toda ficha é verificada por `tools/measure.py` antes do gate G1. Tolerância **±5%**
> (5,60–6,20 cabeças).
> Estabilidade > ambição: um pacote coerente em 5,9 conversa entre si; um pacote em 5,5 com metade das peças
> corrigidas não conversa com nada.

Percentuais obrigatórios no prompt (base = altura total do corpo):

| Segmento | Percentual | Equivalente em u (200 u) |
|---|---:|---:|
| Cabeça (queixo → topo) | **17,0%** | 34 u |
| Topo do ombro | 78,0% | 156 u |
| Cintura | 60,0% | 120 u |
| Quadril | 50,0% | 100 u |
| Joelho | 28,0% | 56 u |
| Tornozelo | 7,0% | 14 u |
| Largura dos ombros | 28,0% | 56 u |
| Largura da cabeça | 15,0% | 30 u |

Resumo do cânone:

- Altura total **200 u**; cabeça **34 u** → **5,9 cabeças** (heroico estilizado, não realista 7,5).
- Cabeça **maior** que o real: destaca cabelo, capacete e expressão (exigência do guia 1).
- Ombros **56 u** de largura; mãos **18 u**; pés **26 u** de comprimento (grandes e estáveis).
- Tronco atlético em "V" suave; cintura 34 u; quadril 40 u.
- Braço: ombro→cotovelo 32 u, cotovelo→punho 30 u. Perna: quadril→joelho 44 u, joelho→tornozelo 42 u.
- Membros **levemente alongados** em personagens musculosos (Vegeta, Piccolo): +6% em braço/perna,
  mantendo cabeça e mãos (senão a leitura muda).

### 5.2 Variações por arquétipo

| Arquétipo | Altura | Cabeça | Cintura | Observação |
|---|---|---|---|---|
| Masculino padrão | 200 u | 36 u | 34 u | base do projeto |
| Feminino padrão | 192 u | 35 u | 30 u (quadril 42) | quadril mais largo, ombros 48 u |
| Musculoso | 210 u | 36 u | 32 u | ombros 68 u, braço mais grosso |
| Infantil | 128 u | 40 u | 30 u | 3,2 cabeças, mãos/pés proporcionalmente maiores |
| Namekuseijin | 205 u | 34 u | 30 u | pescoço, antenas, orelhas pontudas |
| Majin | 190–230 u | variável | — | silhueta elástica, membros finos |
| Raça de Freeza | 165–200 u | 34 u | 28 u | crânio alongado, cauda |
| Criatura pequena | 40–70 u | — | — | 25–33% do padrão |
| Boss gigante | 400–900 u | — | — | rig e escala próprios |

### 5.3 Rosto (padrão do projeto)

- Olhos grandes, expressivos, com **íris saturada + 1 brilho**; pálpebra superior com contorno 1.2 px.
- Sobrancelhas espessas (leitura de emoção a 1x); nos Saiyajins, sobrancelhas mudam por transformação.
- Nariz: 2–3 traços (nunca modelado); boca: linha + bloco de sombra interna quando aberta.
- Piscar é **troca de olhos** (peça `face_eyes`), nunca redesenho da cabeça.

## 6. Paleta

- Fonte para dados: `references/palettes/core_palettes.json` (paletas canônicas iniciais).
- Regras: 5–8 cores principais por design; nenhuma cor fora da paleta do personagem sem justificativa;
  cores de energia sempre **mais saturadas** que a roupa, para destacar VFX.
- Fundos distantes: menos contraste/saturação; primeiro plano: mais contraste.
- Recolorir é permitido só por **máscara nomeada** (skin, hair, eyes, cloth, metal, energy) e nunca em
  personagem canônico de forma que descaracterize (`master §7.5`).

## 7. Silhueta e legibilidade

- Teste obrigatório: o asset deve ser identificável em **1x reduzido a 25%** e em **silhueta preta**.
- Bosses: silhueta única com "gancho" (chifres, cauda, asas, forma de cabeça) — nunca um humanoide maior.
- Armas: silhueta exagerada, ≥60% da altura do corpo em armas de duas mãos.
- Ícones: leitura em 64×64; 1 ideia por ícone.

## 8. Cenários, UI e VFX nesta bíblia

- **Cenários:** sem contorno grosso; atmosfera por camada (fundo frio/claro, frente quente/escura);
  detalhes só onde o jogador pisa ou interage. Detalhes: `environments_standard.md`.
- **UI:** molduras escuras com contorno definido, ouro velho e detalhes tecnológicos de Dragon Ball
  (scouters, linhas de circuito, cápsulas). Legibilidade acima de ornamento. Detalhes: `ui_standard.md`.
- **VFX:** formas puras geométricas + glow aditivo, saturadas, com núcleo branco sempre. Detalhes: `vfx_standard.md`.

## 9. Controle de drift (consistência entre sessões)

Toda sessão que produzir personagem/equipamento deve incluir, no processamento:

1. **Overlay de proporção:** silhueta do rig 200 u sobreposta ao resultado; desvio máximo **±5%** na altura,
   **±4 u** em ombro/quadril/punho/joelho.
2. **Amostra de cor:** 5 pontos (pele, cabelo, tecido, metal, energia) comparados com a paleta
   (`ΔH ≤ 8°`, `ΔS ≤ 10%`, `ΔV ≤ 10%`).
3. **Medição de contorno:** espessura externa de 3 amostras; tolerância `±0.25 px` em 1x.
4. **Referência viva:** as pranchas aprovadas em `references/visual_bible/` são **anexadas como referência**
   nas gerações seguintes (quando a ferramenta permitir `images=[...]`).

Falha em qualquer item → `REWORK_REQUIRED`, nunca "aceito por enquanto".

## 10. Estrutura obrigatória de prompt (scaffolding)

Todo prompt de geração usa os **quatro blocos** abaixo, na ordem. Sem eles, o resultado não é avaliável.

```text
[BLOCO 1 — ESTILO]
2D Flash-browser-game cartoon fantasy sprite, vector-like clean shapes,
bold uniform near-black outer contours, flat solid fills, hard-edged cel shading
with exactly one shadow block and one highlight block per material,
light from above and slightly in front-left, limited palette (5-8 colors),
heroic stylized proportions, no gradients except energy, no texture, no 3D render.

[BLOCO 2 — CONTEÚDO]
<personagem/elemento canônico + forma/transformação + pose + figurino>

[BLOCO 3 — LAYOUT E ENTREGA]
<grade explícita: colunas × linhas, gutter, célula; cada peça centralizada na célula,
não encostando em vizinhas; partes nomeadas na ordem; uniform solid
#FF00FF magenta background; nothing else in frame; no text, no watermark, no grid lines>

[BLOCO 4 — NEGATIVOS]
no background scenery, no shadows on the ground, no merged limbs, no extra limbs,
no pseudo-transparency checkerboard, no blur, no photo texture, no logo, no signature,
no perspective distortion, no cropped parts, no overlapping silhouettes.
```

Modelos de prompt por categoria (personagem/arma/cenário) estão em `asset_guide1.md` §"Instruções de
Prompting"; aqui eles foram adaptados para **grade determinística** (ADR-0001) e **fundo keyable**.

## 11. Do / Don't

| ✅ Faça | ❌ Não faça |
|---|---|
| Contorno 2 px a 1x, constante | Contorno "orgânico" variável por humor |
| 1 sombra + 1 brilho por material | Gradiente para "dar volume" |
| Cabeça 5,9× no corpo | Proporção realista 7,5+ cabeças |
| Membro traseiro escurecido | Braço de trás com brilho próprio |
| Arma 60–120% da altura | Arma "realista" pequena |
| Ícone com 1 ideia, 64 px legível | Ícone com 8 detalhes e texto |
| Peça isolada, centralizada, com gutter | Peças encostadas/se tocando na grade |
| Fundo magenta chapado | Fundo branco, cenário, ou xadrez falso |
| Reuso de rig aprovado | Novo rig por personagem sem necessidade anatômica |
| Silhueta testada em preto | Detalhe que só existe em close |

## 11.1. O que a calibração de 2026-10-22 confirmou

| Regra | Status | Evidência |
|---|---|---|
| Contorno escuro uniforme e grosso | ✅ confirmado | 4 pranchas aprovadas (dummy, materiais, armas, cabeças) |
| Cel-shading de 1 sombra + 1 brilho por material | ✅ confirmado | `DB_REF_MATERIALS_V1` (8 objetos, 4 materiais) |
| Half-shadow em membro traseiro | ✅ confirmado | `DB_REF_MATERIALS_V1` (coluna direita propositalmente escurecida) |
| Luz de cima-frente-esquerda | ✅ confirmado | todas as pranchas, sem exceção |
| Paleta limitada (5–8 cores/design) | ✅ confirmado | armas e cabeças dentro da paleta |
| Silhueta legível / armas oversized | ✅ confirmado | arma de 2 mãos > 100% da altura do corpo |
| Fundo magenta keyable | ✅ confirmado | halo 0,0% em 5 de 6 folhas |
| **Proporção 5,5 cabeças por adjetivo** | ❌ **refutado** | ver §5.1 — usar percentual explícito |
| **Proporção 5,9 cabeças por percentual** | ✅ **adotado** (ADR-0007) | "head = 17%" → 5,88 medido |
| **Peças simétricas saírem singulares** | ❌ **refutado** | o gerador desenha pares L/R; ver `ADR-0006` |

Regras refutadas não foram removidas: foram **substituídas por controle numérico** (proporção) e por
**aceitação explícita do par espelhado** (`mirrored_pair`).

## 12. Critério de aprovação visual (gate G1)

Um asset passa no G1 somente se **todos** forem verdadeiros:

- [ ] Estilo identificável como "cartoon Flash" e coerente com as pranchas aprovadas.
- [ ] Fonte de luz idêntica à canônica.
- [ ] Contorno com espessura da tabela §3.1.
- [ ] Paleta dentro da paleta do personagem/elemento.
- [ ] Proporção dentro da tolerância §9.
- [ ] Silhueta legível em 25% e em preto.
- [ ] Identidade canônica reconhecível (personagem/forma corretos).
- [ ] Zero artefato: sem membro extra, sem fusão, sem dedo a mais, sem texto.

Reprovação é registrada com o motivo exato (`production/qa_reports/`), não com "ficou estranho".

## 13. Coerência entre assets — a regra que faz o pacote "conversar"

Um asset bonito isolado é inútil se não encaixa. Ficam instituídos seis invariantes medidos
(`docs/coherence_standard.md`), auditados por `tools/coherence.py` em **toda** sessão:

| # | Invariante | Tolerância |
|---|---|---|
| C1 | Escala em u | 200 u ±5%, `pixels_per_unit` ∈ {1,2,4} |
| C2 | Proporção 5,9 cabeças | ±5% na razão, ±4 u nas articulações |
| C3 | Peso de contorno | 0,9–1,3% da altura |
| C4 | Paleta | ΔH ≤ 8°, ΔS ≤ 10°, ΔV ≤ 10% |
| C5 | Half-shadow | traseira ≤ 80% da luminância da frontal |
| C6 | Estrutura (âncora/camada/pivô) | 100% |

**Nenhum asset é `APPROVED` com invariante fora de tolerância.** Se um invariante falha em todos os
assets, o padrão está errado — e revisa-se o padrão por ADR, não o asset por conveniência.
