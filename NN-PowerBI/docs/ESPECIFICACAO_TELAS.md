# Especificação das Telas

Use isto só no **Caminho C** (montagem manual). Cada página tem canvas
**1280 × 720** (`Formato da página → Tipo: Personalizado`).

Para cada visual: insira o tipo indicado, posicione pelas coordenadas
(`Formato do visual → Geral → Propriedades → Posição`) e arraste os campos
para as áreas indicadas.

---

## Página 1 — 1. Visão Geral

| Pos. (x, y, larg × alt) | Visual | Título | Campos |
|---|---|---|---|
| 20, 6, 780×34 | Caixa de texto | Texto: **Visão Geral \| Novos Negócios** |  |
| 820, 14, 444×24 | Caixa de texto | Texto: **Foto de hoje do mapeamento ativo de todo o time** |  |
| 16, 56, 240×40 | Segmentação de dados |  | Valores: `Equipe[Nome]` |
| 268, 56, 240×40 | Segmentação de dados |  | Valores: `Unidade de Negócio[Unidade de Negócio]` |
| 520, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Situação]` |
| 772, 56, 240×40 | Segmentação de dados |  | Valores: `Status NN[Status]` |
| 1024, 56, 240×40 | Segmentação de dados |  | Valores: `Calendário[Ano]` |
| 16, 104, 240×72 | Cartão | OPORTUNIDADES | Valores: `_Medidas[Projetos]` (medida) |
| 268, 104, 240×72 | Cartão | EM ANDAMENTO | Valores: `_Medidas[Projetos Ativos]` (medida) |
| 520, 104, 240×72 | Cartão | STAND BY | Valores: `_Medidas[Projetos Stand by]` (medida) |
| 772, 104, 240×72 | Cartão | MOLÉCULAS | Valores: `_Medidas[Moléculas]` (medida) |
| 1024, 104, 240×72 | Cartão | FORNECEDORES | Valores: `_Medidas[Fornecedores]` (medida) |
| 16, 184, 408×215 | Gráfico de colunas agrupadas | QUANTIDADE DE PROJETOS x STATUS | Eixo X / Categoria: `Status NN[Status]`<br>Valores (eixo Y): `_Medidas[Projetos]` (medida) |
| 436, 184, 408×215 | Gráfico de barras agrupadas | PROJETOS x CATEGORIA | Eixo X / Categoria: `Mapeamento[Categoria Padrão]`<br>Valores (eixo Y): `_Medidas[Projetos]` (medida) |
| 856, 184, 408×215 | Mapa | PROJETOS x PAÍS DO FORNECEDOR | Eixo X / Categoria: `País[País]`<br>Tamanho (bolha): `_Medidas[Projetos]` (medida) |
| 16, 407, 618×290 | Tabela | PROJETOS — VISÃO RESUMIDA | Valores: `Mapeamento[Responsável Final]`<br>Valores: `Mapeamento[Molécula]`<br>Valores: `Mapeamento[Fornecedor / Parceiro]`<br>Valores: `Mapeamento[Status NN]`<br>Valores: `Mapeamento[Situação]`<br>Valores: `Mapeamento[Alerta]` |
| 646, 407, 300×290 | Gráfico de rosca | % PROJETOS x COLIGADA | Eixo X / Categoria: `Mapeamento[Coligada Padrão]`<br>Valores (eixo Y): `_Medidas[Projetos]` (medida) |
| 952, 407, 312×290 | Gráfico de rosca | SITUAÇÃO DOS PROJETOS | Eixo X / Categoria: `Mapeamento[Situação]`<br>Valores (eixo Y): `_Medidas[Projetos]` (medida) |

---

## Página 2 — 2. Carregamento do Time

| Pos. (x, y, larg × alt) | Visual | Título | Campos |
|---|---|---|---|
| 20, 6, 780×34 | Caixa de texto | Texto: **Carregamento do Time \| Capacidade x Demanda** |  |
| 820, 14, 444×24 | Caixa de texto | Texto: **Horas empenhadas hoje, por pessoa, status e complexidade** |  |
| 16, 56, 240×40 | Segmentação de dados |  | Valores: `Equipe[Nome]` |
| 268, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Atividade]` |
| 520, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Situação]` |
| 772, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Complexidade]` |
| 1024, 56, 240×40 | Segmentação de dados |  | Valores: `Unidade de Negócio[Unidade de Negócio]` |
| 16, 104, 240×72 | Cartão | PROJETOS ATIVOS | Valores: `_Medidas[Projetos Ativos]` (medida) |
| 268, 104, 240×72 | Cartão | HORAS EMPENHADAS | Valores: `_Medidas[Horas Empenhadas]` (medida) |
| 520, 104, 240×72 | Cartão | CAPACIDADE (H) | Valores: `_Medidas[Capacidade (h)]` (medida) |
| 772, 104, 240×72 | Cartão | % OCUPAÇÃO | Valores: `_Medidas[% Ocupação]` (medida) |
| 1024, 104, 240×72 | Cartão | PROJETOS / PESSOA | Valores: `_Medidas[Projetos por Pessoa]` (medida) |
| 16, 184, 618×240 | Gráfico de barras agrupadas | HORAS EMPENHADAS x CAPACIDADE — POR PESSOA | Eixo X / Categoria: `Equipe[Nome]`<br>Valores (eixo Y): `_Medidas[Horas Empenhadas]` (medida)<br>Valores (eixo Y): `_Medidas[Capacidade (h)]` (medida) |
| 646, 184, 300×240 | Medidor | % DE OCUPAÇÃO DO TIME | Valores (eixo Y): `_Medidas[% Ocupação]` (medida) |
| 952, 184, 312×240 | Gráfico de rosca | HORAS x ATIVIDADE | Eixo X / Categoria: `Mapeamento[Atividade]`<br>Valores (eixo Y): `_Medidas[Horas Empenhadas]` (medida) |
| 16, 432, 618×265 | Gráfico de barras empilhadas | PROJETOS ATIVOS POR STATUS E COMPLEXIDADE | Eixo X / Categoria: `Status NN[Status]`<br>Legenda / Série: `Mapeamento[Complexidade]`<br>Valores (eixo Y): `_Medidas[Projetos Ativos]` (medida) |
| 646, 432, 618×265 | Tabela | OCUPAÇÃO POR PESSOA | Valores: `Equipe[Nome]`<br>Valores: `_Medidas[Projetos Ativos]` (medida)<br>Valores: `_Medidas[Horas Empenhadas]` (medida)<br>Valores: `_Medidas[% Ocupação]` (medida)<br>Valores: `_Medidas[Status Ocupação]` (medida) |

