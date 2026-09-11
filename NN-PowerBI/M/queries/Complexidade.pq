// De-para Categoria -> Complexidade. EDITE AQUI se a régua do time mudar.
let
    Fonte = Table.FromRecords({
        [#"Categoria Padrão" = "INOVADOR RADICAL",     Complexidade = "ALTO",  #"Ordem Complexidade" = 3],
        [#"Categoria Padrão" = "BIOLÓGICO",            Complexidade = "ALTO",  #"Ordem Complexidade" = 3],
        [#"Categoria Padrão" = "M&A",                  Complexidade = "ALTO",  #"Ordem Complexidade" = 3],
        [#"Categoria Padrão" = "INOVADOR INCREMENTAL", Complexidade = "MÉDIO", #"Ordem Complexidade" = 2],
        [#"Categoria Padrão" = "PRODUTO PARA SAÚDE",   Complexidade = "MÉDIO", #"Ordem Complexidade" = 2],
        [#"Categoria Padrão" = "COSMÉTICO",            Complexidade = "MÉDIO", #"Ordem Complexidade" = 2],
        [#"Categoria Padrão" = "SIMILAR / GENÉRICO",   Complexidade = "BAIXO", #"Ordem Complexidade" = 1],
        [#"Categoria Padrão" = "ALIMENTO / SUPLEMENTO",Complexidade = "BAIXO", #"Ordem Complexidade" = 1],
        [#"Categoria Padrão" = "FITOTERÁPICO",         Complexidade = "BAIXO", #"Ordem Complexidade" = 1],
        [#"Categoria Padrão" = "(NÃO INFORMADO)",      Complexidade = "MÉDIO", #"Ordem Complexidade" = 2]
    }),
    DaBase = List.Distinct(List.RemoveNulls(Mapeamento[Categoria Padrão])),
    Faltantes = List.Difference(DaBase, Fonte[Categoria Padrão]),
    Extras = Table.FromRecords(List.Transform(Faltantes, each
        [#"Categoria Padrão" = _, Complexidade = "MÉDIO", #"Ordem Complexidade" = 2])),
    Uniao = Table.Combine({Fonte, Extras}),
    Tipado = Table.TransformColumnTypes(Uniao,
        {{"Categoria Padrão", type text}, {"Complexidade", type text}, {"Ordem Complexidade", Int64.Type}})
in
    Tipado
