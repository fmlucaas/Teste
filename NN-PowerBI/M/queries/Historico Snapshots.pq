// Histórico Snapshots — // OPCIONAL. Lê a pasta HISTORICO, onde cada
// subpasta "yyyy-MM" guarda a cópia dos mapeamentos daquele fechamento.
// Se a pasta não existir, devolve tabela vazia (o relatório não quebra).
// Isto captura o que as datas NÃO conseguem reconstruir: cancelamentos
// sem data de finalização e mudanças de responsável.
// =====================================================================
let
    Vazia = #table(
        type table [ProjetoID = text, #"Data Snapshot" = date, #"Responsável Final" = text,
                    #"Status NN" = text, #"Situação" = text, #"Coligada Padrão" = text,
                    #"Categoria Padrão" = text, #"Motivo Padrão" = text, Molécula = text],
        {}),

    Tentativa = try
        let
            Origem = SharePoint.Contents(pSiteSharePoint, [ApiVersion = 15]),
            fnEntrar = (tbl as table, nome as text) =>
                Table.SelectRows(tbl, each Comparer.OrdinalIgnoreCase(Text.Trim([Name]), Text.Trim(nome)) = 0){0}[Content],
            Biblioteca = fnEntrar(Origem, pBiblioteca),
            Partes = List.Select(List.Transform(Text.Split(pPastaHistorico, "/"), Text.Trim), each _ <> ""),
            Pasta = List.Accumulate(Partes, Biblioteca, (e, p) => fnEntrar(e, p)),

            // subpastas no formato yyyy-MM
            Subpastas = Table.SelectRows(Pasta, each
                Text.Length([Name]) >= 7 and Text.Contains([Name], "-")),

            ComData = Table.AddColumn(Subpastas, "Data Snapshot", each
                try Date.EndOfMonth(#date(
                        Number.From(Text.Start([Name], 4)),
                        Number.From(Text.Middle([Name], 5, 2)), 1)) otherwise null),

            Validas = Table.SelectRows(ComData, each [Data Snapshot] <> null),

            ComArquivos = Table.AddColumn(Validas, "Arqs", each
                Table.SelectRows([Content], each
                    Text.EndsWith(Text.Lower([Name]), ".xlsx") and not Text.StartsWith([Name], "~$"))),

            Exp1 = Table.ExpandTableColumn(
                    Table.SelectColumns(ComArquivos, {"Data Snapshot", "Arqs"}),
                    "Arqs", {"Content", "Name"}, {"Content", "Arquivo"}),

            ComTab = Table.AddColumn(Exp1, "Tab", each
                let
                    wb = Excel.Workbook([Content], null, true),
                    aba = Table.SelectRows(wb, each [Kind] = "Sheet" and
                            Comparer.OrdinalIgnoreCase(Text.Trim([Item]), pAbaMapeamento) = 0),
                    d = if Table.RowCount(aba) = 0 then null else aba{0}[Data],
                    p = if d = null then null else Table.PromoteHeaders(d, [PromoteAllScalars = true]),
                    n = if p = null then null else fnUtil[NormalizaCabecalhos](p)
                in  n),

            SoValidos = Table.SelectRows(ComTab, each [Tab] <> null),

            Cols = {"Responsável", "Molécula", "Coligada", "Categoria",
                    "Status de projeto (NN)", "Projeto em andamento?",
                    "Motivo Cancelamento Projeto", "Fornecedor / Parceiro"},

            Sel = Table.AddColumn(SoValidos, "Sel", each fnUtil[SelecionaColunas]([Tab], Cols)),
            Enx = Table.SelectColumns(Sel, {"Data Snapshot", "Arquivo", "Sel"}),
            Exp2 = Table.ExpandTableColumn(Enx, "Sel", Cols, Cols),
            Uteis = Table.SelectRows(Exp2, each fnUtil[Texto]([Molécula]) <> null),
            ComSeq = Table.AddIndexColumn(Uteis, "Seq", 1, 1, Int64.Type),
            ComID = Table.AddColumn(ComSeq, "ProjetoID", each
                Text.Combine({[Arquivo], Text.From([Seq])}, "#"), type text),
            Padrao = Table.TransformColumns(ComID, {
                {"Responsável", each fnUtil[Chave](_), type nullable text},
                {"Coligada", each fnUtil[Chave](_), type nullable text},
                {"Categoria", each fnUtil[Chave](_), type nullable text},
                {"Status de projeto (NN)", each fnUtil[Chave](_), type nullable text},
                {"Projeto em andamento?", each fnUtil[Chave](_), type nullable text},
                {"Motivo Cancelamento Projeto", each fnUtil[Chave](_), type nullable text},
                {"Molécula", each fnUtil[Texto](_), type nullable text}}),

            // normaliza para EXATAMENTE o mesmo esquema da tabela vazia,
            // senão os dois ramos do try/otherwise divergem e o modelo quebra
            ComSituacao = Table.AddColumn(Padrao, "Situação", each
                let a = [#"Projeto em andamento?"] in
                if a = null then "NÃO INFORMADO"
                else if Text.StartsWith(a, "SIM") then "EM ANDAMENTO"
                else if Text.Contains(a, "STAND") then "STAND BY"
                else if Text.StartsWith(a, "NÃO") or Text.StartsWith(a, "NAO") then "ENCERRADO"
                else a, type text),

            Renomeado = Table.RenameColumns(ComSituacao, {
                {"Responsável", "Responsável Final"},
                {"Status de projeto (NN)", "Status NN"},
                {"Coligada", "Coligada Padrão"},
                {"Categoria", "Categoria Padrão"},
                {"Motivo Cancelamento Projeto", "Motivo Padrão"}}),

            Enxugado = Table.SelectColumns(Renomeado,
                {"ProjetoID", "Data Snapshot", "Responsável Final", "Status NN",
                 "Situação", "Coligada Padrão", "Categoria Padrão", "Motivo Padrão",
                 "Molécula"}, MissingField.UseNull),

            Tipado = Table.TransformColumnTypes(Enxugado, {
                {"ProjetoID", type text}, {"Data Snapshot", type date},
                {"Responsável Final", type text}, {"Status NN", type text},
                {"Situação", type text}, {"Coligada Padrão", type text},
                {"Categoria Padrão", type text}, {"Motivo Padrão", type text},
                {"Molécula", type text}})
        in  Tipado
    otherwise Vazia,

    Resultado = if Tentativa is table then Tentativa else Vazia
in
    Resultado
