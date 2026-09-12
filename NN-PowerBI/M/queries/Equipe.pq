// Gerada da própria base — não precisa manter lista de nomes.
let
    DoMapeamento = Table.SelectColumns(Mapeamento, {"Responsável Final", "Gerência"}),
    SemNulos = Table.SelectRows(DoMapeamento, each [Responsável Final] <> null),
    Agrupado = Table.Group(SemNulos, {"Responsável Final"}, {
        {"Gerência", each List.Mode([Gerência]) ?? "(NÃO INFORMADO)", type text},
        {"Projetos Totais", each Table.RowCount(_), Int64.Type}}),
    Renom = Table.RenameColumns(Agrupado, {{"Responsável Final", "Pessoa"}}),
    ComCapacidade = Table.AddColumn(Renom, "Capacidade Mensal (h)", each pCapacidadeMensalHoras, type number),
    ComNome = Table.AddColumn(ComCapacidade, "Nome", each Text.Proper(Text.Lower([Pessoa])), type text)
in
    ComNome
