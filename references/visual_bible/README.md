# references/visual_bible/

Pranchas de estilo **aprovadas** — a referência viva que impede drift visual entre sessões.

## Estado

⏳ **Vazio por decisão.** As pranchas só entram aqui depois de passar no gate G1 na
`DB-SESSION-0001` (calibração) e serem congeladas na `DB-SESSION-0002` (Visual Bible 1.1.0).
Criar esta pasta vazia com imagens "provisórias" seria fingir validação.

## Conteúdo previsto

| Arquivo | Conteúdo |
|---|---|
| `style_dummy_mf.png` | dummy neutro masculino/feminino, frente e perfil — calibração de proporção e linha |
| `shading_three_tone.png` | demonstração de base + sombra dura + brilho duro em 4 materiais |
| `half_shadow_demo.png` | membro frontal vs traseiro, mostrando a convenção AQW |
| `line_weight_demo.png` | contorno 8/4/2 px (4x/2x/1x) sobre o mesmo objeto |
| `palette_swatches.png` | amostras das paletas aprovadas |
| `do_dont.png` | comparativo de acertos e erros |
| `_provenance.md` | origem, sessão, gate e data de cada prancha |

## Uso

1. As imagens são anexadas como referência nas gerações (`images=[...]`) quando a ferramenta permitir.
2. São citadas nos relatórios de sessão que as usaram.
3. Substituir uma prancha exige ADR + bump da Visual Bible (MINOR/MAJOR conforme o caso).
