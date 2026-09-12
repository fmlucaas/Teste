# Parte 0 — Antes de começar

## 0.1 O que você vai construir

Um relatório do Power BI com **8 telas**, que lê **sozinho** todas as planilhas de
mapeamento ativo da pasta do SharePoint e se atualiza **todo dia de manhã**, sem
ninguém precisar abrir nada.

| Tela | Responde a quê |
|---|---|
| 1. Visão Geral | Quantas oportunidades existem hoje, em que status, de que categoria e de onde vieram |
| 2. Carregamento do Time | Quanto cada pessoa tem na mão, contra a capacidade dela |
| 3. Evolução do Mês | Com quantos o mês começou, quantos entraram, quantos saíram, com quantos terminou |
| 4. Report por Unidade | O one-page de qualquer unidade de negócio — troca no filtro |
| 5. Carteira da Unidade | A lista de oportunidades por trás do one-page |
| 6. Financeiro | VPL, peak sales, faturamento projetado e margem |
| 7. Mapeamento Completo | O consolidado de todos os mapeamentos, exportável para Excel |
| 8. Qualidade da Base | O que falta preencher, por responsável |

> **Antes de começar, veja o resultado pronto.** Abra este endereço no navegador:
> **https://claude.ai/code/artifact/011ee2d5-3d93-4cae-80ef-84412edb2b76**
> É uma maquete navegável das 8 telas, com dados reais do mapeamento. Serve para
> você saber aonde está indo e conferir se o que montou ficou igual.

## 0.2 O que você precisa ter

1. Um computador com **Windows**.
2. **Power BI Desktop** instalado (a Parte 1.1 ensina).
3. Acesso ao SharePoint **https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS**
   com o seu login da EMS. Se você já consegue abrir a pasta dos mapeamentos pelo
   navegador, o acesso está certo.
4. Os **3 arquivos de texto** que vieram junto com este dossiê:
   `1_Mapeamento.pq`, `2_Carregamento_Mensal.pq` e `3_Calendario.pq`.
5. Cerca de **3 horas**, que podem ser divididas em vários dias. O trabalho fica
   salvo no arquivo.

> **CUIDADO, este é o erro que mais estraga tudo:** abra os arquivos `.pq` **sempre
> no Bloco de Notas**, nunca no Word. O Word troca as aspas retas `"` por aspas
> curvas e o Power BI recusa o texto inteiro, com um erro que não explica a causa.

> Não é preciso saber programar. Você vai **copiar e colar** textos prontos e
> **arrastar** campos com o mouse. Nada mais que isso.

## 0.3 Como ler este dossiê

| Quando você vir | Significa |
|---|---|
| Texto em **negrito** | O nome exato de um botão, menu ou janela. Procure por ele escrito assim na tela. |
| `Texto em cinza` | Algo para digitar ou copiar exatamente como está, inclusive acentos e espaços. |
| `Menu → Submenu` | Clique no primeiro, depois no segundo. |
| Uma figura numerada | O desenho da tela. Os círculos vermelhos são a ordem dos cliques. |
| Uma caixa amarela | Um aviso importante. Leia antes de continuar. |
| Uma caixa vermelha | Um erro comum. Leia com atenção. |

> **As figuras são desenhos**, não fotografias da sua tela. Fiz assim porque a
> aparência muda um pouco de computador para computador. O que importa é a
> **posição** e o **nome escrito** — esses são iguais em todas as máquinas.

## 0.4 As 12 palavras do Power BI

Você vai encontrar estas palavras o tempo todo. Leia uma vez e volte aqui quando
precisar.

| Palavra | O que é, em português comum |
|---|---|
| **Consulta** | Uma receita que diz de onde vêm os dados e como limpá-los. Você vai criar 3. |
| **Tabela** | O resultado de uma consulta: linhas e colunas, como no Excel. |
| **Coluna** | Um campo da tabela: Molécula, Status, Data de Entrada. |
| **Medida** | Uma conta pronta: "quantos projetos", "quantas horas". Não é coluna — é cálculo. |
| **Modelo** | O desenho de como as tabelas se conversam. |
| **Relação (ou ligação)** | A linha que liga duas tabelas por um campo em comum. |
| **Visual** | Qualquer gráfico, tabela ou cartão dentro da tela. |
| **Segmentação de dados** | O filtro que fica na tela para o usuário mexer. |
| **Página** | Cada tela do relatório. Ficam em abas na parte de baixo. |
| **Poço (campo do visual)** | A caixinha onde você solta um campo: Eixo X, Eixo Y, Valores. |
| **Publicar** | Mandar o relatório para a nuvem, para os outros verem. |
| **Workspace** | A pasta na nuvem onde o relatório mora. |

## 0.5 O mapa da tela

Antes de qualquer coisa, entenda onde ficam as cinco áreas. Você vai voltar
a esta figura muitas vezes.

![As cinco áreas do Power BI Desktop](docs/figuras/01_mapa_tela.png)

\pagebreak

# Parte 1 — Preparar o Power BI

## 1.1 Instalar (só se você ainda não tem)

1. Aperte a tecla **Windows** do teclado e digite `Microsoft Store`. Aperte Enter.
2. Na lupa de busca da loja, digite `Power BI Desktop` e aperte Enter.
3. Clique no resultado **Power BI Desktop** (o ícone é amarelo).
4. Clique em **Obter** ou **Instalar**. É gratuito.
5. Quando terminar, clique em **Abrir**.
6. Se ele pedir e-mail, coloque o seu e-mail da EMS.

## 1.2 Conferir a versão

1. Com o Power BI aberto, clique em **Arquivo** (o primeiro item da faixa de cima).
2. Clique em **Sobre**.
3. Deve aparecer algo como `Versão: 2.157.1354.0 64-bit (agosto de 2026)`.

Se a sua versão for **mais nova**, tudo funciona igual — só alguns nomes de botão
podem mudar de lugar. Se for **mais antiga**, atualize pela Microsoft Store antes
de continuar.

## 1.3 Três ajustes obrigatórios

> Estes três ajustes evitam os dois erros que mais travam iniciantes. Faça agora,
> antes de qualquer outra coisa.

### Passo 1 — Abrir a janela de Opções

![Caminho até a janela de Opções](docs/figuras/02_opcoes_menu.png)

1. Clique em **Arquivo**.
2. Clique em **Opções e configurações**.
3. Clique em **Opções**. Abre uma janela grande, com uma lista do lado esquerdo.

### Passo 2 — Privacidade

![Janela Opções, seção Privacidade](docs/figuras/03_opcoes_privacidade.png)

1. Na lista da esquerda, role até encontrar o título **ARQUIVO ATUAL**.
   Logo abaixo dele, clique em **Privacidade**.
2. Do lado direito aparecem três bolinhas. Marque a terceira:
   **Sempre ignorar as configurações de nível de Privacidade**.
3. **Não feche a janela ainda.** Vá para o passo 3.

> **Por que isso?** Sem esse ajuste, o Power BI dá um erro chamado
> *Formula.Firewall* quando tenta juntar dados de vários arquivos. Como todas as
> suas planilhas vêm da mesma pasta da empresa, não há risco nenhum em ignorar.

### Passo 3 — Carregamento de Dados

![Janela Opções, seção Carregamento de Dados](docs/figuras/04_opcoes_carregamento.png)

1. Ainda na lista da esquerda, embaixo de **ARQUIVO ATUAL**, clique em
   **Carregamento de Dados**.
2. **Desmarque** a caixinha **Detectar automaticamente novas relações depois que
   os dados forem carregados**.
3. Role um pouco e **desmarque** a caixinha **Data/hora automática para novos
   arquivos**.
4. Agora sim, clique em **OK**.
5. Se ele avisar que precisa reabrir o arquivo, aceite.

> **Por que isso?** A primeira opção faz o Power BI inventar ligações erradas
> entre as tabelas. A segunda cria dezenas de tabelas de data escondidas, que
> deixam o arquivo lento e confundem os gráficos.

## 1.4 Salvar o arquivo antes de começar

1. Aperte **Ctrl+S**.
2. Escolha uma pasta no seu computador onde você ache fácil (exemplo: Documentos).
3. Em **Nome do arquivo**, digite: `Dashboard Novos Negocios`
4. Clique em **Salvar**.

> **Salve com Ctrl+S a cada parte concluída.** O Power BI não salva sozinho.
\pagebreak

# Parte 2 — Conectar às planilhas do SharePoint

## 2.1 O que vai acontecer aqui

Você vai criar **3 consultas**. Cada uma é um texto pronto que você cola. Elas fazem:

| Consulta | O que faz |
|---|---|
| `Mapeamento` | Entra no SharePoint, abre **todas** as planilhas da pasta, junta tudo numa tabela só e limpa os erros de digitação e de data |
| `Carregamento Mensal` | A partir do Mapeamento, monta o histórico mês a mês de cada projeto |
| `Calendário` | Cria a tabela de datas que o Power BI usa para comparar meses e anos |

> **Você não precisa entender o texto que vai colar.** Ele já está pronto e testado.
> Se um dia o caminho da pasta mudar, a Parte 7.2 mostra as 4 linhas que se altera.

## 2.2 Abrir o Editor do Power Query

![Botão Transformar dados](docs/figuras/05_transformar_dados.png)

1. Na faixa de cima, clique na aba **Página Inicial**.
2. Clique em **Transformar dados** (o ícone é uma tabela com uma engrenagem).
3. **Abre uma janela nova**, chamada **Editor do Power Query**. É nela que você
   vai trabalhar nesta parte inteira.

> **Atenção:** são duas janelas diferentes agora. O Power BI Desktop ficou atrás.
> Não feche nenhuma das duas.

## 2.3 Consulta 1 — Mapeamento

### Criar a consulta em branco

![Nova Fonte → Consulta Nula](docs/figuras/06_consulta_nula.png)

1. Na janela do **Editor do Power Query**, clique na aba **Página Inicial**.
2. Clique em **Nova Fonte**.
3. Abre um menu. **Role até o fim** e clique no último item: **Consulta Nula**.
4. Do lado esquerdo aparece uma consulta chamada **Consulta1**.

### Colar o texto

![Editor Avançado](docs/figuras/07_editor_avancado.png)

1. Ainda na aba **Página Inicial**, clique em **Editor Avançado**.
   Abre uma janela com uma caixa branca e um pouco de texto dentro.
2. Clique **dentro da caixa branca**.
3. Aperte **Ctrl+A** (seleciona tudo que está lá) e depois **Delete**.
   A caixa fica vazia.
4. Agora abra o arquivo **`1_Mapeamento.pq`**:
   - Vá até a pasta onde você salvou os arquivos.
   - Clique com o **botão direito** no arquivo `1_Mapeamento.pq`.
   - Escolha **Abrir com** → **Bloco de Notas**.
5. No Bloco de Notas: aperte **Ctrl+A** e depois **Ctrl+C**.
6. Volte para a janela do **Editor Avançado**, clique dentro da caixa branca
   e aperte **Ctrl+V**.
7. Olhe a **faixa cinza embaixo da caixa**. Ela precisa dizer:
   **Nenhum erro de sintaxe foi detectado.**
8. Clique em **Concluído**.

> **CUIDADO:** se a faixa de baixo mostrar um erro em vermelho, você colou só
> parte do texto. Repita os passos 2 a 6 com calma, garantindo o **Ctrl+A** no
> Bloco de Notas antes do **Ctrl+C**.

