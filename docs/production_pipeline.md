# PIPELINE DE PRODUÇÃO (normativo)

**Versão:** 1.0.0 · **Base:** master §3, §19, §20, §25, §26, §29

Como uma sessão acontece, como o orçamento é controlado e como uma imagem bruta se torna asset `APPROVED`.

---

## 1. O ciclo de sessão (9 etapas)

```text
1 PLANEJAR    ler continuity_state + backlog + ledger; escolher lote coeso; reservar orçamento
2 PREPARAR    reunir referências aprovadas, paleta, rig e templates de prompt
3 GERAR       6–8 chamadas novas (máx. 10 no total da sessão)
4 PROCESSAR   keying → alpha → trim → split → normalizar → reduzir escala
5 MONTAR      composição de teste por pivô/âncora + overlay de proporção
6 VALIDAR     G1→G4; reprovar o que não passa (registrar motivo)
7 EXPORTAR    PNG individual, atlas, spritesheet, previews, metadados
8 REGISTRAR   registry, manifest, ledger, QA report, relatório de sessão, continuity
9 ENCERRAR    conciliar orçamento; escrever próxima sessão planejada
```

Duração típica: **uma sessão = um ciclo completo**, não "um dia". Sessão sem etapa 8 **não terminou**.

## 2. Regra de orçamento

| Item | Valor |
|---|---|
| Teto absoluto por sessão | **10 gerações** |
| Meta operacional | 6–8 novas |
| Reserva para correção | 2–4 |
| Consulta obrigatória antes de cada chamada | `production/generation_ledger.json` |
| Ao atingir 10 | **parar**, mesmo com trabalho incompleto |

- Geração = 1 chamada à ferramenta de imagem, independentemente de quantos elementos a imagem contém.
- Variações/edições contam separadamente.
- Reserva não consumida **não** se converte automaticamente em novas gerações.
- `offer_options` (modo interativo que pausa para escolha do usuário) **não é usado** em produção.

### 2.1 Registro (obrigatório)

`production/generation_ledger.json` recebe, ao fim de cada sessão:

```json
{
  "session_id": "DB-SESSION-0007",
  "date": "2026-10-2x",
  "objective": "partes do corpo de Goku base",
  "planned_new": 7,
  "reserved_corrections": 3,
  "executed_new": 7,
  "executed_corrections": 1,
  "total_executed": 8,
  "assets_created": ["DB_CHAR_HERO_GOKU_BASE"],
  "assets_approved": [],
  "assets_rejected": ["DB_CHAR_HERO_GOKU_BASE_HEAD"],
  "corrections": ["re-key G4: halo magenta"],
  "next_session": "DB-SESSION-0008"
}
```

`total_executed` deve ser igual a `executed_new + executed_corrections`. O validador reprova inconsistência.

## 3. Seleção de lote (coesão)

Um lote bom compartilha **personagem, paleta, rig, transformação, cenário ou tipo de habilidade**
(master §20.3). Um lote ruim mistura um boss, um ícone de item e um céu.

Tipos de sessão: `REFERENCE`, `ANATOMY`, `CHARACTER`, `EQUIPMENT`, `ANIMATION`, `VFX`, `ENVIRONMENT`,
`UI`, `CORRECTION`. Cada sessão declara o tipo no relatório.

## 4. Prompt: template operacional

Todo prompt usa os 4 blocos de `art_style_guide.md` §10. O bloco de layout é o mais crítico:

```text
Layout: a 3x4 grid of exactly 12 separated body parts on a uniform flat #FF00FF background.
Each part is centered in its own cell, does not touch cell borders and does not touch any other part.
Minimum 16 px empty gutter between parts. Cell order (left→right, top→bottom):
1 torso 2 pelvis 3 front thigh 4 back thigh 5 front shin 6 back shin
7 front foot 8 back foot 9 front upper arm 10 front forearm 11 front hand 12 back upper arm.
No labels, no grid lines, no text, no ground shadow, no scenery.
```

