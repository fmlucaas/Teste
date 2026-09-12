// =====================================================================
// Mapeamento — FATO principal. Uma linha por oportunidade, de todos os
// arquivos de mapeamento ativo do time. Já vem limpo e padronizado.
// =====================================================================
let
    Arquivos = Fonte_Arquivos,

    // --- abre cada workbook e pega a aba de mapeamento -------------------
    ComPasta = Table.AddColumn(Arquivos, "Conteudo", each
        let
            wb  = Excel.Workbook([Content], null, true),
            aba = Table.SelectRows(wb, each [Kind] = "Sheet" and
                     Comparer.OrdinalIgnoreCase(Text.Trim([Item]), pAbaMapeamento) = 0),
            dados = if Table.RowCount(aba) = 0 then null else aba{0}[Data],
            promovido = if dados = null then null
                        else Table.PromoteHeaders(dados, [PromoteAllScalars = true]),
            normalizado = if promovido = null then null
                          else fnUtil[NormalizaCabecalhos](promovido)
        in  normalizado),

    SoValidos = Table.SelectRows(ComPasta, each [Conteudo] <> null),

    // --- colunas que interessam (nomes JÁ normalizados: sem \n, sem espaço duplo)
    ColunasDesejadas = {
        "Entrada", "Responsável", "Gerência", "Molécula", "Código CI",
        "Marca do Referência BR", "Fornecedor / Parceiro", "País Fornecedor",
        "Contato Fornecedor", "Email Fornecedor",
        "Data de Entrada", "Data de Início do Projeto",
        "Data de Retomada do Projeto (se aplicável)",
        "Data de Finalização do Projeto em NN",
        "Categoria", "Coligada", "Área Terapêutica", "Fase Oportunidade NN",
        "Indicação", "Forma Farmacêutica", "Concentração", "Apresentação / SKU",
        "Projeto em andamento?", "Status de projeto (NN)", "Status interno",
        "Motivo Cancelamento Projeto", "Detalhamento do cancelamento",
        "Data Início Prospecção", "Data Conclusão Prospecção",
        "Data Inicio Processo de CDA", "Data de Concl. CDA", "CDA Status",
        "DATA - Inicio avaliação técnica inicial", "Checklist do parceiro",
        "DATA - Conclusão avaliação técnica Inicial",
        "DATA - Inicio avaliação marketing", "DATA - Conclusão avaliação marketing",
        "DATA - Inicio Negociações com parceiro",
        "Data de recebimento da primeira proposta comercial",
        "DATA - Conclusão Negociações com parceiro",
        "Moeda", "Preço de Fornecimento", "Margem Bruta (%)", "VPL (R$)",
        "Fat. Líq. (Peak Sales, R$)",
        "Fat. Líq. DRE (Ano1)", "Fat. Líq. DRE (Ano2)", "Fat. Líq. DRE (Ano3)",
        "Fat. Líq. DRE (Ano4)", "Fat. Líq. DRE (Ano5)",
        "Data de Início Summary", "Data Conclusão Summary",
        "Data inicio elaboração Term Sheet", "Data Concl. Term Sheet",
        "Início discussão contratual", "Data Assinatura Contrato",
        "Data estimada para Lançamento"
    },

    Padronizado = Table.AddColumn(SoValidos, "Selecionado", each
        fnUtil[SelecionaColunas]([Conteudo], ColunasDesejadas)),

    Enxuto = Table.SelectColumns(Padronizado,
                {"Arquivo", "Responsável (arquivo)", "Selecionado"}),

    Expandido = Table.ExpandTableColumn(Enxuto, "Selecionado",
                    ColunasDesejadas, ColunasDesejadas),

    // --- descarta linhas totalmente vazias / linhas de rodapé ------------
    ComLinhaUtil = Table.SelectRows(Expandido, each
        fnUtil[Texto]([Molécula]) <> null or fnUtil[Texto]([#"Fornecedor / Parceiro"]) <> null),

    // =====================================================================
    // PADRONIZAÇÃO  (aqui mora o maior ganho: a base tem MUITA divergência
    // de digitação — "Legrand"/"LEGRAND", "BRACE PHARM"/"BRACE PHARMA",
    // "INOVAÇÃO INCREMENTAL"/"INOVADOR INCREMENTAL", "concluído"/"CONCLUÍDO"…)
    // =====================================================================
    Limpo = Table.TransformColumns(ComLinhaUtil, {
        {"Entrada",                    each fnUtil[Chave](_), type nullable text},
        {"Responsável",                each fnUtil[Chave](_), type nullable text},
        {"Gerência",                   each fnUtil[Chave](_), type nullable text},
        {"Molécula",                   each fnUtil[Texto](_), type nullable text},
        {"Código CI",                  each fnUtil[Chave](_), type nullable text},
        {"Marca do Referência BR",     each fnUtil[Texto](_), type nullable text},
        {"Fornecedor / Parceiro",      each fnUtil[Texto](_), type nullable text},
        {"País Fornecedor",            each fnUtil[Texto](_), type nullable text},
        {"Contato Fornecedor",         each fnUtil[Texto](_), type nullable text},
        {"Email Fornecedor",           each fnUtil[Texto](_), type nullable text},
        {"Categoria",                  each fnUtil[Chave](_), type nullable text},
        {"Coligada",                   each fnUtil[Chave](_), type nullable text},
        {"Área Terapêutica",           each fnUtil[Chave](_), type nullable text},
        {"Fase Oportunidade NN",       each fnUtil[Chave](_), type nullable text},
        {"Indicação",                  each fnUtil[Texto](_), type nullable text},
        {"Forma Farmacêutica",         each fnUtil[Chave](_), type nullable text},
        {"Concentração",               each fnUtil[Texto](_), type nullable text},
        {"Apresentação / SKU",         each fnUtil[Texto](_), type nullable text},
        {"Projeto em andamento?",      each fnUtil[Chave](_), type nullable text},
        {"Status de projeto (NN)",     each fnUtil[Chave](_), type nullable text},
        {"Status interno",             each fnUtil[Chave](_), type nullable text},
        {"Motivo Cancelamento Projeto",each fnUtil[Chave](_), type nullable text},
        {"Detalhamento do cancelamento", each fnUtil[Texto](_), type nullable text},
        {"CDA Status",                 each fnUtil[Chave](_), type nullable text},
        {"Checklist do parceiro",      each fnUtil[Chave](_), type nullable text},
        {"Moeda",                      each fnUtil[Chave](_), type nullable text},
        // ---- datas ----
        {"Data de Entrada",                                     each fnUtil[Data](_), type nullable date},
        {"Data de Início do Projeto",                           each fnUtil[Data](_), type nullable date},
        {"Data de Retomada do Projeto (se aplicável)",          each fnUtil[Data](_), type nullable date},
        {"Data de Finalização do Projeto em NN",                each fnUtil[Data](_), type nullable date},
        {"Data Início Prospecção",                              each fnUtil[Data](_), type nullable date},
        {"Data Conclusão Prospecção",                           each fnUtil[Data](_), type nullable date},
        {"Data Inicio Processo de CDA",                         each fnUtil[Data](_), type nullable date},
        {"Data de Concl. CDA",                                  each fnUtil[Data](_), type nullable date},
        {"DATA - Inicio avaliação técnica inicial",             each fnUtil[Data](_), type nullable date},
        {"DATA - Conclusão avaliação técnica Inicial",          each fnUtil[Data](_), type nullable date},
        {"DATA - Inicio avaliação marketing",                   each fnUtil[Data](_), type nullable date},
        {"DATA - Conclusão avaliação marketing",                each fnUtil[Data](_), type nullable date},
        {"DATA - Inicio Negociações com parceiro",              each fnUtil[Data](_), type nullable date},
        {"Data de recebimento da primeira proposta comercial",  each fnUtil[Data](_), type nullable date},
        {"DATA - Conclusão Negociações com parceiro",           each fnUtil[Data](_), type nullable date},
        {"Data de Início Summary",                              each fnUtil[Data](_), type nullable date},
        {"Data Conclusão Summary",                              each fnUtil[Data](_), type nullable date},
        {"Data inicio elaboração Term Sheet",                   each fnUtil[Data](_), type nullable date},
        {"Data Concl. Term Sheet",                              each fnUtil[Data](_), type nullable date},
        {"Início discussão contratual",                         each fnUtil[Data](_), type nullable date},
        {"Data Assinatura Contrato",                            each fnUtil[Data](_), type nullable date},
        {"Data estimada para Lançamento",                       each fnUtil[Data](_), type nullable date},
        // ---- números ----
        {"Preço de Fornecimento",      each fnUtil[Numero](_), type nullable number},
        {"Margem Bruta (%)",           each fnUtil[Numero](_), type nullable number},
        {"VPL (R$)",                   each fnUtil[Numero](_), type nullable number},
        {"Fat. Líq. (Peak Sales, R$)", each fnUtil[Numero](_), type nullable number},
        {"Fat. Líq. DRE (Ano1)",       each fnUtil[Numero](_), type nullable number},
        {"Fat. Líq. DRE (Ano2)",       each fnUtil[Numero](_), type nullable number},
        {"Fat. Líq. DRE (Ano3)",       each fnUtil[Numero](_), type nullable number},
        {"Fat. Líq. DRE (Ano4)",       each fnUtil[Numero](_), type nullable number},
        {"Fat. Líq. DRE (Ano5)",       each fnUtil[Numero](_), type nullable number}
    }),

    // --- de-para de valores divergentes ---------------------------------
    ComResponsavel = Table.AddColumn(Limpo, "Responsável Final", each
        [Responsável] ?? [#"Responsável (arquivo)"], type nullable text),

    ComCategoria = Table.AddColumn(ComResponsavel, "Categoria Padrão", each
        let c = [Categoria] in
        if c = null then "(NÃO INFORMADO)"
        else if Text.Contains(c, "INCREMENTAL") then "INOVADOR INCREMENTAL"
        else if Text.Contains(c, "RADICAL")     then "INOVADOR RADICAL"
        else if Text.Contains(c, "SIMILAR") or Text.Contains(c, "GENÉRICO") then "SIMILAR / GENÉRICO"
        else if Text.Contains(c, "SUPLEMENTO") or Text.Contains(c, "ALIMENTO") then "ALIMENTO / SUPLEMENTO"
        else if Text.Contains(c, "FITO")        then "FITOTERÁPICO"
        else if Text.Contains(c, "SAÚDE")       then "PRODUTO PARA SAÚDE"
        else if Text.Contains(c, "BIOL")        then "BIOLÓGICO"
        else if Text.Contains(c, "COSM")        then "COSMÉTICO"
        else if Text.Contains(c, "M&A")         then "M&A"
        else c, type text),

    ComColigada = Table.AddColumn(ComCategoria, "Coligada Padrão", each
        let c = [Coligada] in
        if c = null then "(NÃO INFORMADO)"
        else if Text.StartsWith(c, "BRACE")     then "BRACE PHARMA"
        else if Text.Contains(c, "NON RETAIL") or Text.Contains(c, "NON-RETAIL") then "NON RETAIL"
        else if Text.Contains(c, "PRESCRI")     then "EMS PRESCRIÇÃO"
        else if Text.Contains(c, "GENÉRICO") or Text.Contains(c, "GENERICO") then "EMS GENÉRICOS"
        else if Text.Contains(c, "MARCAS")      then "EMS MARCAS"
        else c, type text),

    ComMotivo = Table.AddColumn(ComColigada, "Motivo Padrão", each
        let m = [Motivo Cancelamento Projeto] in
        if m = null then "(SEM MOTIVO REGISTRADO)"
        else if Text.Contains(m, "PARCERIA")      then "INDISPONIBILIDADE DE PARCERIA"
        else if Text.Contains(m, "CONTATO")       then "INDISPONIBILIDADE DE CONTATO"
        else if Text.Contains(m, "APRESENTAÇÃO")  then "INDISPONIBILIDADE DE APRESENTAÇÃO"
        else if Text.Contains(m, "MÉDIC")         then "INVIABILIDADE ÁREA MÉDICA"
        else if Text.Contains(m, "FINANCEIR")     then "INVIABILIDADE FINANCEIRA"
        else if Text.Contains(m, "REGULAT")       then "INVIABILIDADE REGULATÓRIA"
        else if Text.Contains(m, "PATENT")        then "INVIABILIDADE PATENTES"
        else if Text.Contains(m, "CONTRATUAL")    then "INVIABILIDADE CONTRATUAL"
        else if Text.Contains(m, "MODELO DE NEG") then "INVIABILIDADE MODELO DE NEGÓCIO"
        else if Text.Contains(m, "DESINTERESSE")  then "DESINTERESSE BU"
        else if Text.Contains(m, "PREMISSAS")     then "PREMISSAS BU"
        else if Text.Contains(m, "CMED")          then "PREÇO CMED"
        else if Text.Contains(m, "MERCADO")       then "MERCADO"
        else "OUTROS", type text),

    ComStatus = Table.AddColumn(ComMotivo, "Status NN", each
        let s = [#"Status de projeto (NN)"] in
        if s = null then "(SEM STATUS)"
        else if Text.Contains(s, "AGUARDANDO")   then "AGUARDANDO INÍCIO"
        else if Text.Contains(s, "PROSPEC")      then "PROSPECÇÃO"
        else if s = "CDA"                        then "CDA"
        else if Text.Contains(s, "TÉCNICA")      then "AV. TÉCNICA INICIAL"
        else if Text.Contains(s, "MARKETING")    then "AV. MARKETING"
        else if Text.Contains(s, "NEGOCIA")      then "NEGOCIAÇÃO"
        else if Text.Contains(s, "SUMMARY")      then "APROVAÇÃO SUMMARY"
        else if Text.Contains(s, "TERM SHEET")   then "TERM SHEET"
        else if Text.Contains(s, "CONTRATO")     then "CONTRATO"
        else s, type text),

    ComAndamento = Table.AddColumn(ComStatus, "Situação", each
        let a = [#"Projeto em andamento?"] in
        if a = null then "NÃO INFORMADO"
        else if Text.StartsWith(a, "SIM")   then "EM ANDAMENTO"
        else if Text.Contains(a, "STAND")   then "STAND BY"
        else if Text.StartsWith(a, "NÃO") or Text.StartsWith(a, "NAO") then "ENCERRADO"
        else a, type text),

    ComAtividade = Table.AddColumn(ComAndamento, "Atividade", each
        [Status interno] ?? "(NÃO INFORMADO)", type text),

    // --- franquia terapêutica (separa o prefixo "NR - ", "OFTA - ", "USK - ")
    ComFranquia = Table.AddColumn(ComAtividade, "Franquia", each
        let a = [Área Terapêutica] in
        if a = null then "(NÃO INFORMADO)"
        else if Text.Contains(a, " - ") then Text.BeforeDelimiter(a, " - ")
        else a, type text),

    ComSubArea = Table.AddColumn(ComFranquia, "Sub-área Terapêutica", each
        let a = [Área Terapêutica] in
        if a = null then "(NÃO INFORMADO)"
        else if Text.Contains(a, " - ") then Text.AfterDelimiter(a, " - ")
        else a, type text),

    // --- datas derivadas -------------------------------------------------
    ComInicio = Table.AddColumn(ComSubArea, "Data Início Efetiva", each
        [Data de Entrada] ?? [Data de Início do Projeto] ?? [Data Início Prospecção],
        type nullable date),

    ComUltimaData = Table.AddColumn(ComInicio, "Última Data Registrada", each
        List.Max(List.RemoveNulls({
            [Data de Entrada], [Data de Início do Projeto], [Data Início Prospecção],
            [Data Conclusão Prospecção], [Data Inicio Processo de CDA], [Data de Concl. CDA],
            [#"DATA - Inicio avaliação técnica inicial"], [#"DATA - Conclusão avaliação técnica Inicial"],
            [#"DATA - Inicio avaliação marketing"], [#"DATA - Conclusão avaliação marketing"],
            [#"DATA - Inicio Negociações com parceiro"], [#"DATA - Conclusão Negociações com parceiro"],
            [Data de Início Summary], [Data Conclusão Summary],
            [Data inicio elaboração Term Sheet], [Data Concl. Term Sheet],
            [Início discussão contratual], [Data de Finalização do Projeto em NN]
        })), type nullable date),

    // Fim efetivo: usa a data oficial; se não houver e o projeto não estiver
    // ativo, estima pela última data registrada (controlado por parâmetro).
    ComFim = Table.AddColumn(ComUltimaData, "Data Fim Efetiva", each
        if [Data de Finalização do Projeto em NN] <> null
            then [Data de Finalização do Projeto em NN]
        else if [Situação] = "EM ANDAMENTO" then null
        else if pEstimarFimQuandoAusente then [Última Data Registrada]
        else null, type nullable date),

    ComFimEstimado = Table.AddColumn(ComFim, "Fim Estimado?", each
        [Data de Finalização do Projeto em NN] = null and [Data Fim Efetiva] <> null,
        type logical),

    ComDuracao = Table.AddColumn(ComFimEstimado, "Dias em NN", each
        if [Data Início Efetiva] = null then null
        else Duration.Days(([Data Fim Efetiva] ?? Date.From(DateTime.LocalNow())) - [Data Início Efetiva]),
        Int64.Type),

    // --- chave única do projeto -----------------------------------------
    ComIndice = Table.AddIndexColumn(ComDuracao, "Seq", 1, 1, Int64.Type),
    ComID = Table.AddColumn(ComIndice, "ProjetoID", each
        Text.Combine({[Arquivo], Text.From([Seq])}, "#"), type text),

    Final = Table.RemoveColumns(ComID, {"Seq"}, MissingField.Ignore)
in
    Final