---

## Página 3 — 3. Evolução do Mês

| Pos. (x, y, larg × alt) | Visual | Título | Campos |
|---|---|---|---|
| 20, 6, 780×34 | Caixa de texto | Texto: **Evolução do Mês \| Como transcorreu o carregamento** |  |
| 820, 14, 444×24 | Caixa de texto | Texto: **Entradas, saídas e carteira mês a mês — e não apenas a foto do dia** |  |
| 16, 56, 240×40 | Segmentação de dados |  | Valores: `Equipe[Nome]` |
| 268, 56, 240×40 | Segmentação de dados |  | Valores: `Calendário[Ano]` |
| 520, 56, 240×40 | Segmentação de dados |  | Valores: `Calendário[Mês]` |
| 772, 56, 240×40 | Segmentação de dados |  | Valores: `Unidade de Negócio[Unidade de Negócio]` |
| 1024, 56, 240×40 | Segmentação de dados |  | Valores: `Carregamento Mensal[Status no Mês]` |
| 16, 104, 240×72 | Cartão | INÍCIO DO MÊS | Valores: `_Medidas[Ativos no Início do Mês]` (medida) |
| 268, 104, 240×72 | Cartão | ENTRARAM | Valores: `_Medidas[Entradas no Mês]` (medida) |
| 520, 104, 240×72 | Cartão | SAÍRAM | Valores: `_Medidas[Saídas no Mês]` (medida) |
| 772, 104, 240×72 | Cartão | FIM DO MÊS | Valores: `_Medidas[Ativos no Fim do Mês]` (medida) |
| 1024, 104, 240×72 | Cartão | HOJE vs FIM DO MÊS | Valores: `_Medidas[Diferença Hoje vs Mês]` (medida) |
| 16, 184, 618×245 | Coluna agrupada e linha (combo) | CARTEIRA, ENTRADAS E SAÍDAS POR MÊS | Eixo X / Categoria: `Calendário[Ano-Mês]`<br>Valores (eixo Y): `_Medidas[Ativos no Fim do Mês]` (medida)<br>Valores da linha: `_Medidas[Entradas no Mês]` (medida)<br>Valores da linha: `_Medidas[Saídas no Mês]` (medida) |
| 646, 184, 618×245 | Gráfico em cascata | SALDO DO MÊS (ENTRADAS − SAÍDAS) | Eixo X / Categoria: `Calendário[Ano-Mês]`<br>Valores (eixo Y): `_Medidas[Saldo do Mês]` (medida) |
| 16, 437, 618×190 | Matriz | CARTEIRA POR PESSOA E MÊS | Linhas: `Equipe[Nome]`<br>Colunas: `Calendário[Ano-Mês]`<br>Valores: `_Medidas[Ativos no Fim do Mês]` (medida) |
| 646, 437, 618×190 | Gráfico de colunas empilhadas | COMPOSIÇÃO DO FUNIL AO LONGO DO TEMPO | Eixo X / Categoria: `Calendário[Ano-Mês]`<br>Legenda / Série: `Carregamento Mensal[Status no Mês]`<br>Valores (eixo Y): `_Medidas[Projetos no Mês]` (medida) |
| 16, 635, 1248×62 | Cartão | RESUMO PARA O REPORT | Valores: `_Medidas[Narrativa do Mês]` (medida) |

