# Dashboard Novos Negócios — Dossiê de Implantação

> **Se o `.pbit` não abriu no seu Power BI, pule direto para o Caminho B**
> (seção 2). Ele monta o modelo inteiro — 15 tabelas, 76 medidas e 16
> relacionamentos — em um clique, e não depende do formato de arquivo que
> falhou. Leia só a seção do caminho que você for usar.

---

## 0. O que tem em cada pasta

| Pasta / arquivo | Para que serve |
|---|---|
| `dist/Dashboard_Novos_Negocios.pbit` | **Caminho A.** Modelo + 8 páginas prontos. Abre, pede o endereço do SharePoint, carrega sozinho. |
| `dist/Dashboard_Novos_Negocios_PBIP/` | **Caminho A2.** Mesmo conteúdo em formato de projeto (pasta), caso o `.pbit` não abra. |
| `dist/Regua_Esforco_NN.xlsx` | **A régua de horas, em branco.** Preencha com o time e coloque no SharePoint. |
| `modelo/Model.bim` | **Caminho B.** Definição completa do modelo (tabelas, relações, 76 medidas) para o Tabular Editor. |
| `modelo/Layout.json` | Definição das 8 páginas do relatório. |
| `modelo/Section1.m` | Todas as 29 consultas do Power Query num arquivo só. |
| `M/queries/*.pq` | **Caminho C.** Uma consulta por arquivo, pronta para colar no Editor Avançado. |
| `DAX/01_Colunas_Calculadas.dax` | As 7 colunas calculadas. |
| `DAX/02_Medidas.dax` | As 76 medidas. |
| `docs/DOSSIE.md` | Este arquivo (versão em PDF em `docs/pdf/`). |
| `docs/DIAGNOSTICO_BASE.md` | O que encontrei na sua base hoje e o que precisa mudar no processo. |

---

## 1. Caminho A — abrir o `.pbit` (5 minutos)

1. Baixe `dist/Dashboard_Novos_Negocios.pbit` para o seu computador.
2. Dê **dois cliques** no arquivo. O Power BI Desktop abre e mostra uma janela
   de parâmetros.
3. Preencha assim (os valores já vêm preenchidos — só confira):

   | Parâmetro | Valor |
   |---|---|
   | `pSiteSharePoint` | `https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS` |
   | `pBiblioteca` | `Documentos Compartilhados` |
   | `pPastaMapeamentos` | `DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS` |
   | `pPastaHistorico` | `DEMANDAS NN - ALIANÇA/HISTORICO` |
   | `pAbaMapeamento` | `Mapeamento NN` |
   | `pAbaSolicitacoes` | `Solicitações` |
   | `pArquivoRegua` | `Regua_Esforco_NN.xlsx` |
   | `pCapacidadeMensalHoras` | `168` |
   | `pAnoMinimo` | `2022` |
   | `pEstimarFimQuandoAusente` | `true` |

4. Clique **Carregar**.
5. Vai aparecer uma janela pedindo credencial do SharePoint.
   Escolha **Conta organizacional** → **Entrar** → use seu e-mail EMS →
   **Conectar**.
6. Espere a carga (a primeira leva alguns minutos — ele lê todos os arquivos).
7. **Arquivo → Salvar como** → salve como `.pbix` num local seu.

**Se der erro de privacidade** (mensagem com *"Formula.Firewall"* ou
*"níveis de privacidade"*):
`Arquivo → Opções e configurações → Opções → Arquivo atual → Privacidade →`
marque **"Ignorar os níveis de privacidade"** → **OK** → `Página Inicial → Atualizar`.

