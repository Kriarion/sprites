# references/character_sheets/

Fichas canônicas por personagem/forma: base para gerar peças fiéis e para reprovar desvios com critério.

## Estrutura prevista

```text
character_sheets/
└── goku/
    ├── _sheet.md                 texto: continuidade, saga, figurino, marcas, cores, detalhes
    ├── front_base.png            frente (4x)
    ├── side_base.png             perfil (4x)
    ├── back_base.png             costas (4x)
    ├── detail_face.png           close de rosto (olhos, sobrancelha)
    ├── detail_boots_wrist.png    detalhes de bota e pulseira
    ├── palette_extracted.json    paleta medida a partir da ficha aprovada
    └── _provenance.md            sessão, prompts, gate, data
```

## Regras

- Ficha é **referência**, não asset: não é jogável, não tem pivô de montagem, não entra no registry como
  `APPROVED` de personagem (entra como `reference` quando registrada).
- A ficha é aprovada no gate G1 **antes** das peças.
- Toda peça de personagem declara `provenance.canonical_reference` apontando para a ficha usada.
- Personagens de continuidades diferentes têm fichas separadas (ex.: `broly_dbz` e `broly_dbs`).
- Fichas evitam texto legível nas roupas para permitir espelhamento (ou marcam `mirror_safe: false`).