---

## Página 4 — 4. Report por Unidade de Negócio

| Pos. (x, y, larg × alt) | Visual | Título | Campos |
|---|---|---|---|
| 20, 6, 780×34 | Caixa de texto | Texto: **One Page Report \| Unidade de Negócio** |  |
| 820, 14, 444×24 | Caixa de texto | Texto: **Selecione a unidade e o ano — o report que hoje é feito à mão** |  |
| 16, 56, 240×40 | Segmentação de dados |  | Valores: `Unidade de Negócio[Unidade de Negócio]` |
| 268, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Franquia]` |
| 520, 56, 240×40 | Segmentação de dados |  | Valores: `Calendário[Ano]` |
| 772, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Categoria Padrão]` |
| 1024, 56, 240×40 | Segmentação de dados |  | Valores: `Equipe[Nome]` |
| 16, 104, 240×72 | Cartão | MOLÉCULAS AVALIADAS | Valores: `_Medidas[Moléculas]` (medida) |
| 268, 104, 240×72 | Cartão | OPORTUNIDADES | Valores: `_Medidas[Projetos]` (medida) |
| 520, 104, 240×72 | Cartão | EM ANDAMENTO | Valores: `_Medidas[Projetos Ativos]` (medida) |
| 772, 104, 240×72 | Cartão | CANCELADAS / STAND BY | Valores: `_Medidas[Cancelados + Stand by]` (medida) |
| 1024, 104, 240×72 | Cartão | PRINCIPAL MOTIVO | Valores: `_Medidas[Motivo nº 1]` (medida) |
| 16, 184, 408×250 | Barras 100% empilhadas | ESTÁGIO DAS OPORTUNIDADES EM ANDAMENTO | Eixo X / Categoria: `Status NN[Status]`<br>Valores (eixo Y): `_Medidas[Projetos Ativos]` (medida) |
| 436, 184, 408×250 | Gráfico de barras agrupadas | FRANQUIAS DE ATUAÇÃO DE NOVOS NEGÓCIOS | Eixo X / Categoria: `Unidade de Negócio[Unidade de Negócio]`<br>Valores (eixo Y): `_Medidas[Projetos]` (medida) |
| 856, 184, 408×250 | Gráfico de barras agrupadas | MOTIVOS DE CANCELAMENTO / STAND BY | Eixo X / Categoria: `Motivo Cancelamento[Motivo]`<br>Valores (eixo Y): `_Medidas[Cancelados + Stand by]` (medida) |
| 16, 442, 408×255 | Gráfico de rosca | CATEGORIA DAS MOLÉCULAS | Eixo X / Categoria: `Mapeamento[Categoria Padrão]`<br>Valores (eixo Y): `_Medidas[Moléculas]` (medida) |
| 436, 442, 408×255 | Gráfico de barras agrupadas | MATURIDADE (FASE DA OPORTUNIDADE) | Eixo X / Categoria: `Mapeamento[Fase Oportunidade NN]`<br>Valores (eixo Y): `_Medidas[Moléculas]` (medida) |
| 856, 442, 408×255 | Tabela | OPORTUNIDADES EM DESTAQUE | Valores: `Mapeamento[Molécula]`<br>Valores: `Mapeamento[Fornecedor / Parceiro]`<br>Valores: `Mapeamento[Fase Oportunidade NN]`<br>Valores: `Mapeamento[Indicação]`<br>Valores: `Mapeamento[Status NN]`<br>Valores: `Mapeamento[Situação]` |