**Se o arquivo não abrir de jeito nenhum** (mensagem do tipo "não foi possível
abrir o arquivo"), não insista: vá para o **Caminho A2**, e se ainda assim não
funcionar, para o **Caminho B**. O trabalho pesado (as consultas, o modelo e as
medidas) está pronto nos três caminhos — muda só a forma de carregar.

---

## 1b. Caminho A2 — abrir como projeto `.pbip`

1. No Power BI Desktop: `Arquivo → Opções e configurações → Opções →
   Recursos de visualização` → marque **"Salvar arquivos de projeto do Power BI (.pbip)"**
   → **OK** → feche e reabra o Power BI Desktop.
2. Copie a pasta `dist/Dashboard_Novos_Negocios_PBIP` para o seu computador.
3. `Arquivo → Abrir → Procurar` → abra `Dashboard_Novos_Negocios.pbip`.
4. Siga do passo 5 do Caminho A em diante.

---

## 2. Caminho B — montar o modelo com o Tabular Editor (20 minutos)

**É o caminho mais confiável, e o recomendado se o `.pbit` não abriu.**
Ele monta **o modelo inteiro** (15 tabelas + 76 medidas + 16 relacionamentos)
de uma vez, a partir de um arquivo de texto — sem depender de nenhum formato
binário. Só as telas ficam por sua conta, e para elas existe a seção 3.6.

1. Baixe o **Tabular Editor 2** (gratuito): <https://github.com/TabularEditor/TabularEditor/releases>
   → arquivo `TabularEditor.Installer.msi`. Instale.
2. Abra o **Power BI Desktop**, crie um **relatório em branco** e **salve** como
   `Dashboard_Novos_Negocios.pbix`. Deixe aberto.
3. Abra o **Tabular Editor**.
4. `File → Open → From DB…` → em **Local instance**, selecione a instância que
   aparece (é o seu Power BI Desktop aberto) → **OK**.
5. `File → Open → File…` → escolha `modelo/Model.bim`.
   *(Se ele avisar que vai substituir o modelo atual, confirme — o modelo atual está vazio.)*
6. `File → Save` (Ctrl+S). O Tabular Editor grava tudo dentro do Power BI Desktop.
7. Volte ao Power BI Desktop. `Página Inicial → Atualizar`.
   Ele vai pedir os parâmetros e a credencial — responda como no Caminho A.
8. Monte as telas usando a seção 3.6.

**Se o passo 4 não listar nenhuma instância local:** confirme que o Power BI
Desktop está aberto com um arquivo salvo (não pode ser um relatório nunca
salvo). Se ainda assim não aparecer, feche o Tabular Editor, reabra **como
administrador** e repita.

**Se o passo 6 der erro ao salvar:** normalmente é uma tabela que o Power BI
Desktop não conseguiu processar por falta de credencial. Faça o passo 7
primeiro (Atualizar), autentique, e então repita o passo 6.

---

## 3. Caminho C — montagem manual completa

Só faça isso se A e B falharem. São cerca de 2 horas. Siga na ordem exata.

### 3.1 Preparar o Power BI Desktop

1. Abra o Power BI Desktop.
2. `Arquivo → Opções e configurações → Opções → Global → Configurações regionais`:
   **Português (Brasil)**.
3. `Arquivo → Opções e configurações → Opções → Arquivo atual → Privacidade`:
   marque **"Ignorar os níveis de privacidade"**.
4. `Arquivo → Opções e configurações → Opções → Arquivo atual → Carregamento de dados`:
   **desmarque** "Detectar automaticamente novos relacionamentos" e
   **desmarque** "Data/hora automática".
   *(Isso é importante: senão o Power BI cria relacionamentos errados sozinho.)*

### 3.2 Criar os 10 parâmetros

`Página Inicial → Transformar dados` → abre o Editor do Power Query.
Lá dentro: `Página Inicial → Gerenciar Parâmetros → Novo Parâmetro`.

Crie um de cada vez, exatamente com estes nomes (respeite maiúsculas):

| Nome | Tipo | Valor atual |
|---|---|---|
| `pSiteSharePoint` | Texto | `https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS` |
| `pBiblioteca` | Texto | `Documentos Compartilhados` |
| `pPastaMapeamentos` | Texto | `DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS` |
| `pPastaHistorico` | Texto | `DEMANDAS NN - ALIANÇA/HISTORICO` |
| `pAbaMapeamento` | Texto | `Mapeamento NN` |
| `pAbaSolicitacoes` | Texto | `Solicitações` |
| `pArquivoRegua` | Texto | `Regua_Esforco_NN.xlsx` |
| `pCapacidadeMensalHoras` | Número Decimal | `168` |
| `pAnoMinimo` | Número Decimal | `2022` |
| `pEstimarFimQuandoAusente` | Verdadeiro/Falso | `true` |

### 3.3 Criar as 17 consultas

Para **cada** arquivo da pasta `M/queries/`, faça:

1. No Editor do Power Query: `Página Inicial → Nova Fonte → Consulta Nula`.
2. `Página Inicial → Editor Avançado`.
3. **Apague tudo** o que estiver lá.
4. Abra o arquivo `.pq` no Bloco de Notas, **copie tudo**, cole no Editor Avançado.
5. **Concluído**.
6. No painel da esquerda, clique com o botão direito na consulta → **Renomear** →
   use o **nome exato da tabela** da coluna "Nome no Power BI" abaixo.

**Ordem obrigatória** (uma depende da outra):

| # | Arquivo | Nome no Power BI | Carregar? |
|---|---|---|---|
| 1 | `fnUtil.pq` | `fnUtil` | ❌ não |
| 2 | `Fonte_Arquivos.pq` | `Fonte_Arquivos` | ❌ não |
| 2b | `Fonte_Regua.pq` | `Fonte_Regua` | ❌ não |
| 3 | `Mapeamento.pq` | `Mapeamento` | ✅ sim |
| 4 | `Carregamento Mensal.pq` | `Carregamento Mensal` | ✅ sim |
| 5 | `Calendario.pq` | `Calendário` | ✅ sim |
| 6 | `Status NN.pq` | `Status NN` | ✅ sim |
| 7 | `Complexidade.pq` | `Complexidade` | ✅ sim |
| 8 | `Esforco.pq` | `Esforço` | ✅ sim |
| 9 | `Equipe.pq` | `Equipe` | ✅ sim |
| 10 | `Unidade de Negocio.pq` | `Unidade de Negócio` | ✅ sim |
| 11 | `Motivo Cancelamento.pq` | `Motivo Cancelamento` | ✅ sim |
| 12 | `Pais.pq` | `País` | ✅ sim |
| 13 | `Solicitações.pq` | `Solicitações` | ✅ sim |
| 14 | `Qualidade de Dados.pq` | `Qualidade de Dados` | ✅ sim |
| 15 | `Historico Snapshots.pq` | `Histórico Snapshots` | ✅ sim |
| 16 | `Faturamento Projetado.pq` | `Faturamento Projetado` | ✅ sim |
| 17 | `Unidade Referencia.pq` | `Unidade Referência` | ✅ sim |

> ⚠️ **Atenção aos nomes com acento** (`Calendário`, `Esforço`, `País`,
> `Solicitações`, `Unidade de Negócio`, `Histórico Snapshots`). As medidas
> referenciam esses nomes exatamente assim. Um acento faltando quebra tudo.

**"Carregar? ❌ não"** significa: botão direito na consulta →
**desmarque "Habilitar carga"**. São auxiliares, não viram tabela.

Ao terminar: `Página Inicial → Fechar e Aplicar`.

### 3.4 Criar a tabela de medidas

1. `Página Inicial → Inserir dados`.
2. Deixe uma coluna chamada `_` com uma linha contendo `x`.
3. Nome da tabela: `_Medidas` → **Carregar**.
4. No painel Dados, clique com o botão direito na coluna `_` → **Ocultar**.

### 3.5 Criar colunas, relacionamentos e medidas

**a) Colunas calculadas** — abra `DAX/01_Colunas_Calculadas.dax`.
Para cada bloco: selecione a tabela indicada no comentário
(`// ---------- Tabela: X ----------`), então
`Modelagem → Nova coluna`, apague o texto padrão e cole o bloco inteiro
(o nome, o `=` e a expressão). São 7 no total.

