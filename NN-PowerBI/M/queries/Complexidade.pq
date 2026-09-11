// Complexidade — de-para Categoria -> Complexidade (BAIXO / MÉDIO / ALTO).
//
// >>> TAMBÉM NASCE EM BRANCO. <<<
// Preencha no arquivo  Regua_Esforco_NN.xlsx  (aba "Complexidade").
// Sem preenchimento, toda categoria fica como "(A DEFINIR)" e o cálculo de
// horas fica zerado — sem quebrar nenhuma outra parte do relatório.
let
    DoArquivo = Fonte_Regua[Aba]("Complexidade"),

    Preenchido =
        if DoArquivo = null then null
        else let
            cols = fnUtil[SelecionaColunas](DoArquivo, {"Categoria", "Complexidade"}),
            limpo = Table.TransformColumns(cols, {
                {"Categoria",    each fnUtil[Chave](_), type nullable text},
                {"Complexidade", each fnUtil[Chave](_), type nullable text}}),
            validos = Table.SelectRows(limpo, each [Categoria] <> null and [Complexidade] <> null),
            renom = Table.RenameColumns(validos, {{"Categoria", "Categoria Padrão"}})
        in  Table.Distinct(renom, {"Categoria Padrão"}),

    // toda categoria que existe na base precisa existir aqui
    DaBase = List.Distinct(List.RemoveNulls(Mapeamento[Categoria Padrão])),
    Base = Table.FromList(DaBase, Splitter.SplitByNothing(), {"Categoria Padrão"}),

    Combinado =
        if Preenchido = null
        then Table.AddColumn(Base, "Complexidade", each "(A DEFINIR)", type text)
        else let
            merge = Table.NestedJoin(Base, {"Categoria Padrão"},
                        Preenchido, {"Categoria Padrão"}, "m", JoinKind.LeftOuter),
            exp = Table.ExpandTableColumn(merge, "m", {"Complexidade"}, {"Complexidade"}),
            semNulo = Table.TransformColumns(exp,
                        {{"Complexidade", each _ ?? "(A DEFINIR)", type text}})
        in  semNulo,

    ComOrdem = Table.AddColumn(Combinado, "Ordem Complexidade", each
        if [Complexidade] = "BAIXO" then 1
        else if [Complexidade] = "MÉDIO" then 2
        else if [Complexidade] = "ALTO" then 3
        else 0, Int64.Type),

    Tipado = Table.TransformColumnTypes(ComOrdem,
        {{"Categoria Padrão", type text}, {"Complexidade", type text}})
in
    Tipado
