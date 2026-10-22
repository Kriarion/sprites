# CONTROLE DE QUALIDADE (normativo)

**Versão:** 1.0.0 · **Base:** master §19, §23, §25

Nenhum asset é considerado pronto sem passar pelos gates abaixo, com **evidência registrada**.
"Está bonito" não é evidência. "Passou no G2 com log do validador" é.

---

## 1. Estados de um asset

| Status | Significado | Pode ir para entrega? |
|---|---|---|
| `PLANNED` | no backlog, sem arquivo | não |
| `GENERATED` | imagem bruta existe, não processada | não |
| `PROCESSING` | em keying/split/normalização | não |
| `QA_PENDING` | processado, aguardando avaliação | não |
| `APPROVED` | passou em G1–G4 | **sim** |
| `REWORK_REQUIRED` | reprovado com motivo; pode ser refeito | não |
| `BLOCKED` | impossível tecnicamente agora (registrar causa) | não |
| `DEPRECATED` | substituído por versão melhor | não (mantido por rastreio) |

Transições permitidas:

```text
PLANNED → GENERATED → PROCESSING → QA_PENDING → APPROVED
                         ↑              │
                    REWORK_REQUIRED ◄───┘
GENERATED/QA_PENDING → BLOCKED (motivo técnico obrigatório)
APPROVED → DEPRECATED (com substituto registrado)
```

`APPROVED → REWORK_REQUIRED` é proibido sem: ADR ou defeito documentado (ex.: pivô errado descoberto depois).

## 2. Gates

| Gate | Nome | Pergunta-chave | Responsável |
|---|---|---|---|
| **G0** | Orçamento e escopo | O asset está no backlog? Há orçamento nesta sessão? | Curador |
| **G1** | Identidade visual | É o estilo certo e o personagem certo? | Diretor de Arte |
| **G2** | Técnica | Arquivo, alpha, dimensão, pivô, metadados estão corretos? | Technical Artist |
| **G3** | Função | Monta? Anima? Equipa? Renderiza? | Technical Artist / QA |
| **G4** | Documentação | ID, origem, dependências, versão, restrições estão registrados? | Curador |

Fluxo: `G0 → G1 → G2 → G3 → G4 → APPROVED`. Falha em qualquer gate volta para `REWORK_REQUIRED` com motivo
em `production/qa_reports/`.

## 3. G1 — Checklist visual

- [ ] Estilo coerente com a Visual Bible (§2 e §11 do `art_style_guide.md`).
- [ ] Personagem/elemento/forma canônica correta (nome, figurino, cor, símbolo).
- [ ] Fonte de luz idêntica à canônica.
- [ ] Contorno com espessura da tabela (2 px @1x / 4 px @2x / 8 px @4x).
- [ ] Paleta do personagem/elemento respeitada (ΔH ≤ 8°, ΔS ≤ 10%, ΔV ≤ 10%).
- [ ] Proporção dentro de ±5% (altura) e ±4 u (articulações).
- [ ] Silhueta legível em 25% e em preto puro.
- [ ] Zero artefato: sem membro extra, sem dedo a mais, sem fusão de peças, sem texto/assinatura.
- [ ] Nenhum detalhe que só existe em close.

**Reprovações imediatas:** anatomia deformada, membro extra, personagem errado, transformação errada,
fundo não removível com qualidade, partes cortadas, resolução insuficiente.

## 4. G2 — Checklist técnico

- [ ] PNG válido, RGBA, sem perfil ICC/EXIF.
- [ ] Alpha real (≥1 px transparente e ≥1 opaco), sem resíduo de fundo-chave > 0,5% da área.
- [ ] Sem halo magenta/verde; sem borda branca de 1 px.
- [ ] `trim` aplicado com 2 px de respiro.
- [ ] Dimensões na faixa da categoria (`technical_specification.md` §3).
- [ ] `pivot_px` dentro da imagem (ou `pivot_outside` justificado).
- [ ] `layer` no vocabulário; sem empate no mesmo personagem.
- [ ] `pivot_norm` = `pivot_px / size` (verificado por cálculo).
- [ ] Metadados validam no schema.
- [ ] Todos os arquivos citados existem; nenhuma dependência quebrada.
- [ ] ID único e conforme `naming_conventions.md`.
- [ ] Dentro do orçamento de peso/atlas.

