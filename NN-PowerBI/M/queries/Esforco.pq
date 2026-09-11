// Esforço — RÉGUA DE CARREGAMENTO: horas/mês que UM projeto consome,
// por Status x Complexidade.
//
// >>> ESTA TABELA NASCE EM BRANCO, DE PROPÓSITO. <<<
// Preencha com o time no arquivo  Regua_Esforco_NN.xlsx  (aba "Esforço"),
// colocado na mesma pasta do SharePoint dos mapeamentos. Enquanto as horas
// não forem preenchidas, o dashboard funciona normalmente — só os
// indicadores de horas e de ocupação ficam vazios, com aviso na tela.
let
    Statuses = {"AGUARDANDO INÍCIO", "PROSPECÇÃO", "CDA", "AV. TÉCNICA INICIAL",
                "AV. MARKETING", "NEGOCIAÇÃO", "APROVAÇÃO SUMMARY",
                "TERM SHEET", "CONTRATO"},
    Complexidades = {"BAIXO", "MÉDIO", "ALTO"},

    // grade completa: todas as combinações sempre existem
    Grade = Table.FromRows(
        List.Combine(List.Transform(Statuses, (s) =>
            List.Transform(Complexidades, (c) => {s, c}))),
        {"Status", "Complexidade"}),

    // o que veio do arquivo da régua (se houver)
    DoArquivo = Fonte_Regua[Aba]("Esforço"),

    Preenchido =
        if DoArquivo = null then null
        else let
            cols = fnUtil[SelecionaColunas](DoArquivo, {"Status", "Complexidade", "Horas Mês"}),
            limpo = Table.TransformColumns(cols, {
                {"Status",       each fnUtil[Chave](_),  type nullable text},
                {"Complexidade", each fnUtil[Chave](_),  type nullable text},
                {"Horas Mês",    each fnUtil[Numero](_), type nullable number}}),
            validos = Table.SelectRows(limpo, each [Status] <> null and [Complexidade] <> null)
        in  Table.Distinct(validos, {"Status", "Complexidade"}),

    Combinado =
        if Preenchido = null then Table.AddColumn(Grade, "Horas Mês", each null, type nullable number)
        else let
            merge = Table.NestedJoin(Grade, {"Status", "Complexidade"},
                        Preenchido, {"Status", "Complexidade"}, "m", JoinKind.LeftOuter),
            exp = Table.ExpandTableColumn(merge, "m", {"Horas Mês"}, {"Horas Mês"})
        in  exp,

    Tipado = Table.TransformColumnTypes(Combinado,
        {{"Status", type text}, {"Complexidade", type text}, {"Horas Mês", type nullable number}}),
    Chave = Table.AddColumn(Tipado, "ChaveEsforco", each [Status] & "|" & [Complexidade], type text)
in
    Chave
