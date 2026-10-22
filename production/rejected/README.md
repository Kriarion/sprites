# rejected/

Arquivo de auditoria de imagens e lotes reprovados.

## Estrutura

```text
rejected/
└── DB-SESSION-NNNN/
    ├── _reason.md            (objetivo da sessão + por que cada arquivo foi reprovado)
    ├── pm_sheet_core_v1.png
    └── ...
```

## Regras

- Nada é apagado: reprovação faz parte do histórico e é prova de honestidade do ledger.
- `_reason.md` lista cada arquivo com: defeito, gate que reprovou, e a decisão (refazer, substituir, ignorar).
- Imagem rejeitada **não** entra no registry como asset (só como referência de erro, quando útil).
- O conteúdo desta pasta é ignorado pelo Git por padrão (`.gitignore`); para preservar uma reprovação
  didática, salve o `_reason.md` e uma miniatura, nunca o lote inteiro.