## 5. G3 — Checklist funcional

- [ ] **Monta:** composição por JSON reproduz o personagem (sem ajuste manual).
- [ ] **Articula:** rotação ±35° em cada junta sem gap visível.
- [ ] **Anima:** pelo menos idle + 1 ação tocam na timeline sem pop.
- [ ] **Equipa:** troca de slot funciona (armor/helm/weapon) sem clipping crítico.
- [ ] **Renderiza:** aparece corretamente sobre 2 fundos distintos (claro e escuro).
- [ ] **Coexiste:** convive com os assets já aprovados (escala, paleta, contorno).
- [ ] **Espelha:** flip horizontal sem artefato e sem texto invertido.

## 6. G4 — Checklist de documentação

- [ ] ID no `asset_registry.json` com status atualizado.
- [ ] Origem (sessão, prompt, referência canônica) registrada.
- [ ] Arquivos associados e dependências listados.
- [ ] Versão e `changelog` atualizados.
- [ ] Padrões vigentes (`standards`) congelados nos metadados.
- [ ] `ownership` e `restrictions` preenchidos (`LICENSE_NOTES.md` §4).
- [ ] Preview em `exports/previews/` e referenciado.
- [ ] Relatório de QA correspondente em `production/qa_reports/`.

## 7. Testes automáticos (obrigatórios)

`tools/validate.py` deve verificar:

| # | Teste | Falha |
|---|---|---|
| 1 | Arquivos citados existem | referência quebrada |
| 2 | PNG abre (Pillow) | arquivo inválido |
| 3 | Modo RGBA + alpha real | alpha ausente |
| 4 | Cobertura de resíduo de fundo < 0,5% | keying falhou |
| 5 | Dimensões na faixa da categoria | dimensão inesperada |
| 6 | `pivot_px` dentro da imagem | pivô inválido |
| 7 | JSON valida no schema | metadados inválidos |
| 8 | IDs únicos e no padrão | ID duplicado/fora do padrão |
| 9 | Camadas no vocabulário e sem empate | ordem de camada inválida |
| 10 | Atlas: coordenadas dentro, sem sobreposição, padding ≥2 | atlas inválido |
| 11 | Dependências existem no registry | dependência inexistente |
| 12 | `asset_manifest.json` concorda com o registry | manifesto desatualizado |
| 13 | Ledger: soma de gerações coerente | orçamento inconsistente |
| 14 | Nenhum asset `APPROVED` sem QA report | aprovação sem evidência |

Falha em qualquer teste → **status não avança**. O validador nunca "conserta" nada.

## 8. Testes visuais (obrigatórios)

Previews geradas por `tools/compose.py`:

- [ ] Personagem montado (idle).
- [ ] Personagem com equipamento.
- [ ] Personagem transformado.
- [ ] Ciclo de animação (APNG, 2 ciclos).
- [ ] Habilidade (sequência completa).
- [ ] Cenário composto com personagem de referência.
- [ ] Interface composta sobre cenário.

Preview é **evidência**, não ornamento: deve ter nome do asset, versão e data.

## 9. Registro de QA

Formato mínimo de `production/qa_reports/<asset_id>_<AAAAMMDD>.md`:

```text
ASSET: DB_...   VERSION: 1.0.0   SESSION: DB-SESSION-00XX
G0: PASS/FAIL — observação
G1: PASS/FAIL — observação (com item reprovado)
G2: PASS/FAIL — log do validador (colar saída)
G3: PASS/FAIL — preview anexado
G4: PASS/FAIL — campos faltantes
RESULTADO: APPROVED | REWORK_REQUIRED | BLOCKED
MOTIVO (obrigatório em caso de falha):
PRÓXIMA AÇÃO:
```

## 10. Regra de honestidade

É proibido:

- Marcar `APPROVED` sem existir PNG + metadados + preview + QA report.
- Registrar "validado" sem log/saída de validador.
- Declarar rig funcional sem teste de rotação.
- Declarar peças separadas quando existe apenas uma folha com desenhos lado a lado.
- Ajustar o ledger para "fechar" o orçamento.

Se algo não pôde ser verificado, o status é `QA_PENDING` ou `BLOCKED`, com a razão escrita.
