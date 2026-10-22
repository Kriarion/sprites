# PLANEJAMENTO DO PROJETO

**Projeto:** Dragon Ball — AQW-Style Complete Asset Pack
**Versão do plano:** 1.0.0 · **Data:** 2026-10-22 · **Fase:** 0 (Auditoria e Planejamento)
**Autoridade:** `docs/master-prompt.md` + `docs/asset_guide1.md` + `docs/asset_guide2.md`

---

## 1. Visão

Construir, de forma incremental e verificável, uma **biblioteca profissional de assets 2D** que permita a
um desenvolvedor montar um MMORPG 2D de apresentação lateral — personagens customizáveis, combate em
tempo real com técnicas de Ki, mundos em camadas, HUD completo — **sem redesenhar nada**.

O diferencial não é a imagem bonita: é a **completude técnica**. Um Goku com 21 peças, rig, pivôs, idle e
kamehameha separada em componentes vale mais que 50 ilustrações de Goku que não podem ser animadas.

## 2. Objetivos

| # | Objetivo | Métrica de sucesso |
|---|---|---|
| O1 | Padrão visual único e reproduzível | Visual Bible validada em imagem; 3 verificações de drift com desvio aceitável |
| O2 | Paper-doll funcional | 1 personagem montado a partir de peças independentes, animado, em engine 2D |
| O3 | Reutilização real | ≥60% dos personagens da fase 4 montados sobre rigs já aprovados |
| O4 | Equipamentos intercambiáveis | Trocar armor/helm/weapon sem redesenho e sem clipping crítico |
| O5 | Componentização de habilidades | Kamehameha com ≥7 componentes separados e reutilizáveis |
| O6 | Cenários montáveis | 5–10 mapas compostos por camadas + tiles + props + colisão |
| O7 | UI utilizável | Kit completo com 9-slice e todos os estados |
| O8 | Continuidade | Nenhuma sessão recomeça do zero; estado sempre reconstruível pelos arquivos |
| O9 | Disciplina de orçamento | Nunca >10 gerações/sessão; ledger 100% conciliado |
| O10 | Honestidade técnica | Zero asset `APPROVED` sem PNG válido, pivô, metadados e preview |

## 3. Escopo

### 3.1 Dentro do escopo

- Personagens canônicos (DB, DBZ, DBS, DBGT, filmes) em sistema paper-doll modular.
- Transformações como conjuntos de substituição (cabelo, olhos, anatomia, aura, VFX) — não recolor de imagem inteira.
- Equipamentos (armaduras, roupas, helms, capas, luvas, botas, acessórios, armas).
- Inimigos comuns, elites, bosses com escala e rig próprios.
- Pets, companheiros e invocações.
- Habilidades e VFX componentizados + ícones.
- Cenários 2.5D em camadas com tiles, props, portais e dados de colisão.
- Kit de HUD/UI de MMORPG 2D.
- Metadados JSON, atlases, spritesheets, rigs, timelines e documentação de integração.
- Ferramentas de validação do pipeline (alpha, dimensões, pivôs, IDs, referências).

### 3.2 Fora do escopo (por enquanto)

- Código de jogo, gameplay, servidor, netcode, balanceamento, economia.
- Áudio (SFX/música) — apenas *sugestões* documentadas, sem produção.
- Animação 3D, modelos 3D, rigs 3D.
- Pixel art, pintura realista, aquarela, 3D fotorrealista (proibidos pelo master §2).
- Cópia, extração ou redistribuição de assets oficiais de AQW.
- Publicação, loja, monetização ou distribuição comercial (ver `LICENSE_NOTES.md`).
- Localização de textos (UI é entregue sem texto embutido, por desenho).

### 3.3 Premissas

- A ferramenta de geração produz **1 imagem por chamada**, sem alpha nativo confiável → o pipeline precisa
  de keying e segmentação próprios (ver `tooling_audit.md` e `ADR-0001`).