### Dar o nome certo

![Renomear a consulta](docs/figuras/08_renomear.png)

1. Do lado esquerdo, clique com o **botão direito** em **Consulta1**.
2. Clique em **Renomear**.
3. Apague o que estiver escrito e digite exatamente:

```
Mapeamento
```

4. Aperte **Enter**.

> O nome precisa ser **exatamente** esse: M maiúsculo, resto minúsculo, sem espaço
> antes ou depois. As outras consultas procuram por este nome.

### Fazer login no SharePoint

Neste momento aparece uma janela pedindo credencial. Se não aparecer agora, ela
vai aparecer daqui a pouco — o procedimento é o mesmo.

![Janela de credenciais](docs/figuras/09_credenciais.png)

1. Do lado esquerdo da janela, clique em **Conta organizacional**.
2. Clique no botão **Entrar**.
3. Faça login com o seu **e-mail da EMS** (o mesmo do computador).
4. Quando o seu nome aparecer na janela, clique em **Conectar**.

**Agora espere.** O Power BI está abrindo, uma por uma, todas as planilhas da
pasta. Na primeira vez isso leva de 2 a 10 minutos, dependendo de quantos
arquivos existem. Você vai ver uma barrinha se mexendo embaixo.

Quando terminar, a tabela aparece cheia de linhas na área central.

> **Confira agora:** role a tabela para a direita e procure a coluna **Arquivo**.
> Ela deve mostrar nomes diferentes de planilha (uma por pessoa da equipe). Se só
> aparecer um nome, a pasta está errada — veja a Parte 8, erro nº 3.

## 2.4 Consulta 2 — Carregamento Mensal

Repita **exatamente** o mesmo procedimento da consulta 1:

1. **Página Inicial** → **Nova Fonte** → role até o fim → **Consulta Nula**.
2. **Página Inicial** → **Editor Avançado**.
3. Dentro da caixa: **Ctrl+A**, **Delete**.
4. Abra o arquivo **`2_Carregamento_Mensal.pq`** no Bloco de Notas,
   **Ctrl+A**, **Ctrl+C**.
5. Volte ao Editor Avançado, clique na caixa, **Ctrl+V**.
6. Confira a faixa: **Nenhum erro de sintaxe foi detectado**.
7. **Concluído**.
8. Botão direito na consulta nova → **Renomear** → digite exatamente:

```
Carregamento Mensal
```

9. **Enter**.

> Repare no espaço entre as duas palavras e nos acentos. `Carregamento Mensal`
> é diferente de `CarregamentoMensal`.

## 2.5 Consulta 3 — Calendário

Mesma coisa, pela terceira vez:

1. **Nova Fonte** → **Consulta Nula**.
2. **Editor Avançado** → **Ctrl+A** → **Delete**.
3. Abra **`3_Calendario.pq`** no Bloco de Notas → **Ctrl+A** → **Ctrl+C**.
4. Cole com **Ctrl+V** → **Concluído**.
5. Botão direito → **Renomear** → digite exatamente:

```
Calendário
```

6. **Enter**.

> **O acento no "a" é obrigatório**: `Calendário`, e não `Calendario`.
> Várias medidas que você vai criar na Parte 4 procuram por este nome com acento.

## 2.6 Carregar tudo para o relatório

![Fechar e Aplicar](docs/figuras/10_fechar_aplicar.png)

1. Antes de clicar em qualquer coisa, **confira a lista da esquerda**.
   Precisa haver exatamente três consultas, com estes nomes:

```
Mapeamento
Carregamento Mensal
Calendário
```

2. Se algum nome estiver errado, corrija agora (botão direito → Renomear).
3. Clique em **Fechar e Aplicar** (o primeiro botão da aba Página Inicial).
4. A janela do Editor fecha e o Power BI Desktop volta a aparecer, carregando.
5. Espere terminar.

## 2.7 Conferir se deu certo

1. Na barra da **esquerda** do Power BI, clique no **segundo ícone** de cima para
   baixo (uma tabela) — é a **Exibição de Tabela**.
2. No painel **Dados** (direita), clique em **Mapeamento**.
3. Você deve ver a tabela com muitas linhas e muitas colunas.
4. Repita para **Carregamento Mensal** e **Calendário**.

**Aperte Ctrl+S para salvar.** A parte mais difícil acabou.

> **Se alguma tabela estiver vazia ou faltando**, não siga adiante: vá para a
> Parte 8 e resolva primeiro. Construir os gráficos em cima de tabela errada só
> dá trabalho dobrado.
\pagebreak

# Parte 3 — Montar o modelo

## 3.1 O que é o modelo, em uma frase

As três tabelas ainda não se conhecem. O modelo é onde você diz ao Power BI:
*"esta linha do Carregamento Mensal pertence àquele projeto do Mapeamento"*.
Sem isso, filtrar por um responsável não filtra o gráfico do mês.

São só **duas ligações**. Cinco minutos.

## 3.2 Criar as duas ligações

![Exibição de Modelo e as duas ligações](docs/figuras/11_modelo_ligacoes.png)

1. Na barra da **esquerda**, clique no **terceiro ícone** de cima para baixo.
   Ele parece dois retângulos ligados por uma linha. É a **Exibição de Modelo**.
2. Aparecem três caixas, uma para cada tabela. Se estiverem sobrepostas, arraste
   pelo título para separá-las.

### Ligação 1 — Carregamento Mensal com Mapeamento

3. Na caixa **Carregamento Mensal**, encontre o campo **ProjetoID**.
4. Clique nele e **segure o botão do mouse**.
5. Arraste até o campo **ProjetoID** da caixa **Mapeamento**.
6. Solte.
7. Aparece uma linha ligando as duas tabelas.

### Ligação 2 — Carregamento Mensal com Calendário

8. Na caixa **Carregamento Mensal**, encontre o campo **Data Referência**.
9. Arraste até o campo **Data** da caixa **Calendário**. Solte.

### Conferir

10. Passe o mouse em cima de cada linha. Deve aparecer:
    - do lado do **Carregamento Mensal**: um **asterisco (\*)**
    - do lado do **Mapeamento** e do **Calendário**: o número **1**

> Isso quer dizer "muitos para um": muitos meses para um projeto, muitos meses
> para uma data. É o certo. Se aparecer `*` dos dois lados, apague a linha
> (clique nela e aperte Delete) e refaça arrastando na ordem do texto acima.

> **CUIDADO: não crie uma terceira ligação.** Especialmente entre `Mapeamento` e
> `Calendário`. Se você criar, a tela 3 passa a mostrar números errados. Por isso
> desligamos a detecção automática lá na Parte 1.3.

## 3.3 Marcar o Calendário como tabela de data

![Marcar como tabela de data](docs/figuras/12_marcar_data.png)

1. Na barra da esquerda, volte para o **segundo ícone** (**Exibição de Tabela**).
2. No painel **Dados** (direita), clique uma vez sobre o nome **Calendário**.
3. No topo aparece uma aba nova: **Ferramentas de tabela**. Clique nela.
4. Clique em **Marcar como tabela de data** → **Marcar como tabela de data**.
5. Na janelinha, no campo **Coluna de data**, escolha **Data**.
6. Clique em **OK**.

> **Para que serve:** sem isso, a medida que compara com o mês anterior não
> funciona. É obrigatório.

## 3.4 Ordenar as colunas de texto

Por padrão o Power BI ordena texto em ordem alfabética. Isso deixa os status do
funil fora de ordem (CDA antes de Prospecção) e os meses bagunçados. Vamos
corrigir com três ajustes.

![Classificar por coluna](docs/figuras/13_classificar_coluna.png)

**Ajuste 1 — Status NN**

1. No painel **Dados**, abra a tabela **Mapeamento** (clique na setinha).
2. Clique **na coluna** `Status NN`.
3. No topo, clique na aba **Ferramentas de coluna**.
4. Clique em **Classificar por coluna**.
5. Escolha `Ordem Status`.

**Ajuste 2 — Status no Mês**

6. Abra a tabela **Carregamento Mensal**.
7. Clique na coluna `Status no Mês`.
8. **Ferramentas de coluna** → **Classificar por coluna** → escolha `Ordem Status Mês`.

**Ajuste 3 — Mês**

9. Abra a tabela **Calendário**.
10. Clique na coluna `Mês`.
11. **Ferramentas de coluna** → **Classificar por coluna** → escolha `Nº Mês`.

> Se aparecer um aviso de "dependência circular", você escolheu a coluna errada.
> Refaça escolhendo exatamente a coluna indicada acima.

## 3.5 Esconder as colunas que não se usa

Não é obrigatório, mas deixa o painel Dados limpo e evita que você arraste a
coluna errada mais tarde.

1. No painel **Dados**, na tabela **Mapeamento**, clique com o **botão direito**
   em cada coluna da lista abaixo e escolha **Ocultar no modo de exibição de relatório**:

```
Arquivo            Ordem Status       ProjetoID
Categoria          Coligada           Entrada
Status de projeto (NN)                Projeto em andamento?
Motivo Cancelamento Projeto           Última Data
```

2. Na tabela **Carregamento Mensal**, oculte:

```
ProjetoID          Arquivo            Ordem Status Mês       Data Referência
```

> **Por quê?** Essas colunas existem para o Power BI trabalhar, não para você
> usar em gráficos. Exemplo: `Categoria` é o texto cru da planilha, com os erros
> de digitação; quem você usa nos gráficos é `Categoria Padrão`, já limpo.

## 3.6 Conferência final da Parte 3

Marque cada item antes de seguir:

| Conferir | Como saber que está certo |
|---|---|
| Três tabelas existem | No painel Dados aparecem `Mapeamento`, `Carregamento Mensal` e `Calendário` |
| Duas ligações, nem mais nem menos | Na Exibição de Modelo há exatamente 2 linhas ligando caixas |
| Calendário marcado como data | Ao lado do nome `Calendário` aparece um pequeno ícone de calendário |
| Status na ordem certa | Você verá na Parte 5, quando montar o primeiro gráfico |

**Ctrl+S para salvar.**
\pagebreak

# Parte 4 — Criar as medidas

## 4.1 O que é uma medida

Uma **coluna** guarda um dado de cada linha (a molécula, a data).
Uma **medida** é uma **conta** que o Power BI refaz toda vez que você mexe num
filtro: "quantos projetos", "quantas horas", "qual a variação contra o mês
passado".

Você vai criar **52 medidas**. Parece muito, mas cada uma leva 20 segundos: é
colar um texto e apertar Enter. Reserve uns 40 minutos.

> **Não pule nenhuma.** Várias medidas usam outras. Se faltar uma do meio, as de
> baixo dão erro. Crie na ordem em que estão listadas.

## 4.2 Criar a tabela que guarda as medidas

As medidas precisam morar em algum lugar. Vamos criar uma tabela vazia só para
elas — assim ficam todas juntas e fáceis de achar.

1. Na barra da esquerda, clique no **primeiro ícone** (**Exibição de Relatório**).
2. Na faixa de cima, aba **Página Inicial**, clique em **Inserir dados**.
3. Abre uma janelinha com uma gradezinha tipo Excel.
4. Clique no título da coluna (onde está escrito `Coluna1`) e digite: `_`
5. Na primeira célula abaixo, digite: `x`
6. Embaixo, no campo **Nome**, apague e digite exatamente: `_Medidas`
7. Clique em **Carregar**.
8. No painel **Dados**, clique na setinha de `_Medidas`, clique com o **botão
   direito** na coluna `_` e escolha **Ocultar no modo de exibição de relatório**.

