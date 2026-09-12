let
    Hoje = Date.From(DateTime.LocalNow()),
    Min1 = List.Min(List.RemoveNulls(Mapeamento[Data Início Efetiva])),
    Inicio = Date.StartOfYear(Min1 ?? #date(pAnoMinimo, 1, 1)),
    Fim = Date.EndOfYear(Date.AddYears(Hoje, 1)),
    Dias = Duration.Days(Fim - Inicio) + 1,
    Lista = List.Dates(Inicio, Dias, #duration(1, 0, 0, 0)),
    Tabela = Table.FromList(Lista, Splitter.SplitByNothing(), {"Data"}),
    Tipada = Table.TransformColumnTypes(Tabela, {{"Data", type date}}),
    C = Table.AddColumn(Tipada, "Ano", each Date.Year([Data]), Int64.Type),
    C2 = Table.AddColumn(C, "Nº Mês", each Date.Month([Data]), Int64.Type),
    C3 = Table.AddColumn(C2, "Mês", each Text.Proper(Date.MonthName([Data], "pt-BR")), type text),
    C4 = Table.AddColumn(C3, "Mês Abrev", each Text.Proper(Text.Start(Date.MonthName([Data], "pt-BR"), 3)), type text),
    C5 = Table.AddColumn(C4, "Ano-Mês", each Text.From(Date.Year([Data])) & "-" & Text.PadStart(Text.From(Date.Month([Data])), 2, "0"), type text),
    C6 = Table.AddColumn(C5, "ChaveMes", each Date.Year([Data]) * 100 + Date.Month([Data]), Int64.Type),
    C7 = Table.AddColumn(C6, "Trimestre", each "T" & Text.From(Date.QuarterOfYear([Data])), type text),
    C8 = Table.AddColumn(C7, "Ano-Trimestre", each Text.From(Date.Year([Data])) & "-T" & Text.From(Date.QuarterOfYear([Data])), type text),
    C9 = Table.AddColumn(C8, "Início do Mês", each Date.StartOfMonth([Data]), type date),
    C10 = Table.AddColumn(C9, "Fim do Mês", each Date.EndOfMonth([Data]), type date),
    C11 = Table.AddColumn(C10, "É Mês Atual", each Date.StartOfMonth([Data]) = Date.StartOfMonth(Hoje), type logical),
    C12 = Table.AddColumn(C11, "É Ano Atual", each Date.Year([Data]) = Date.Year(Hoje), type logical),
    C13 = Table.AddColumn(C12, "Passado ou Hoje", each [Data] <= Hoje, type logical)
in
    C13
