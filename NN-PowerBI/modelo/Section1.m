section Section1;

shared pSiteSharePoint = "https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];

shared pBiblioteca = "Documentos Compartilhados" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];

shared pPastaMapeamentos = "DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];

shared pPastaHistorico = "DEMANDAS NN - ALIANÇA/HISTORICO" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false];

shared pAbaMapeamento = "Mapeamento NN" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];

shared pAbaSolicitacoes = "Solicitações" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false];

shared pCapacidadeMensalHoras = 168 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=true];

shared pAnoMinimo = 2022 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=false];

shared pEstimarFimQuandoAusente = true meta [IsParameterQuery=true, Type="Logical", IsParameterQueryRequired=false];

shared fnUtil = // =====================================================================
// fnUtil — funções utilitárias compartilhadas
// Crie UMA consulta em branco chamada exatamente  fnUtil  e cole isto.
// Uso: fnUtil[Data](valor) , fnUtil[Texto](valor) , etc.
// =====================================================================
let
    // ---- Limpeza de texto: remove NBSP, quebras de linha, espaços duplos ----
    Texto = (v as any) as nullable text =>
        let
            t0 = if v = null then null else Text.From(v),
            t1 = if t0 = null then null else
                 Text.Replace(Text.Replace(Text.Replace(Text.Replace(t0,
                     Character.FromNumber(160), " "), "#(cr)", " "), "#(lf)", " "), "#(tab)", " "),
            t2 = if t1 = null then null else Text.Trim(t1),
            t3 = if t2 = null then null else
                 List.Accumulate({1..5}, t2, (s, _) => Text.Replace(s, "  ", " ")),
            t4 = if t3 = null or t3 = "" then null else t3
        in  t4,

    // ---- Padroniza rótulos: MAIÚSCULA sem acento duplicado, para agrupar ----
    Chave = (v as any) as nullable text =>
        let t = Texto(v) in if t = null then null else Text.Upper(t),

    // ---- Título: Primeira Letra Maiúscula (para exibição) ----
    Titulo = (v as any) as nullable text =>
        let t = Texto(v) in if t = null then null else Text.Proper(Text.Lower(t)),

    // ---- Conversão de data à prova de bala -------------------------------
    // Aceita: data real, datetime, número (serial Excel), texto dd/MM/yyyy,
    // dd-MM-yyyy, dd.MM.yyyy, dd/MM.yyyy (erro de digitação real na base),
    // yyyy-MM-dd. Descarta anos fora de 2000..2040 (lixo tipo 1913 e 5039).
    Data = (v as any) as nullable date =>
        let
            bruto = if v = null then null else v,
            porTipo =
                if bruto = null then null
                else if Value.Is(bruto, type date) then bruto
                else if Value.Is(bruto, type datetime) then DateTime.Date(bruto)
                else if Value.Is(bruto, type datetimezone) then DateTime.Date(DateTimeZone.RemoveZone(bruto))
                else if Value.Is(bruto, type number) then
                    (if bruto >= 36526 and bruto <= 51136   // 2000-01-01 .. 2040-01-01
                     then Date.From(#date(1899,12,30) + #duration(Number.RoundDown(bruto),0,0,0))
                     else null)
                else null,
            comoTexto = if porTipo <> null then null else Texto(bruto),
            limpo = if comoTexto = null then null else
                    Text.Replace(Text.Replace(comoTexto, ".", "/"), "-", "/"),
            partes = if limpo = null then null else
                     List.Select(Text.Split(limpo, "/"), each Text.Trim(_) <> ""),
            numeros = if partes = null then null else
                      List.Transform(partes, each try Number.From(Text.Trim(Text.Start(_, 4))) otherwise null),
            valido  = if numeros = null then false else
                      (List.Count(numeros) >= 3 and not List.Contains(numeros, null)),
            porTexto =
                if not valido then null
                else let
                    a = numeros{0}, b = numeros{1}, c = numeros{2},
                    // yyyy/MM/dd  ou  dd/MM/yyyy
                    tentativa = if a > 31 then (try #date(a, b, c) otherwise null)
                                          else (try #date(c, b, a) otherwise null)
                in tentativa,
            final = porTipo ?? porTexto,
            saida = if final = null then null
                    else if Date.Year(final) < 2000 or Date.Year(final) > 2040 then null
                    else final
        in  saida,

    // ---- Número à prova de bala (aceita "1.234,56", "R$ 297", "138.82") ----
    Numero = (v as any) as nullable number =>
        let
            porTipo = if v = null then null
                      else if Value.Is(v, type number) then v
                      else null,
            txt = if porTipo <> null then null else Texto(v),
            // mantém apenas dígitos, vírgula, ponto e sinal negativo
            cru = if txt = null then null
                  else Text.Select(txt, {"0".."9", ",", ".", "-"}),
            temVirgula = cru <> null and Text.Contains(cru, ","),
            temPonto   = cru <> null and Text.Contains(cru, "."),
            qtdPontos  = if cru = null then 0
                         else List.Count(List.Select(Text.ToList(cru), each _ = ".")),
            // pt-BR "1.234,56"  -> ponto = milhar, vírgula = decimal
            // "1.234.567"       -> pontos = milhar
            // "138.82"          -> ponto = decimal
            padronizado =
                if cru = null then null
                else if temVirgula and temPonto then Text.Replace(Text.Replace(cru, ".", ""), ",", ".")
                else if temVirgula then Text.Replace(cru, ",", ".")
                else if qtdPontos > 1 then Text.Replace(cru, ".", "")
                else cru,
            porTexto = if padronizado = null or padronizado = "" or padronizado = "-" then null
                       else try Number.From(padronizado, "en-US") otherwise null
        in  porTipo ?? porTexto,

    // ---- Normaliza nomes de coluna (tira \n, espaços duplos, trim) ------
    NormalizaCabecalhos = (t as table) as table =>
        let
            nomes = Table.ColumnNames(t),
            limpos = List.Transform(nomes, each Texto(_) ?? "Coluna"),
            unicos = List.Accumulate(
                List.Positions(limpos), {},
                (acc, i) =>
                    let n = limpos{i},
                        n2 = if List.Contains(acc, n) then n & "_" & Text.From(i) else n
                    in acc & {n2}),
            renom = Table.RenameColumns(t, List.Zip({nomes, unicos}))
        in  renom,

    // ---- Garante que as colunas existam (cria como null se faltarem) ----
    GaranteColunas = (t as table, cols as list) as table =>
        let
            faltantes = List.Difference(cols, Table.ColumnNames(t)),
            completo = List.Accumulate(faltantes, t,
                (s, c) => Table.AddColumn(s, c, each null))
        in  completo,

    // ---- Seleciona só as colunas desejadas, tolerando ausências ---------
    SelecionaColunas = (t as table, cols as list) as table =>
        Table.SelectColumns(GaranteColunas(t, cols), cols),

    Saida = [
        Texto = Texto, Chave = Chave, Titulo = Titulo,
        Data = Data, Numero = Numero,
        NormalizaCabecalhos = NormalizaCabecalhos,
        GaranteColunas = GaranteColunas,
        SelecionaColunas = SelecionaColunas
    ]
in
    Saida;

shared Fonte_Arquivos = // =====================================================================
// Fonte_Arquivos — navega no SharePoint e devolve a lista de planilhas
// de mapeamento ativo. Uma linha por arquivo .xlsx da pasta.
// =====================================================================
let
    Origem = SharePoint.Contents(pSiteSharePoint, [ApiVersion = 15]),

    // entra numa subpasta pelo nome, ignorando maiúsc./minúsc.
    fnEntrar = (tbl as table, nome as text) as table =>
        let
            achado = Table.SelectRows(tbl, each
                        Comparer.OrdinalIgnoreCase(Text.Trim([Name]), Text.Trim(nome)) = 0),
            conteudo =
                if Table.RowCount(achado) = 0
                then error Error.Record("Pasta não encontrada",
                        "Não existe a pasta/biblioteca '" & nome & "' neste nível do SharePoint.",
                        "Níveis disponíveis: " & Text.Combine(tbl[Name], " | "))
                else achado{0}[Content]
        in  conteudo,

    Biblioteca = fnEntrar(Origem, pBiblioteca),

    Partes = List.Select(
                List.Transform(Text.Split(pPastaMapeamentos, "/"), Text.Trim),
                each _ <> ""),

    Pasta = List.Accumulate(Partes, Biblioteca, (estado, parte) => fnEntrar(estado, parte)),

    SoArquivos = Table.SelectRows(Pasta, each
        [Content] <> null
        and Text.EndsWith(Text.Lower([Name]), ".xlsx")
        and not Text.StartsWith([Name], "~$")),

    ComResponsavel = Table.AddColumn(SoArquivos, "Arquivo", each [Name], type text),

    // Nome do responsável deduzido do arquivo (fallback caso a coluna venha vazia)
    ComNomeArquivo = Table.AddColumn(ComResponsavel, "Responsável (arquivo)", each
        let
            semExt = Text.BeforeDelimiter([Name], ".", {0, RelativePosition.FromEnd}),
            semPrefixo = if Text.Contains(Text.Lower(semExt), "mapeamento")
                         then Text.AfterDelimiter(semExt, "_")
                         else semExt,
            comEspaco = Text.Trim(Text.Replace(Text.Replace(semPrefixo, "_", " "), "-", " "))
        in  if comEspaco = "" then semExt else Text.Upper(comEspaco), type text),

    Final = Table.SelectColumns(ComNomeArquivo,
                {"Content", "Arquivo", "Responsável (arquivo)", "Date modified"},
                MissingField.UseNull)
in
    Final;

shared Mapeamento = // =====================================================================
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
    Final;

shared #"Carregamento Mensal" = // =====================================================================
// Carregamento Mensal — FATO de período (snapshot reconstruído)
// Grão: 1 linha por PROJETO x MÊS em que ele esteve aberto em NN.
// Responde: "quantos projetos o analista tinha em JUNHO?", "quantos
// entraram, quantos saíram, e em que status ele estava naquele mês".
// Reconstruído a partir das datas de etapa já existentes na planilha —
// não depende de nenhuma infraestrutura nova.
// =====================================================================
let
    Hoje = Date.From(DateTime.LocalNow()),

    Base = Table.SelectRows(Mapeamento, each [Data Início Efetiva] <> null),

    ComFimSerie = Table.AddColumn(Base, "FimSerie", each
        let f = [Data Fim Efetiva] ?? Hoje in
        if f > Hoje then Hoje else f, type date),

    Valido = Table.SelectRows(ComFimSerie, each [FimSerie] >= [Data Início Efetiva]),

    // ---- gera um registro por mês entre início e fim --------------------
    ComMeses = Table.AddColumn(Valido, "MesInicio", each
        List.Generate(
            () => Date.StartOfMonth([Data Início Efetiva]),
            each _ <= Date.StartOfMonth([FimSerie]),
            each Date.AddMonths(_, 1)
        ), type list),

    Explodido = Table.ExpandListColumn(ComMeses, "MesInicio"),

    // data de corte usada para dizer em que status o projeto estava
    ComRef = Table.AddColumn(Explodido, "Data Referência", each
        List.Min({Date.EndOfMonth([MesInicio]), [FimSerie]}), type date),

    // ---- status reconstruído na data de referência ----------------------
    ComStatus = Table.AddColumn(ComRef, "Status no Mês", each
        let
            ref = [Data Referência],
            etapas = {
                [o = 1, s = "AGUARDANDO INÍCIO",   d = [Data Início Efetiva]],
                [o = 2, s = "PROSPECÇÃO",          d = [Data Início Prospecção] ?? [Data de Início do Projeto]],
                [o = 3, s = "CDA",                 d = [Data Inicio Processo de CDA]],
                [o = 4, s = "AV. TÉCNICA INICIAL", d = [#"DATA - Inicio avaliação técnica inicial"]],
                [o = 5, s = "AV. MARKETING",       d = [#"DATA - Inicio avaliação marketing"]],
                [o = 6, s = "NEGOCIAÇÃO",          d = [#"DATA - Inicio Negociações com parceiro"]],
                [o = 7, s = "APROVAÇÃO SUMMARY",   d = [Data de Início Summary]],
                [o = 8, s = "TERM SHEET",          d = [Data inicio elaboração Term Sheet]],
                [o = 9, s = "CONTRATO",            d = [Início discussão contratual]]
            },
            atingidas = List.Select(etapas, each _[d] <> null and _[d] <= ref),
            maiorOrdem = if List.Count(atingidas) = 0 then null
                         else List.Max(List.Transform(atingidas, each _[o])),
            porData = if maiorOrdem = null then null
                      else List.Select(etapas, each _[o] = maiorOrdem){0}[s]
        in
            porData ?? [Status NN], type text),

    // ---- marcadores de fluxo do mês ------------------------------------
    ComEntrada = Table.AddColumn(ComStatus, "Entrou no Mês", each
        Date.StartOfMonth([Data Início Efetiva]) = [MesInicio], type logical),

    ComSaida = Table.AddColumn(ComEntrada, "Saiu no Mês", each
        [Data Fim Efetiva] <> null
        and Date.StartOfMonth([Data Fim Efetiva]) = [MesInicio], type logical),

    ComAtivo = Table.AddColumn(ComSaida, "Ativo no Fim do Mês", each
        not [Saiu no Mês], type logical),

    ComChave = Table.AddColumn(ComAtivo, "ChaveMes", each
        Date.Year([MesInicio]) * 100 + Date.Month([MesInicio]), Int64.Type),

    // ---- enxuga: o resto vem por relacionamento com Mapeamento ----------
    Final = Table.SelectColumns(ComChave, {
        "ProjetoID", "Arquivo", "Responsável Final", "Gerência",
        "MesInicio", "Data Referência", "ChaveMes",
        "Status no Mês", "Entrou no Mês", "Saiu no Mês", "Ativo no Fim do Mês",
        "Categoria Padrão", "Coligada Padrão", "Franquia", "Motivo Padrão",
        "Atividade", "Situação", "Fim Estimado?"
    }, MissingField.UseNull),

    Renomeado = Table.RenameColumns(Final, {{"MesInicio", "Mês"}})
in
    Renomeado;

shared Calendário = let
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
    C13;

shared #"Status NN" = // Ordem do funil + agrupamento + sinalização do que está em desuso.
let
    Fonte = Table.FromRecords({
        [Status = "AGUARDANDO INÍCIO",   Ordem = 1,  Grupo = "Entrada",     #"Em Uso" = true],
        [Status = "PROSPECÇÃO",          Ordem = 2,  Grupo = "Prospecção",  #"Em Uso" = true],
        [Status = "CDA",                 Ordem = 3,  Grupo = "Prospecção",  #"Em Uso" = true],
        [Status = "AV. TÉCNICA INICIAL", Ordem = 4,  Grupo = "Avaliação",   #"Em Uso" = true],
        [Status = "AV. MARKETING",       Ordem = 5,  Grupo = "Avaliação",   #"Em Uso" = true],
        [Status = "NEGOCIAÇÃO",          Ordem = 6,  Grupo = "Negociação",  #"Em Uso" = true],
        [Status = "APROVAÇÃO SUMMARY",   Ordem = 7,  Grupo = "Negociação",  #"Em Uso" = true],
        [Status = "TERM SHEET",          Ordem = 8,  Grupo = "Contratação", #"Em Uso" = true],
        [Status = "CONTRATO",            Ordem = 9,  Grupo = "Contratação", #"Em Uso" = true],
        // ---- etapas de Projetos & Alianças: continuam no de-para da planilha,
        //      mas NÃO têm nenhuma coluna preenchida hoje (em desuso em NN) ----
        [Status = "INICIAÇÃO",           Ordem = 10, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "DUE DILIGENCE",       Ordem = 11, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "REGULATORY PLAN",     Ordem = 12, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "PRÉ-SUBMISSÃO",       Ordem = 13, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "AVALIAÇÃO ANVISA",    Ordem = 14, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "LANÇAMENTO",          Ordem = 15, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "LANÇADO",             Ordem = 16, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "EM DESCONTINUAÇÃO",   Ordem = 17, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "DESCONTINUADO",       Ordem = 18, Grupo = "Pós-NN (P&A)", #"Em Uso" = false],
        [Status = "CANCELADO",           Ordem = 19, Grupo = "Encerrado",    #"Em Uso" = false],
        [Status = "(SEM STATUS)",        Ordem = 99, Grupo = "Sem Status",   #"Em Uso" = true]
    }),
    // acrescenta qualquer status novo que apareça na base e não esteja na lista
    DaBase = List.Distinct(List.RemoveNulls(Mapeamento[Status NN])),
    Faltantes = List.Difference(DaBase, Fonte[Status]),
    Extras = Table.FromRecords(List.Transform(Faltantes, each
        [Status = _, Ordem = 98, Grupo = "Não mapeado", #"Em Uso" = true])),
    Uniao = Table.Combine({Fonte, Extras}),
    Tipado = Table.TransformColumnTypes(Uniao,
        {{"Status", type text}, {"Ordem", Int64.Type}, {"Grupo", type text}, {"Em Uso", type logical}})
in
    Tipado;

shared Complexidade = // De-para Categoria -> Complexidade. EDITE AQUI se a régua do time mudar.
let
    Fonte = Table.FromRecords({
        [#"Categoria Padrão" = "INOVADOR RADICAL",     Complexidade = "ALTO",  #"Ordem Complexidade" = 3],
        [#"Categoria Padrão" = "BIOLÓGICO",            Complexidade = "ALTO",  #"Ordem Complexidade" = 3],
        [#"Categoria Padrão" = "M&A",                  Complexidade = "ALTO",  #"Ordem Complexidade" = 3],
        [#"Categoria Padrão" = "INOVADOR INCREMENTAL", Complexidade = "MÉDIO", #"Ordem Complexidade" = 2],
        [#"Categoria Padrão" = "PRODUTO PARA SAÚDE",   Complexidade = "MÉDIO", #"Ordem Complexidade" = 2],
        [#"Categoria Padrão" = "COSMÉTICO",            Complexidade = "MÉDIO", #"Ordem Complexidade" = 2],
        [#"Categoria Padrão" = "SIMILAR / GENÉRICO",   Complexidade = "BAIXO", #"Ordem Complexidade" = 1],
        [#"Categoria Padrão" = "ALIMENTO / SUPLEMENTO",Complexidade = "BAIXO", #"Ordem Complexidade" = 1],
        [#"Categoria Padrão" = "FITOTERÁPICO",         Complexidade = "BAIXO", #"Ordem Complexidade" = 1],
        [#"Categoria Padrão" = "(NÃO INFORMADO)",      Complexidade = "MÉDIO", #"Ordem Complexidade" = 2]
    }),
    DaBase = List.Distinct(List.RemoveNulls(Mapeamento[Categoria Padrão])),
    Faltantes = List.Difference(DaBase, Fonte[Categoria Padrão]),
    Extras = Table.FromRecords(List.Transform(Faltantes, each
        [#"Categoria Padrão" = _, Complexidade = "MÉDIO", #"Ordem Complexidade" = 2])),
    Uniao = Table.Combine({Fonte, Extras}),
    Tipado = Table.TransformColumnTypes(Uniao,
        {{"Categoria Padrão", type text}, {"Complexidade", type text}, {"Ordem Complexidade", Int64.Type}})
in
    Tipado;

shared Esforço = // Horas/mês consumidas por UM projeto, por Status x Complexidade.
// >>> ESTA É A RÉGUA DE CARREGAMENTO. Ajuste os números com o time. <<<
let
    Fonte = Table.FromRecords({
        [Status = "AGUARDANDO INÍCIO",   BAIXO = 0.5, #"MÉDIO" = 1,  ALTO = 1.5],
        [Status = "PROSPECÇÃO",          BAIXO = 2,   #"MÉDIO" = 3,  ALTO = 4],
        [Status = "CDA",                 BAIXO = 1,   #"MÉDIO" = 1.5,ALTO = 2],
        [Status = "AV. TÉCNICA INICIAL", BAIXO = 4,   #"MÉDIO" = 6,  ALTO = 8],
        [Status = "AV. MARKETING",       BAIXO = 3,   #"MÉDIO" = 4,  ALTO = 6],
        [Status = "NEGOCIAÇÃO",          BAIXO = 6,   #"MÉDIO" = 8,  ALTO = 12],
        [Status = "APROVAÇÃO SUMMARY",   BAIXO = 3,   #"MÉDIO" = 4,  ALTO = 6],
        [Status = "TERM SHEET",          BAIXO = 5,   #"MÉDIO" = 7,  ALTO = 10],
        [Status = "CONTRATO",            BAIXO = 6,   #"MÉDIO" = 8,  ALTO = 12],
        [Status = "(SEM STATUS)",        BAIXO = 0,   #"MÉDIO" = 0,  ALTO = 0]
    }),
    Despivotado = Table.UnpivotOtherColumns(Fonte, {"Status"}, "Complexidade", "Horas Mês"),
    Tipado = Table.TransformColumnTypes(Despivotado,
        {{"Status", type text}, {"Complexidade", type text}, {"Horas Mês", type number}}),
    Chave = Table.AddColumn(Tipado, "ChaveEsforco", each [Status] & "|" & [Complexidade], type text)
in
    Chave;

shared Equipe = // Gerada da própria base — não precisa manter lista de nomes.
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
    ComNome;

shared #"Unidade de Negócio" = // De-para Coligada -> Unidade de Negócio (o eixo dos reports de BU).
let
    Fonte = Table.FromRecords({
        [#"Coligada Padrão" = "EMS PRESCRIÇÃO", #"Unidade de Negócio" = "EMS Prescrição", Ordem = 1],
        [#"Coligada Padrão" = "NON RETAIL",     #"Unidade de Negócio" = "Non-Retail",     Ordem = 2],
        [#"Coligada Padrão" = "USK",            #"Unidade de Negócio" = "USK",            Ordem = 3],
        [#"Coligada Padrão" = "OFTA",           #"Unidade de Negócio" = "Ofta",           Ordem = 4],
        [#"Coligada Padrão" = "OTC",            #"Unidade de Negócio" = "OTC",            Ordem = 5],
        [#"Coligada Padrão" = "BRACE PHARMA",   #"Unidade de Negócio" = "Brace Pharma",   Ordem = 6],
        [#"Coligada Padrão" = "LEGRAND",        #"Unidade de Negócio" = "Legrand",        Ordem = 7],
        [#"Coligada Padrão" = "MULTILAB",       #"Unidade de Negócio" = "Multilab",       Ordem = 8],
        [#"Coligada Padrão" = "GERMED",         #"Unidade de Negócio" = "Germed",         Ordem = 9],
        [#"Coligada Padrão" = "EMS MARCAS",     #"Unidade de Negócio" = "EMS Marcas",     Ordem = 10],
        [#"Coligada Padrão" = "EMS GENÉRICOS",  #"Unidade de Negócio" = "EMS Genéricos",  Ordem = 11],
        [#"Coligada Padrão" = "NOVA QUÍMICA",   #"Unidade de Negócio" = "Nova Química",   Ordem = 12],
        [#"Coligada Padrão" = "(NÃO INFORMADO)",#"Unidade de Negócio" = "(Não informado)",Ordem = 99]
    }),
    DaBase = List.Distinct(List.RemoveNulls(Mapeamento[Coligada Padrão])),
    Faltantes = List.Difference(DaBase, Fonte[Coligada Padrão]),
    Extras = Table.FromRecords(List.Transform(Faltantes, each
        [#"Coligada Padrão" = _, #"Unidade de Negócio" = Text.Proper(Text.Lower(_)), Ordem = 98])),
    Uniao = Table.Combine({Fonte, Extras}),
    Tipado = Table.TransformColumnTypes(Uniao,
        {{"Coligada Padrão", type text}, {"Unidade de Negócio", type text}, {"Ordem", Int64.Type}})
in
    Tipado;

shared #"Motivo Cancelamento" = let
    Fonte = Table.FromRecords({
        [#"Motivo Padrão" = "INDISPONIBILIDADE DE PARCERIA",     #"Motivo" = "Indisponibilidade de Parceria",     Bloco = "Parceiro"],
        [#"Motivo Padrão" = "INDISPONIBILIDADE DE CONTATO",      #"Motivo" = "Indisponibilidade de Contato",      Bloco = "Parceiro"],
        [#"Motivo Padrão" = "INDISPONIBILIDADE DE APRESENTAÇÃO", #"Motivo" = "Indisponibilidade de Apresentação", Bloco = "Parceiro"],
        [#"Motivo Padrão" = "INVIABILIDADE ÁREA MÉDICA",         #"Motivo" = "Inviabilidade Área Médica",         Bloco = "Técnico"],
        [#"Motivo Padrão" = "INVIABILIDADE REGULATÓRIA",         #"Motivo" = "Inviabilidade Regulatória",         Bloco = "Técnico"],
        [#"Motivo Padrão" = "INVIABILIDADE PATENTES",            #"Motivo" = "Inviabilidade Patentes",            Bloco = "Técnico"],
        [#"Motivo Padrão" = "INVIABILIDADE FINANCEIRA",          #"Motivo" = "Inviabilidade Financeira",          Bloco = "Financeiro"],
        [#"Motivo Padrão" = "PREÇO CMED",                        #"Motivo" = "Preço CMED",                        Bloco = "Financeiro"],
        [#"Motivo Padrão" = "INVIABILIDADE CONTRATUAL",          #"Motivo" = "Inviabilidade Contratual",          Bloco = "Contratual"],
        [#"Motivo Padrão" = "INVIABILIDADE MODELO DE NEGÓCIO",   #"Motivo" = "Inviabilidade Modelo de Negócio",   Bloco = "Contratual"],
        [#"Motivo Padrão" = "DESINTERESSE BU",                   #"Motivo" = "Desinteresse BU",                   Bloco = "Unidade de Negócio"],
        [#"Motivo Padrão" = "PREMISSAS BU",                      #"Motivo" = "Premissas BU",                      Bloco = "Unidade de Negócio"],
        [#"Motivo Padrão" = "MERCADO",                           #"Motivo" = "Mercado",                           Bloco = "Mercado"],
        [#"Motivo Padrão" = "OUTROS",                            #"Motivo" = "Outros",                            Bloco = "Outros"],
        [#"Motivo Padrão" = "(SEM MOTIVO REGISTRADO)",           #"Motivo" = "(Sem motivo registrado)",           Bloco = "Sem registro"]
    }),
    Tipado = Table.TransformColumnTypes(Fonte,
        {{"Motivo Padrão", type text}, {"Motivo", type text}, {"Bloco", type text}})
in
    Tipado;

shared País = // Lê a aba "PAÍS" do primeiro arquivo que a tiver (traz o ISO ALPHA-3,
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
    Tipado;

shared Solicitações = // Solicitações — // FATO de demandas às áreas técnicas (Médica, Patentes,
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
    Final;

shared #"Qualidade de Dados" = // Qualidade de Dados — // uma linha por PROBLEMA encontrado.
// É o que transforma o dashboard em ferramenta de gestão da própria base:
// mostra, por responsável, exatamente o que falta preencher.
// =====================================================================
let
    M = Mapeamento,

    fnRegra = (nome as text, gravidade as text, criterio as function, impacto as text) as table =>
        let
            afetados = Table.SelectRows(M, criterio),
            comCampos = Table.SelectColumns(afetados,
                {"ProjetoID", "Arquivo", "Responsável Final", "Molécula",
                 "Fornecedor / Parceiro", "Status NN", "Situação"}, MissingField.UseNull),
            comRegra = Table.AddColumn(comCampos, "Regra", each nome, type text),
            comGrav = Table.AddColumn(comRegra, "Gravidade", each gravidade, type text),
            comImp = Table.AddColumn(comGrav, "Impacto", each impacto, type text)
        in  comImp,

    Regras = {
        fnRegra("Projeto encerrado sem Data de Finalização", "Alta",
            each [Situação] <> "EM ANDAMENTO" and [Data de Finalização do Projeto em NN] = null,
            "Impede medir quando o projeto saiu do carregamento — o histórico do mês fica estimado."),
        fnRegra("Projeto encerrado sem Motivo de Cancelamento", "Alta",
            each [Situação] = "ENCERRADO" and [Motivo Cancelamento Projeto] = null,
            "Impede o report de motivos de cancelamento por unidade de negócio."),
        fnRegra("Sem Data de Entrada", "Alta",
            each [Data de Entrada] = null,
            "Projeto não entra em nenhuma análise temporal."),
        fnRegra("Sem Coligada / Unidade de Negócio", "Alta",
            each [Coligada] = null,
            "Projeto não aparece no report da BU."),
        fnRegra("Sem Categoria", "Média",
            each [Categoria] = null,
            "Sem categoria não há complexidade — o cálculo de horas usa MÉDIO por padrão."),
        fnRegra("Sem Área Terapêutica", "Média",
            each [Área Terapêutica] = null,
            "Projeto não aparece nos cortes por franquia."),
        fnRegra("Sem Status interno (NN / Interno / Parceiro)", "Média",
            each [Status interno] = null,
            "Impede a visão de onde o tempo do time está sendo gasto."),
        fnRegra("Sem Fase da Oportunidade", "Baixa",
            each [Fase Oportunidade NN] = null,
            "Falta no gráfico de maturidade das moléculas."),
        fnRegra("Sem País do Fornecedor", "Baixa",
            each [País Fornecedor] = null,
            "Projeto não aparece no mapa."),
        fnRegra("Em Negociação sem dado financeiro", "Média",
            each List.Contains({"NEGOCIAÇÃO", "APROVAÇÃO SUMMARY", "TERM SHEET", "CONTRATO"}, [Status NN])
                 and [#"VPL (R$)"] = null and [#"Margem Bruta (%)"] = null,
            "Projeto em fase avançada sem VPL nem margem — a visão financeira fica cega."),
        fnRegra("Data de fim anterior à data de início", "Alta",
            each [Data Fim Efetiva] <> null and [Data Início Efetiva] <> null
                 and [Data Fim Efetiva] < [Data Início Efetiva],
            "Inconsistência de datas: distorce duração e histórico.")
    },

    Tudo = Table.Combine(Regras),
    Tipado = Table.TransformColumnTypes(Tudo,
        {{"Regra", type text}, {"Gravidade", type text}, {"Impacto", type text}}),
    ComPeso = Table.AddColumn(Tipado, "Peso", each
        if [Gravidade] = "Alta" then 3 else if [Gravidade] = "Média" then 2 else 1, Int64.Type)
in
    ComPeso;

shared #"Histórico Snapshots" = // Histórico Snapshots — // OPCIONAL. Lê a pasta HISTORICO, onde cada
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
    Resultado;

shared _Medidas = let
    Fonte = #table(type table [_ = text], {{"x"}})
in
    Fonte;