---

## Página 5 — 5. Financeiro

| Pos. (x, y, larg × alt) | Visual | Título | Campos |
|---|---|---|---|
| 20, 6, 780×34 | Caixa de texto | Texto: **Visão Financeira \| Valor do Pipeline** |  |
| 820, 14, 444×24 | Caixa de texto | Texto: **VPL, faturamento projetado e margem dos projetos avaliados** |  |
| 16, 56, 240×40 | Segmentação de dados |  | Valores: `Unidade de Negócio[Unidade de Negócio]` |
| 268, 56, 240×40 | Segmentação de dados |  | Valores: `Equipe[Nome]` |
| 520, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Situação]` |
| 772, 56, 240×40 | Segmentação de dados |  | Valores: `Status NN[Status]` |
| 1024, 56, 240×40 | Segmentação de dados |  | Valores: `Calendário[Ano]` |
| 16, 104, 240×72 | Cartão | VPL TOTAL | Valores: `_Medidas[VPL Total]` (medida) |
| 268, 104, 240×72 | Cartão | PEAK SALES | Valores: `_Medidas[Peak Sales]` (medida) |
| 520, 104, 240×72 | Cartão | FAT. LÍQ. 5 ANOS | Valores: `_Medidas[Faturamento 5 Anos]` (medida) |
| 772, 104, 240×72 | Cartão | MARGEM BRUTA MÉDIA | Valores: `_Medidas[Margem Bruta Média]` (medida) |
| 1024, 104, 240×72 | Cartão | % COM DADO FINANCEIRO | Valores: `_Medidas[% Cobertura Financeira]` (medida) |
| 16, 184, 618×245 | Gráfico de barras agrupadas | VPL POR MOLÉCULA | Eixo X / Categoria: `Mapeamento[Molécula]`<br>Valores (eixo Y): `_Medidas[VPL Total]` (medida) |
| 646, 184, 618×245 | Gráfico de colunas agrupadas | VPL POR UNIDADE DE NEGÓCIO | Eixo X / Categoria: `Unidade de Negócio[Unidade de Negócio]`<br>Valores (eixo Y): `_Medidas[VPL Total]` (medida) |
| 16, 437, 618×260 | Tabela | PROJETOS COM DADOS FINANCEIROS | Valores: `Mapeamento[Molécula]`<br>Valores: `Mapeamento[Fornecedor / Parceiro]`<br>Valores: `Mapeamento[Moeda]`<br>Valores: `_Medidas[VPL Total]` (medida)<br>Valores: `_Medidas[Peak Sales]` (medida)<br>Valores: `_Medidas[Margem Bruta Média]` (medida)<br>Valores: `_Medidas[Faturamento 5 Anos]` (medida) |
| 646, 437, 618×260 | Gráfico de colunas agrupadas | VPL POR ESTÁGIO DO FUNIL | Eixo X / Categoria: `Status NN[Status]`<br>Valores (eixo Y): `_Medidas[VPL Total]` (medida) |

---

## Página 6 — 6. Mapeamento Completo

| Pos. (x, y, larg × alt) | Visual | Título | Campos |
|---|---|---|---|
| 20, 6, 780×34 | Caixa de texto | Texto: **Mapeamento Ativo Completo \| Consolidado de todo o time** |  |
| 820, 14, 444×24 | Caixa de texto | Texto: **Todas as colunas, todos os responsáveis — exportável em Excel** |  |
| 16, 56, 240×40 | Segmentação de dados |  | Valores: `Equipe[Nome]` |
| 268, 56, 240×40 | Segmentação de dados |  | Valores: `Unidade de Negócio[Unidade de Negócio]` |
| 520, 56, 240×40 | Segmentação de dados |  | Valores: `Status NN[Status]` |
| 772, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Situação]` |
| 1024, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Categoria Padrão]` |
| 16, 102, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Franquia]` |
| 268, 102, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Entrada]` |
| 520, 102, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Atividade]` |
| 772, 102, 240×40 | Segmentação de dados |  | Valores: `Motivo Cancelamento[Motivo]` |
| 1024, 102, 240×40 | Segmentação de dados |  | Valores: `Calendário[Ano]` |
| 16, 152, 1248×545 | Tabela | MAPEAMENTO ATIVO — BASE COMPLETA | Valores: `Mapeamento[Responsável Final]`<br>Valores: `Mapeamento[Gerência]`<br>Valores: `Mapeamento[Entrada]`<br>Valores: `Mapeamento[Molécula]`<br>Valores: `Mapeamento[Código CI]`<br>Valores: `Mapeamento[Marca do Referência BR]`<br>Valores: `Mapeamento[Fornecedor / Parceiro]`<br>Valores: `Mapeamento[País Fornecedor]`<br>Valores: `Mapeamento[Categoria Padrão]`<br>Valores: `Mapeamento[Coligada Padrão]`<br>Valores: `Mapeamento[Área Terapêutica]`<br>Valores: `Mapeamento[Fase Oportunidade NN]`<br>Valores: `Mapeamento[Indicação]`<br>Valores: `Mapeamento[Forma Farmacêutica]`<br>Valores: `Mapeamento[Status NN]`<br>Valores: `Mapeamento[Situação]`<br>Valores: `Mapeamento[Atividade]`<br>Valores: `Mapeamento[Motivo Padrão]`<br>Valores: `Mapeamento[Detalhamento do cancelamento]`<br>Valores: `Mapeamento[Data de Entrada]`<br>Valores: `Mapeamento[Data Início Efetiva]`<br>Valores: `Mapeamento[Data Fim Efetiva]`<br>Valores: `Mapeamento[Dias em NN]`<br>Valores: `Mapeamento[Complexidade]`<br>Valores: `Mapeamento[Faixa de Duração]`<br>Valores: `Mapeamento[Alerta]` |

