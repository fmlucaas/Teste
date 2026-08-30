# Auditoria da planilha financeira

Quatro scripts, cada um com um ângulo diferente. Rode todos depois de qualquer
mudança estrutural no gerador.

```
python p1.py ../../Oppa_DRE_Projetada_Viabilidade.xlsx      # mecânica
python p2.py ../../Oppa_DRE_Projetada_Viabilidade.xlsx 1    # cenário 1
python p2.py ../../Oppa_DRE_Projetada_Viabilidade.xlsx 2    # cenário 2
python p2.py ../../Oppa_DRE_Projetada_Viabilidade.xlsx 3    # cenário 3
python p3.py ../../Oppa_DRE_Projetada_Viabilidade.xlsx      # valores derivados
python p4.py ../../Oppa_DRE_Projetada_Viabilidade.xlsx      # comportamento
python p5.py ../../Oppa_DRE_Projetada_Viabilidade.xlsx      # aba Sócios
```

| Script | O que faz |
|---|---|
| `p1.py` | Referências para célula vazia, coluna TOTAL x soma dos meses, linhas de total x parcelas, número fixo em linha de fórmula, percentual fora de faixa, intervalo que contém a própria célula, fórmula sem resultado |
| `p2.py` | Reimplementa o modelo inteiro em Python, lendo só as premissas, e compara 26 linhas x 60 meses contra a aba Cenários. É a verificação mais forte: um erro de lógica no motor aparece aqui |
| `p3.py` | Identidades contábeis da DRE, blocos anuais x soma dos meses, amortização e saldo contábil, cap table, compromisso dos fundadores, VPL, payback, capital requerido, break-even, métricas de unidade, Fator R e tabelas do Simples |
| `p5.py` | Apuração da aba Sócios: lucro do ano contra a DRE, encadeamento dos acumulados, limite de caixa e de lucro, rateio por participação |
| `p4.py` | Muda uma premissa, recalcula e confere a reação: troca de cenário, adiamento do lançamento, churn zero, plano de contratações desligado, aportes previstos, acordos em negociação, TMA, conversão zero e troca de regime |
| `p5.py` | Apuração da aba Sócios: encadeamento dos acumulados, limite do caixa livre, rateio por sócio |
| `p6.py` | Receita B2B: painel de consentimento, mínimo comercial, interruptor de iniciativas em estudo, modelo por usuário, e a checagem de que a receita de dados não paga comissão de loja nem taxa de pagamento, mas paga imposto |

## Cuidados ao escrever novas verificações

O `p2.py` precisa replicar o **ROUND do Excel** (metade sempre para longe do zero).
O `round()` do Python arredonda para o par e produz divergências de um assinante
entre planos, o que já gerou um falso positivo.

Casar rótulo por `in` também engana: `"(=) EBIT"` casa com `"(=) EBITDA"`,
`"FATOR R"` casa com o cabeçalho da seção e `"Iniciativa"` casa com o título
"Iniciativas de receita B2B" antes do cabeçalho da tabela. Prefira comparação exata.

**Nunca use offset numérico do bloco de cenário.** Inserir uma linha no meio do
bloco desloca todos os offsets seguintes, e o auditor passa a comparar a linha
errada em silêncio — aconteceu três vezes. Todos os scripts agora localizam a
linha pelo rótulo em coluna A dentro do bloco. O gerador faz o mesmo, via o
objeto `O` de `engine.py`.