**b) Marcar a tabela de datas** — selecione a tabela `Calendário` →
`Modelagem → Marcar como tabela de data` → coluna **Data** → OK.

**c) Ordenação de colunas** — selecione a coluna, depois
`Modelagem → Classificar por coluna`:

| Tabela | Coluna | Classificar por |
|---|---|---|
| `Calendário` | `Mês` | `Nº Mês` |
| `Calendário` | `Mês Abrev` | `Nº Mês` |
| `Calendário` | `Ano-Mês` | `ChaveMes` |
| `Status NN` | `Status` | `Ordem` |
| `Complexidade` | `Complexidade` | `Ordem Complexidade` |
| `Unidade de Negócio` | `Unidade de Negócio` | `Ordem` |
| `Carregamento Mensal` | `Status no Mês` | `Ordem Status Mês` |

**d) Relacionamentos** — `Modelagem → Gerenciar relações → Nova`.
Crie exatamente estes 16. Em todos, **Cardinalidade = Muitos para um (\*:1)**
e **Direção do filtro cruzado = Único**:

| # | Tabela (muitos) | Coluna | Tabela (um) | Coluna | Ativo |
|---|---|---|---|---|---|
| 1 | `Mapeamento` | `Responsável Final` | `Equipe` | `Pessoa` | ✅ |
| 2 | `Mapeamento` | `Status NN` | `Status NN` | `Status` | ✅ |
| 3 | `Mapeamento` | `Categoria Padrão` | `Complexidade` | `Categoria Padrão` | ✅ |
| 4 | `Mapeamento` | `Coligada Padrão` | `Unidade de Negócio` | `Coligada Padrão` | ✅ |
| 5 | `Mapeamento` | `Motivo Padrão` | `Motivo Cancelamento` | `Motivo Padrão` | ✅ |
| 6 | `Mapeamento` | `País Fornecedor` | `País` | `País` | ✅ |
| 7 | `Carregamento Mensal` | `ProjetoID` | `Mapeamento` | `ProjetoID` | ✅ |
| 8 | `Qualidade de Dados` | `ProjetoID` | `Mapeamento` | `ProjetoID` | ✅ |
| 8b | `Faturamento Projetado` | `ProjetoID` | `Mapeamento` | `ProjetoID` | ✅ |
| 9 | `Carregamento Mensal` | `Data Referência` | `Calendário` | `Data` | ✅ |
| 10 | `Mapeamento` | `Data de Entrada` | `Calendário` | `Data` | ❌ **inativo** |
| 11 | `Mapeamento` | `Data Fim Efetiva` | `Calendário` | `Data` | ❌ **inativo** |
| 12 | `Solicitações` | `Data Solicitação` | `Calendário` | `Data` | ✅ |
| 13 | `Solicitações` | `Solicitante` | `Equipe` | `Pessoa` | ✅ |
| 14 | `Histórico Snapshots` | `Data Snapshot` | `Calendário` | `Data` | ✅ |
| 15 | `Histórico Snapshots` | `Responsável Final` | `Equipe` | `Pessoa` | ✅ |

