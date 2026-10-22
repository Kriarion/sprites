# VERSION — Controle de versão do pacote

O projeto versiona **o pacote** e **os padrões** de forma independente. Um asset pode ser regenerado
(versão própria) sem que a especificação técnica mude, e vice-versa.

## 1. Componentes versionados

| Componente | Versão atual | Arquivo de referência | Regra de mudança |
|---|---|---|---|
| Pack (conteúdo) | `0.2.0` | `asset_manifest.json` | SemVer — ver §2 |
| Visual Bible | `1.1.0` | `docs/art_style_guide.md` | MINOR = novo padrão documentado; MAJOR = mudança que invalida assets existentes |
| Technical Standard | `1.0.0` | `docs/technical_specification.md` | MAJOR = quebra compatibilidade de coordenadas/pivôs/atlas |
| Naming Standard | `1.0.0` | `docs/naming_conventions.md` | MAJOR = renomeação em massa (exige plano de migração) |
| Rig Standard | `1.0.0` | `docs/anatomy_and_rigging.md` | MAJOR = mudança na hierarquia/âncoras |
| Animation Standard | `1.0.0` | `docs/animation_standard.md` | MAJOR = mudança de durações/eventos consumidos por engine |
| UI Standard | `1.0.0` | `docs/ui_standard.md` | MAJOR = mudança em 9-slice/resoluções base |
| Backlog | `2026.10` | `production/production_backlog.json` | Revisado a cada onda |

Cada asset carrega, em seus metadados, a versão dos padrões vigentes **no momento da aprovação**
(`standards: { visual_bible, technical, naming, rig, animation }`). Isso permite detectar drift.

## 2. Versionamento do pack (SemVer adaptado)

`MAJOR.MINOR.PATCH`

- **PATCH** (`0.1.0 → 0.1.1`): correções, reprocessamento de alpha, ajuste de metadados, novos previews.
  Nenhum asset novo. Nenhuma quebra de ID.
- **MINOR** (`0.1.x → 0.2.0`): novo conjunto coerente de assets aprovados (um personagem fechado,
  um pack de VFX, um mapa completo). Retrocompatível.
- **MAJOR** (`0.x → 1.0.0`): mudança incompatível — renomeação de IDs, mudança de escala canônica,
  mudança de ordem de camadas, reorganização de diretórios. **Exige ADR + plano de migração.**

### Marcos de versão planejados

| Versão | Significado | Fase |
|---|---|---|
| `0.1.0` | Documentação e infraestrutura (atual) | Fase 0 |
| `0.2.0` | ✅ **atingido** — Visual Bible 1.1.0 validada em imagem + decomposição por componentes provada | Fase 1 |
| `0.3.0` | Corpos base + rigs + montagem funcional | Fase 2 |
| `0.4.0` | Vertical slice Goku jogável (idle/run/attack/kimehameha/HUD) | Fase 3 |
| `0.5.0` | Roster inicial (8 personagens) + transformações | Fases 4–5 |
| `0.7.0` | Equipamentos + VFX + inimigos | Fases 6–8 |
| `0.9.0` | Pets + ambientes + UI completa | Fases 9–11 |
| `1.0.0` | QA final, integração demonstrada, metas §22 atingidas | Fase 13 |

`1.0.0` **não** é uma data; é um critério. Ver `docs/roadmap.md`.

## 3. Versionamento de asset individual

Formato `vMAJOR.MINOR` dentro do campo `version` dos metadados:

- **MAJOR**: mudança visual perceptível que invalida composição/animação existente (redesenho de peça,
  mudança de pivô).
- **MINOR**: refino invisível em jogo (limpeza de alpha, despeckle, correção de 1 px, remoção de resíduo).

Todo incremento registra entrada no histórico do asset (`changelog` no registro) e o motivo.

## 4. Histórico do projeto

| Data | Versão | Mudança |
|---|---|---|
| 2026-10-22 | `0.1.0` | Fase 0: leitura dos guides, auditoria de ferramentas, planejamento, roadmap, Visual Bible em prosa, especificações técnicas, ADRs 0001–0005, registros de produção inicializados. Nenhum asset gerado. |
| 2026-10-22 | `0.2.0` | **DB-SESSION-0001** (10 gerações): Visual Bible **1.1.0** calibrada em imagem; 5 pranchas de referência aprovadas; `tools/` implementado (key, decompose, compose, validate, measure, cellstats); decomposição validada (9/9 objetos); grid refutada → **ADR-0006**; 1 conjunto de teste `QA_PENDING` com G3 reprovado. **Nenhum asset canônico de jogo.** |