- O projeto é de **longo prazo**: 60–80 sessões para atingir `1.0.0`. Não haverá "pacote concluído" em poucas sessões.
- O trabalho é executado por agente com autonomia de produção, mas sem autoridade para alterar padrões
  silenciosamente.

---

## 4. Princípios de engenharia

1. **Técnica antes de volume.** Nada é produzido em massa antes de o pipeline provar que produz peças
   separadas, com alpha correto e pivô alinhado.
2. **Vertical slice primeiro.** Um personagem completo (Goku) valida tudo antes do roster.
3. **Dado, não desenho.** O que garante a montagem são pivôs, âncoras e ordem de camadas — não a arte.
4. **Determinismo onde possível.** Layouts de geração em grade fixa, nomes fixos, âncoras fixas: o
   pós-processamento precisa ser scriptável, não artesanal.
5. **Rastreabilidade total.** Todo asset aponta para sessão, prompt, referência e padrões vigentes.
6. **Falha explícita.** Asset ruim é reprovado e registrado como `REWORK_REQUIRED`/`BLOCKED`; nunca "consertado" no relatório.
7. **Engine-agnostic.** Nada essencial depende de `.tscn`, `.prefab`, `.anim` ou formato proprietário.
8. **Orçamento é lei.** 10 gerações por sessão, 6–8 novas, 2–4 de reserva.
9. **Continuidade acima de velocidade.** `continuity_state.json` é atualizado ao fim de cada sessão.
10. **Direitos respeitados.** Sem asset de AQW, sem declaração de licença fictícia.

---

## 5. Arquitetura de produção

### 5.1 Visão em estágios

```text
[1] PLANEJAR      backlog + orçamento + lote coeso
        │
[2] REFERENCIAR   folha canônica + paleta + proporção (quando o lote exige)
        │
[3] GERAR         ≤10 chamadas, em grade/template determinístico
        │
[4] PROCESSAR     keying → alpha real → trim → split → normalize → scale
        │
[5] MONTAR        composição de teste por pivô/âncora + overlay de proporção
        │
[6] VALIDAR       gates G1–G4 (visual, técnico, funcional, documentação)
        │
[7] EXPORTAR      PNG individual → spritesheet/atlas → metadados → preview
        │
[8] REGISTRAR     registry + manifest + ledger + relatório + continuity
        │
[9] ENCERRAR      conciliação de orçamento → próxima sessão
```

Detalhamento operacional: `docs/production_pipeline.md`.

### 5.2 Cadeia de valor de dados

```text
referência canônica ─┐
Visual Bible ────────┼─► prompt template ─► imagem bruta (PNG)
escala/rig ──────────┘                        │
                                              ▼
                            máscara alpha + grade de células
                                              │
                     ┌────────────────────────┼───────────────────────┐
                     ▼                        ▼                       ▼
              peças PNG + pivô          spritesheet/atlas      metadados JSON
                     │                        │                       │
                     └──────────► rig/timeline ► composição/preview ◄─┘
                                              │
                                              ▼
                                 registry + manifest + relatório
```

### 5.3 Responsabilidades do agente de produção

| Papel | Responsabilidade |
|---|---|
| Diretor de Arte | Aplicar a Visual Bible, aprovar/reprovar identidade e silhueta |
| Technical Artist | Garantir alpha, escala, pivôs, camadas, atlas e metadados |
| Sprite/Animador 2D | Poses, timelines, eventos, envelopes de ataque |
| Designer de UI | Kit de HUD, 9-slice, estados, legibilidade |
| Engenheiro de Pipeline | Ferramentas de recorte/validação/montagem; determinismo |
| Curador de Produção | Ledger, backlog, registry, continuidade, relatórios |

O mesmo agente exerce todos os papéis — por isso os **gates existem**: eles impedem que o "artista"
aprove o próprio trabalho sem evidência.

---

## 6. Modelo de conteúdo

### 6.1 Hierarquia

