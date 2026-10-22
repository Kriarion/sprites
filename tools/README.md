# tools/ — Ferramentas do pipeline

> **Estado:** contrato definido; **nenhuma ferramenta implementada ainda.**
> Implementação é o item `BL-001` do backlog, na `DB-SESSION-0001`.
> Enquanto elas não existirem, nenhum asset pode atingir `APPROVED` (gates G2/G3 dependem delas).

## Instalação

```bash
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
```

O venv não é versionado (`.gitignore`). Pillow e numpy não estão disponíveis no sistema por padrão.

## Ferramentas previstas

| Ferramenta | Entrada | Saída | Critério de aceite |
|---|---|---|---|
| `key.py` | PNG bruto + cor-chave | PNG RGBA com alpha real, despill, erode 1 px | resíduo de fundo < 0,5% da área |
| `decompose.py` | PNG keyed + template JSON | peças PNG + `parts.json` com bbox e pivô | 12/12 peças separadas, `cell-fit` OK |
| `compose.py` | rig JSON + asset JSON + timeline | PNG de montagem / APNG de preview / overlay de proporção | composição reproduz o personagem sem ajuste manual |
| `validate.py` | registry + arquivos + schemas | log PASS/FAIL, exit code | 14 testes de `quality_checklist.md` §7 |
| `atlas.py` | lista de peças | atlas potência de 2 + `.atlas.json` | padding ≥2 px, sem sobreposição, sem bleeding |
| `build_manifest.py` | registry | `asset_manifest.json` | determinístico, com hash |
| `palette_check.py` | asset + paleta | relatório de ΔH/ΔS/ΔV | tolerância de `art_style_guide.md` §9 |

## Contratos obrigatórios

1. **Sem interatividade.** Nenhuma ferramenta pede confirmação; tudo por argumentos e arquivo de config.
2. **Sem escrita fora do diretório alvo.** Nada de sobrescrever `characters/` a partir de `exports/`.
3. **Determinismo.** Mesma entrada → mesma saída (sem timestamp no pixel, sem aleatoriedade sem seed).
4. **Falha explícita.** Erro retorna exit code ≠ 0 e mensagem com o motivo, nunca "corrige e segue".
5. **Não aprova nada.** Ferramenta não altera status no registry; promoção é decisão de gate.

## Templates de grade

`tools/templates/PART_SHEET_*.json` descrevem, célula por célula: peça, âncora, camada e fração de pivô.
O pivô vem **do template**, não do desenho (ADR-0001 §2.2). Alterar um template exige bump de versão do
Technical Standard e revalidação das peças que o usam.

## Saída de log

Toda execução escreve um log em `production/qa_reports/logs/<tool>_<AAAAMMDD-HHMM>.log` (pasta a criar na
primeira execução). O relatório de QA cita o log — sem log, sem aprovação.