## 4.3 Como criar cada medida

![Nova medida e a barra de fórmulas](docs/figuras/14_nova_medida.png)

**Repita este ciclo para cada uma das 52 medidas:**

1. No painel **Dados**, clique uma vez sobre a tabela **_Medidas** para
   selecioná-la.
2. Na faixa de cima, aba **Modelagem**, clique em **Nova medida**.
3. Aparece uma barra de fórmulas no topo, com um texto tipo `Medida = `.
4. **Apague tudo** que estiver na barra (clique nela, Ctrl+A, Delete).
5. **Cole o bloco inteiro** da medida — o nome, o sinal de `=` e a fórmula.
6. Aperte **Enter**.
7. A medida aparece no painel Dados, dentro de `_Medidas`, com o símbolo **∑**.

**Depois de criar, dê o formato:**

8. Com a medida ainda selecionada, olhe a aba **Ferramentas de medida** no topo.
9. No campo **Formato**, escolha o que a tabela da Parte 4.5 indica para
   aquela medida.

> **Se a medida cair em outra tabela** (acontece quando você esquece de
> selecionar `_Medidas` antes): clique nela no painel Dados, vá em
> **Ferramentas de medida** → **Tabela inicial** → escolha `_Medidas`.

> **CUIDADO com o Ctrl+A na barra de fórmulas.** Se você não apagar o texto que
> já está lá, vai ficar `Medida = Projetos = DISTINCTCOUNT(...)`, que dá erro.

## 4.4 A régua de horas — o campo que o time vai preencher

Antes das medidas, crie **uma coluna calculada**. Ela é a régua que converte
"projeto em tal status, de tal complexidade" em **horas por mês**.

**Ela nasce zerada de propósito.** Você e o time definem os números depois; até
lá, todo o resto do dashboard funciona normalmente e só os indicadores de horas
ficam em zero, com um aviso na tela 2 explicando.

### Criar a coluna

1. No painel **Dados**, clique na tabela **Mapeamento**.
2. Aba **Modelagem** → **Nova coluna** (não é "Nova medida"!).
3. Apague o texto da barra de fórmulas.
4. Cole o bloco `Horas Mês` que está no **Anexo B** deste dossiê.
5. **Enter**.

### Preencher depois, quando o time decidir

Quando vocês definirem a régua:

1. No painel **Dados**, clique na coluna `Horas Mês` da tabela `Mapeamento`.
2. A fórmula aparece na barra de cima.
3. Troque cada `0` pelo número de horas. **Use vírgula para decimal**: `1,5`.
4. Aperte **Enter**. Os números aparecem na hora em todo o dashboard.

A pergunta a fazer ao time, para cada uma das 27 combinações:

> *"Um projeto de complexidade ALTA, parado em NEGOCIAÇÃO, consome quantas horas
> suas por mês?"*

E a complexidade sai da categoria do produto. Esse de-para está na consulta 1,
no trecho marcado `COMPLEXIDADE`. Hoje ele diz:

| Categoria | Complexidade |
|---|---|
| Inovador Radical, Biológico | ALTO |
| Inovador Incremental, Produto para Saúde, Cosmético | MÉDIO |
| Similar / Genérico, Alimento / Suplemento, Fitoterápico | BAIXO |

Para mudar, veja a Parte 7.3.

## 4.5 As 52 medidas

A lista completa, com a fórmula para copiar e o formato de cada uma, está no
**Anexo B**, organizada em 9 grupos:

| Grupo | Quantas | Para que servem |
|---|---|---|
| A. Contagens básicas | 9 | Quantos projetos, moléculas, fornecedores |
| B. Carregamento | 6 | Horas, capacidade, ocupação |
| C. Evolução do mês | 10 | Entradas, saídas, carteira, comparação com o mês anterior |
| D. Funil e ciclo | 4 | Tempo médio, taxa de conversão |
| E. Cancelamentos | 3 | Motivos e pesos |
| F. Report por unidade | 5 | Participação da BU, resumo em texto |
| G. Financeiro | 6 | VPL, peak sales, margem |
| H. Qualidade da base | 8 | O que falta preencher |
| I. Apoio | 1 | Carimbo de atualização |

> **Dica para não se perder:** vá marcando com caneta cada medida criada,
> direto no Anexo B impresso. São 52 repetições da mesma tarefa e é muito fácil
> pular uma sem perceber.

**Ctrl+S ao terminar.**
\pagebreak

# Parte 5 — Montar as 8 telas

## 5.1 Como criar uma página

1. Na barra da esquerda, clique no **primeiro ícone** (**Exibição de Relatório**).
2. Lá embaixo, na barra de abas, clique no **+** para criar uma página nova.
3. Clique com o **botão direito** na aba criada → **Renomear página** → digite o nome da tela.
4. Repita até ter as 8 páginas, com os nomes exatos:

```
1. Visão Geral            5. Carteira da Unidade
2. Carregamento do Time   6. Financeiro
3. Evolução do Mês        7. Mapeamento Completo
4. Report por Unidade     8. Qualidade da Base
```

> Crie as 8 páginas agora, de uma vez. Depois volte na página 1 para começar a montar.

> **Você não precisa terminar tudo de uma vez.** Cada tela funciona sozinha assim que
> fica pronta. Monte a tela 1, salve, e volte outro dia para a tela 2. O trabalho fica
> guardado no arquivo `.pbix`.

## 5.2 Como inserir um visual — o ciclo que se repete 73 vezes

![Os poços de campos de um visual](docs/figuras/16_pocos_campos.png)

**Para cada linha das tabelas deste capítulo, faça:**

1. Clique num **espaço vazio** da página (para não alterar um visual existente).
2. No painel **Visualizações** (direita), clique no **ícone do tipo** indicado na coluna *Tipo*.
   Um quadro vazio aparece na página.
3. Arraste o quadro para a posição e puxe os cantos para dar o tamanho.
4. Com o quadro **selecionado**, olhe o painel **Visualizações**: aparecem os **poços**
   (Eixo X, Eixo Y, Valores...).
5. No painel **Dados** (direita), encontre cada campo da coluna *O que arrastar* e
   **arraste para o poço indicado**.
6. Dê o título: painel **Visualizações** → aba **Formatar seu visual** (o ícone de pincel)
   → **Geral** → **Título** → ligue e escreva o texto da coluna *Visual*.

![O painel Visualizações e os ícones](docs/figuras/15_painel_visualizacoes.png)

> **Os ícones não têm nome escrito.** Passe o mouse em cima e espere meio segundo:
> aparece uma tarja com o nome exato. Confira sempre antes de clicar.

## 5.3 Como criar as segmentações (os filtros)

Toda tela começa com uma faixa de filtros no topo. Para cada um:

1. Clique num espaço vazio.
2. No painel **Visualizações**, clique no ícone **Segmentação de dados**.
3. Arraste o campo indicado para o poço **Campo**.
4. Deixe fino e largo, e alinhe os filtros lado a lado no topo da página.
5. Para virar lista suspensa (ocupa menos espaço): com a segmentação selecionada,
   clique na **setinha** que aparece no canto superior direito dela e escolha **Lista suspensa**.

> **Copiar e colar economiza muito tempo.** Monte a faixa de filtros da página 1,
> selecione os 5 de uma vez (segure Ctrl e clique em cada), **Ctrl+C**, vá para a
> página 2 e **Ctrl+V**. Depois é só trocar os campos que mudam.

\pagebreak

## 5.4 Tela 1. Visão Geral

*Foto de hoje de todo o mapeamento ativo*

![Rascunho da tela 1. Visão Geral](docs/figuras/20_tela1.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Responsável]` |
| 2 | `Mapeamento[Unidade de Negócio]` |
| 3 | `Mapeamento[Situação]` |
| 4 | `Mapeamento[Status NN]` |
| 5 | `Mapeamento[Ano de Entrada]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| OPORTUNIDADES | Cartão | **Campos:** `Projetos` (medida) |
| EM ANDAMENTO | Cartão | **Campos:** `Projetos Ativos` (medida) |
| STAND BY | Cartão | **Campos:** `Projetos Stand by` (medida) |
| MOLÉCULAS | Cartão | **Campos:** `Moléculas` (medida) |
| FORNECEDORES | Cartão | **Campos:** `Fornecedores` (medida) |
| QUANTIDADE DE PROJETOS × STATUS | Gráfico de colunas clusterizado | **Eixo X:** `Mapeamento[Status NN]`¶**Eixo Y:** `Projetos` (medida) |
| PROJETOS × CATEGORIA | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Categoria Padrão]`¶**Eixo X:** `Projetos` (medida) |
| ORIGEM DA OPORTUNIDADE | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Origem]`¶**Eixo X:** `Projetos` (medida) |
| PROJETOS POR COLIGADA | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Unidade de Negócio]`¶**Eixo X:** `Projetos` (medida) |
| PROJETOS — VISÃO RESUMIDA | Tabela | **Colunas:** `Mapeamento[Responsável]`¶**Colunas:** `Mapeamento[Molécula]`¶**Colunas:** `Mapeamento[Fornecedor / Parceiro]`¶**Colunas:** `Mapeamento[Status NN]`¶**Colunas:** `Mapeamento[Situação]`¶**Colunas:** `Mapeamento[Alerta]`¶**Colunas:** `Mapeamento[Dias em NN]` |

> **Ordene a barra maior em cima.** Clique nos três pontinhos (**...**) do canto
> do gráfico → **Classificar eixo** → escolha a medida → **Classificação decrescente**.
> Faça isso em todos os gráficos de barras deste dossiê.

\pagebreak

## 5.5 Tela 2. Carregamento do Time

*Quanto cada pessoa tem na mão contra a capacidade*

![Rascunho da tela 2. Carregamento do Time](docs/figuras/21_tela2.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Responsável]` |
| 2 | `Mapeamento[Status interno]` |
| 3 | `Mapeamento[Situação]` |
| 4 | `Mapeamento[Complexidade]` |
| 5 | `Mapeamento[Unidade de Negócio]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| PROJETOS ATIVOS | Cartão | **Campos:** `Projetos Ativos` (medida) |
| HORAS EMPENHADAS | Cartão | **Campos:** `Horas Empenhadas` (medida) |
| CAPACIDADE (H) | Cartão | **Campos:** `Capacidade (h)` (medida) |
| HORAS DISPONÍVEIS | Cartão | **Campos:** `Horas Disponíveis` (medida) |
| % DE OCUPAÇÃO | Cartão | **Campos:** `% Ocupação` (medida) |
| PROJETOS ATIVOS POR PESSOA | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Responsável]`¶**Eixo X:** `Projetos Ativos` (medida) |
| % DE OCUPAÇÃO DO TIME | Medidor | **Valor:** `% Ocupação` (medida) |
| ONDE O TEMPO É GASTO | Gráfico de rosca | **Legenda:** `Mapeamento[Status interno]`¶**Valores:** `Projetos Ativos` (medida) |
| PROJETOS ATIVOS POR STATUS E COMPLEXIDADE | Gráfico de barras empilhadas | **Eixo Y:** `Mapeamento[Status NN]`¶**Eixo X:** `Projetos Ativos` (medida)¶**Legenda:** `Mapeamento[Complexidade]` |
| CARGA POR PESSOA | Tabela | **Colunas:** `Mapeamento[Responsável]`¶**Colunas:** `Projetos Ativos` (medida)¶**Colunas:** `Horas Empenhadas` (medida)¶**Colunas:** `% Ocupação` (medida)¶**Colunas:** `Status Ocupação` (medida) |
| AVISO DA RÉGUA | Cartão | **Campos:** `Aviso Régua` (medida) |

