# references/palettes/

`core_palettes.json` é a fonte de cores do projeto, organizada em cinco blocos:

| Bloco | Uso |
|---|---|
| `global` | constantes de contorno, opacidades de sombra/brilho e multiplicador de half-shadow |
| `characters` | paleta por personagem/forma (pele, roupa, cabelo, olhos) |
| `elements` | energia por tipo (ki, kamehameha, fogo, divino, hakai, cura) com `blend` sugerido |
| `materials` | metal, ouro, couro, tecido, pedra, madeira (base/sombra/brilho) |
| `ui` | painel, bordas, barras (HP/Ki/XP/classe), texto |
| `environments` | atmosfera por mapa |

## Regras

1. Os valores são **direção de arte aproximada**, não amostragem de material oficial.
   A paleta oficial de um asset nasce da **ficha canônica aprovada** daquele personagem.
2. Ao aprovar uma ficha, copie a paleta final para cá com o sufixo `_approved` e a sessão de origem.
3. Controle de drift: 5 pontos amostrados por asset comparados com a paleta
   (`ΔH ≤ 8°`, `ΔS ≤ 10%`, `ΔV ≤ 10%`).
4. Nenhuma cor entra "só porque ficou bonita": cor nova = atualização deste arquivo + menção no relatório.
