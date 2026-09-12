// Faturamento Projetado — despivota o DRE (Ano1..Ano5) do mapeamento.
// Grão: 1 linha por projeto x ano do DRE. Permite ver a curva de receita
// projetada do pipeline, que hoje fica presa em 5 colunas soltas.
let
    Base = Table.SelectColumns(Mapeamento, {
        "ProjetoID",
        "Fat. Líq. DRE (Ano1)", "Fat. Líq. DRE (Ano2)", "Fat. Líq. DRE (Ano3)",
        "Fat. Líq. DRE (Ano4)", "Fat. Líq. DRE (Ano5)"}, MissingField.UseNull),

    Despivotado = Table.UnpivotOtherColumns(Base, {"ProjetoID"}, "Coluna", "Valor"),

    SoValores = Table.SelectRows(Despivotado, each [Valor] <> null and [Valor] <> 0),

    ComAno = Table.AddColumn(SoValores, "Ano do DRE", each
        try Number.From(Text.BetweenDelimiters([Coluna], "Ano", ")")) otherwise null, Int64.Type),

    ComRotulo = Table.AddColumn(ComAno, "Ano Projetado", each
        "Ano " & Text.From([Ano do DRE]), type text),

    Final = Table.SelectColumns(ComRotulo, {"ProjetoID", "Ano do DRE", "Ano Projetado", "Valor"}),
    Tipado = Table.TransformColumnTypes(Final, {{"Valor", type number}})
in
    Tipado
