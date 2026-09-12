// De-para Coligada -> Unidade de Negócio (o eixo dos reports de BU).
let
    Fonte = Table.FromRecords({
        [#"Coligada Padrão" = "EMS PRESCRIÇÃO", #"Unidade de Negócio" = "EMS Prescrição", Ordem = 1],
        [#"Coligada Padrão" = "NON RETAIL",     #"Unidade de Negócio" = "Non-Retail",     Ordem = 2],
        [#"Coligada Padrão" = "USK",            #"Unidade de Negócio" = "USK",            Ordem = 3],
        [#"Coligada Padrão" = "OFTA",           #"Unidade de Negócio" = "Ofta",           Ordem = 4],
        [#"Coligada Padrão" = "OTC",            #"Unidade de Negócio" = "OTC",            Ordem = 5],
        [#"Coligada Padrão" = "BRACE PHARMA",   #"Unidade de Negócio" = "Brace Pharma",   Ordem = 6],
        [#"Coligada Padrão" = "LEGRAND",        #"Unidade de Negócio" = "Legrand",        Ordem = 7],
        [#"Coligada Padrão" = "MULTILAB",       #"Unidade de Negócio" = "Multilab",       Ordem = 8],
        [#"Coligada Padrão" = "GERMED",         #"Unidade de Negócio" = "Germed",         Ordem = 9],
        [#"Coligada Padrão" = "EMS MARCAS",     #"Unidade de Negócio" = "EMS Marcas",     Ordem = 10],
        [#"Coligada Padrão" = "EMS GENÉRICOS",  #"Unidade de Negócio" = "EMS Genéricos",  Ordem = 11],
        [#"Coligada Padrão" = "NOVA QUÍMICA",   #"Unidade de Negócio" = "Nova Química",   Ordem = 12],
        [#"Coligada Padrão" = "(NÃO INFORMADO)",#"Unidade de Negócio" = "(Não informado)",Ordem = 99]
    }),
    DaBase = List.Distinct(List.RemoveNulls(Mapeamento[Coligada Padrão])),
    Faltantes = List.Difference(DaBase, Fonte[Coligada Padrão]),
    Extras = Table.FromRecords(List.Transform(Faltantes, each
        [#"Coligada Padrão" = _, #"Unidade de Negócio" = Text.Proper(Text.Lower(_)), Ordem = 98])),
    Uniao = Table.Combine({Fonte, Extras}),
    Tipado = Table.TransformColumnTypes(Uniao,
        {{"Coligada Padrão", type text}, {"Unidade de Negócio", type text}, {"Ordem", Int64.Type}})
in
    Tipado
