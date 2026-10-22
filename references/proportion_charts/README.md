# references/proportion_charts/

Overlays de proporção usados para detectar drift entre sessões (`art_style_guide.md` §9).

## Arquivos previstos

| Arquivo | Conteúdo | Como é gerado |
|---|---|---|
| `body_200u.png` | silhueta esquemática do humanoide padrão (200 u) com linhas de ombro, quadril, joelho, punho e pescoço | `tools/compose.py --overlay` a partir do rig JSON (não desenhado à mão) |
| `head_36u.png` | grade de cabeça (olhos, queixo, topo) | idem |
| `boss_scale.png` | comparação de escalas (200 / 400 / 900 u) | idem |
| `check_<asset>.png` | overlay aplicado sobre um asset real, com desvio medido | por sessão |

## Medidas de referência (u)

```text
topo do cranio   200      ombro        156 ±4      quadril      100
linha dos olhos  182      cotovelo     124 ±4      joelho        56 ±4
queixo           164      punho         94 ±4      tornozelo     14 ±4
pescoco          162      ponta dedos   80        planta         0
```

## Regra

O overlay é **calculado**, não estimado. Se o asset não encaixa, o asset é `REWORK_REQUIRED` — o overlay
não é ajustado para caber no asset.
