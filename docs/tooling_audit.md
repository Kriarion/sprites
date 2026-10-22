# AUDITORIA DE CAPACIDADES (PASSO 2 do master prompt)

**Data da auditoria:** 2026-10-22 · **Ambiente:** sandbox Linux, Python 3.11.2, Node 22.22.3
**Método:** verificação executada no shell + inspeção das ferramentas do agente. Nada aqui é suposto.

---

## 1. Resultado da verificação

| Verificação | Comando | Resultado |
|---|---|---|
| Python | `python3 -V` | ✅ `3.11.2` |
| Node | `node -v` | ✅ `v22.22.3` |
| Pillow | `import PIL` | ❌ ausente no sistema → ✅ instalado em venv (`Pillow 13.0.0`) |
| numpy | `import numpy` | ❌ ausente no sistema → ✅ instalado em venv (`2.4.6`) |
| ImageMagick | `which convert` | ✅ `/usr/bin/convert` |
| jq | `which jq` | ✅ `/usr/bin/jq` |
| git / gh | `which git gh` | ✅ ambos, autenticados |
| Fontes de sistema | `fc-list \| wc -l` | ⚠️ **0 fontes** — qualquer texto renderizado por script exigirá fonte própria ou será evitado |
| Godot / Unity / navegador | — | ❌ não disponíveis |

Reprodução do ambiente Python (o venv **não** é versionado):

```bash
python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
```

---

## 2. Matriz de capacidades × necessidades do projeto

| Necessidade (master §29) | Situação | Ferramenta / método | Limitação real | Impacto no plano |
|---|---|---|---|---|
| Gerar imagens | ✅ | `generate_image` | **1 imagem por chamada**; chamadas são o teto de 10/sessão; sem alpha nativo | Cada chamada deve render um **lote em grade** com muitas peças |
| Editar/estender imagem | ✅ | `generate_image` com `images=[...]` | Edição pode alterar geometria/estilo do resto | Usar só para correção localizada; nunca para "consertar" montagem |
| Escolha entre variações | ✅ mas **proibido em produção** | `offer_options` | **Pausa a sessão** esperando escolha humana e move as não escolhidas para `Unselected files` | **Nunca usar em sessão de produção** — quebraria o orçamento e a autonomia |
| Remover fundo | ⚠️ parcial | Keying por cor (magenta/verde) com Pillow/numpy | Não há remoção semântica ("remove background"); requer fundo uniforme e despill | Prompt deve exigir fundo chapado de contraste; pipeline de despill obrigatório |
| Alpha verdadeiro | ✅ (pós-processo) | Pillow (`RGBA`, `putalpha`, threshold) | Alpha vem do keying, não do gerador | Gate G2 exige inspeção de borda e teste automático de alpha |
| Recorte e split de peças | ✅ | Pillow + numpy (grade + bbox + componentes conexos) | Peças que se tocam na geração fundem na segmentação | Template obriga espaçamento; ADR-0001 trata o caso |
| Redimensionar/normalizar | ✅ | Pillow (LANCZOS) | Redução repetida degrada linha | Sempre reduzir do master para 1x/2x, nunca ampliar |
| Spritesheet / atlas | ✅ | Script próprio (`tools/atlas.py`) | Algoritmo de packing precisa ser escrito | Incluído na W1 |
| Preview animado | ✅ parcial | Pillow (APNG/GIF) + folha de poses | Sem player de engine; preview é aproximação | Preview é evidência, não prova de runtime |
| Validação automática | ✅ | Python (JSON Schema manual, PIL, `jq`) | Schemas sem validador oficial de terceiros → validação implementada à mão | `tools/validate.py` é entregável da W1 |
| Vetorização / edição vetorial | ❌ | — | Sem Inkscape/Illustrator; rasterização não reversível | Vetor sai do escopo: entrega **raster em resolução-mestre** |
| Rigging esqueletal (software) | ❌ | — | Sem Spine/DragonBones/Animate | Rig é **dado JSON** (bones, limites, âncoras) consumível por qualquer engine; preview por composição |
| Criação de `.psd`/`.fla` master | ❌ | — | Formatos proprietários não geráveis | Master = PNG em 4x + JSON. Documentado como decisão (ADR-0003) |
| Referências visuais externas | ⚠️ | `web_search`, `image_search`, `fetch_page` | Acesso de rede restrito (github/npm/pypi); **imagens de terceiros não podem ser commitadas** | Referência é **descritiva** (texto) ou **original** (gerada pelo projeto); nunca arquivo copiado |
| Inspeção visual dos resultados | ✅ | `read_file` em PNG/JPG | Inspeção é do agente (julgamento), não de um orquestrador humano | Dupla checagem via overlay de proporção e composição de teste |
| Continuidade entre sessões | ✅ | Repositório + `continuity_state.json` | "Sessão" é unidade lógica; não há contador global de gerações imposto pela plataforma | Ledger é a fonte de verdade e deve ser conciliado à mão/script |
| Rodar engine para validar | ❌ | — | Sem Godot/Unity/navegador | Validação de integração é **de dados** + implementação de referência em pseudocódigo/Python |