Regras:
- Sempre nomear as peças na **ordem exata** das células: o split é posicional, não mágico.
- Sempre exigir fundo chapado (#FF00FF ou #00FF00 conforme contraste do objeto).
- Sempre proibir texto, rótulos, linhas de grade, sombra no chão e cenário.
- Nunca pedir "transparent background" (o gerador simula xadrez; o resultado é pior para keying).

## 5. Processamento (de imagem bruta a peças)

```text
PNG bruto
  → 1. detecção da cor de fundo dominante nas bordas
  → 2. máscara alpha (distância de cor + tolerância)
  → 3. limpeza: erode 1 px, remoção de componentes < 24 px (ruído)
  → 4. despill (neutralizar a cor-chave nas bordas)
  → 5. detecção de células (grade declarada) e bbox de cada peça
  → 6. validação cell-fit (a peça está na célula esperada? não tocou vizinha?)
  → 7. corte com 2 px de respiro
  → 8. identificação da peça (ordem declarada) → nome de arquivo
  → 9. pivô derivado da âncora do template (§5.1)
  → 10. redução para a escala de entrega (LANCZOS, sempre a partir do mestre)
```

Cada etapa grava log em `production/qa_reports/`. Falha em (6) → a peça é `REWORK_REQUIRED`, não
"recortada no olho".

### 5.1 Pivô derivado, não adivinhado

O template de grade declara, para cada célula, a **âncora nomeada** e o **ponto de pivô relativo à peça**
(ex.: `front_forearm` → pivô no canto superior esquerdo da bbox + deslocamento `(w×0.18, h×0.06)`).
Assim o pivô vem do **template**, não da interpretação do desenho — o que evita o erro mais caro do projeto
(pivô errado = articulação abrindo).

O template fica em `tools/templates/<nome>.json` e é versionado.

## 6. Promoção (estado → estado)

| Etapa | Quem decide | Evidência |
|---|---|---|
| `GENERATED` | pipeline | arquivo bruto + entrada no ledger |
| `PROCESSING` | pipeline | log de split |
| `QA_PENDING` | pipeline | PNGs + metadados gerados |
| `APPROVED` | gates G1–G4 | QA report + preview |
| `REWORK_REQUIRED` | G1/G2/G3 | motivo escrito |
| `BLOCKED` | qualquer gate | causa técnica escrita |

Detalhes: `quality_checklist.md`.

## 7. Exportação

1. `exports/individual_png/` — peças normalizadas (fonte para engines).
2. `exports/atlases/` — atlas 2048² por personagem/conjunto + `.atlas.json`.
3. `exports/spritesheets/` — animações em grade regular (para engines sem skeletal).
4. `exports/metadata/` — cópia dos JSONs prontos para consumo.
5. `exports/previews/` — composições e APNGs de evidência.

Os arquivos em `characters/`, `equipment/` etc. são a **fonte**; `exports/` é o **material de consumo**.
Nunca editar `exports/` à mão — regenerar por script.

## 8. Relatório de sessão (obrigatório)

Arquivo `production/session_reports/DB-SESSION-NNNN.md`, no formato do master §25, incluindo:

- Orçamento: planejado × executado (novas e correções).
- Assets criados/aprovados/reprovados/pendentes.
- Arquivos exportados e metadados atualizados.
- Problemas de qualidade e correções feitas.
- Status do projeto e objetivo da próxima sessão.

O relatório **não** pode listar arquivos inexistentes. O validador cruza relatório × registry.

## 9. Continuidade

Ao encerrar:

1. Atualizar `production/continuity_state.json` (`last_completed_session`, `next_session`, listas, prioridades).
2. Atualizar `production/production_backlog.json` (o que foi feito sai de `pending`).
3. Atualizar `production/asset_registry.json` (novos IDs e status).
4. Regenerar `asset_manifest.json` (`tools/build_manifest.py`).
5. Append no `generation_ledger.json`.
6. Commit com mensagem `DB-SESSION-NNNN: <objetivo>`.

## 10. Erros comuns e como o pipeline os trata

| Erro | Sintoma | Tratamento |
|---|---|---|
| Peças se tocam na grade | segmentação funde duas peças | reprovar o lote; regerar com gutter explícito |
| Fundo não uniforme | gradiente/vignette no magenta | keying com tolerância adaptativa; se falhar, reprovar |
| Xadrez falso de transparência | "alpha" desenhado | detectar padrão e reprovar (não é alpha real) |
| Gerador adicionou cenário | sombra, chão, fundo cinza | reprovar; reforçar negativos |
| Peça cortada na célula | contorno faltando | reprovar (nunca "completar" o contorno à mão) |
| Estilo escorregou | contorno fino, gradiente | reprovar no G1, realinhar com referência aprovada |
| Orçamento estourado | ledger > 10 | sessão encerrada com o que existe; registrar incidente |

## 11. Autonomia × controle

O agente **pode** decidir lote, ordem, reprovação e correção sem pedir aprovação a cada sessão
(master §26). O agente **não pode**: passar de 10 gerações, inventar arquivo, fingir validação, mudar padrão
silenciosamente, publicar externamente.

Quando uma decisão mudar o padrão do pacote, ela **para** e vira ADR para revisão humana.
