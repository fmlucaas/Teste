# Gerador da priorização do backlog

Constrói `Oppa_Backlog_Priorizado.xlsx` a partir da planilha original do sócio técnico.

| Arquivo | Conteúdo |
|---|---|
| `dados.py` | as notas de cada PBI, as dependências, as 16 lacunas e as 8 observações |
| `ordena.py` | calcula o peso de dependência a partir do grafo e ordena por WSJF de cadeia |
| `monta.py` | monta as cinco abas do arquivo final |

## Refazer

```
python monta.py ../../Oppa_Backlog_Priorizado.xlsx
```

Para mudar uma prioridade, altere as notas em `dados.py` e rode de novo — a ordem
se reajusta sozinha, respeitando as dependências. As notas são `(VU, OBR, MON, ESF,
[pré-requisitos], justificativa)`; o peso de dependência não é digitado, é calculado.
