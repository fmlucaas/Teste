# Diagnóstico da base atual

Análise do arquivo `Mapeamento_Lucas_Medina.xlsx` (354 oportunidades preenchidas,
91 colunas, aba `Mapeamento NN`). Como todos os mapeamentos seguem o mesmo
modelo, o que vale aqui deve valer para os demais.

---

## 1. Colunas em desuso — sua percepção está certa, e dá para medir

Das **91 colunas**, **23 estão 100% vazias** (21 nomeadas + 2 sem cabeçalho) e
outras estão praticamente vazias.
O padrão é nítido: **tudo que é etapa de Projetos & Alianças (pós-handover) nunca
é preenchido no mapeamento de Novos Negócios.**

### As 21 totalmente vazias (0 de 354 linhas) — candidatas a remoção imediata

| Coluna | Bloco |
|---|---|
| Data de Aprovação Summary pelo PCA | Summary |
| N° Chamado Term Sheet | Term Sheet |
| N° Chamado Contrato | Contrato |
| Início elaboração resumo de contrato | Contrato |
| Data conclusão resumo de contrato | Contrato |
| Data de assinatura de resumo de contrato | Contrato |
| Anotações (Sumário) | Contrato |
| Recebimento Dossiê | P&A |
| Data Conclusão Due Diligence | P&A |
| Data Início elaboração Regulatory Plan | P&A |
| Data Conclusão Elaboração Regulatory Plan | P&A |
| Data reunião de consenso regulatory Plan com parceiro | P&A |
| Kick Off Pré Submissão | P&A |
| Data de início de adequação dossiê | P&A |
| Data de término adequação dossiê | P&A |
| Handover P&A para PSO Novos Produtos | P&A |
| Data Protocolo ANVISA | P&A |
| Data Aprovação ANVISA | P&A |
| Início lançamento | P&A |
| Término lançamento (1 lote em estoque) | P&A |
| Histórico / comentários (a segunda) | Duplicada |

### Quase vazias (1 a 8 linhas de 354) — o funil morre antes do fim

| Coluna | Preenchidas |
|---|---|
| Data de Retomada do Projeto | 1 |
| Data Concl. Term Sheet | 1 |
| Data Assinatura Contrato | 1 |
| Anotações (Contrato) | 1 |
| Handover NN para Projetos & Alianças | 1 |
| Apresentação ao parceiro / Kick Off Iniciação / Kick Off DD / Início DD | 1 cada |
| Data Conclusão Summary | 2 |
| Data estimada para Lançamento | 2 |
| Data de Início Summary / Data início Term Sheet | 4 cada |
| Início discussão contratual | 6-8 |
| VPL, Peak Sales, DRE Ano1–Ano5 | 7-8 |

**Leitura:** o funil registrado vai até "Negociação" com consistência e some
depois disso. Os status `INICIAÇÃO`, `DUE DILIGENCE`, `REGULATORY PLAN`,
`PRÉ-SUBMISSÃO`, `AVALIAÇÃO ANVISA`, `LANÇAMENTO`, `LANÇADO`,
`EM DESCONTINUAÇÃO` e `DESCONTINUADO` existem na lista de validação da aba
`PAÍS`, mas **nenhum projeto está neles**.

**O que fiz:** mantive esses status na dimensão `Status NN`, marcados com
`Em Uso = Falso`, agrupados como `Pós-NN (P&A)`. Assim eles não poluem os
gráficos (é só filtrar `Em Uso = Verdadeiro`) e, se um dia voltarem a ser usados,
o modelo já os reconhece.

---

## 2. Divergências de digitação — corrigidas automaticamente

A mesma informação aparece escrita de várias formas. Isso **quebra qualquer
contagem** no Power BI, porque ele trata cada grafia como uma categoria
diferente. Encontrei e tratei:

| Campo | Grafias encontradas | Padronizado para |
|---|---|---|
| Motivo Cancelamento | `Indisponibilidade de Parceria` (81) e `INDISPONIBILIDADE DE PARCERIA` (6) | uma só categoria (87) |
| Motivo Cancelamento | `Inviabilidade Área Médica` (60) e `INVIABILIDADE MÉDICA` (3) | uma só (63) |
| Motivo Cancelamento | `Inviabilidade Financeira` (24) e `INVIABILIDADE FINANCEIRA` (5) | uma só (29) |
| Motivo Cancelamento | mais 6 pares no mesmo padrão | — |
| Categoria | `INOVADOR INCREMENTAL` (65) e `INOVAÇÃO INCREMENTAL` (1) | uma só |
| Coligada | `BRACE PHARMA` (1) e `BRACE PHARM` (1) | uma só |
| Coligada | `Legrand` e `LEGRAND` | uma só |
| Fase Oportunidade | `PRÉ REGISTRO` (17) e `PRÉ-REGISTRO` (1) | uma só |
| CDA Status | `Concluído` / `concluído` / `CONCLUÍDO` / `Assinado.` | normalizado |
| Entrada | `FEIRAS / CONGRESSOS` (11) e `FEIRAS/CONGRESSOS` (6) | uma só (17) |
| Entrada | `WISHLIST / MARKETING` (30) e `WISHLIST MARKETING` (1) | uma só |

Sem esse tratamento, o report de motivos de cancelamento por unidade de negócio
sai com os números divididos — que é exatamente o tipo de erro difícil de notar
numa apresentação.

---

## 3. Datas gravadas como texto