> ⚠️ A tabela **`Unidade Referência` não entra em nenhum relacionamento** —
> ela é desconectada de propósito (explicação na seção 5).
>
> Os relacionamentos **10 e 11 precisam ficar inativos** (desmarque
> "Tornar esta relação ativa"). Se ficarem ativos, filtrar um mês passa a mostrar
> só os projetos que *entraram* naquele mês — e a página de evolução fica errada.

**e) Medidas** — abra `DAX/02_Medidas.dax`. Para cada medida: selecione a tabela
`_Medidas` → `Modelagem → Nova medida` → apague o texto padrão → cole o bloco
(nome + `=` + expressão) → Enter. São 76.
Depois, na faixa `Ferramentas de medida`, aplique o formato indicado no
comentário `// formato:` de cada uma.

### 3.6 Montar as telas

As 7 páginas, com os campos de cada visual, estão em
`docs/ESPECIFICACAO_TELAS.md`. Cada linha é: tipo de visual, posição e
quais campos arrastar para quais áreas.

---

## 4. Publicar e deixar atualizando sozinho

1. No Power BI Desktop: `Página Inicial → Publicar` → escolha o workspace do time.
2. No Power BI Service (navegador), abra o workspace → encontre o **modelo semântico**
   (mesmo nome do arquivo) → `···` → **Configurações**.
3. Em **Credenciais da fonte de dados** → **Editar credenciais** →
   Método: **OAuth2** → **Entrar** com a conta EMS.
   Nível de privacidade: **Organizacional**.
4. Em **Atualização agendada** → ative → fuso **(UTC-03:00) Brasília** →
   adicione os horários (sugestão: **07:00** e **13:00**, dias úteis).
