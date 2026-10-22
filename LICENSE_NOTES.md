# LICENSE_NOTES — Direitos, uso e limitações

Este documento **não é uma licença de software**. É um registro de situação jurídica e de política de uso,
exigido pelo Master Prompt (§27). Nenhuma declaração aqui deve ser lida como autorização, cessão ou
licenciamento por parte dos titulares de direitos.

## 1. Dragon Ball

- **Dragon Ball**, seus personagens, nomes, designs, transformações, técnicas, símbolos, lokações e
  logotipos pertencem aos respectivos titulares (Akira Toriyama / Bird Studio, Shueisha, Toei Animation,
  Bandai Namco e licenciados, conforme território).
- Este projeto utiliza **referências a personagens e elementos protegidos**, conforme solicitado
  explicitamente no Master Prompt. Personagens canônicos são reconstruídos por fidelidade a designs
  oficiais e **não são de autoria original deste projeto**.
- O pacote **não é** um produto oficial, autorizado, endossado ou afiliado à franquia.
- **Distribuição pública, publicação em loja, monetização, uso em produtos comerciais** ou envio a
  plataformas de terceiros **podem exigir autorização formal** dos titulares. A responsabilidade pelo uso
  é de quem distribui.
- Uso pretendido e defensável: estudo, protótipo interno, portfólio técnico, pipeline de produção,
  demonstração de ferramentas e pesquisa. Uso comercial requer avaliação jurídica própria.

## 2. AdventureQuest Worlds (AQW)

- A referência a AQW limita-se a **linguagem visual, modularidade e conceitos gerais de apresentação**
  (paper-doll, cel-shading, camadas parallax, HUD de MMO 2D).
- **Não** se copiam, extraem, vetorizam, traçam, redistribuem ou recriam assets oficiais de AQW
  (sprites, SWFs, interfaces, ícones, mapas, música). Nenhum arquivo de AQW entra neste repositório.
- AQW e seus assets pertencem a Artix Entertainment. Nada aqui implica afiliação ou aval.

## 3. Conteúdo original deste projeto

- A documentação, os padrões, os JSONs, os scripts de pipeline e os metadados produzidos aqui são de
  autoria do projeto e podem ser reutilizados como metodologia.
- Desenhos originais criados para o pacote (equipamentos, criaturas, props, variações de UI) são obra
  derivada do universo Dragon Ball quando representam elementos protegidos — a mesma restrição da §1 se
  aplica.
- Não será adicionada nenhuma "licença oficial" fictícia a este repositório.

## 4. Política de proveniência (obrigatória)

Todo asset deve registrar, nos metadados:

| Campo | Conteúdo |
|---|---|
| `ownership` | `canonical_ip` (personagem/elemento da franquia) · `original_design` (criação do projeto) · `pipeline_artifact` (máscara, atlas, preview) |
| `canonical_reference` | Descrição da referência canônica usada (saga/continuidade/forma), sem link para material pirata |
| `aqw_reference` | Se houve inspiração estrutural em AQW e em quê (ex.: "ordem de camadas paper-doll") |
| `restrictions` | Ex.: `non_commercial_study_only`, `no_redistribution` |

Assets sem esses campos **não podem** ser promovidos a `APPROVED`.

## 5. Ferramentas e dependências

- Geração de imagens por modelos de terceiros; os termos da plataforma de geração se aplicam às saídas.
- Pillow / numpy (BSD) e ImageMagick (ImageMagick License) usados apenas como processamento local.
- Nenhuma dependência de runtime proprietária é exigida pelos entregáveis (ver `docs/integration_guide.md`).

## 6. Símbolos sensíveis

Evitar, em qualquer asset, reprodução de símbolos reais de organizações políticas ou religiosas,
mesmo quando presentes em adaptações não canônicas. Substituir por desenho equivalente fictício e
registrar a decisão.