**53 células de data** estão como texto ou número cru, não como data.
As piores: *Data de Entrada* (13 casos) e *Data de Início do Projeto* (12).
Exemplos reais:

- `"26/07/2022"` (13 casos em *Data de Entrada*) — texto em formato brasileiro
- `"27/05.2026"` — erro de digitação: ponto no lugar da barra
- `"1913-10-16"` em *Data Concl. Term Sheet* — provavelmente um `45821` digitado
  numa célula formatada como data
- `5039` em *Início discussão contratual* — número serial cru
- `45821` e `45784` em *Anotações (Term Sheet)* — datas na coluna errada
- Uma célula com espaço não separável (`&nbsp;`), que parece vazia mas não é

**O que fiz:** a função `fnUtil[Data]` converte todos esses casos e
**descarta anos fora da faixa 2000–2040**, eliminando o `1913` e o `5039` sem
precisar mexer na planilha.

---

## 4. O ponto crítico: sem data de saída não há histórico de saída

| Situação | Projetos | Com "Data de Finalização" |
|---|---|---|
| Não (encerrado) | 188 | **24** |
| Stand by | 152 | **14** |
| Sim (ativo) | 14 | 1 |

**265 projetos saíram do carregamento sem registrar quando.**

Isso é exatamente o que impede o report que você descreveu — saber que o
analista tinha 30 projetos e 20 foram cancelados **naquele mês**. A data de
entrada está bem preenchida (340 de 354), então o *lado das entradas* é
confiável; o *lado das saídas* não.

**O que fiz:**
1. O modelo **estima** a data de saída pela última data preenchida na linha,
   e marca a coluna `Fim Estimado?` para você saber quando está olhando uma
   estimativa. (Dá para desligar no parâmetro `pEstimarFimQuandoAusente`.)
2. A página **7. Qualidade da Base** lista, por responsável e por projeto,
   exatamente quais estão sem a data — é a lista de cobrança.
3. A seção 7 do dossiê traz o fluxo de snapshot mensal, que resolve de vez
   daqui para frente.

---

## 5. A visão financeira existe, mas está rasa

| Campo | Preenchidos (de 354) |
|---|---|
| Moeda | 14 |
| Preço de Fornecimento | 13 (7 numéricos, 6 em texto livre) |
| Margem Bruta (%) | 11 |
| VPL (R$) | 7 |
| Peak Sales | 8 |
| DRE Ano 1 a 5 | 8 |

A página **5. Financeiro** está montada e funciona — mas hoje ela vai falar
sobre 7 a 8 projetos. Faz sentido: só projetos que chegam em negociação avançada
ganham número. O indicador `% Cobertura Financeira` mostra essa proporção
explicitamente, e a regra *"Em Negociação sem dado financeiro"* na página de
qualidade aponta quem já deveria ter preenchido.

`Preço de Fornecimento` tem conteúdo como `"1 g: 205,93 / 200 mg: 61,93"` —
dois preços numa célula. Esses casos entram como nulo (a função de conversão
não adivinha qual dos dois usar). Se isso for frequente, vale desmembrar em
duas colunas na planilha.

---

## 6. Abas ocultas que não estão sendo aproveitadas

| Aba | Situação | Recomendação |
|---|---|---|
| `Solicitações` | **93 linhas com dados reais** — demandas às áreas Médica, Patentes, Regulatória e Econômicos, com data de solicitação, previsão e recebimento | **Incorporei.** Virou a página de SLA das áreas técnicas. É um indicador de gargalo que hoje ninguém vê. |
| `Análise de risco` | Estrutura montada, **zero linhas** | Ou passa a ser usada, ou remova — hoje só confunde |
| `Cópia de Obsoleto` | 1.292 linhas de um modelo antigo de mapeamento | Histórico morto. Arquive fora da planilha viva |
| `Planejamento - Projetos de melhoria` | Cabeçalho montado, **zero linhas** | Idem "Análise de risco" |
| `Página5` | 7 produtos EMS Marcas com faturamento 2022-2026 | Não tem relação com mapeamento ativo — mover para outro arquivo |
| `PAÍS` | Listas de validação (países + ISO-3, formas farmacêuticas, áreas terapêuticas, responsáveis, status) | **Aproveitei o ISO-3** para o mapa acertar 100% dos países |
| `MOTIVO CANCELAMENTO` | Dicionário dos 12 motivos com exemplos | Excelente documentação — usei como base da dimensão de motivos |

---

## 7. Resumo das recomendações de processo

Em ordem de impacto:

1. **Exigir "Data de Finalização do Projeto em NN"** ao encerrar ou colocar em
   stand by. É o único campo que falta para o histórico deixar de ser estimativa.
2. **Ligar o snapshot mensal** (seção 7 do dossiê). 15 minutos de configuração,
   uma vez só.
3. **Travar as listas de validação** nas colunas Motivo, Categoria, Coligada,
   Fase e Status em todos os arquivos, apontando para a aba `PAÍS`. Isso mata as
   divergências de digitação na origem. Hoje o Power BI corrige, mas corrigir na
   origem é melhor.
4. **Formatar as colunas de data como Data** (não Texto) em todos os arquivos.
5. **Remover as 23 colunas 100% vazias** (21 de P&A/contrato + 2 sem cabeçalho) — ou, se a intenção é usá-las,
   definir quem preenche e quando.
6. **Preencher Coligada e Área Terapêutica sempre** — são os dois eixos dos
   reports de unidade de negócio. Hoje 15 e 17 projetos estão sem.
