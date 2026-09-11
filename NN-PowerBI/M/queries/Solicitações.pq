// Solicitações — // FATO de demandas às áreas técnicas (Médica, Patentes,
// Regulatória, Econômicos). Mede SLA de resposta e taxa de viabilidade.
// =====================================================================
let
    Arquivos = Fonte_Arquivos,
    ComAba = Table.AddColumn(Arquivos, "Tab", each
        let
            wb = Excel.Workbook([Content], null, true),
            aba = Table.SelectRows(wb, each [Kind] = "Sheet" and
                    Comparer.OrdinalIgnoreCase(Text.Trim([Item]), pAbaSolicitacoes) = 0),
            dados = if Table.RowCount(aba) = 0 then null else aba{0}[Data],
            promov = if dados = null then null else Table.PromoteHeaders(dados, [PromoteAllScalars = true]),
            norm = if promov = null then null else fnUtil[NormalizaCabecalhos](promov)
        in  norm),

    ComDados = Table.SelectRows(ComAba, each [Tab] <> null),

    Colunas = {"ÁREA TÉCNICA", "SOLICITANTE", "MOLÉCULA", "DATA DA SOLICITAÇÃO",
               "DATA DE PREVISÃO", "STATUS", "DIAS DISPONÍVEIS",
               "DATA DO RECEBIMENTO", "RECEBIDO", "VIABILIDADE", "OBS"},

    Selec = Table.AddColumn(ComDados, "Sel", each fnUtil[SelecionaColunas]([Tab], Colunas)),
    Enxuto = Table.SelectColumns(Selec, {"Arquivo", "Responsável (arquivo)", "Sel"}),
    Expand = Table.ExpandTableColumn(Enxuto, "Sel", Colunas, Colunas),

    Uteis = Table.SelectRows(Expand, each fnUtil[Texto]([MOLÉCULA]) <> null),

    Limpo = Table.TransformColumns(Uteis, {
        {"ÁREA TÉCNICA",        each fnUtil[Chave](_), type nullable text},
        {"SOLICITANTE",         each fnUtil[Chave](_), type nullable text},
        {"MOLÉCULA",            each fnUtil[Texto](_), type nullable text},
        {"STATUS",              each fnUtil[Chave](_), type nullable text},
        {"VIABILIDADE",         each fnUtil[Chave](_), type nullable text},
        {"OBS",                 each fnUtil[Texto](_), type nullable text},
        {"DATA DA SOLICITAÇÃO", each fnUtil[Data](_),  type nullable date},
        {"DATA DE PREVISÃO",    each fnUtil[Data](_),  type nullable date},
        {"DATA DO RECEBIMENTO", each fnUtil[Data](_),  type nullable date}
    }),

    ComSLA = Table.AddColumn(Limpo, "Dias de Resposta", each
        if [DATA DA SOLICITAÇÃO] = null or [DATA DO RECEBIMENTO] = null then null
        else Duration.Days([DATA DO RECEBIMENTO] - [DATA DA SOLICITAÇÃO]), Int64.Type),

    ComPrazo = Table.AddColumn(ComSLA, "Dentro do Prazo", each
        if [DATA DE PREVISÃO] = null or [DATA DO RECEBIMENTO] = null then null
        else [DATA DO RECEBIMENTO] <= [DATA DE PREVISÃO], type nullable logical),

    ComViab = Table.AddColumn(ComPrazo, "Viabilidade Padrão", each
        let v = [VIABILIDADE] in
        if v = null then "(Sem parecer)"
        else if Text.StartsWith(v, "VIÁVEL") or v = "VIAVEL" then "Viável"
        else if Text.Contains(v, "RESSALVA") then "Com ressalvas"
        else if Text.Contains(v, "INVIÁVEL") or Text.Contains(v, "INVIAVEL") then "Inviável"
        else Text.Proper(Text.Lower(v)), type text),

    Renom = Table.RenameColumns(ComViab, {
        {"ÁREA TÉCNICA", "Área Técnica"}, {"SOLICITANTE", "Solicitante"},
        {"MOLÉCULA", "Molécula"}, {"STATUS", "Status Solicitação"},
        {"DATA DA SOLICITAÇÃO", "Data Solicitação"},
        {"DATA DE PREVISÃO", "Data Previsão"},
        {"DATA DO RECEBIMENTO", "Data Recebimento"}}),

    Final = Table.RemoveColumns(Renom, {"DIAS DISPONÍVEIS", "RECEBIDO", "VIABILIDADE"}, MissingField.Ignore)
in
    Final