```text
Wave (agrupamento de fases)
└── Fase (F0–F13, do master §21)
    └── Sessão (DB-SESSION-XXXX, ≤10 gerações)
        └── Lote (conjunto coeso: personagem / set / técnica / mapa)
            └── Asset (ID único, status, versão)
                └── Peça (PNG + pivô + âncora + camada)
```

### 6.2 Categorias e IDs

`DB_[CATEGORY]_[SUBCATEGORY]_[NAME]_[VARIANT]_[STATE]` — tabelas completas em `docs/naming_conventions.md`.

### 6.3 Priorização

Três tiers aplicados a todo conteúdo (personagens, mapas, skills, UI):

- **P0 — necessário para o vertical slice.** Bloqueia avanço se faltar.
- **P1 — necessária para o roster inicial e o "demo jogável".**
- **P2 — expansão por saga** (preenche lacunas, alimenta waves finais).

Catálogo: `docs/character_catalog.md`. Backlog executável: `production/production_backlog.json`.

---

## 7. Governança

| Instrumento | Função | Frequência |
|---|---|---|
| `production/generation_ledger.json` | Controle do orçamento de gerações | Toda sessão |
| `production/asset_registry.json` | Fonte da verdade de IDs/status/arquivos | Toda promoção |
| `production/production_backlog.json` | Prioridade executável | Toda sessão |
| `production/continuity_state.json` | Retomada sem perda de contexto | Fim de toda sessão |
| `production/session_reports/DB-SESSION-XXXX.md` | Relatório obrigatório (formato do master §25) | Toda sessão |
| `production/qa_reports/` | Evidência de validação (visual/técnica) | Toda promoção |
| ADR em `docs/decisions/` | Mudança de padrão, escala, formato, IDs | Sob demanda |
| `VERSION.md` | Rastreio de versão de pack e padrões | Toda mudança de padrão/release |

### 7.1 Regras de mudança

- Mudança em **escala, contornos, proporções, ordem de camadas, pivôs ou IDs** → ADR + bump de versão +
  plano de compatibilidade para assets já aprovados.
- Mudança em **conteúdo** (novo personagem, novo set) → não exige ADR, apenas backlog + sessão.
- Mudança no **master prompt ou guides** → ADR obrigatório e revisão da Visual Bible.

---

## 8. Riscos

| # | Risco | Prob. | Impacto | Mitigação | Dono do gate |
|---|---|---|---|---|---|
| R1 | **Peças não ficam realmente separadas** (gerador desenha tudo junto) | Alta | Crítico | Grade determinística (ADR-0001) + segmentação por célula/bbox; spike na Sessão 0001; fallback = status `REFERENCE_ONLY`, nunca `APPROVED` | G1/G2 |
| R2 | **Alpha sujo** (xadrez falso, halo, fundo branco) | Alta | Alto | Chroma-key + despill + erode 1 px + inspeção de borda; teste automático de alpha | G2 |
| R3 | **Drift visual entre sessões** (linha, cor, proporção, estilo de olho) | Alta | Alto | Visual Bible normativa + overlay de proporção + fichas de referência reutilizadas nas sessões seguintes | G1 |
| R4 | **Perda de fidelidade canônica** (personagem errado, cor errada) | Média | Alto | Ficha de referência por personagem + revisão contra o catálogo + reprovação explícita | G1 |
| R5 | **Estouro de orçamento** | Média | Alto | Ledger consultado antes de cada chamada; 2–4 de reserva; parada dura em 10 | G0 |
| R6 | **Perda de contexto entre sessões** | Média | Alto | `continuity_state.json` + último relatório + registry como fonte de verdade | G5 |
| R7 | **Clipping de equipamento** | Média | Médio | Âncoras fixas, ordem de camadas, teste de montagem com dummy em 3 poses | G3 |
| R8 | **Peso/performance** (atlases grandes, camadas demais) | Média | Médio | Orçamento por categoria, atlas 2048 máx., limite de camadas por personagem | G2 |
| R9 | **Escopo infinito** (universo Dragon Ball é enorme) | Alta | Médio | Tiers P0/P1/P2 + waves fechadas; nada entra em produção sem estar no backlog | backlog review |
| R10 | **Deriva jurídica** (uso comercial do IP) | Baixa | Crítico | `LICENSE_NOTES.md`, `restrictions` nos metadados, aviso em README | G4 |
| R11 | **Ferramenta de geração com modos que bloqueiam a sessão** (ex.: escolha interativa do usuário) | Média | Médio | Modo de produção sempre direto, nunca interativo (ver tooling_audit) | pipeline |
| R12 | **Pivô inferido errado** (rotação abre a articulação) | Alta | Alto | Pivô derivado da âncora do template, não "do desenho"; teste de rotação ±35° em cada junta | G3 |