> **No medidor**, depois de arrastar a medida para **Valor**: abra
> **Formatar seu visual** → **Eixo do medidor** → em **Máximo** digite `1`.
> Assim 100% fica no fim do arco.

> O cartão **AVISO DA RÉGUA** fica vazio quando a régua estiver preenchida.
> É o comportamento certo.

\pagebreak

## 5.6 Tela 3. Evolução do Mês

*O mês inteiro, e não só a foto do dia*

![Rascunho da tela 3. Evolução do Mês](docs/figuras/22_tela3.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Responsável]` |
| 2 | `Calendário[Ano]` |
| 3 | `Calendário[Mês]` |
| 4 | `Mapeamento[Unidade de Negócio]` |
| 5 | `Carregamento Mensal[Status no Mês]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| CARTEIRA NO INÍCIO DO MÊS | Cartão | **Campos:** `Ativos no Início do Mês` (medida) |
| ENTRARAM NO MÊS | Cartão | **Campos:** `Entradas no Mês` (medida) |
| SAÍRAM NO MÊS | Cartão | **Campos:** `Saídas no Mês` (medida) |
| CARTEIRA NO FIM DO MÊS | Cartão | **Campos:** `Ativos no Fim do Mês` (medida) |
| HOJE vs FIM DO MÊS | Cartão | **Campos:** `Diferença Hoje vs Mês` (medida) |
| CARTEIRA, ENTRADAS E SAÍDAS POR MÊS | Gráfico de colunas e linhas clusterizado | **Eixo X:** `Calendário[Ano-Mês]`¶**Eixo Y da coluna:** `Entradas no Mês` (medida)¶**Eixo Y da coluna:** `Saídas no Mês` (medida)¶**Eixo Y da linha:** `Ativos no Fim do Mês` (medida) |
| SALDO DO MÊS | Gráfico em cascata | **Categoria:** `Calendário[Ano-Mês]`¶**Eixo Y:** `Saldo do Mês` (medida) |
| COMPOSIÇÃO DO FUNIL AO LONGO DO TEMPO | Gráfico de área empilhada | **Eixo X:** `Calendário[Ano-Mês]`¶**Eixo Y:** `Projetos no Mês` (medida)¶**Legenda:** `Carregamento Mensal[Status no Mês]` |
| RESUMO MÊS A MÊS | Matriz | **Linhas:** `Calendário[Ano-Mês]`¶**Valores:** `Ativos no Início do Mês` (medida)¶**Valores:** `Entradas no Mês` (medida)¶**Valores:** `Saídas no Mês` (medida)¶**Valores:** `Ativos no Fim do Mês` (medida)¶**Valores:** `Variação vs Mês Anterior` (medida) |
| NARRATIVA DO MÊS | Cartão | **Campos:** `Narrativa do Mês` (medida) |

> **CUIDADO — o erro mais fácil de cometer nesta tela.** Nos gráficos de
> evolução use sempre `Calendário[Ano-Mês]` no eixo e
> `Carregamento Mensal[Status no Mês]` na legenda.
> Se você usar `Mapeamento[Status NN]` (o status de **hoje**), o gráfico
> reescreve o passado com a situação atual e os números ficam errados.

\pagebreak

## 5.7 Tela 4. Report por Unidade de Negócio

*O one-page, adaptável a qualquer unidade*

![Rascunho da tela 4. Report por Unidade de Negócio](docs/figuras/23_tela4.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Unidade de Negócio]` |
| 2 | `Mapeamento[Franquia]` |
| 3 | `Mapeamento[Ano de Entrada]` |
| 4 | `Mapeamento[Categoria Padrão]` |
| 5 | `Mapeamento[Responsável]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| MOLÉCULAS AVALIADAS | Cartão | **Campos:** `Moléculas` (medida) |
| % DO TOTAL DE NN | Cartão | **Campos:** `% da Unidade no Total` (medida) |
| EM ANDAMENTO | Cartão | **Campos:** `Projetos Ativos` (medida) |
| CANCELADAS / STAND BY | Cartão | **Campos:** `Cancelados + Stand by` (medida) |
| PRINCIPAL MOTIVO | Cartão | **Campos:** `Motivo nº 1` (medida) |
| ESTÁGIO DAS OPORTUNIDADES EM ANDAMENTO | Gráfico de barras 100% empilhadas | **Eixo Y:** `Mapeamento[Status NN]`¶**Eixo X:** `Projetos Ativos` (medida) |
| FRANQUIAS DE ATUAÇÃO DE NN | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Unidade de Negócio]`¶**Eixo X:** `Moléculas` (medida) |
| MOTIVOS DE CANCELAMENTO / STAND BY | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Motivo]`¶**Eixo X:** `Cancelados + Stand by` (medida) |
| CATEGORIA DAS MOLÉCULAS | Gráfico de rosca | **Legenda:** `Mapeamento[Categoria Padrão]`¶**Valores:** `Moléculas` (medida) |
| MATURIDADE (FASE DA OPORTUNIDADE) | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Fase Oportunidade NN]`¶**Eixo X:** `Moléculas` (medida) |
| ÁREA TERAPÊUTICA | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Área Terapêutica (detalhe)]`¶**Eixo X:** `Moléculas` (medida) |
| RESUMO DA UNIDADE | Cartão | **Campos:** `Resumo da Unidade` (medida) |

![Editar interações](docs/figuras/17_editar_interacoes.png)

> **Um ajuste obrigatório nesta tela.** O gráfico **FRANQUIAS DE ATUAÇÃO DE NN**
> precisa mostrar **todas** as unidades mesmo quando você filtra uma — é esse
> contraste que produz a frase *"esta BU representou X% do que NN avaliou"*.

> Para isso: clique na **segmentação Unidade de Negócio** → aba **Formato** no topo
> → **Editar interações**. Aparecem dois botõezinhos sobre cada gráfico.
> No gráfico **FRANQUIAS DE ATUAÇÃO**, clique no botão **⊘** (círculo cortado).
> Clique de novo em **Editar interações** para sair do modo.

\pagebreak

## 5.8 Tela 5. Carteira da Unidade

*A lista por trás do one-page*

![Rascunho da tela 5. Carteira da Unidade](docs/figuras/24_tela5.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Unidade de Negócio]` |
| 2 | `Mapeamento[Franquia]` |
| 3 | `Mapeamento[Situação]` |
| 4 | `Mapeamento[Status NN]` |
| 5 | `Mapeamento[Ano de Entrada]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| MOLÉCULAS | Cartão | **Campos:** `Moléculas` (medida) |
| CARREGADAS NO PERÍODO | Cartão | **Campos:** `Novas no Período` (medida) |
| DIAS MÉDIOS EM NN | Cartão | **Campos:** `Dias Médios em NN` (medida) |
| DIAS ATÉ 1ª PROPOSTA | Cartão | **Campos:** `Dias Médios até 1ª Proposta` (medida) |
| PRINCIPAL MOTIVO | Cartão | **Campos:** `Motivo nº 1` (medida) |
| CARREGAMENTO DE MOLÉCULAS POR MÊS | Gráfico de colunas clusterizado | **Eixo X:** `Mapeamento[Mês de Entrada]`¶**Eixo Y:** `Moléculas` (medida) |
| ÁREA TERAPÊUTICA × SITUAÇÃO | Gráfico de barras empilhadas | **Eixo Y:** `Mapeamento[Área Terapêutica (detalhe)]`¶**Eixo X:** `Moléculas` (medida)¶**Legenda:** `Mapeamento[Situação]` |
| OPORTUNIDADES DA UNIDADE | Tabela | **Colunas:** `Mapeamento[Molécula]`¶**Colunas:** `Mapeamento[Fornecedor / Parceiro]`¶**Colunas:** `Mapeamento[Fase Oportunidade NN]`¶**Colunas:** `Mapeamento[Indicação]`¶**Colunas:** `Mapeamento[Status NN]`¶**Colunas:** `Mapeamento[Situação]`¶**Colunas:** `Mapeamento[Motivo]`¶**Colunas:** `Mapeamento[Responsável]`¶**Colunas:** `Mapeamento[Data de Entrada]` |

\pagebreak

## 5.9 Tela 6. Financeiro

*O valor do pipeline*

