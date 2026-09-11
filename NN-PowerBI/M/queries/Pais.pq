// Lê a aba "PAÍS" do primeiro arquivo que a tiver (traz o ISO ALPHA-3,
// que faz o mapa do Power BI acertar 100% dos países).
let
    Arquivos = Fonte_Arquivos,
    ComAba = Table.AddColumn(Arquivos, "Tab", each
        let
            wb = Excel.Workbook([Content], null, true),
            aba = Table.SelectRows(wb, each [Kind] = "Sheet" and Text.Upper(Text.Trim([Item])) = "PAÍS")
        in  if Table.RowCount(aba) = 0 then null else aba{0}[Data]),
    ComDados = Table.SelectRows(ComAba, each [Tab] <> null),
    Primeiro = if Table.RowCount(ComDados) = 0 then null else ComDados{0}[Tab],

    DaTabela =
        if Primeiro = null then #table({"País", "ISO3"}, {})
        else let
            colA = Table.SelectColumns(Primeiro, {"Column1", "Column2"}, MissingField.UseNull),
            renom = Table.RenameColumns(colA, {{"Column1", "País"}, {"Column2", "ISO3"}}),
            limpo = Table.TransformColumns(renom, {
                {"País", each fnUtil[Texto](_), type nullable text},
                {"ISO3", each fnUtil[Texto](_), type nullable text}}),
            validos = Table.SelectRows(limpo, each
                [País] <> null and [ISO3] <> null and Text.Length([ISO3]) = 3
                and [País] <> "Nome do país ou território")
        in  validos,

    // garante que todo país presente na base exista na dimensão
    DaBase = List.Distinct(List.RemoveNulls(Mapeamento[País Fornecedor])),
    Faltantes = List.Difference(DaBase, DaTabela[País]),
    Extras = Table.FromRecords(List.Transform(Faltantes, each [País = _, ISO3 = null])),
    Uniao = Table.Combine({DaTabela, Extras}),
    SemDup = Table.Distinct(Uniao, {"País"}),
    Tipado = Table.TransformColumnTypes(SemDup, {{"País", type text}, {"ISO3", type nullable text}})
in
    Tipado