---

## 3. Consequências estruturais (o que o plano assume por causa da auditoria)

1. **Geração em grade é obrigatória.** Com 1 imagem por chamada e teto de 10, gerar "uma peça por imagem"
   inviabiliza o projeto (21 peças > orçamento de uma sessão). Ver `ADR-0001`.
2. **Keying + despill são infraestrutura crítica**, não detalhe. Sem isso, nenhum asset passa no gate G2.
3. **Não existe atalho de vetor.** A qualidade vem de resolução-mestre alta (2x–4x) reduzida com LANCZOS,
   não de reescalar vetor.
4. **Rig é dado.** Isso é uma vantagem: nada depende de software pago e o pacote fica engine-agnostic de fato.
5. **`offer_options` está vetado em produção.** Pausa humana + realocação de arquivos = sessão inválida.
6. **Não há fontes no sistema.** Todo texto de UI será entregue como componente sem texto; se precisar
   render texto em preview, embutir fonte própria em `references/fonts/` (a criar) ou desenhar à mão.
7. **Nenhum calendário prometido.** Sessões são contadas, não datadas (ver `roadmap.md` §8).

## 4. Riscos técnicos derivados

| Risco | Evidência | Mitigação |
|---|---|---|
| Peças vizinhas se fundem no keying | Segmentação por cor de fundo é sensível a sombra/contato | Grade com gutter de ≥16 px e exigência explícita de "partes que não se tocam" no prompt |
| Halo/serrilhado nas bordas | Anti-aliasing do gerador contra fundo magenta | Despill (reduzir magenta próximo à borda), erode 1 px, matte de 1 px |
| Gerador ignora a grade | Modelos não obedecem layout rígido com precisão | Validar cell-fit; se a taxa de acerto ficar baixa, cair para plan B (ADR-0001 §6) |
| Redução degrada linha preta fina | Downscale 4x→1x | Reduzir de 2x→1x (fator 2) e testar contorno; manter espessura mínima de 1 px em 1x |
| Estouro silencioso de orçamento | Não há contador da plataforma | Ledger antes de cada chamada; parada dura em 10 por sessão |

## 5. Ferramentas a construir (W1)

| Ferramenta | Função | Critério de aceite |
|---|---|---|
| `tools/requirements.txt` | Dependências reprodutíveis | `pip install -r` funciona em ambiente limpo |
| `tools/key.py` | Keying por cor + despill + erode + trim | Gera PNG RGBA sem resíduo de fundo em amostra de teste |
| `tools/decompose.py` | Split por grade → peças + bbox + pivô por template | 12 peças de uma grade 3×4 em arquivos separados |
| `tools/compose.py` | Montagem por rig/âncora (preview) | Compõe personagem e escreve PNG + relatório de encaixe |
| `tools/validate.py` | Valida metadados, alpha, dimensões, IDs, referências | Falha com código ≠0 em asset inválido |
| `tools/atlas.py` | Empacota atlas potência de 2 + JSON de coordenadas | Atlas 1024/2048 sem bleeding |
| `tools/build_manifest.py` | Regenera `asset_manifest.json` a partir do registry | Determinístico, com hash |

Detalhes de contrato em `tools/README.md`. Nenhuma dessas ferramentas existe ainda: **serão construídas e
testadas na W1**, e até lá nenhum asset pode ser `APPROVED` (o gate G2 depende delas).