![Rascunho da tela 6. Financeiro](docs/figuras/25_tela6.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Unidade de Negócio]` |
| 2 | `Mapeamento[Responsável]` |
| 3 | `Mapeamento[Situação]` |
| 4 | `Mapeamento[Status NN]` |
| 5 | `Mapeamento[Ano de Entrada]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| VPL TOTAL | Cartão | **Campos:** `VPL Total` (medida) |
| PEAK SALES | Cartão | **Campos:** `Peak Sales` (medida) |
| FATURAMENTO 5 ANOS | Cartão | **Campos:** `Faturamento 5 Anos` (medida) |
| MARGEM BRUTA MÉDIA | Cartão | **Campos:** `Margem Bruta Média` (medida) |
| % COM DADO FINANCEIRO | Cartão | **Campos:** `% Cobertura Financeira` (medida) |
| VPL POR MOLÉCULA | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Molécula]`¶**Eixo X:** `VPL Total` (medida) |
| PEAK SALES POR UNIDADE DE NEGÓCIO | Gráfico de colunas clusterizado | **Eixo X:** `Mapeamento[Unidade de Negócio]`¶**Eixo Y:** `Peak Sales` (medida) |
| PROJETOS COM DADOS FINANCEIROS | Tabela | **Colunas:** `Mapeamento[Molécula]`¶**Colunas:** `Mapeamento[Fornecedor / Parceiro]`¶**Colunas:** `Mapeamento[Status NN]`¶**Colunas:** `Mapeamento[Moeda]`¶**Colunas:** `VPL Total` (medida)¶**Colunas:** `Peak Sales` (medida)¶**Colunas:** `Margem Bruta Média` (medida)¶**Colunas:** `Faturamento 5 Anos` (medida) |

> **Mostre só os 10 maiores no VPL por molécula:** clique no gráfico, abra o painel
> **Filtros** (fica à esquerda do painel Visualizações), em **Molécula** mude
> **Tipo de filtro** para **N Principais**, **Mostrar itens: Superior** `10`,
> e arraste a medida `VPL Total` para **Por valor**. Clique em **Aplicar filtro**.

\pagebreak

## 5.10 Tela 7. Mapeamento Completo

*O consolidado que hoje precisa ser pedido*

![Rascunho da tela 7. Mapeamento Completo](docs/figuras/26_tela7.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Responsável]` |
| 2 | `Mapeamento[Unidade de Negócio]` |
| 3 | `Mapeamento[Status NN]` |
| 4 | `Mapeamento[Situação]` |
| 5 | `Mapeamento[Categoria Padrão]` |
| 6 | `Mapeamento[Franquia]` |
| 7 | `Mapeamento[Origem]` |
| 8 | `Mapeamento[Motivo]` |
| 9 | `Mapeamento[Ano de Entrada]` |
| 10 | `Mapeamento[País Fornecedor]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| LINHAS EXIBIDAS | Cartão | **Campos:** `Projetos` (medida) |
| MOLÉCULAS | Cartão | **Campos:** `Moléculas` (medida) |
| FORNECEDORES | Cartão | **Campos:** `Fornecedores` (medida) |
| RESPONSÁVEIS | Cartão | **Campos:** `Responsáveis` (medida) |
| DIAS MÉDIOS EM NN | Cartão | **Campos:** `Dias Médios em NN` (medida) |
| MAPEAMENTO ATIVO — BASE COMPLETA | Tabela | **Colunas:** `Mapeamento[Responsável]`¶**Colunas:** `Mapeamento[Gerência]`¶**Colunas:** `Mapeamento[Origem]`¶**Colunas:** `Mapeamento[Molécula]`¶**Colunas:** `Mapeamento[Marca do Referência BR]`¶**Colunas:** `Mapeamento[Fornecedor / Parceiro]`¶**Colunas:** `Mapeamento[País Fornecedor]`¶**Colunas:** `Mapeamento[Categoria Padrão]`¶**Colunas:** `Mapeamento[Unidade de Negócio]`¶**Colunas:** `Mapeamento[Área Terapêutica (detalhe)]`¶**Colunas:** `Mapeamento[Fase Oportunidade NN]`¶**Colunas:** `Mapeamento[Indicação]`¶**Colunas:** `Mapeamento[Forma Farmacêutica]`¶**Colunas:** `Mapeamento[Status NN]`¶**Colunas:** `Mapeamento[Situação]`¶**Colunas:** `Mapeamento[Status interno]`¶**Colunas:** `Mapeamento[Motivo]`¶**Colunas:** `Mapeamento[Detalhamento do cancelamento]`¶**Colunas:** `Mapeamento[Data de Entrada]`¶**Colunas:** `Mapeamento[Data Fim]`¶**Colunas:** `Mapeamento[Dias em NN]`¶**Colunas:** `Mapeamento[Complexidade]`¶**Colunas:** `Mapeamento[Alerta]` |

> Esta tela é uma tabela só, bem larga. Deixe-a ocupando a página inteira
> abaixo dos filtros. O usuário exporta com os três pontinhos (**...**) →
> **Exportar dados**.

\pagebreak

## 5.11 Tela 8. Qualidade da Base

*O que falta preencher, por responsável*

![Rascunho da tela 8. Qualidade da Base](docs/figuras/27_tela8.png)

**Filtros do topo** (segmentação de dados, um para cada):

| # | Campo a arrastar |
|---|---|
| 1 | `Mapeamento[Responsável]` |
| 2 | `Mapeamento[Unidade de Negócio]` |
| 3 | `Mapeamento[Situação]` |
| 4 | `Mapeamento[Status NN]` |
| 5 | `Mapeamento[Ano de Entrada]` |

**Cartões e gráficos:**

| Visual | Tipo | O que arrastar |
|---|---|---|
| SEM DATA DE FIM | Cartão | **Campos:** `Sem Data de Fim` (medida) |
| % SEM DATA DE FIM | Cartão | **Campos:** `% Sem Data de Fim` (medida) |
| SEM MOTIVO | Cartão | **Campos:** `Sem Motivo` (medida) |
| SEM UNIDADE DE NEGÓCIO | Cartão | **Campos:** `Sem Unidade de Negócio` (medida) |
| PARADOS HÁ MAIS DE 90 DIAS | Cartão | **Campos:** `Projetos Parados` (medida) |
| PENDÊNCIAS POR RESPONSÁVEL | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Responsável]`¶**Eixo X:** `Total de Pendências` (medida) |
| SITUAÇÃO DOS PROJETOS ATIVOS | Gráfico de barras clusterizado | **Eixo Y:** `Mapeamento[Alerta]`¶**Eixo X:** `Projetos` (medida) |
| PENDÊNCIAS — DETALHE POR PROJETO | Tabela | **Colunas:** `Mapeamento[Responsável]`¶**Colunas:** `Mapeamento[Molécula]`¶**Colunas:** `Mapeamento[Fornecedor / Parceiro]`¶**Colunas:** `Mapeamento[Status NN]`¶**Colunas:** `Mapeamento[Situação]`¶**Colunas:** `Mapeamento[Data Fim]`¶**Colunas:** `Mapeamento[Motivo]`¶**Colunas:** `Mapeamento[Alerta]` |
\pagebreak

# Parte 6 — Publicar e atualizar sozinho todo dia

Até aqui o relatório existe só no seu computador e só mostra dados do momento em
que você carregou. Nesta parte ele vai para a nuvem e passa a se atualizar
sozinho, todo dia, sem ninguém abrir nada.

## 6.1 Publicar

![Publicar no workspace](docs/figuras/30_publicar.png)

1. Aperte **Ctrl+S** para garantir que está tudo salvo.
2. Aba **Página Inicial** → botão **Publicar** (fica na ponta direita da faixa).
3. Se pedir login, entre com o e-mail da EMS.
4. Escolha o **workspace do time** — não use **Meu workspace**, porque nele
   ninguém além de você enxerga o relatório.
5. Clique em **Selecionar**.
6. Espere a mensagem de sucesso e clique no link
   **Abrir "Dashboard Novos Negocios" no Power BI**.

> Se o workspace do time ainda não existir, peça para a área de TI/BI criar um,
> ou crie você: no site do Power BI, menu da esquerda → **Workspaces** →
> **Novo workspace**.

## 6.2 Dar a senha para a nuvem

O Power BI na nuvem ainda não sabe entrar no SharePoint. É preciso autorizar
uma vez.

![Credenciais e atualização agendada](docs/figuras/31_agendamento.png)

1. No site **app.powerbi.com**, menu da esquerda → **Workspaces** → o workspace do time.
2. Na lista, procure a linha com o **mesmo nome** do relatório, mas do tipo
   **Modelo semântico** (antigamente chamado "conjunto de dados"). **Não é a linha
   do relatório.**
3. Passe o mouse nela, clique nos **três pontinhos (...)** → **Configurações**.
4. Abra a seção **Credenciais da fonte de dados**.
5. Clique em **Editar credenciais**.
6. Preencha:
   - **Método de autenticação**: `OAuth2`
   - **Configuração de nível de privacidade**: `Organizacional`
7. Clique em **Entrar** e faça o login da EMS.
8. Espere aparecer a marca verde de sucesso.

> **Não precisa de gateway.** Gateway só é necessário quando os dados estão num
> servidor dentro da empresa. O SharePoint Online já está na nuvem, então a
> conexão é direta.

## 6.3 Ligar a atualização diária

Na **mesma página de Configurações**, logo abaixo:

1. Abra a seção **Atualização agendada**.
2. Ligue a chave **Manter os dados atualizados** (fica verde).
3. **Frequência de atualização**: escolha `Diariamente`.
4. **Fuso horário**: escolha `(UTC-03:00) Brasília`.
5. Em **Horário**, clique em **Adicionar outro horário** e coloque:
   - `07:00`
   - `13:00`
6. Marque **Enviar e-mail de notificação de falha de atualização para mim**.
7. Clique em **Aplicar**.

> **Por que dois horários?** O de 07:00 garante o dado fresco antes da reunião da
> manhã. O de 13:00 pega o que o time atualizou durante a manhã. Com licença Pro
> você pode agendar até 8 horários por dia.

## 6.4 Testar agora

1. Ainda na lista do workspace, passe o mouse na linha do **modelo semântico**.
2. Clique no ícone de **Atualizar agora** (duas setinhas em círculo).
3. Espere. Na coluna **Atualizado** deve aparecer a hora de agora.
4. Abra o relatório e confira se os números batem.

> **Se falhar**, o erro aparece ao passar o mouse no ícone de aviso. Na maioria
> das vezes é credencial — refaça a Parte 6.2.

## 6.5 Dar acesso ao time

1. No workspace, na linha do **relatório** (não do modelo semântico), clique nos
   **três pontinhos (...)** → **Compartilhar**.
2. Digite os e-mails das pessoas.
3. **Desmarque** "Permitir que os destinatários compartilhem este relatório" se
   você quiser controlar quem vê.
4. Clique em **Conceder acesso**.

> Para o time ver pelo celular, basta instalar o aplicativo **Power BI** na loja
> do telefone e entrar com o e-mail da EMS.

## 6.6 A partir de agora

| O que acontece | O que você precisa fazer |
|---|---|
| Alguém edita uma planilha no SharePoint | **Nada.** Entra na próxima atualização (07:00 ou 13:00) |
| Entra uma pessoa nova no time e cria a planilha dela na pasta | **Nada.** A consulta lê todos os arquivos da pasta |
| Alguém adiciona uma coluna nova na planilha | **Nada.** A consulta só usa as colunas que conhece |
| Alguém **renomeia** uma coluna que o dashboard usa | Aí sim quebra — veja a Parte 8, erro nº 6 |
| Você quer um gráfico novo | Abra o `.pbix` no seu computador, monte e publique de novo |
\pagebreak

# Parte 7 — Manutenção

## 7.1 Entrou gente nova no time

**Não faça nada.** A consulta lê **todos** os arquivos `.xlsx` da pasta. Basta a
pessoa criar o mapeamento dela lá, com a aba chamada `Mapeamento NN` e os mesmos
cabeçalhos. Na próxima atualização ela aparece sozinha em todos os filtros.

> Só confira duas coisas no arquivo novo: a **aba** precisa se chamar
> `Mapeamento NN` e a coluna **Responsável** precisa estar preenchida.

## 7.2 Mudou o caminho da pasta no SharePoint

1. No Power BI Desktop: **Página Inicial** → **Transformar dados**.
2. Do lado esquerdo, clique na consulta **Mapeamento**.
3. **Página Inicial** → **Editor Avançado**.
4. Altere apenas estas 4 linhas do começo:

```
SITE       = "https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS",
BIBLIOTECA = "Documentos Compartilhados",
PASTA      = "DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS",
ABA        = "Mapeamento NN",
```

5. **Concluído** → **Fechar e Aplicar**.

> **Como descobrir o caminho certo:** abra a pasta no navegador. O endereço mostra
> o site até `/sites/NOME`, e depois o caminho das pastas. Use a barra `/` para
> separar níveis. Não coloque barra no começo nem no fim.

## 7.3 Preencher ou mudar a régua de horas

**Parte A — as horas** (o que o time definir):

1. No painel **Dados**, clique na coluna `Horas Mês` da tabela `Mapeamento`.
2. A fórmula aparece na barra de cima.
3. Troque os `0` pelos números combinados. Decimal com **vírgula**: `1,5`.
4. **Enter**. Tudo recalcula na hora.

**Parte B — a complexidade** (qual categoria é alta, média ou baixa):

1. **Página Inicial** → **Transformar dados** → consulta **Mapeamento** →
   **Editor Avançado**.
2. Procure o trecho marcado com o comentário `COMPLEXIDADE`.
3. Mude as categorias de lugar entre `"ALTO"`, `"MÉDIO"` e `"BAIXO"`.
4. **Concluído** → **Fechar e Aplicar**.

**Parte C — a capacidade** (168 h por pessoa por mês):

