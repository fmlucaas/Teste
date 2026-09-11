# Dashboard Novos Negócios — Dossiê de Implantação

> **Leia só a seção do caminho que funcionar.** Comece pelo **Caminho A**.
> Se ele abrir, você terminou em 5 minutos e pode pular para a seção 4.

---

## 0. O que tem em cada pasta

| Pasta / arquivo | Para que serve |
|---|---|
| `dist/Dashboard_Novos_Negocios.pbit` | **Caminho A.** Modelo + 7 páginas prontos. Abre, pede o endereço do SharePoint, carrega sozinho. |
| `dist/Dashboard_Novos_Negocios_PBIP/` | **Caminho A2.** Mesmo conteúdo em formato de projeto (pasta), caso o `.pbit` não abra. |
| `modelo/Model.bim` | **Caminho B.** Definição completa do modelo (tabelas, relações, 60 medidas) para o Tabular Editor. |
| `modelo/Layout.json` | Definição das 7 páginas do relatório. |
| `modelo/Section1.m` | Todas as 25 consultas do Power Query num arquivo só. |
| `M/queries/*.pq` | **Caminho C.** Uma consulta por arquivo, pronta para colar no Editor Avançado. |
| `DAX/01_Colunas_Calculadas.dax` | As 7 colunas calculadas. |
| `DAX/02_Medidas.dax` | As 60 medidas. |
| `docs/DOSSIE.md` | Este arquivo. |
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

Esse caminho monta **o modelo inteiro** (13 tabelas + 60 medidas + 15
relacionamentos) de uma vez. Só as telas ficam por sua conta — e para elas
existe a seção 3.6.

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

### 3.2 Criar os 9 parâmetros

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
| `pCapacidadeMensalHoras` | Número Decimal | `168` |
| `pAnoMinimo` | Número Decimal | `2022` |
| `pEstimarFimQuandoAusente` | Verdadeiro/Falso | `true` |

### 3.3 Criar as 15 consultas

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
Crie exatamente estes 15. Em todos, **Cardinalidade = Muitos para um (\*:1)**
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
| 9 | `Carregamento Mensal` | `Data Referência` | `Calendário` | `Data` | ✅ |
| 10 | `Mapeamento` | `Data de Entrada` | `Calendário` | `Data` | ❌ **inativo** |
| 11 | `Mapeamento` | `Data Fim Efetiva` | `Calendário` | `Data` | ❌ **inativo** |
| 12 | `Solicitações` | `Data Solicitação` | `Calendário` | `Data` | ✅ |
| 13 | `Solicitações` | `Solicitante` | `Equipe` | `Pessoa` | ✅ |
| 14 | `Histórico Snapshots` | `Data Snapshot` | `Calendário` | `Data` | ✅ |
| 15 | `Histórico Snapshots` | `Responsável Final` | `Equipe` | `Pessoa` | ✅ |

> Os relacionamentos **10 e 11 precisam ficar inativos** (desmarque
> "Tornar esta relação ativa"). Se ficarem ativos, filtrar um mês passa a mostrar
> só os projetos que *entraram* naquele mês — e a página de evolução fica errada.

**e) Medidas** — abra `DAX/02_Medidas.dax`. Para cada medida: selecione a tabela
`_Medidas` → `Modelagem → Nova medida` → apague o texto padrão → cole o bloco
(nome + `=` + expressão) → Enter. São 60.
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
                    │  Calendário  │  (tabela de datas)
                    └──────┬───────┘
            ┌──────────────┼──────────────┬─────────────────┐
            ▼              ▼(inativo)     ▼                 ▼
  ┌───────────────────┐  ┌────────────┐  ┌──────────────┐ ┌─────────────────────┐
  │ Carregamento      │  │            │  │ Solicitações │ │ Histórico Snapshots │
  │ Mensal            │◄─┤ Mapeamento ├─►│              │ │                     │
  │ (1 linha por      │  │ (1 linha   │  └──────┬───────┘ └──────────┬──────────┘
  │  projeto x mês)   │  │  por       │         │                    │
  └───────────────────┘  │  projeto)  │         ▼                    ▼
                         └─┬──┬──┬──┬─┘      ┌────────┐         ┌────────┐
                           │  │  │  │        │ Equipe │◄────────┤ Equipe │
     ┌─────────────────────┘  │  │  └──────┐ └────────┘         └────────┘
     ▼            ▼           ▼  ▼         ▼
