# ADR-0002 — Escala canônica, unidades e resoluções

- **Status:** Aceita
- **Data:** 2026-10-22
- **Afeta:** todos os assets; `technical_specification.md` §2–§3; `anatomy_and_rigging.md`

## 1. Contexto

O guia 1 e o guia 2 dão faixas (150–250 px de altura; 24 fps; atlas potência de 2), mas não uma
escala única. O master (§6.4) exige **uma escala canônica de produção documentada** e conversível para
qualquer resolução. Sem isso, cada sessão inventaria um tamanho e o pacote se torna inutilizável.

## 2. Decisão

1. **Unidade de rig `u` = 1 px na escala 1x.** Toda medida (bones, pivôs em u, ROM, hitboxes) é expressa em `u`.
2. **Corpo humanoide adulto = 200 u** de altura (topo do crânio → planta do pé), cabeça **36 u** (5,5 cabeças).
3. **Escalas de exportação: 1x (200 px), 2x (400 px), 4x (800 px mestre).** Sempre **reduzir do 4x**,
   nunca ampliar.
4. **Tela de design: 1280 × 720**, linha do chão em `y = 620`, banda caminhável `y = 440–700`.
5. Resoluções por categoria fechadas em `technical_specification.md` §3 (peças 512 no maior lado,
   ícones 256→128/64, UI 512 para 9-slice, atlas 2048²).
6. `pixels_per_unit` é obrigatório nos metadados e deve ser **1, 2 ou 4**.

## 3. Alternativas consideradas

| Alternativa | Problema |
|---|---|
| Usar 150–250 px "livre" do guia | impossibilita encaixe; nenhuma proporção é reutilizável |
| Escala 1x = 512 px (retina-first) | exagera custo de textura; personagem ocupa 71% da tela |
| Unidade de mundo arbitrária (ex.: 1 un = 100 px) | confunde pivôs e hitboxes; engine precisa converter tudo |
| Escala por Y (perspectiva) | quebra consistência de rig (guia2 §8 não exige) |

## 4. Consequências

- Personagem 1x = 200 px → 28% da altura da tela; 8 personagens legíveis ao mesmo tempo.
- Atlas 2048² cabe 1 personagem completo em 2x com folga (orçamento de 32 MB RGBA/personagem).
- Máximo de 4 formas por personagem em um único par de atlas; formas adicionais ganham atlas próprio.
- Qualquer pedido de "resolução maior" é atendido pela existência do mestre 4x, não por novo padrão.
- Mudar a altura canônica exige **ADR novo** + bump MAJOR do Technical Standard + plano de remontagem.

## 5. Verificação

`tools/validate.py` rejeita asset cujo `pixels_per_unit` ∉ {1,2,4}, cuja altura renderizada divirja mais de
5% de 200 u (personagens padrão) ou cujas dimensões estejam fora da faixa da categoria.