1. No painel **Dados**, clique na medida `Capacidade (h)`.
2. Na barra de fórmulas, troque o `168` pelo número certo.
3. **Enter**.

## 7.4 Guardar o histórico de verdade (opcional, mas recomendado)

A tela 3 reconstrói o passado a partir das datas que já existem na planilha. Isso
funciona muito bem para **entradas** e para **avanço de etapa**. Mas tem um limite
que você precisa conhecer:

> **No mapeamento que analisei, apenas 36 de 354 projetos encerrados tinham a
> "Data de Finalização do Projeto em NN" preenchida.** Sem essa data não dá para
> saber em que mês o projeto saiu. O dashboard **estima** pela última data
> preenchida na linha — e marca isso na coluna `Fim Estimado`.

Há duas saídas, e o ideal é fazer as duas.

**Saída 1 — processo (custo zero).** Passar a exigir o preenchimento da
"Data de Finalização" e do "Motivo de Cancelamento" sempre que um projeto sai.
A **tela 8** existe para cobrar isso: ela lista, por responsável, quem está
devendo.

**Saída 2 — cópia mensal automática.** Um fluxo no Power Automate que, todo dia
1º, copia os mapeamentos para uma pasta com o nome do mês. Aí o histórico vira
fato, não estimativa.

Receita do fluxo (15 minutos, uma vez só):

1. Acesse **make.powerautomate.com** → **Criar** → **Fluxo de nuvem agendado**.
2. Nome: `NN - Snapshot mensal`. Repetir a cada **1 Mês**, dia **1**, às **06:00**.
3. **Nova etapa** → procure `SharePoint` → ação **Obter arquivos (somente propriedades)**.
   - Endereço do site: `https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS`
   - Biblioteca: `Documentos Compartilhados`
   - Pasta: `/DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS`
4. **Nova etapa** → **Obter conteúdo do arquivo** (SharePoint).
   Em Identificador escolha o campo dinâmico **Identificador**.
   O Power Automate cria um "Aplicar a cada" sozinho.
5. Dentro do "Aplicar a cada" → **Criar arquivo** (SharePoint).
   - Caminho da pasta: `/Documentos Compartilhados/DEMANDAS NN - ALIANÇA/HISTORICO/`
     e, colado logo depois, a **Expressão**:
     `formatDateTime(addDays(utcNow(),-1),'yyyy-MM')`
   - Nome do arquivo: campo dinâmico **Nome com extensão**
   - Conteúdo: campo dinâmico **Conteúdo do arquivo**
6. **Salvar**.

A partir daí nasce uma pasta `2026-10`, `2026-11`… a cada virada de mês.
Quando tiver alguns meses acumulados, me avise que eu monto a consulta que lê
esse histórico real.

## 7.5 O que **não** fazer

| Nunca | Por quê |
|---|---|
| Criar uma ligação entre `Mapeamento` e `Calendário` | Quebra a tela 3: filtrar um mês passa a mostrar só quem **entrou** naquele mês |
| Religar "Detectar automaticamente novas relações" | Ele inventa ligações erradas na próxima atualização |
| Usar `Mapeamento[Status NN]` num gráfico da tela 3 | Reescreve o passado com o status de hoje |
| Renomear as tabelas ou as colunas | As 52 medidas param de funcionar de uma vez |
| Editar as planilhas direto pelo Power BI | Ele só lê. Corrija sempre no Excel, no SharePoint |
| Salvar o `.pbix` só no seu computador | Guarde uma cópia no SharePoint ou no OneDrive. Se o notebook morrer, o trabalho vai junto |

## 7.6 Rotina sugerida

| Quando | O quê |
|---|---|
| Toda manhã | Abrir o relatório na nuvem. Se houver aviso de falha, refazer a Parte 6.2 |
| Toda segunda | Olhar a **tela 8** e cobrar as pendências da semana |
| Todo dia 1º | Tirar o print da **tela 3** com o mês fechado, para o report |
| Todo trimestre | Rever a régua de horas com o time (Parte 7.3) |
\pagebreak

# Parte 8 — Quando der errado

Use esta tabela antes de pedir ajuda. A coluna da esquerda é o que aparece na
tela; a da direita é o que fazer.

## 8.1 Erros na conexão (Parte 2)

**Erro nº 1 — "Não encontrei 'Documentos Compartilhados'. Disponíveis aqui: ..."**

A mensagem **lista os nomes que existem** no seu SharePoint. Copie o nome correto
da lista e coloque na linha `BIBLIOTECA` da consulta 1 (Parte 7.2). Em alguns
sites o nome é `Documentos` ou `Shared Documents`.

**Erro nº 2 — "Formula.Firewall: a consulta faz referência a outras consultas"**

Você pulou a Parte 1.3, passo 2. Faça agora e depois clique em
**Página Inicial → Atualizar**.

**Erro nº 3 — A tabela carregou, mas só com os dados de uma pessoa**

O caminho está apontando para uma subpasta errada. Confira a linha `PASTA`.
Para conferir dentro do Power BI: **Transformar dados**, clique na consulta
`Mapeamento`, e do lado direito, no painel **Etapas Aplicadas**, clique em
`Arquivos`. A tabela do meio deve listar **todas** as planilhas do time.

**Erro nº 4 — "Acesso negado" ou fica pedindo senha sem parar**

1. **Arquivo → Opções e configurações → Configurações da fonte de dados**.
2. Selecione a linha do SharePoint.
3. Clique em **Limpar permissões** → **Excluir**.
4. Feche a janela e clique em **Página Inicial → Atualizar**.
5. Faça o login de novo, escolhendo **Conta organizacional**.

**Erro nº 5 — A tabela veio vazia (0 linhas)**

O nome da aba mudou. Abra qualquer mapeamento no Excel e veja o nome exato da aba
lá embaixo. Coloque esse nome na linha `ABA` da consulta 1.

**Erro nº 6 — "A coluna 'X' da tabela não foi encontrada"**

Alguém renomeou uma coluna na planilha. Duas saídas:

- **A melhor:** peça para voltarem o nome antigo na planilha.
- **A alternativa:** no Editor Avançado da consulta 1, procure a lista `COLS` e
  troque o nome antigo pelo novo. Depois procure se esse nome aparece em outros
  lugares do texto e troque também.

**Erro nº 7 — Demora muito e parece travado**

Normal na primeira carga: ele abre todas as planilhas, uma por uma. Espere até
10 minutos. Da segunda vez em diante é mais rápido.

## 8.2 Erros no modelo (Parte 3)

**Erro nº 8 — "Dependência circular detectada" ao classificar por coluna**

Você escolheu a coluna errada. Confira na Parte 3.4: `Status NN` ordena por
`Ordem Status`; `Status no Mês` por `Ordem Status Mês`; `Mês` por `Nº Mês`.

**Erro nº 9 — A ligação aparece pontilhada em vez de contínua**

Pontilhada quer dizer **inativa**. Clique duas vezes nela e marque
**Tornar esta relação ativa**.

**Erro nº 10 — Aparece "muitos para muitos" ao criar a ligação**

Você arrastou na direção errada, ou existe ProjetoID repetido. Apague a ligação
(clique nela, Delete) e refaça **do Carregamento Mensal para o Mapeamento**,
nessa ordem.

## 8.3 Erros nas medidas (Parte 4)

**Erro nº 11 — "Não foi possível determinar um valor único para a coluna"**

Falta um `SUM(...)` ou um `DISTINCTCOUNT(...)` em volta da coluna. Confira se
você colou a medida **inteira**, sem cortar o fim.

**Erro nº 12 — "A função esperava uma referência de tabela ou coluna"**

Quase sempre é acento ou aspas. Confira:
- `Calendário` com acento no "a";
- as aspas precisam ser retas `"` e não curvas `"`. O Bloco de Notas preserva as
  retas; o Word troca por curvas. **Nunca use o Word** para abrir os arquivos.

**Erro nº 13 — A medida ficou dentro da tabela errada**

Clique nela no painel **Dados** → aba **Ferramentas de medida** →
**Tabela inicial** → escolha `_Medidas`.

**Erro nº 14 — Escrito `Medida = Projetos = DISTINCTCOUNT(...)`**

Você esqueceu de apagar o texto que já estava na barra. Apague tudo (Ctrl+A,
Delete) e cole de novo.

## 8.4 Erros nos gráficos (Parte 5)

**Erro nº 15 — O gráfico mostra "Mais de uma coluna" ou fica em branco**

Você arrastou uma **coluna** onde era para ir uma **medida** (ou o contrário).
Medidas têm o símbolo **∑** ao lado do nome no painel Dados.

**Erro nº 16 — Os status aparecem em ordem alfabética**

Faltou a Parte 3.4. Faça e o gráfico se corrige sozinho.

**Erro nº 17 — Os meses aparecem como 2026-01, 2026-02... fora de ordem**

O campo `Ano-Mês` já vem no formato certo para ordenar sozinho. Se estiver
bagunçado, você usou `Mês` em vez de `Ano-Mês`.

**Erro nº 18 — A tela 3 mostra números estranhos ao filtrar um mês**

Você criou a terceira ligação (Mapeamento com Calendário). Vá na **Exibição de
Modelo**, clique na linha entre essas duas tabelas e aperte **Delete**.

**Erro nº 19 — O gráfico de Franquias some ao filtrar uma unidade**

Faltou o **Editar interações** da Parte 5.7.

## 8.5 Erros na publicação (Parte 6)

**Erro nº 20 — "Falha ao atualizar as credenciais"**

Refaça a Parte 6.2 escolhendo `OAuth2` e nível `Organizacional`.

**Erro nº 21 — A atualização agendada falha só às vezes**

Provavelmente alguém deixou uma planilha **aberta e bloqueada** no SharePoint.
Peça para o time fechar os arquivos ao sair.

**Erro nº 22 — "Você não tem permissão para acessar o workspace"**

Peça para o dono do workspace te adicionar como **Membro** (não como Visualizador
— Visualizador não publica).

## 8.6 Se nada disso resolveu

Antes de pedir ajuda, junte estas quatro informações:

1. Em que **Parte e passo** você estava.
2. A **mensagem de erro completa** (print da tela inteira).
3. O que aparece em **Transformar dados → painel Etapas Aplicadas** da consulta
   que falhou.
4. Sua versão: **Arquivo → Sobre**.

Com isso dá para achar a causa. Sem a mensagem, qualquer resposta é chute.
\pagebreak

# Anexo A — As três consultas

Os textos completos estão nos arquivos que vieram com este dossiê:

| Arquivo | Nome da consulta no Power BI |
|---|---|
| `1_Mapeamento.pq` | `Mapeamento` |
| `2_Carregamento_Mensal.pq` | `Carregamento Mensal` |
| `3_Calendario.pq` | `Calendário` |

> **Abra sempre no Bloco de Notas**, nunca no Word. O Word troca as aspas retas
> por aspas curvas e o Power BI não aceita.

Se você perder os arquivos, eles também estão no repositório, na pasta `SIMPLES/`.

\pagebreak

# Anexo B — As 52 medidas e a régua

## B.1 A coluna calculada da régua de horas

Crie esta **antes** das medidas. É **Nova coluna**, não Nova medida, e vai na
tabela **Mapeamento**.

