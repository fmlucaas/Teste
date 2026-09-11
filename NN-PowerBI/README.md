# Dashboard Novos Negócios — Power BI

Reconstrução do dashboard de carregamento do time de Novos Negócios, com as
visões de reporte por unidade de negócio (que hoje são feitas à mão em PDF/PPT),
visão financeira, mapeamento completo e — o que não existia — **evolução do
carregamento dentro do mês**.

## Comece por aqui

**→ [`docs/DOSSIE.md`](docs/DOSSIE.md)** — como colocar no ar.
Tem três caminhos, do mais rápido ao mais manual. Comece pelo Caminho A.

**→ [`docs/DIAGNOSTICO_BASE.md`](docs/DIAGNOSTICO_BASE.md)** — o que encontrei na
base atual: colunas em desuso (com números), divergências de digitação, e o
campo que falta para o histórico funcionar.

## As 7 páginas

| # | Página | O que responde |
|---|---|---|
| 1 | Visão Geral | A foto de hoje: quantas oportunidades, em que status, de que categoria, de onde vieram |
| 2 | Carregamento do Time | Quantas horas cada pessoa tem empenhadas contra a capacidade dela |
| 3 | **Evolução do Mês** | *Começou o mês com quantos, entraram quantos, saíram quantos, terminou com quantos* |
| 4 | **Report por Unidade de Negócio** | O one-page de qualquer BU — troca no filtro. NR e SNC são só dois casos |
| 5 | **Carteira da Unidade** | O detalhe por trás do one-page: carregamento por mês e lista de oportunidades |
| 6 | Financeiro | VPL, peak sales, faturamento projetado (DRE 5 anos) e margem do pipeline |
| 7 | **Mapeamento Completo** | O consolidado de todos os mapeamentos, sem precisar pedir para ninguém |
| 8 | Qualidade da Base | Por responsável, o que falta preencher e por que isso importa |

## O que mudou em relação ao PBI atual

- **Histórico de verdade.** Além da foto do dia, o modelo reconstrói mês a mês
  como o carregamento se comportou — a partir das datas que já existem na
  planilha, sem infraestrutura nova.
- **Padronização automática.** Variações de digitação (`Legrand`/`LEGRAND`,
  `INOVAÇÃO`/`INOVADOR INCREMENTAL`, 9 pares de motivos de cancelamento) deixam
  de dividir os números dos gráficos.
- **Datas à prova de bala.** As 53 células de data gravadas como texto passam a
  ser lidas; os valores impossíveis (ano 1913, o número 5039) são descartados.
- **Régua de horas em aberto.** O cálculo de carregamento saiu de dentro do
  arquivo e virou um Excel (`Regua_Esforco_NN.xlsx`) que o time preenche quando
  decidir. Até lá, todo o resto funciona normalmente.
- **Aba `Solicitações` incorporada.** 93 demandas às áreas técnicas que hoje não
  aparecem em lugar nenhum viram SLA e taxa de viabilidade.
- **Página de qualidade.** 11 regras que apontam, por responsável, o que impede
  cada análise.

## Estrutura

```
dist/       Dashboard_Novos_Negocios.pbit   ← tente este primeiro
            Dashboard_Novos_Negocios_PBIP/  ← alternativa em formato projeto
            Regua_Esforco_NN.xlsx           ← a régua de horas, para o time preencher
modelo/     Model.bim, Layout.json, Section1.m
M/queries/  as 17 consultas do Power Query, uma por arquivo
DAX/        as 76 medidas e as 7 colunas calculadas
docs/       DOSSIE.md, DIAGNOSTICO_BASE.md, ESPECIFICACAO_TELAS.md
build/      scripts que geram tudo acima (Python)
```

## Para regenerar

```bash
python3 build/build_model.py    # Model.bim
python3 build/build_report.py   # Layout.json
python3 build/package.py        # .pbit e .pbip
```
