# Comece aqui

Três coisas, nesta ordem. **A primeira leva 2 minutos e não precisa de Power BI.**

---

## 1. Veja o dashboard antes de instalar nada

Abra este link no navegador (Chrome, Edge, qualquer um):

> **https://claude.ai/code/artifact/011ee2d5-3d93-4cae-80ef-84412edb2b76**

São as 8 telas, com os 354 projetos reais do seu mapeamento. Clique nas abas,
mexa nos filtros. **Não é o Power BI** — é uma maquete fiel, feita para você
aprovar as telas antes de instalar.

Me diga o que mudar: qual gráfico tirar, qual trocar, o que falta. Eu ajusto e
só depois vale a pena mexer no Power BI.

---

## 2. Instale o Power BI Desktop

Se você já tem, pule.

1. Abra a **Microsoft Store** no Windows (ícone da sacolinha, ou tecla Windows e
   digite "Microsoft Store").
2. Na busca, escreva **Power BI Desktop**.
3. Clique em **Obter** / **Instalar**. É gratuito.
4. Quando terminar, abra. Se pedir login, use seu e-mail da EMS.

---

## 3. Monte o relatório — 3 colagens

> Esqueça os arquivos `.pbit` e a pasta `PBIP`. Não funcionaram no seu
> computador e eu não consigo testá-los daqui. **Este caminho é texto puro:
> se der erro, o Power BI diz exatamente em qual linha.**

### 3.1 Prepare o programa (uma vez só)

1. Com o Power BI Desktop aberto, clique em **Arquivo** (canto superior esquerdo).
2. **Opções e configurações** → **Opções**.
3. Na lista da esquerda, em *ARQUIVO ATUAL*, clique em **Privacidade**.
4. Marque **"Ignorar os níveis de privacidade..."**.
5. Ainda na lista da esquerda, clique em **Carregamento de Dados**.
6. **Desmarque** "Detectar automaticamente novos relacionamentos".
7. **Desmarque** "Data/hora automática para novos arquivos".
8. **OK**.

### 3.2 Cole a consulta 1

1. Na faixa de cima, aba **Página Inicial** → botão **Transformar dados**
   (ícone de tabela com lápis). Abre uma janela nova, o *Editor do Power Query*.
2. Nessa janela nova: **Página Inicial** → **Nova Fonte** → role até o fim →
   **Consulta Nula**.
3. **Página Inicial** → **Editor Avançado**. Abre uma caixa com um texto dentro.
4. Clique dentro da caixa, dê **Ctrl+A** (seleciona tudo) e **Delete**.
5. Abra o arquivo **`SIMPLES/1_Mapeamento.pq`** no **Bloco de Notas**
   (botão direito no arquivo → Abrir com → Bloco de Notas).
6. No Bloco de Notas: **Ctrl+A**, **Ctrl+C**.
7. Volte ao Editor Avançado, clique dentro da caixa e **Ctrl+V**.
8. Clique em **Concluído**.
9. Do lado esquerdo aparece **Consulta1**. Clique com o **botão direito** nela →
   **Renomear** → apague e escreva exatamente:

   ```
   Mapeamento
   ```

   → Enter.

**Neste momento ele vai pedir para entrar na sua conta.** Aparece uma janela
"Acessar conteúdo do SharePoint":
- clique em **Conta organizacional**
- clique em **Entrar**
- use seu e-mail da EMS
- clique em **Conectar**

Espere. Ele está lendo os arquivos de todo mundo — pode levar alguns minutos.
Quando terminar, você vê a tabela preenchida.

### 3.3 Cole a consulta 2

Repita **exatamente** os passos 2 a 9 acima, mas:
- usando o arquivo **`SIMPLES/2_Carregamento_Mensal.pq`**
- e o nome da consulta é:

  ```
  Carregamento Mensal
  ```

### 3.4 Cole a consulta 3

De novo os passos 2 a 9, com:
- o arquivo **`SIMPLES/3_Calendario.pq`**
- e o nome:

  ```
  Calendário
  ```

  (com acento no "a" — o Power BI diferencia)

### 3.5 Carregue

Na janela do Editor do Power Query: **Página Inicial** → **Fechar e Aplicar**
(botão da esquerda). Espere carregar.

### 3.6 Ligue as três tabelas

1. Na barra da **esquerda** do Power BI, clique no terceiro ícone de cima para
   baixo (parece um diagrama de tabelas ligadas) — é o **Modelo**.
2. Você vê três caixas. Vamos criar duas ligações **arrastando**:

   **Ligação 1:** na caixa **Carregamento Mensal**, clique e segure o campo
   **ProjetoID**, arraste até o campo **ProjetoID** da caixa **Mapeamento** e solte.

   **Ligação 2:** na caixa **Carregamento Mensal**, arraste o campo
   **Data Referência** até o campo **Data** da caixa **Calendário** e solte.

3. Pronto. Se aparecer alguma janela pedindo confirmação, clique **OK**.

### 3.7 Marque a tabela de datas

1. Clique na barra da esquerda no segundo ícone (**Dados**, parece uma tabela).
2. Do lado direito, no painel **Dados**, clique em **Calendário**.
3. Na faixa de cima aparece a aba **Ferramentas de tabela** → clique em
   **Marcar como tabela de data** → **Marcar como tabela de data**.
4. Em "Coluna de data" escolha **Data** → **OK**.

### 3.8 Salve

**Arquivo** → **Salvar como** → escolha uma pasta sua → nome
`Dashboard Novos Negocios` → **Salvar**.

**Pronto: os dados estão dentro do Power BI.** A partir daqui é arrastar campos
para montar os gráficos — e aí eu te ajudo com a tela que você quiser primeiro.

---

## Se algo der errado

| O que apareceu | O que fazer |
|---|---|
| "Não encontrei 'Documentos Compartilhados'" | A mensagem lista os nomes que existem no site. Me mande essa lista — ajusto a linha `BIBLIOTECA =` da consulta 1. |
| "Formula.Firewall" ou fala em "níveis de privacidade" | Você pulou o passo 3.1. Refaça-o e depois **Página Inicial → Atualizar**. |
| "Acesso negado" / pede senha de novo | **Arquivo → Opções e configurações → Configurações da fonte de dados** → selecione a linha do SharePoint → **Limpar permissões** → feche → **Atualizar** e faça login de novo. |
| A tabela veio vazia | O nome da aba mudou. Abra qualquer mapeamento no Excel, veja o nome exato da aba lá embaixo, e troque na linha `ABA =` da consulta 1. |
| Demora muito | Normal na primeira vez — ele lê todos os arquivos da pasta. Da segunda vez em diante é mais rápido. |
| Qualquer outra mensagem | Tire um print e me mande. Sem a mensagem eu só chuto. |

---

## Sobre o `.pbit` que não abriu

Eu montei aquele arquivo por programação, sem poder abrir o Power BI daqui para
testar. Ele tem um formato interno proprietário da Microsoft que eu não consigo
validar às cegas — por isso falhou, e por isso não insisto nele.

**Se você me mandar a mensagem de erro exata que apareceu**, eu consigo atacar a
causa. Sem ela, o caminho das 3 colagens acima é o único que eu sei que funciona,
porque é texto que o próprio Power BI interpreta e critica linha a linha.