```
Horas Mês =
// ===================================================================
// RÉGUA DE ESFORÇO — preencha quando o time definir (Parte 4.4)
// Troque cada 0 pelo número de HORAS POR MÊS que um projeto naquele
// status e complexidade consome. Aceita decimais: use 1,5 e não 1.5
// ===================================================================
VAR c = Mapeamento[Complexidade]
VAR s = Mapeamento[Status NN]
RETURN
SWITCH (
    TRUE (),
    s = "AGUARDANDO INÍCIO"   && c = "BAIXO", 0,
    s = "AGUARDANDO INÍCIO"   && c = "MÉDIO", 0,
    s = "AGUARDANDO INÍCIO"   && c = "ALTO",  0,
    s = "PROSPECÇÃO"          && c = "BAIXO", 0,
    s = "PROSPECÇÃO"          && c = "MÉDIO", 0,
    s = "PROSPECÇÃO"          && c = "ALTO",  0,
    s = "CDA"                 && c = "BAIXO", 0,
    s = "CDA"                 && c = "MÉDIO", 0,
    s = "CDA"                 && c = "ALTO",  0,
    s = "AV. TÉCNICA INICIAL" && c = "BAIXO", 0,
    s = "AV. TÉCNICA INICIAL" && c = "MÉDIO", 0,
    s = "AV. TÉCNICA INICIAL" && c = "ALTO",  0,
    s = "AV. MARKETING"       && c = "BAIXO", 0,
    s = "AV. MARKETING"       && c = "MÉDIO", 0,
    s = "AV. MARKETING"       && c = "ALTO",  0,
    s = "NEGOCIAÇÃO"          && c = "BAIXO", 0,
    s = "NEGOCIAÇÃO"          && c = "MÉDIO", 0,
    s = "NEGOCIAÇÃO"          && c = "ALTO",  0,
    s = "APROVAÇÃO SUMMARY"   && c = "BAIXO", 0,
    s = "APROVAÇÃO SUMMARY"   && c = "MÉDIO", 0,
    s = "APROVAÇÃO SUMMARY"   && c = "ALTO",  0,
    s = "TERM SHEET"          && c = "BAIXO", 0,
    s = "TERM SHEET"          && c = "MÉDIO", 0,
    s = "TERM SHEET"          && c = "ALTO",  0,
    s = "CONTRATO"            && c = "BAIXO", 0,
    s = "CONTRATO"            && c = "MÉDIO", 0,
    s = "CONTRATO"            && c = "ALTO",  0,
    0
)
```

> Ela nasce zerada. Quando o time definir a régua, troque os `0` pelas horas.
> Decimal com vírgula: `1,5`.


## B.2 Grupo A. Contagens básicas

#### Projetos

Quantas oportunidades existem no filtro atual.

```
Projetos =
DISTINCTCOUNT ( Mapeamento[ProjetoID] )
```

