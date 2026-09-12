// ===========================================================================
//  CONSULTA 3 de 3  —  CALENDÁRIO
//  Renomeie a consulta para:   Calendário
//  (com acento no "a", exatamente assim)
//
//  É a tabela de datas. O Power BI precisa dela para comparar meses e anos.
// ===========================================================================
let
    Hoje = Date.From(DateTime.LocalNow()),
    Menor = List.Min(List.RemoveNulls(Mapeamento[Data Início])),
    Inicio = Date.StartOfYear(Menor ?? #date(2022, 1, 1)),
    Fim = Date.EndOfYear(Date.AddYears(Hoje, 1)),
    Lista = List.Dates(Inicio, Duration.Days(Fim - Inicio) + 1, #duration(1, 0, 0, 0)),
    Tabela = Table.TransformColumnTypes(
        Table.FromList(Lista, Splitter.SplitByNothing(), {"Data"}), {{"Data", type date}}),
    C1 = Table.AddColumn(Tabela, "Ano", each Date.Year([Data]), Int64.Type),
    C2 = Table.AddColumn(C1, "Nº Mês", each Date.Month([Data]), Int64.Type),
    C3 = Table.AddColumn(C2, "Mês", each Text.Proper(Date.MonthName([Data], "pt-BR")), type text),
    C4 = Table.AddColumn(C3, "Ano-Mês", each
        Text.From(Date.Year([Data])) & "-" & Text.PadStart(Text.From(Date.Month([Data])), 2, "0"), type text),
    C5 = Table.AddColumn(C4, "Trimestre", each "T" & Text.From(Date.QuarterOfYear([Data])), type text),
    C6 = Table.AddColumn(C5, "É Mês Atual", each
        Date.StartOfMonth([Data]) = Date.StartOfMonth(Hoje), type logical)
in
    C6
