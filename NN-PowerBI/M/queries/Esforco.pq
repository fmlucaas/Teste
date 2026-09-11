// Horas/mês consumidas por UM projeto, por Status x Complexidade.
// >>> ESTA É A RÉGUA DE CARREGAMENTO. Ajuste os números com o time. <<<
let
    Fonte = Table.FromRecords({
        [Status = "AGUARDANDO INÍCIO",   BAIXO = 0.5, #"MÉDIO" = 1,  ALTO = 1.5],
        [Status = "PROSPECÇÃO",          BAIXO = 2,   #"MÉDIO" = 3,  ALTO = 4],
        [Status = "CDA",                 BAIXO = 1,   #"MÉDIO" = 1.5,ALTO = 2],
        [Status = "AV. TÉCNICA INICIAL", BAIXO = 4,   #"MÉDIO" = 6,  ALTO = 8],
        [Status = "AV. MARKETING",       BAIXO = 3,   #"MÉDIO" = 4,  ALTO = 6],
        [Status = "NEGOCIAÇÃO",          BAIXO = 6,   #"MÉDIO" = 8,  ALTO = 12],
        [Status = "APROVAÇÃO SUMMARY",   BAIXO = 3,   #"MÉDIO" = 4,  ALTO = 6],
        [Status = "TERM SHEET",          BAIXO = 5,   #"MÉDIO" = 7,  ALTO = 10],
        [Status = "CONTRATO",            BAIXO = 6,   #"MÉDIO" = 8,  ALTO = 12],
        [Status = "(SEM STATUS)",        BAIXO = 0,   #"MÉDIO" = 0,  ALTO = 0]
    }),
    Despivotado = Table.UnpivotOtherColumns(Fonte, {"Status"}, "Complexidade", "Horas Mês"),
    Tipado = Table.TransformColumnTypes(Despivotado,
        {{"Status", type text}, {"Complexidade", type text}, {"Horas Mês", type number}}),
    Chave = Table.AddColumn(Tipado, "ChaveEsforco", each [Status] & "|" & [Complexidade], type text)
in
    Chave
