# references/ — Referências internas do projeto

Material de apoio à produção. **Nada aqui é asset de jogo** e nada aqui contém obra de terceiros copiada.

| Pasta | Conteúdo | Estado |
|---|---|---|
| `palettes/` | Paletas canônicas e de elementos em JSON | ✅ com dados iniciais |
| `visual_bible/` | Pranchas de estilo aprovadas (imagens) | ⏳ vazio — populado na `DB-SESSION-0002` |
| `proportion_charts/` | Overlay de proporção 200 u para checagem de drift | ⏳ gerado por script na W1 |
| `character_sheets/` | Fichas canônicas por personagem (frente/perfil/costas + detalhes) | ⏳ criado por personagem |

## Política de proveniência

- **Proibido** commitar imagens de terceiros (screenshots, scans, fan arts, material oficial de AQW ou
  Dragon Ball). Referência canônica é **descritiva** (texto, medidas, paleta aproximada) ou **original**
  (gerada pelo pipeline do projeto).
- Toda imagem em `references/` deve ter origem registrada em `_provenance.md` da pasta correspondente:
  asset_id ou sessão que a produziu, data e status de aprovação.
- Referência aprovada é **usada como input** nas gerações seguintes (controle de drift,
  `art_style_guide.md` §9).