┌──────────┐ ┌─────────┐ ┌────────────┐ ┌──────┐ ┌───────────────────┐
│ Status NN│ │Complexi-│ │Unidade de  │ │ País │ │Motivo Cancelamento│
│          │ │ dade    │ │ Negócio    │ │      │ │                   │
└──────────┘ └─────────┘ └────────────┘ └──────┘ └───────────────────┘

  `Esforço` fica solta de propósito: é consultada por LOOKUPVALUE
  (Status x Complexidade → horas/mês), não por relacionamento.
  `Qualidade de Dados` liga em Mapeamento por ProjetoID.
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

## 6. A régua de horas — onde ajustar

O PBI atual calcula horas por uma régua que está dentro dele e que eu não
consigo ler. Então **montei uma régua nova, explícita e editável**. Ela tem
duas partes:

**a) Categoria → Complexidade** (arquivo `M/queries/Complexidade.pq`):

| Categoria | Complexidade |
|---|---|
| Inovador Radical, Biológico, M&A | ALTO |
| Inovador Incremental, Produto para Saúde, Cosmético | MÉDIO |
| Similar / Genérico, Alimento / Suplemento, Fitoterápico | BAIXO |

**b) Status × Complexidade → horas/mês** (arquivo `M/queries/Esforco.pq`):

| Status | Baixo | Médio | Alto |
|---|---|---|---|
| Aguardando Início | 0,5 | 1 | 1,5 |
| Prospecção | 2 | 3 | 4 |
| CDA | 1 | 1,5 | 2 |
| Av. Técnica Inicial | 4 | 6 | 8 |
| Av. Marketing | 3 | 4 | 6 |
| Negociação | 6 | 8 | 12 |
| Aprovação Summary | 3 | 4 | 6 |
| Term Sheet | 5 | 7 | 10 |
| Contrato | 6 | 8 | 12 |

> **Estes números são uma proposta minha, não um dado da sua base.**
> Rode uma reunião de 30 minutos com o time perguntando
> *"quantas horas por mês um projeto nesse status realmente consome?"* e
> substitua. Para editar: `Página Inicial → Transformar dados` → consulta
> `Esforço` → `Editor Avançado` → troque os números → `Fechar e Aplicar`.

A **capacidade** (168 h/mês) está no parâmetro `pCapacidadeMensalHoras`.
Para dar capacidade diferente por pessoa, edite a consulta `Equipe` e troque
`each pCapacidadeMensalHoras` por um `if [Pessoa] = "FULANO" then 120 else 168`.

---

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

## 8. Perguntas que preciso que você responda

Estas decisões eu tomei sozinho para não travar a entrega. Vale revisar:

1. **A régua de horas da seção 6** — os números são chute meu, calibrado pelo
   bom senso. Os do PBI atual estão dentro dele e não consegui lê-los.
2. **Complexidade = Categoria.** Assumi que "Inovador Radical" é alto e
   "Similar/Genérico" é baixo. Se o time tem outro critério (por exemplo, país
   do fornecedor ou forma farmacêutica), dá para trocar na consulta `Complexidade`.
3. **"Stand by" não conta horas** na medida `Horas Empenhadas`. Deixei uma
   medida alternativa (`Horas Empenhadas (com Stand by)`) caso você discorde —
   e é uma boa discussão, porque 152 dos 354 projetos do seu arquivo estão em
   stand by.
4. **Capacidade de 168 h/mês para todos.** Se há gente em tempo parcial ou com
   outras atribuições, ajuste como descrito na seção 6.