**Formato:** Número inteiro (#.##0)

#### Moléculas

Quantas moléculas diferentes. Uma molécula pode ter vários fornecedores.

```
Moléculas =
DISTINCTCOUNT ( Mapeamento[Molécula] )
```

**Formato:** Número inteiro (#.##0)

#### Fornecedores

Quantas empresas diferentes foram abordadas.

```
Fornecedores =
DISTINCTCOUNT ( Mapeamento[Fornecedor / Parceiro] )
```

**Formato:** Número inteiro (#.##0)

#### Responsáveis

Quantas pessoas do time aparecem no filtro atual.

```
Responsáveis =
DISTINCTCOUNT ( Mapeamento[Responsável] )
```

**Formato:** Número inteiro (#.##0)

#### Projetos Ativos

Só os projetos que estão rodando agora.

```
Projetos Ativos =
CALCULATE ( [Projetos], Mapeamento[Situação] = "Em andamento" )
```

**Formato:** Número inteiro (#.##0)

#### Projetos Stand by

Projetos pausados.

```
Projetos Stand by =
CALCULATE ( [Projetos], Mapeamento[Situação] = "Stand by" )
```

**Formato:** Número inteiro (#.##0)

#### Projetos Encerrados

Projetos cancelados/finalizados.

```
Projetos Encerrados =
CALCULATE ( [Projetos], Mapeamento[Situação] = "Encerrado" )
```

**Formato:** Número inteiro (#.##0)

#### % Ativos

Quanto da carteira está de fato rodando.

```
% Ativos =
DIVIDE ( [Projetos Ativos], [Projetos] )
```

**Formato:** Porcentagem, 1 casa

#### Projetos por Pessoa

Média de projetos ativos por pessoa.

```
Projetos por Pessoa =
DIVIDE ( [Projetos Ativos], [Responsáveis] )
```

**Formato:** 1 casa decimal


## B.2 Grupo B. Carregamento

#### Capacidade (h)

Horas úteis disponíveis. 168 h por pessoa por mês — troque o número se a régua do time for outra.

```
Capacidade (h) =
[Responsáveis] * 168
```

**Formato:** Número inteiro (#.##0)

#### Horas Empenhadas

Soma das horas que os projetos ativos consomem por mês. Fica ZERO até a régua ser preenchida.

```
Horas Empenhadas =
CALCULATE ( SUMX ( Mapeamento, Mapeamento[Horas Mês] ), Mapeamento[Situação] = "Em andamento" )
```

**Formato:** 1 casa decimal

#### Horas Disponíveis

Quanto ainda cabe.

```
Horas Disponíveis =
[Capacidade (h)] - [Horas Empenhadas]
```

**Formato:** 1 casa decimal

#### % Ocupação

Acima de 100% = time sobrecarregado.

```
% Ocupação =
DIVIDE ( [Horas Empenhadas], [Capacidade (h)] )
```

**Formato:** Porcentagem, 1 casa

#### Aviso Régua

Texto que aparece na tela 2 enquanto a régua estiver zerada. Some sozinho quando você preencher.

```
Aviso Régua =
IF (
    [Horas Empenhadas] = 0,
    "A régua de horas ainda não foi preenchida — veja a Parte 4.4 do dossiê.",
    BLANK ()
)
```

**Formato:** Texto (sem formato)

#### Status Ocupação

Classificação em palavras, para a tabela por pessoa.

```
Status Ocupação =
VAR o = [% Ocupação]
RETURN
SWITCH (
    TRUE (),
    [Horas Empenhadas] = 0, "Régua não preenchida",
    o > 1.1,  "Sobrecarregado",
    o > 0.9,  "No limite",
    o > 0.6,  "Saudável",
              "Com folga"
)
```

**Formato:** Texto (sem formato)


## B.2 Grupo C. Evolução do mês

#### Projetos no Mês

Quantos projetos passaram pelo mês selecionado.

```
Projetos no Mês =
DISTINCTCOUNT ( 'Carregamento Mensal'[ProjetoID] )
```

**Formato:** Número inteiro (#.##0)

#### Ativos no Fim do Mês

A carteira na virada do mês. É o número do report.

```
Ativos no Fim do Mês =
CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Ativo no Fim do Mês] = TRUE () )
```

**Formato:** Número inteiro (#.##0)

#### Entradas no Mês

Quantos projetos NOVOS entraram naquele mês.

```
Entradas no Mês =
CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Entrou no Mês] = TRUE () )
```

**Formato:** Número inteiro (#.##0)

#### Saídas no Mês

Quantos saíram (cancelados, stand by ou concluídos).

```
Saídas no Mês =
CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Saiu no Mês] = TRUE () )
```

**Formato:** Número inteiro (#.##0)

#### Saldo do Mês

Positivo = a carteira cresceu. Negativo = encolheu.

```
Saldo do Mês =
[Entradas no Mês] - [Saídas no Mês]
```

**Formato:** Número inteiro (#.##0)

#### Ativos no Início do Mês

Com quantos o mês começou.

```
Ativos no Início do Mês =
[Ativos no Fim do Mês] - [Saldo do Mês]
```

**Formato:** Número inteiro (#.##0)

#### Ativos Mês Anterior

O mesmo número, um mês antes.

```
Ativos Mês Anterior =
CALCULATE ( [Ativos no Fim do Mês], DATEADD ( 'Calendário'[Data], -1, MONTH ) )
```

**Formato:** Número inteiro (#.##0)

#### Variação vs Mês Anterior

Cresceu ou caiu quanto.

```
Variação vs Mês Anterior =
VAR anterior = [Ativos Mês Anterior]
RETURN
    IF ( NOT ISBLANK ( anterior ), [Ativos no Fim do Mês] - anterior )
```

**Formato:** Número inteiro (#.##0)

#### Diferença Hoje vs Mês

A diferença entre a foto de hoje e o fechamento do mês. É o ponto que você levantou no report.

```
Diferença Hoje vs Mês =
[Projetos Ativos] - [Ativos no Fim do Mês]
```

**Formato:** Número inteiro (#.##0)

#### Narrativa do Mês

Frase pronta para colar no report mensal. Muda sozinha conforme os filtros.

```
Narrativa do Mês =
VAR ini = [Ativos no Início do Mês]
VAR ent = [Entradas no Mês]
VAR sai = [Saídas no Mês]
VAR fim = [Ativos no Fim do Mês]
VAR quem = IF ( HASONEVALUE ( Mapeamento[Responsável] ), SELECTEDVALUE ( Mapeamento[Responsável] ), "O time" )
VAR mes  = IF ( HASONEVALUE ( 'Calendário'[Ano-Mês] ), SELECTEDVALUE ( 'Calendário'[Ano-Mês] ), "o período" )
RETURN
    IF (
        ISBLANK ( fim ),
        "Sem movimentação no período.",
        quem & " começou " & mes & " com " & FORMAT ( ini, "0" ) & " projetos, recebeu "
            & FORMAT ( ent, "0" ) & ", encerrou " & FORMAT ( sai, "0" )
            & " e terminou com " & FORMAT ( fim, "0" ) & " em carteira."
    )
```

**Formato:** Texto (sem formato)


## B.2 Grupo D. Funil e ciclo

#### Dias Médios em NN

Quanto tempo, em média, um projeto fica com o time.

```
Dias Médios em NN =
AVERAGE ( Mapeamento[Dias em NN] )
```

**Formato:** Número inteiro (#.##0)

#### Dias Médios até 1ª Proposta

Da entrada até o parceiro mandar preço.

```
Dias Médios até 1ª Proposta =
AVERAGEX (
    FILTER (
        Mapeamento,
        NOT ISBLANK ( Mapeamento[Data de recebimento da primeira proposta comercial] )
            && NOT ISBLANK ( Mapeamento[Data Início] )
    ),
    DATEDIFF (
        Mapeamento[Data Início],
        Mapeamento[Data de recebimento da primeira proposta comercial],
        DAY
    )
)
```

**Formato:** Número inteiro (#.##0)

#### % da Etapa

Quanto cada etapa representa do funil.

```
% da Etapa =
DIVIDE (
    [Projetos],
    CALCULATE ( [Projetos], REMOVEFILTERS ( Mapeamento[Status NN] ) )
)
```

**Formato:** Porcentagem, 1 casa

#### Taxa de Conversão até Contrato

Quantos chegam a Term Sheet ou Contrato.

```
Taxa de Conversão até Contrato =
DIVIDE (
    CALCULATE (
        [Projetos],
        Mapeamento[Ordem Status] >= 8,
        REMOVEFILTERS ( Mapeamento[Status NN] )
    ),
    CALCULATE ( [Projetos], REMOVEFILTERS ( Mapeamento[Status NN] ) )
)
```

**Formato:** Porcentagem, 1 casa


## B.2 Grupo E. Cancelamentos

#### Cancelados + Stand by

Tudo que saiu do fluxo, por qualquer motivo.

```
Cancelados + Stand by =
CALCULATE ( [Projetos], Mapeamento[Situação] IN { "Encerrado", "Stand by" } )
```

**Formato:** Número inteiro (#.##0)

#### % do Motivo

Peso de cada motivo no total.

```
% do Motivo =
DIVIDE (
    [Cancelados + Stand by],
    CALCULATE ( [Cancelados + Stand by], REMOVEFILTERS ( Mapeamento[Motivo] ) )
)
```

**Formato:** Porcentagem, 1 casa

#### Motivo nº 1

O motivo mais frequente, em texto. Vai direto para o cartão do one-page.

```
Motivo nº 1 =
VAR t =
    ADDCOLUMNS (
        FILTER ( VALUES ( Mapeamento[Motivo] ), Mapeamento[Motivo] <> "(Sem motivo registrado)" ),
        "@q", [Cancelados + Stand by]
    )
VAR topo = TOPN ( 1, FILTER ( t, [@q] > 0 ), [@q], DESC )
RETURN
    CONCATENATEX ( topo, Mapeamento[Motivo] )
```

**Formato:** Texto (sem formato)


## B.2 Grupo F. Report por unidade

#### Unidade Selecionada

Mostra qual unidade está filtrada.

```
Unidade Selecionada =
SELECTEDVALUE ( Mapeamento[Unidade de Negócio], "Todas as unidades" )
```

**Formato:** Texto (sem formato)

#### Moléculas (Todas as Unidades)

O total de NN, ignorando o filtro de unidade. Serve de denominador.

```
Moléculas (Todas as Unidades) =
CALCULATE ( [Moléculas], REMOVEFILTERS ( Mapeamento[Unidade de Negócio] ) )
```

**Formato:** Número inteiro (#.##0)

#### % da Unidade no Total

A frase 'esta BU representou X% do que NN avaliou'.

```
% da Unidade no Total =
DIVIDE ( [Moléculas], [Moléculas (Todas as Unidades)] )
```

**Formato:** Porcentagem, 1 casa

#### Novas no Período

Moléculas carregadas no ano/período filtrado (use o filtro Ano de Entrada).

```
Novas no Período =
CALCULATE (
    [Moléculas],
    NOT ISBLANK ( Mapeamento[Data de Entrada] )
)
```

**Formato:** Número inteiro (#.##0)

#### Resumo da Unidade

Parágrafo pronto para o slide da unidade de negócio.

```
Resumo da Unidade =
VAR part = [% da Unidade no Total]
VAR ativas = [Projetos Ativos]
VAR paradas = [Cancelados + Stand by]
RETURN
    IF (
        ISBLANK ( [Projetos] ),
        "Sem oportunidades para os filtros selecionados.",
        [Unidade Selecionada] & " representa " & FORMAT ( part, "0,0%" )
            & " das moléculas avaliadas por Novos Negócios no período. "
            & FORMAT ( ativas, "0" ) & " em andamento e " & FORMAT ( paradas, "0" )
            & " canceladas ou em stand by. Principal motivo: " & [Motivo nº 1] & "."
    )
```

**Formato:** Texto (sem formato)


## B.2 Grupo G. Financeiro

#### VPL Total

Soma do valor presente líquido.

```
VPL Total =
SUM ( Mapeamento[VPL (R$)] )
```

**Formato:** Moeda R$, 0 casas

#### Peak Sales

Pico de faturamento previsto.

```
Peak Sales =
SUM ( Mapeamento[Fat. Líq. (Peak Sales, R$)] )
```

**Formato:** Moeda R$, 0 casas

#### Faturamento 5 Anos

Soma dos 5 anos do DRE.

```
Faturamento 5 Anos =
SUM ( Mapeamento[Fat. Líq. DRE (Ano1)] )
    + SUM ( Mapeamento[Fat. Líq. DRE (Ano2)] )
    + SUM ( Mapeamento[Fat. Líq. DRE (Ano3)] )
    + SUM ( Mapeamento[Fat. Líq. DRE (Ano4)] )
    + SUM ( Mapeamento[Fat. Líq. DRE (Ano5)] )
```

**Formato:** Moeda R$, 0 casas

#### Margem Bruta Média

Margem média dos projetos que têm o dado.

```
Margem Bruta Média =
AVERAGE ( Mapeamento[Margem Bruta (%)] )
```

**Formato:** Porcentagem, 1 casa

#### Projetos com VPL

Quantos têm número financeiro.

```
Projetos com VPL =
CALCULATE ( [Projetos], NOT ISBLANK ( Mapeamento[VPL (R$)] ) )
```

**Formato:** Número inteiro (#.##0)

#### % Cobertura Financeira

Quanto do funil tem número. Hoje é baixo — mostra o tamanho do buraco.

```
% Cobertura Financeira =
DIVIDE (
    [Projetos com VPL],
    CALCULATE ( [Projetos], Mapeamento[Situação] IN { "Em andamento", "Stand by" } )
)
```

**Formato:** Porcentagem, 1 casa


## B.2 Grupo H. Qualidade da base

#### Sem Data de Fim

Projetos que saíram sem registrar quando. É a pendência nº 1.

```
Sem Data de Fim =
CALCULATE (
    [Projetos],
    Mapeamento[Situação] <> "Em andamento",
    ISBLANK ( Mapeamento[Data de Finalização do Projeto em NN] )
)
```

**Formato:** Número inteiro (#.##0)

#### % Sem Data de Fim

Em percentual.

```
% Sem Data de Fim =
DIVIDE (
    [Sem Data de Fim],
    CALCULATE ( [Projetos], Mapeamento[Situação] <> "Em andamento" )
)
```

**Formato:** Porcentagem, 1 casa

#### Sem Motivo

Encerrados sem justificativa registrada.

```
Sem Motivo =
CALCULATE (
    [Projetos],
    Mapeamento[Situação] = "Encerrado",
    Mapeamento[Motivo] = "(Sem motivo registrado)"
)
```

**Formato:** Número inteiro (#.##0)

#### Sem Unidade de Negócio

Não aparecem em nenhum report de BU.

```
Sem Unidade de Negócio =
CALCULATE ( [Projetos], Mapeamento[Unidade de Negócio] = "(Não informado)" )
```

**Formato:** Número inteiro (#.##0)

#### Sem Categoria

Sem categoria não há complexidade nem cálculo de horas.

```
Sem Categoria =
CALCULATE ( [Projetos], Mapeamento[Categoria Padrão] = "(NÃO INFORMADO)" )
```

**Formato:** Número inteiro (#.##0)

#### Sem Área Terapêutica

Somem dos cortes por franquia.

```
Sem Área Terapêutica =
CALCULATE ( [Projetos], Mapeamento[Franquia] = "(NÃO INFORMADO)" )
```

**Formato:** Número inteiro (#.##0)

#### Total de Pendências

Soma das pendências. Quanto menor, melhor.

```
Total de Pendências =
[Sem Data de Fim] + [Sem Motivo] + [Sem Unidade de Negócio]
    + [Sem Categoria] + [Sem Área Terapêutica]
```

**Formato:** Número inteiro (#.##0)

#### Projetos Parados

Ativos sem nenhuma data nova há mais de 90 dias.

```
Projetos Parados =
CALCULATE ( [Projetos], Mapeamento[Alerta] = "3. Parado" )
```

**Formato:** Número inteiro (#.##0)


## B.2 Grupo I. Apoio

#### Atualizado em

Carimbo da última atualização. Coloque no rodapé de cada página.

```
Atualizado em =
"Dados atualizados em " & FORMAT ( NOW (), "dd/mm/yyyy HH:mm" )
```

**Formato:** Texto (sem formato)

\pagebreak

# Anexo C — Lista de conferência

Marque cada item. Só passe adiante quando o anterior estiver certo.

| ✔ | Parte | O que conferir |
|---|---|---|
|  | 1.3 | Privacidade em 'Sempre ignorar' |
|  | 1.3 | 'Detectar automaticamente novas relações' desmarcado |
|  | 1.3 | 'Data/hora automática' desmarcado |
|  | 1.4 | Arquivo salvo como `Dashboard Novos Negocios.pbix` |
|  | 2.3 | Consulta `Mapeamento` criada e com linhas |
|  | 2.3 | A coluna `Arquivo` mostra VÁRIOS nomes de planilha |
|  | 2.4 | Consulta `Carregamento Mensal` criada |
|  | 2.5 | Consulta `Calendário` criada, com acento |
|  | 2.6 | 'Fechar e Aplicar' concluído sem erro |
|  | 3.2 | Ligação `Carregamento Mensal[ProjetoID]` → `Mapeamento[ProjetoID]` |
|  | 3.2 | Ligação `Carregamento Mensal[Data Referência]` → `Calendário[Data]` |
|  | 3.2 | Existem EXATAMENTE 2 ligações |
|  | 3.3 | `Calendário` marcado como tabela de data |
|  | 3.4 | `Status NN` classificado por `Ordem Status` |
|  | 3.4 | `Status no Mês` classificado por `Ordem Status Mês` |
|  | 3.4 | `Mês` classificado por `Nº Mês` |
|  | 4.2 | Tabela `_Medidas` criada, coluna `_` oculta |
|  | 4.4 | Coluna calculada `Horas Mês` criada em `Mapeamento` |
|  | 4.5 | As 52 medidas criadas, todas dentro de `_Medidas` |
|  | 5.1 | As 8 páginas criadas com os nomes certos |
|  | 5.4 | Tela 1 montada |
|  | 5.5 | Tela 2 montada (medidor com máximo = 1) |
|  | 5.6 | Tela 3 montada (sem usar `Status NN` nos gráficos de evolução) |
|  | 5.7 | Tela 4 montada + **Editar interações** no gráfico de Franquias |
|  | 5.8 | Tela 5 montada |
|  | 5.9 | Tela 6 montada (filtro N Principais = 10 no VPL) |
|  | 5.10 | Tela 7 montada |
|  | 5.11 | Tela 8 montada |
|  | 6.1 | Publicado no workspace do time |
|  | 6.2 | Credenciais OAuth2 / Organizacional configuradas |
|  | 6.3 | Atualização diária ligada, 07:00 e 13:00, fuso Brasília |
|  | 6.3 | E-mail de falha marcado |
|  | 6.4 | 'Atualizar agora' funcionou |
|  | 6.5 | Time com acesso |
|  | 7.3 | Régua de horas preenchida com o time *(pode ficar para depois)* |
|  | 7.4 | Fluxo de snapshot mensal criado *(opcional)* |

---

## Quando tudo estiver marcado

Você tem um dashboard que:

- lê sozinho **todas** as planilhas do time, sem ninguém exportar nada;
- se atualiza **duas vezes por dia**, sem ninguém abrir o Power BI;
- mostra **o mês inteiro**, e não só a foto do dia;
- gera o **one-page de qualquer unidade de negócio** trocando um filtro;
- entrega o **mapeamento consolidado** sem precisar pedir a ninguém;
- e aponta, por responsável, **o que falta preencher** na base.

O único item que continua dependendo de decisão humana é a régua de horas.
Enquanto ela não for definida, tudo o mais funciona normalmente.
