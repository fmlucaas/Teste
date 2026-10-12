# Ajustes aplicados sobre a planilha do usuário

O gerador em `../gerador/` constrói a planilha do zero. Isso não serve quando o
arquivo já voltou com edições — aportes reais, projeções revistas, preços novos.
Regerar apagaria tudo.

Estes scripts fazem o contrário: abrem o arquivo que chegou, acrescentam o que
falta e devolvem. Nenhuma célula existente é tocada.

```
python3 aplica.py entrada.xlsx saida.xlsx
python3 /caminho/para/recalc.py saida.xlsx 420
python3 ../auditoria/p8.py saida.xlsx
```

| Arquivo | O que faz |
|---|---|
| `comum.py` | estilos e, principalmente, `linha_por_rotulo` — a busca por rótulo |
| `preco_claro.py` | cria a aba **Preço**: custo por assinante, componente por componente |
| `reorganiza.py` | ordem, cor e visibilidade das abas, e o mapa na aba Como usar |
| `aplica.py` | roda os dois e salva |

## A regra que não se quebra

**Nunca localize linha por número aqui.** O arquivo que chega pode ter sido
mexido em qualquer lugar. Tudo passa por `linha_por_rotulo`, que levanta erro se
não achar o rótulo — quebrar na hora é melhor do que gravar uma fórmula
apontando para a linha errada e descobrir depois.

## Por que a aba Preço tem quatro colunas

Porque "o preço" não é um número. O custo variável por assinante quase não muda
com a escala; o custo fixo por assinante despenca. Uma coluna só esconderia
exatamente a variável que decide a resposta — quantas pessoas estão dividindo a
conta.

## As duas linhas de conferência

A aba decompõe o custo de um jeito que a DRE não usa (por assinante, com o CAC
diluído na vida do cliente). Decomposição que não fecha com o original é
decomposição errada, então a aba carrega duas provas:

- **custo contra a DRE, sem o marketing** — nuvem, suporte, pessoas, marketing
  recorrente e administrativo têm de dar exatamente o que a DRE gasta nesses
  itens. O marketing de aquisição fica fora de propósito: aqui entra diluído,
  na DRE entra no mês do desembolso.
- **nuvem** — as três parcelas de nuvem desta aba, multiplicadas pelos
  assinantes, mais a parcela fixa, têm de dar a linha de nuvem da DRE.

As duas têm de ficar zeradas nos quatro momentos. `p8.py` cobra isso.
