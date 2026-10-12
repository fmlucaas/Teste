# Modelo mensal da Oppa — a reconstrução

Seis abas. O modelo anterior tinha treze e premissas anuais; este tem cinco abas
de conteúdo e **nenhuma premissa anual em lugar nenhum**.

```
python3 main.py ../../Oppa_Modelo_Mensal.xlsx
python3 /caminho/para/recalc.py ../../Oppa_Modelo_Mensal.xlsx 420
python3 audita.py ../../Oppa_Modelo_Mensal.xlsx
```

| Arquivo | Aba | O que faz |
|---|---|---|
| `base.py` | — | estilos e a linha do tempo de 60 meses |
| `comecar.py` | Começar aqui | meia tela: o que é cada aba e como funciona uma premissa |
| `resumo.py` | Resumo | começa com **quanto a empresa precisa de dinheiro**; cenário e TMA |
| `dre.py` | DRE Mensal | o modelo: drivers → usuários → faturamento → custo → EBITDA → caixa |
| `nuvem.py` | Nuvem e Escala | a conta de nuvem ancorada por tamanho de base, interpolada mês a mês |
| `quadros.py` | Equipe, Aportes | as duas tabelas que o usuário já mantinha, com os dados dele |
| `audita.py` | — | 14 testes de comportamento |

## As três decisões de desenho

**1. Premissa mensal com reancoragem.** Cada linha de driver tem `valor inicial`,
`evolução por mês` e `mês de início`, e cada mês lê o mês anterior:

```
mês i = IF(nº do mês < mês de início; 0; IF(mês anterior = 0; valor inicial;
           mês anterior × (1 + evolução)))
```

Isso dá três coisas de uma vez: a curva se preenche sozinha sem digitar 60
células; **digitar por cima de um mês reancora a curva dali para frente e não
toca no passado**; e a evolução é mensal, não anual. O teste
*"Digitar por cima de um mês reancora a curva dali"* é o que prova isso.

**2. A conta de nuvem, não o custo por usuário.** Provedor de nuvem não cobra por
usuário — cobra uma conta. Então a entrada é a **conta mensal** em alguns
tamanhos de base, e o custo por usuário é a divisão. É a conta de trás pra
frente, e é o que faz o custo unitário cair de R$ 6,40 com 100 usuários para
R$ 0,55 com 1 milhão.

Entre as âncoras o modelo **interpola** em vez de usar faixa em degrau. Com
degrau, sair de 999 para 1.001 usuários derrubaria a conta pela metade — o custo
total **cairia** ao ganhar um usuário. A aba carrega uma linha de conferência que
acusaria exatamente isso.

**3. O peso do usuário gratuito.** A nuvem não escala com a base: escala com
*consumo*. Um assinante pagante tem monitoramento contínuo; um usuário do plano
gratuito abre o app de vez em quando. O modelo tem uma célula para esse peso
(padrão 10%) e mostra separadamente **quanto o plano gratuito custa** e qual é o
**subsídio por assinante pagante**. No mês do lançamento esse subsídio passa do
próprio preço da assinatura — é o número que decide se o plano gratuito cabe no
modelo.

## A armadilha que custou uma rodada de depuração

Rótulo de linha que começa com `=` o openpyxl grava como **fórmula**. `"= EBITDA"`
na coluna A virou `#NAME?`. Convenção contábil `(=)` resolve e fica mais legível.
Se aparecer `#NAME?` ou `#VALUE!` na coluna A, é isto.

## Verificação

Três conferências vivem dentro da planilha, no Resumo e na DRE:

- faturamento líquido − custo − EBITDA = 0, em todos os 60 meses;
- base de usuários − pagantes − gratuitos = 0, em todos os 60 meses;
- a conta de nuvem nunca cai quando a base sobe.

E `audita.py` roda 14 testes de comportamento: cada um muda **uma** célula,
recalcula a planilha inteira no LibreOffice e confere o efeito — inclusive onde
o efeito tem de ser **nenhum** (dobrar o preço não pode mexer no número de
pagantes nem na conta de nuvem).