---

## 9. Métricas

### 9.1 Por sessão

- Gerações executadas / orçamento (alvo 6–8/10).
- Taxa de aprovação: assets aprovados / gerados (alvo ≥70% a partir da fase 3).
- Peças com pivô validado / peças produzidas (alvo 100%).
- Defeitos abertos por categoria (alpha, proporção, identidade, clipping).

### 9.2 Por fase

- Critérios de saída atendidos (binário — ver `roadmap.md`).
- Cobertura das metas do master §22 (tabela de conteúdo).
- Reutilização: % de assets montados sobre rig/base já aprovados.

### 9.3 De saúde do repositório

- `asset_registry.json` 100% consistente com arquivos em disco (validador obrigatório).
- Zero ID duplicado, zero referência quebrada, zero asset `APPROVED` sem metadados válidos.
- Ledger conciliado: soma das gerações por sessão = total declarado.

---

## 10. Capacidades e limitações (resumo)

Auditoria completa em `docs/tooling_audit.md`. Resumo que condiciona o plano:

| Necessidade | Situação | Consequência no plano |
|---|---|---|
| Gerar imagem | Disponível — 1 imagem por chamada | Cada chamada deve conter um lote de peças em grade |
| Alpha nativo confiável | **Não disponível** | Keying obrigatório (ADR-0001) |
| Vetorização / edição vetorial | **Não disponível** | Entrega em raster; vetor descartado como requisito |
| Segmentação de imagem | Disponível via script (Pillow/numpy) | Split por grade + bbox + componentes conexos |
| Criação de spritesheet/atlas | Disponível via script | Ferramenta própria em `tools/` |
| Rigging esqueletal automático | **Não disponível** | Rig é **dado** (JSON), não binário de software; preview por composição |
| Preview animado | Parcial (montagem de frames via script; GIF/APNG viável) | Preview em APNG/GIF + folha de poses |
| Continuidade entre sessões | Disponível via repositório | Obrigatório ao fim de cada sessão |

---

## 11. Definição de Pronto (DoD)

Um asset só é `APPROVED` com:

1. ID único registrado no registry.
2. PNG RGBA com alpha verdadeiro, dimensões dentro da categoria, sem resíduo de fundo.
3. Pivô em px e normalizado, âncora nomeada, camada definida.
4. Metadados válidos no schema (`production/schemas/asset_metadata.schema.json`).
5. Montagem de teste aprovada (composição reproduz o personagem/objeto).
6. Preview gerado.
7. Checklist de `docs/quality_checklist.md` preenchido com evidência.
8. Origem, sessão e restrições de uso registradas.

Fases têm critérios de saída adicionais em `docs/roadmap.md` — e **nenhuma fase avança por entusiasmo**.

## 12. O que este planejamento explicitamente recusa

- "Gerar 200 imagens e chamar de pack."
- "Considerar uma folha com peças lado a lado como asset modular pronto."
- "Declarar rig feito porque existe um JSON com nomes de bones e nenhuma montagem testada."
- "Reduzir todos os bosses ao tamanho de personagem comum para simplificar."
- "Ajustar o relatório para parecer que o orçamento foi cumprido."
- "Recomeçar o projeto do zero na próxima sessão por falta de memória."