5. Marque **"Enviar e-mail de notificação de falha de atualização"** para você.

> Como a fonte é SharePoint Online (nuvem), **não precisa de gateway**.

---

## 5. Como o modelo está montado

```
                         ┌──────────────┐
                         │  Calendário  │   (tabela de datas)
                         └──────┬───────┘
        ┌───────────────┬───────┴───────┬────────────────┐
        ▼               ▼ (inativo)     ▼                ▼
┌────────────────┐  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐
│  Carregamento  │  │            │  │ Solicitações │  │ Histórico Snapshots │
│     Mensal     │◄─┤ Mapeamento ├─►│              │  │                     │
│ (projeto x mês)│  │ (projeto)  │  └──────┬───────┘  └──────────┬──────────┘
└────────────────┘  └─┬─┬─┬─┬─┬──┘         │                     │
                      │ │ │ │ │            ▼                     ▼
   ┌──────────────────┘ │ │ │ └──────┐  ┌────────┐          ┌────────┐
   │      ┌─────────────┘ │ └────┐   │  │ Equipe │          │ Equipe │
   ▼      ▼               ▼      ▼   ▼  └────────┘          └────────┘
┌────────┐ ┌──────────┐ ┌──────┐ ┌──────────────┐ ┌───────────────────┐
│Status  │ │Complexi- │ │ País │ │  Unidade de  │ │Motivo Cancelamento│
│  NN    │ │  dade    │ │      │ │   Negócio    │ │                   │
└────────┘ └──────────┘ └──────┘ └──────────────┘ └───────────────────┘

  Mapeamento também alimenta, por ProjetoID:
      Qualidade de Dados   e   Faturamento Projetado

  DUAS TABELAS FICAM SOLTAS DE PROPÓSITO:
  ┌──────────┐   consultada por LOOKUPVALUE (Status × Complexidade → horas).
  │ Esforço  │   É a régua que o time preenche no Excel.
  └──────────┘
  ┌────────────────────┐  eixo do gráfico "Franquias de Atuação" no one-page.
  │ Unidade Referência │  Fica desconectada para que aquele gráfico continue
  └────────────────────┘  mostrando TODAS as unidades quando você filtra uma.
```

**As duas tabelas de fato e a diferença entre elas:**

- **`Mapeamento`** = a **foto de hoje**. Uma linha por oportunidade, com o
  status atual. É o que o PBI atual já faz.
- **`Carregamento Mensal`** = **o filme**. Uma linha por projeto **por mês** em
  que ele esteve aberto, com o status que ele tinha **naquele mês**.
  É isto que responde *"o analista tem 10 hoje, mas tinha 30 semana passada"*.

> **Regra de ouro ao montar visuais:** na página de evolução use
> `Carregamento Mensal[Status no Mês]`. Se você usar `Mapeamento[Status NN]`
> (o status de hoje) num gráfico histórico, o resultado sai errado — ele vai
> reescrever o passado com o status atual.

---

## 6. A régua de horas — **está em branco, esperando o time**

O cálculo de carregamento depende de duas definições que **só o time pode dar**.
Por isso elas **não estão embutidas no relatório**: elas moram num arquivo Excel
separado, que vocês preenchem quando decidirem.

**Enquanto o arquivo não for preenchido, nada quebra.** O dashboard inteiro
funciona; apenas os indicadores de horas e de ocupação ficam vazios, e a página
2 mostra um aviso explicando o motivo.

### Como preencher

1. Abra `dist/Regua_Esforco_NN.xlsx`. Ele tem três abas: **Instruções**,
   **Complexidade** e **Esforço**. **Só as células amarelas são para preencher.**

2. **Aba `Complexidade`** — para cada categoria de produto, diga se ela é
   `BAIXO`, `MÉDIO` ou `ALTO` (a célula tem lista suspensa).
   *A pergunta para o time:* "um projeto desta categoria dá mais ou menos
   trabalho que os outros?"

   | Categoria | Complexidade |
   |---|---|
   | INOVADOR RADICAL | _(a preencher)_ |
   | INOVADOR INCREMENTAL | _(a preencher)_ |
   | SIMILAR / GENÉRICO | _(a preencher)_ |
   | … mais 7 categorias | |