---

## Página 7 — 7. Qualidade da Base

| Pos. (x, y, larg × alt) | Visual | Título | Campos |
|---|---|---|---|
| 20, 6, 780×34 | Caixa de texto | Texto: **Qualidade da Base \| O que falta preencher** |  |
| 820, 14, 444×24 | Caixa de texto | Texto: **Cada linha aqui é um campo que impede uma análise** |  |
| 16, 56, 240×40 | Segmentação de dados |  | Valores: `Equipe[Nome]` |
| 268, 56, 240×40 | Segmentação de dados |  | Valores: `Qualidade de Dados[Gravidade]` |
| 520, 56, 240×40 | Segmentação de dados |  | Valores: `Qualidade de Dados[Regra]` |
| 772, 56, 240×40 | Segmentação de dados |  | Valores: `Unidade de Negócio[Unidade de Negócio]` |
| 1024, 56, 240×40 | Segmentação de dados |  | Valores: `Mapeamento[Situação]` |
| 16, 104, 240×72 | Cartão | ÍNDICE DE QUALIDADE | Valores: `_Medidas[Índice de Qualidade]` (medida) |
| 268, 104, 240×72 | Cartão | PENDÊNCIAS | Valores: `_Medidas[Problemas]` (medida) |
| 520, 104, 240×72 | Cartão | PENDÊNCIAS GRAVES | Valores: `_Medidas[Problemas Graves]` (medida) |
| 772, 104, 240×72 | Cartão | PROJETOS AFETADOS | Valores: `_Medidas[Projetos com Problema]` (medida) |
| 1024, 104, 240×72 | Cartão | % SEM DATA DE FIM | Valores: `_Medidas[% Projetos Sem Data de Fim]` (medida) |
| 16, 184, 618×245 | Gráfico de barras agrupadas | PENDÊNCIAS POR REGRA | Eixo X / Categoria: `Qualidade de Dados[Regra]`<br>Valores (eixo Y): `_Medidas[Problemas]` (medida) |
| 646, 184, 618×245 | Gráfico de barras agrupadas | PENDÊNCIAS POR RESPONSÁVEL | Eixo X / Categoria: `Equipe[Nome]`<br>Valores (eixo Y): `_Medidas[Problemas]` (medida) |
| 16, 437, 1248×260 | Tabela | PENDÊNCIAS — DETALHE POR PROJETO | Valores: `Qualidade de Dados[Responsável Final]`<br>Valores: `Qualidade de Dados[Molécula]`<br>Valores: `Qualidade de Dados[Fornecedor / Parceiro]`<br>Valores: `Qualidade de Dados[Regra]`<br>Valores: `Qualidade de Dados[Gravidade]`<br>Valores: `Qualidade de Dados[Impacto]` |
