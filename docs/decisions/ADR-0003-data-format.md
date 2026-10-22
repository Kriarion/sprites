# ADR-0003 — Formato de dados engine-agnostic

- **Status:** Aceita
- **Data:** 2026-10-22
- **Afeta:** todo o pacote; `technical_specification.md` §8–§11; `integration_guide.md`

## 1. Contexto

O master (§18.5) proíbe dependência de formatos proprietários de engine. O ambiente **não** tem
Inkscape/Illustrator/Animate/Spine: não há como produzir `.svg`, `.ai`, `.fla`, `.psd` ou `.spine`
como fonte de verdade. Precisamos de um formato que qualquer engine consuma e que o agente consiga
produzir e **validar**.

## 2. Decisão

Fonte de verdade em **PNG (RGBA) + JSON**, com JSON Schemas versionados no repositório:

| Artefato | Formato | Papel |
|---|---|---|
| Peça | `PNG` RGBA 8-bit, não premultiplicado | imagem |
| Asset | `<id>.asset.json` | metadados, partes, pivôs, camadas, dependências |
| Rig | `<rig_id>.rig.json` | bones, ROM, slots, âncoras |
| Animação | `<anim>.anim.json` | keys, eventos, hitboxes |
| Atlas | `<atlas>.atlas.json` | frames, pivôs, padding |
| Mapa | `map.json` | camadas, colisão, spawns, portais |

Regras:
- Nenhum arquivo proprietário é **necessário**; se um exemplo for gerado (ex.: `.tscn`), vive em `examples/`
  e pode ser apagado sem quebrar o pacote.
- JSON sempre UTF-8, indentado, chaves em `snake_case`, datas ISO-8601.
- Schemas em `production/schemas/*.schema.json`; validação local (sem dependência de serviço externo).
- Sem `__meta__` inventado em runtime: o que a engine precisa está declarado.
- Não premultiplicar alpha (evita halo em engines que não despremultiplicam).

## 3. Alternativas consideradas

| Alternativa | Problema |
|---|---|
| Spine/DragonBones como fonte | software indisponível; formato proprietário |
| Godot `.tres`/`.tscn` como fonte | viola §18.5 (engine-agnostic) |
| SVG/PDF como fonte | não produzível no ambiente; rasterização não reversível |
| Planilha/CSV para metadados | sem estrutura para pivôs e hierarquia |
| Binário customizado (`.dat`) | ilegível para o usuário; inviabiliza auditoria |

## 4. Consequências

- O pacote é auditável com `jq`, `diff` e `git` — inclusive por humanos.
- Falta de ferramenta vetorial é compensada por mestres raster 4x (ADR-0002).
- Adapters para engines são **exemplos documentados**, não dependências.
- Qualquer evolução de schema exige bump de versão e política de migração (`naming_conventions.md` §8).