3. **Aba `Esforço`** — 27 linhas (9 status × 3 complexidades). Em cada uma,
   quantas **horas por mês** um único projeto naquele status e complexidade
   consome.
   *A pergunta para o time:* "um projeto de complexidade ALTA parado em
   NEGOCIAÇÃO consome quantas horas suas por mês?"

   | Status | Complexidade | Horas Mês |
   |---|---|---|
   | AGUARDANDO INÍCIO | BAIXO | _(a preencher)_ |
   | AGUARDANDO INÍCIO | MÉDIO | _(a preencher)_ |
   | … | | |

   Aceita decimais (1,5). O que ficar em branco vale zero — dá para preencher
   por partes, começando pelos status mais comuns.

4. Salve o arquivo **com o nome `Regua_Esforco_NN.xlsx`** (exatamente assim)
   na **mesma pasta do SharePoint** onde ficam os mapeamentos:
   `Documentos Compartilhados / DEMANDAS NN - ALIANÇA / DEMANDAS NN - ALIANÇAS`

5. No Power BI: `Página Inicial → Atualizar`. As horas aparecem.

> Quer guardar a régua em outra pasta ou com outro nome? Mude o parâmetro
> `pArquivoRegua` (`Transformar dados → Gerenciar Parâmetros`). Ele procura o
> arquivo na mesma pasta dos mapeamentos.

### A capacidade fica em outro lugar

As horas disponíveis por pessoa/mês **não** estão nesse Excel — são o parâmetro
`pCapacidadeMensalHoras` (padrão **168 h**). Para dar capacidade diferente por
pessoa, edite a consulta `Equipe` e troque

```m
each pCapacidadeMensalHoras
```

por algo como

```m
each if [Pessoa] = "FULANO DE TAL" then 120 else pCapacidadeMensalHoras
```

## 7. Histórico de verdade — snapshots mensais (recomendado)

A página "Evolução do Mês" reconstrói o passado a partir das datas que já
existem na planilha. Isso funciona muito bem para **entradas** e para
**avanço de etapa**. Mas tem um limite que você precisa conhecer:

> Na planilha que você me mandou, **apenas 36 de 354 projetos encerrados têm
> "Data de Finalização do Projeto em NN" preenchida**. Sem essa data, não dá
> para saber *em que mês* o projeto saiu da carteira. Hoje o modelo **estima**
> essa data pela última data preenchida na linha (e marca a coluna
> `Fim Estimado?` como verdadeira, para você saber quando está olhando uma
> estimativa).

Existem duas saídas, e o ideal é fazer as duas:

**Saída 1 (processo, custo zero):** passar a exigir o preenchimento de
"Data de Finalização do Projeto em NN" e "Motivo Cancelamento" sempre que um
projeto sair. A página **7. Qualidade da Base** foi feita exatamente para
cobrar isso — ela lista, por responsável, quais projetos estão sem a data.

**Saída 2 (snapshot automático):** um fluxo no Power Automate que, todo dia 1º,
copia os mapeamentos para uma pasta com o nome do mês. Aí o histórico passa a
ser um fato, não uma estimativa.

Receita do fluxo (leva ~15 min para montar, uma única vez):

1. Acesse <https://make.powerautomate.com> → **Criar** → **Fluxo de nuvem agendado**.
2. Nome: `NN - Snapshot mensal do mapeamento`.
   Repetir a cada **1 Mês**, no dia **1**, às **06:00**.
3. **Nova etapa** → pesquise `SharePoint` → ação **Obter arquivos (somente propriedades)**.
   - Endereço do site: `https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS`
   - Biblioteca: `Documentos Compartilhados`
   - Pasta: `/DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS`
4. **Nova etapa** → **Obter conteúdo do arquivo** (SharePoint).
   - Identificador: escolha o campo dinâmico **Identificador** do passo anterior.
   - *(O Power Automate vai criar um "Aplicar a cada" automaticamente.)*
