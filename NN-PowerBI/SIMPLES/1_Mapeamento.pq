// ===========================================================================
//  CONSULTA 1 de 3  —  MAPEAMENTO
//  Cole este texto inteiro no Editor Avançado e renomeie a consulta para:
//      Mapeamento
//  (o nome precisa ser exatamente esse, com M maiúsculo)
//
//  Se um dia o caminho do SharePoint mudar, altere só as 4 linhas abaixo.
// ===========================================================================
let
    SITE       = "https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS",
    BIBLIOTECA = "Documentos Compartilhados",
    PASTA      = "DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS",
    ABA        = "Mapeamento NN",

    // ---------- limpeza de texto (tira espaço duplo, quebra de linha, NBSP) ----------
    fnTexto = (v as any) as nullable text =>
        let t = if v = null then null else Text.Trim(
                  Text.Replace(Text.Replace(Text.Replace(Text.From(v),
                    Character.FromNumber(160), " "), "#(cr)", " "), "#(lf)", " "))
        in  if t = null or t = "" then null
            else List.Accumulate({1..4}, t, (s, _) => Text.Replace(s, "  ", " ")),
    fnChave = (v as any) as nullable text =>
        let t = fnTexto(v) in if t = null then null else Text.Upper(t),

    // ---------- datas: aceita data real, número do Excel e texto dd/mm/aaaa ----------
    fnData = (v as any) as nullable date =>
        let
            porTipo =
                if v = null then null
                else if Value.Is(v, type date) then v
                else if Value.Is(v, type datetime) then DateTime.Date(v)
                else if Value.Is(v, type number) then
                    (if v >= 36526 and v <= 51136
                     then Date.From(#date(1899,12,30) + #duration(Number.RoundDown(v),0,0,0)) else null)
                else null,
            txt = if porTipo <> null then null else fnTexto(v),
            limpo = if txt = null then null else Text.Replace(Text.Replace(txt, ".", "/"), "-", "/"),
            partes = if limpo = null then null else List.Select(Text.Split(limpo, "/"), each Text.Trim(_) <> ""),
            nums = if partes = null then null
                   else List.Transform(partes, each try Number.From(Text.Trim(Text.Start(_,4))) otherwise null),
            ok = if nums = null then false else (List.Count(nums) >= 3 and not List.Contains(nums, null)),
            porTexto = if not ok then null
                       else (if nums{0} > 31 then try #date(nums{0}, nums{1}, nums{2}) otherwise null
                                             else try #date(nums{2}, nums{1}, nums{0}) otherwise null),
            d = porTipo ?? porTexto
        in  if d = null then null else (if Date.Year(d) < 2000 or Date.Year(d) > 2040 then null else d),

    fnNumero = (v as any) as nullable number =>
        if v = null then null else if Value.Is(v, type number) then v
        else let
            cru = Text.Select(fnTexto(v) ?? "", {"0".."9", ",", ".", "-"}),
            temV = Text.Contains(cru, ","), temP = Text.Contains(cru, "."),
            qtdP = List.Count(List.Select(Text.ToList(cru), each _ = ".")),
            pad = if temV and temP then Text.Replace(Text.Replace(cru,".",""),",",".")
                  else if temV then Text.Replace(cru,",",".")
                  else if qtdP > 1 then Text.Replace(cru,".","") else cru
        in  if pad = "" or pad = "-" then null else try Number.From(pad, "en-US") otherwise null,

    // ---------- navega até a pasta no SharePoint ----------
    Origem = SharePoint.Contents(SITE, [ApiVersion = 15]),
    fnEntrar = (tbl as table, nome as text) as table =>
        let achado = Table.SelectRows(tbl, each
                Comparer.OrdinalIgnoreCase(Text.Trim([Name]), Text.Trim(nome)) = 0)
        in  if Table.RowCount(achado) = 0
            then error "Não encontrei '" & nome & "'. Disponíveis aqui: " & Text.Combine(tbl[Name], " | ")
            else achado{0}[Content],
    Biblioteca = fnEntrar(Origem, BIBLIOTECA),
    Pasta = List.Accumulate(
        List.Select(List.Transform(Text.Split(PASTA, "/"), Text.Trim), each _ <> ""),
        Biblioteca, (e, p) => fnEntrar(e, p)),

    Arquivos = Table.SelectRows(Pasta, each
        [Content] <> null and Text.EndsWith(Text.Lower([Name]), ".xlsx")
        and not Text.StartsWith([Name], "~$")),

    // ---------- abre cada planilha e pega a aba do mapeamento ----------
    ComAba = Table.AddColumn(Arquivos, "Tab", each
        let
            wb = Excel.Workbook([Content], null, true),
            aba = Table.SelectRows(wb, each [Kind] = "Sheet"
                    and Comparer.OrdinalIgnoreCase(Text.Trim([Item]), ABA) = 0),
            dados = if Table.RowCount(aba) = 0 then null else aba{0}[Data],
            prom = if dados = null then null
                   else Table.PromoteHeaders(dados, [PromoteAllScalars = true]),
            nomes = if prom = null then null else Table.ColumnNames(prom),
            limpos = if prom = null then null else List.Transform(nomes, each fnTexto(_) ?? "Coluna"),
            unicos = if prom = null then null else List.Accumulate(List.Positions(limpos), {},
                (acc, i) => acc & {if List.Contains(acc, limpos{i}) then limpos{i} & "_" & Text.From(i) else limpos{i}}),
            norm = if prom = null then null else Table.RenameColumns(prom, List.Zip({nomes, unicos}))
        in  norm),
    Validos = Table.SelectRows(ComAba, each [Tab] <> null),

    COLS = {"Entrada","Responsável","Gerência","Molécula","Código CI","Marca do Referência BR",
            "Fornecedor / Parceiro","País Fornecedor","Data de Entrada","Data de Início do Projeto",
            "Data de Finalização do Projeto em NN","Categoria","Coligada","Área Terapêutica",
            "Fase Oportunidade NN","Indicação","Forma Farmacêutica","Concentração",
            "Projeto em andamento?","Status de projeto (NN)","Status interno",
            "Motivo Cancelamento Projeto","Detalhamento do cancelamento",
            "Data Início Prospecção","Data Conclusão Prospecção","Data Inicio Processo de CDA",
            "Data de Concl. CDA","CDA Status","DATA - Inicio avaliação técnica inicial",
            "DATA - Conclusão avaliação técnica Inicial","DATA - Inicio avaliação marketing",
            "DATA - Conclusão avaliação marketing","DATA - Inicio Negociações com parceiro",
            "Data de recebimento da primeira proposta comercial","Data de Início Summary",
            "Data inicio elaboração Term Sheet","Início discussão contratual","Moeda",
            "Margem Bruta (%)","VPL (R$)","Fat. Líq. (Peak Sales, R$)","Fat. Líq. DRE (Ano1)",
            "Fat. Líq. DRE (Ano2)","Fat. Líq. DRE (Ano3)","Fat. Líq. DRE (Ano4)","Fat. Líq. DRE (Ano5)"},

    // cria as colunas que faltarem em algum arquivo, para nenhum arquivo quebrar
    Selec = Table.AddColumn(Validos, "Sel", each
        let
            falta = List.Difference(COLS, Table.ColumnNames([Tab])),
            compl = List.Accumulate(falta, [Tab], (s, c) => Table.AddColumn(s, c, each null))
        in  Table.SelectColumns(compl, COLS)),

    Expandido = Table.ExpandTableColumn(
        Table.SelectColumns(Selec, {"Name", "Sel"}), "Sel", COLS, COLS),
    Renom = Table.RenameColumns(Expandido, {{"Name", "Arquivo"}}),
    Uteis = Table.SelectRows(Renom, each
        fnTexto([Molécula]) <> null or fnTexto([#"Fornecedor / Parceiro"]) <> null),

    // ---------- padroniza ----------
    Limpo = Table.TransformColumns(Uteis, {
        {"Entrada", each fnChave(_), type nullable text},
        {"Responsável", each fnChave(_), type nullable text},
        {"Gerência", each fnChave(_), type nullable text},
        {"Molécula", each fnTexto(_), type nullable text},
        {"Marca do Referência BR", each fnTexto(_), type nullable text},
        {"Fornecedor / Parceiro", each fnTexto(_), type nullable text},
        {"País Fornecedor", each fnTexto(_), type nullable text},
        {"Categoria", each fnChave(_), type nullable text},
        {"Coligada", each fnChave(_), type nullable text},
        {"Área Terapêutica", each fnChave(_), type nullable text},
        {"Fase Oportunidade NN", each fnChave(_), type nullable text},
        {"Indicação", each fnTexto(_), type nullable text},
        {"Forma Farmacêutica", each fnChave(_), type nullable text},
        {"Projeto em andamento?", each fnChave(_), type nullable text},
        {"Status de projeto (NN)", each fnChave(_), type nullable text},
        {"Status interno", each fnChave(_), type nullable text},
        {"Motivo Cancelamento Projeto", each fnChave(_), type nullable text},
        {"Detalhamento do cancelamento", each fnTexto(_), type nullable text},
        {"CDA Status", each fnChave(_), type nullable text},
        {"Moeda", each fnChave(_), type nullable text},
        {"Data de Entrada", each fnData(_), type nullable date},
        {"Data de Início do Projeto", each fnData(_), type nullable date},
        {"Data de Finalização do Projeto em NN", each fnData(_), type nullable date},
        {"Data Início Prospecção", each fnData(_), type nullable date},
        {"Data Conclusão Prospecção", each fnData(_), type nullable date},
        {"Data Inicio Processo de CDA", each fnData(_), type nullable date},
        {"Data de Concl. CDA", each fnData(_), type nullable date},
        {"DATA - Inicio avaliação técnica inicial", each fnData(_), type nullable date},
        {"DATA - Conclusão avaliação técnica Inicial", each fnData(_), type nullable date},
        {"DATA - Inicio avaliação marketing", each fnData(_), type nullable date},
        {"DATA - Conclusão avaliação marketing", each fnData(_), type nullable date},
        {"DATA - Inicio Negociações com parceiro", each fnData(_), type nullable date},
        {"Data de recebimento da primeira proposta comercial", each fnData(_), type nullable date},
        {"Data de Início Summary", each fnData(_), type nullable date},
        {"Data inicio elaboração Term Sheet", each fnData(_), type nullable date},
        {"Início discussão contratual", each fnData(_), type nullable date},
        {"Margem Bruta (%)", each fnNumero(_), type nullable number},
        {"VPL (R$)", each fnNumero(_), type nullable number},
        {"Fat. Líq. (Peak Sales, R$)", each fnNumero(_), type nullable number},
        {"Fat. Líq. DRE (Ano1)", each fnNumero(_), type nullable number},
        {"Fat. Líq. DRE (Ano2)", each fnNumero(_), type nullable number},
        {"Fat. Líq. DRE (Ano3)", each fnNumero(_), type nullable number},
        {"Fat. Líq. DRE (Ano4)", each fnNumero(_), type nullable number},
        {"Fat. Líq. DRE (Ano5)", each fnNumero(_), type nullable number}
    }),

    // ---------- colunas prontas para usar nos gráficos ----------
    C1 = Table.AddColumn(Limpo, "Categoria Padrão", each
        let c = [Categoria] in
        if c = null then "(NÃO INFORMADO)"
        else if Text.Contains(c,"INCREMENTAL") then "INOVADOR INCREMENTAL"
        else if Text.Contains(c,"RADICAL") then "INOVADOR RADICAL"
        else if Text.Contains(c,"SIMILAR") or Text.Contains(c,"GENÉRICO") then "SIMILAR / GENÉRICO"
        else if Text.Contains(c,"SUPLEMENTO") or Text.Contains(c,"ALIMENTO") then "ALIMENTO / SUPLEMENTO"
        else if Text.Contains(c,"FITO") then "FITOTERÁPICO"
        else if Text.Contains(c,"SAÚDE") then "PRODUTO PARA SAÚDE"
        else if Text.Contains(c,"BIOL") then "BIOLÓGICO"
        else if Text.Contains(c,"COSM") then "COSMÉTICO" else c, type text),

    C2 = Table.AddColumn(C1, "Unidade de Negócio", each
        let c = [Coligada] in
        if c = null then "(Não informado)"
        else if Text.StartsWith(c,"BRACE") then "Brace Pharma"
        else if Text.Contains(c,"NON RETAIL") or Text.Contains(c,"NON-RETAIL") then "Non-Retail"
        else if Text.Contains(c,"PRESCRI") then "EMS Prescrição"
        else if Text.Contains(c,"GENÉRICO") or Text.Contains(c,"GENERICO") then "EMS Genéricos"
        else if Text.Contains(c,"MARCAS") then "EMS Marcas"
        else Text.Proper(Text.Lower(c)), type text),

    C3 = Table.AddColumn(C2, "Motivo", each
        let m = [Motivo Cancelamento Projeto] in
        if m = null then "(Sem motivo registrado)"
        else if Text.Contains(m,"PARCERIA") then "Indisponibilidade de Parceria"
        else if Text.Contains(m,"CONTATO") then "Indisponibilidade de Contato"
        else if Text.Contains(m,"APRESENTAÇÃO") then "Indisponibilidade de Apresentação"
        else if Text.Contains(m,"MÉDIC") then "Inviabilidade Área Médica"
        else if Text.Contains(m,"FINANCEIR") then "Inviabilidade Financeira"
        else if Text.Contains(m,"REGULAT") then "Inviabilidade Regulatória"
        else if Text.Contains(m,"PATENT") then "Inviabilidade Patentes"
        else if Text.Contains(m,"CONTRATUAL") then "Inviabilidade Contratual"
        else if Text.Contains(m,"MODELO DE NEG") then "Inviabilidade Modelo de Negócio"
        else if Text.Contains(m,"DESINTERESSE") then "Desinteresse BU"
        else if Text.Contains(m,"PREMISSAS") then "Premissas BU"
        else if Text.Contains(m,"CMED") then "Preço CMED"
        else if Text.Contains(m,"MERCADO") then "Mercado" else "Outros", type text),

    C4 = Table.AddColumn(C3, "Status NN", each
        let s = [#"Status de projeto (NN)"] in
        if s = null then "(SEM STATUS)"
        else if Text.Contains(s,"AGUARDANDO") then "AGUARDANDO INÍCIO"
        else if Text.Contains(s,"PROSPEC") then "PROSPECÇÃO"
        else if s = "CDA" then "CDA"
        else if Text.Contains(s,"TÉCNICA") then "AV. TÉCNICA INICIAL"
        else if Text.Contains(s,"MARKETING") then "AV. MARKETING"
        else if Text.Contains(s,"NEGOCIA") then "NEGOCIAÇÃO"
        else if Text.Contains(s,"SUMMARY") then "APROVAÇÃO SUMMARY"
        else if Text.Contains(s,"TERM SHEET") then "TERM SHEET"
        else if Text.Contains(s,"CONTRATO") then "CONTRATO" else s, type text),

    C5 = Table.AddColumn(C4, "Ordem Status", each
        List.PositionOf({"AGUARDANDO INÍCIO","PROSPECÇÃO","CDA","AV. TÉCNICA INICIAL","AV. MARKETING",
            "NEGOCIAÇÃO","APROVAÇÃO SUMMARY","TERM SHEET","CONTRATO"}, [Status NN]) + 1, Int64.Type),

    C6 = Table.AddColumn(C5, "Situação", each
        let a = [#"Projeto em andamento?"] in
        if a = null then "Não informado"
        else if Text.StartsWith(a,"SIM") then "Em andamento"
        else if Text.Contains(a,"STAND") then "Stand by"
        else if Text.StartsWith(a,"NÃO") or Text.StartsWith(a,"NAO") then "Encerrado" else a, type text),

    C7 = Table.AddColumn(C6, "Origem", each
        let o = [Entrada] in
        if o = null then "(NÃO INFORMADO)"
        else if Text.StartsWith(o,"FEIRAS") then "FEIRAS / CONGRESSOS"
        else if Text.StartsWith(o,"WISHLIST") then "WISHLIST / MARKETING"
        else if Text.StartsWith(o,"BOARD") or Text.StartsWith(o,"MÉDICO") then "MÉDICO CIENTÍFICO"
        else o, type text),

    C8 = Table.AddColumn(C7, "Franquia", each
        let a = [Área Terapêutica] in
        if a = null then "(NÃO INFORMADO)"
        else if Text.Contains(a," - ") then Text.BeforeDelimiter(a," - ") else a, type text),
    C9 = Table.AddColumn(C8, "Área Terapêutica (detalhe)", each
        let a = [Área Terapêutica] in
        if a = null then "(NÃO INFORMADO)"
        else if Text.Contains(a," - ") then Text.AfterDelimiter(a," - ") else a, type text),

    // ---------- COMPLEXIDADE: edite este de-para com o time quando decidirem ----------
    C10 = Table.AddColumn(C9, "Complexidade", each
        let c = [Categoria Padrão] in
        if c = "INOVADOR RADICAL" or c = "BIOLÓGICO" then "ALTO"
        else if c = "INOVADOR INCREMENTAL" or c = "PRODUTO PARA SAÚDE" or c = "COSMÉTICO" then "MÉDIO"
        else if c = "SIMILAR / GENÉRICO" or c = "ALIMENTO / SUPLEMENTO" or c = "FITOTERÁPICO" then "BAIXO"
        else "A DEFINIR", type text),

    // ---------- datas derivadas ----------
    D1 = Table.AddColumn(C10, "Data Início", each
        [Data de Entrada] ?? [Data de Início do Projeto] ?? [Data Início Prospecção], type nullable date),
    D2 = Table.AddColumn(D1, "Última Data", each
        List.Max(List.RemoveNulls({[Data de Entrada],[Data de Início do Projeto],[Data Início Prospecção],
            [Data Conclusão Prospecção],[Data Inicio Processo de CDA],[Data de Concl. CDA],
            [#"DATA - Inicio avaliação técnica inicial"],[#"DATA - Conclusão avaliação técnica Inicial"],
            [#"DATA - Inicio avaliação marketing"],[#"DATA - Conclusão avaliação marketing"],
            [#"DATA - Inicio Negociações com parceiro"],[Data de Início Summary],
            [Data inicio elaboração Term Sheet],[Início discussão contratual],
            [Data de Finalização do Projeto em NN]})), type nullable date),
    D3 = Table.AddColumn(D2, "Data Fim", each
        if [Data de Finalização do Projeto em NN] <> null then [Data de Finalização do Projeto em NN]
        else if [Situação] = "Em andamento" then null else [Última Data], type nullable date),
    D4 = Table.AddColumn(D3, "Fim Estimado", each
        [Data de Finalização do Projeto em NN] = null and [Data Fim] <> null, type logical),
    D5 = Table.AddColumn(D4, "Dias em NN", each
        if [Data Início] = null then null
        else Duration.Days(([Data Fim] ?? Date.From(DateTime.LocalNow())) - [Data Início]), Int64.Type),
    D6 = Table.AddColumn(D5, "Dias Parado", each
        if [Última Data] = null then null
        else Duration.Days(Date.From(DateTime.LocalNow()) - [Última Data]), Int64.Type),
    D7 = Table.AddColumn(D6, "Alerta", each
        if [Situação] <> "Em andamento" then "4. Não ativo"
        else if [Dias Parado] = null then "5. Sem data"
        else if [Dias Parado] <= 30 then "1. Em dia"
        else if [Dias Parado] <= 90 then "2. Atenção" else "3. Parado", type text),

    // ano e mês da entrada, prontos para usar em filtros e gráficos
    // (assim não é preciso criar uma terceira ligação com o Calendário)
    D8 = Table.AddColumn(D7, "Ano de Entrada", each
        if [Data de Entrada] = null then null else Date.Year([Data de Entrada]), Int64.Type),
    D9 = Table.AddColumn(D8, "Mês de Entrada", each
        if [Data de Entrada] = null then null
        else Text.From(Date.Year([Data de Entrada])) & "-"
             & Text.PadStart(Text.From(Date.Month([Data de Entrada])), 2, "0"), type text),

    ComIndice = Table.AddIndexColumn(D9, "Seq", 1, 1, Int64.Type),
    ComID = Table.AddColumn(ComIndice, "ProjetoID", each [Arquivo] & "#" & Text.From([Seq]), type text),
    Final = Table.RemoveColumns(ComID, {"Seq"})
in
    Final
