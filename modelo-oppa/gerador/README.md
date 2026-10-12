# Gerador do modelo financeiro da Oppa

Scripts que constroem `Oppa_DRE_Projetada_Viabilidade.xlsx`. A planilha é o entregável;
estes scripts existem para que ela possa ser reconstruída ou alterada estruturalmente.

Para ajustar **premissas** (preços, churn, conversão, custos, aportes), edite direto na
planilha — as células azuis são todas editáveis e o modelo inteiro recalcula.
Use os scripts apenas para mudar a **estrutura** (linhas, abas, fórmulas).

## Reconstruir

```
pip install openpyxl
python main.py ../Oppa_DRE_Projetada_Viabilidade.xlsx
python /caminho/para/recalc.py ../Oppa_DRE_Projetada_Viabilidade.xlsx 420
python verifica.py ../Oppa_DRE_Projetada_Viabilidade.xlsx
```

O passo de recálculo é obrigatório: o openpyxl grava fórmulas sem valores em cache.
Requer LibreOffice **com o pacote `libreoffice-calc`** instalado.

## Duas regras que não se quebram

**Nunca referencie uma linha do motor por número.** Use os offsets nomeados de
`engine.py` (`O.bruta`, `O.fcl_ac`). Inserir uma linha no meio do bloco já quebrou
três células em silêncio — a última delas, o TOTAL da alíquota efetiva, que passou a
dividir a receita bruta pelas parcerias e mostrava 0,00%.

**A aba Ajuste Mensal é feita para ficar vazia.** Toda fórmula que a referencia tem
de estar envolvida em `IF(célula="";premissa_anual;célula)`. A auditoria `p1.py`
cobra isso: referência à aba sem o tratamento do vazio é achado de severidade ALTA.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `common.py` | estilos, formatos numéricos, linha do tempo de 60 meses |
| `premissas.py` | aba Premissas — todos os inputs, com as fontes em comentário de célula |
| `ajuste.py` | aba Ajuste Mensal — override mês a mês dos drivers anuais |
| `bases.py` | abas Tributos (Anexos III/V, Fator R) e Aportes (cap table) |
| `pessoas.py` | aba Pessoas — quadro de pessoal linha a linha e cálculo do Fator R |
| `comousar.py` | aba Como usar — guia de operação da planilha |
| `investimentos.py` | aba Investimentos — CAPEX e amortização |
| `engine.py` | aba Cenários — o motor: 3 cenários × 60 meses, fonte única de verdade |
| `detalhe.py` | abas Usuários, Faturamento, Análise Fluxo e DRE Projetada |
| `capital.py` | aba Necessidade de Capital — quanto captar, de quem e até quando |
| `preco.py` | aba Preço Mínimo — a conta de trás pra frente, do custo para o preço |
| `resumo.py` | aba Resumo — painel executivo e teste Go/No-Go |
| `socios.py` | aba Sócios — lucro distribuível e rateio por participação |
| `verifica.py` | confere os valores calculados e a reconciliação entre abas |
