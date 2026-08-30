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

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `common.py` | estilos, formatos numéricos, linha do tempo de 60 meses |
| `premissas.py` | aba Premissas — todos os inputs, com as fontes em comentário de célula |
| `bases.py` | abas Tributos (Anexos III/V, Fator R) e Aportes (cap table) |
| `pessoas.py` | aba Pessoas — quadro de pessoal linha a linha e cálculo do Fator R |
| `comousar.py` | aba Como usar — guia de operação da planilha |
| `investimentos.py` | aba Investimentos — CAPEX e amortização |
| `engine.py` | aba Cenários — o motor: 3 cenários × 60 meses, fonte única de verdade |
| `detalhe.py` | abas Usuários, Faturamento, Análise Fluxo e DRE Projetada |
| `resumo.py` | aba Resumo — painel executivo e teste Go/No-Go |
| `verifica.py` | confere os valores calculados e a reconciliação entre abas |