5. Ainda dentro do "Aplicar a cada" → **Criar arquivo** (SharePoint).
   - Endereço do site: o mesmo.
   - Caminho da pasta:
     `/Documentos Compartilhados/DEMANDAS NN - ALIANÇA/HISTORICO/` e, **colado**
     logo depois, uma **Expressão**:
     `formatDateTime(addDays(utcNow(),-1),'yyyy-MM')`
   - Nome do arquivo: campo dinâmico **Nome com extensão**.
   - Conteúdo do arquivo: campo dinâmico **Conteúdo do arquivo**.
6. **Salvar**.

Pronto: toda virada de mês nasce uma pasta `2026-09`, `2026-10`… e a consulta
`Histórico Snapshots` passa a lê-las sozinha. Enquanto a pasta não existir,
a consulta devolve tabela vazia e **nada quebra**.

---

## 8. O que ainda depende de você

1. **A régua de esforço (seção 6).** É a única coisa que falta para os
   indicadores de horas e ocupação ligarem. Enquanto isso, todas as outras
   páginas já funcionam.

2. **"Stand by" não conta horas** na medida `Horas Empenhadas`. Deixei a medida
   alternativa `Horas Empenhadas (com Stand by)` caso vocês discordem — e vale a
   discussão: **152 dos 354 projetos** do seu arquivo estão em stand by. Se um
   projeto em stand by ainda consome acompanhamento, a conta atual subestima o
   carregamento do time.

3. **Capacidade de 168 h/mês para todos** (seção 6, final).

4. **A data de finalização dos projetos** (seção 7). É o único campo que falta
   para o histórico mensal deixar de ser estimativa.

---

## 9. O que foi removido e por quê

Ajustes feitos na revisão, para o relatório não carregar visual que não decide
nada:

| Página | Saiu | Motivo | Entrou no lugar |
|---|---|---|---|
| 1. Visão Geral | **Mapa de países** | Reproduzia a origem dos fornecedores sem gerar decisão; o país continua disponível como coluna na base completa | **Origem da Oportunidade** (Prospecção Ativa, Parceiro, Wishlist, Feiras…) — mostra de onde o pipeline nasce |
| 1. Visão Geral | Rosca "Situação dos Projetos" | Repetia exatamente o que os três cartões do topo já diziam | Espaço devolvido à tabela, que ficou maior |
| 1. Visão Geral | Rosca "% Projetos x Coligada" | 11 categorias numa rosca são ilegíveis | Mesmo dado em **barras ordenadas** |
| 2. Carregamento | Cartão "% Ocupação" | Duplicava o medidor logo abaixo | Cartão **Horas Disponíveis** |
| 3. Evolução | Colunas empilhadas do funil | Com 9 status × muitos meses vira serrilha | **Área empilhada**, que lê composição ao longo do tempo |
| 6. Financeiro | "VPL por Estágio do Funil" | Só 7 projetos têm VPL — o gráfico nascia vazio | **Faturamento líquido projetado (DRE, 5 anos)**, que usa as 5 colunas de DRE que estavam sem uso |
| 6. Financeiro | Top 15 de VPL | Mais linhas do que dados existentes | Top 10 |

E o report de unidade de negócio **virou duas páginas**, espelhando a estrutura
dos seus documentos atuais:

- **Página 4 — Report por Unidade de Negócio**: o one-page. O filtro
  `▼ UNIDADE DE NEGÓCIO` troca a unidade inteira — NR, SNC (EMS Prescrição +
  franquia NEURO), USK, Ofta, OTC, Brace, Legrand, ou qualquer outra que
  apareça na base. Ganhou o gráfico de **Área Terapêutica** e um **resumo em
  texto** pronto para colar no slide.
- **Página 5 — Carteira da Unidade**: o detalhe. Carregamento de moléculas por
  mês, área terapêutica × situação, e a tabela de oportunidades.

> **Detalhe técnico que vale conhecer:** no one-page, o gráfico
> *"Franquias de Atuação de NN (todas as unidades)"* **não** é filtrado quando
> você seleciona uma unidade — ele continua mostrando o bolo inteiro, que é o
> contraste que dá a leitura *"esta BU representou X% do que NN avaliou"*.
> Isso é feito pela tabela desconectada `Unidade Referência`. Se você conectá-la
> por engano a alguma outra tabela, esse gráfico para de funcionar.
