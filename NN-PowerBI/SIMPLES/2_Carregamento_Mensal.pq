// ===========================================================================
//  CONSULTA 2 de 3  —  CARREGAMENTO MENSAL
//  Renomeie a consulta para:   Carregamento Mensal
//
//  Esta é a consulta que responde "com quantos projetos o analista começou o
//  mês, quantos entraram, quantos saíram". Ela usa a consulta Mapeamento,
//  então crie a consulta 1 primeiro.
// ===========================================================================
let
    Hoje = Date.From(DateTime.LocalNow()),
    Base = Table.SelectRows(Mapeamento, each [Data Início] <> null),

    ComFim = Table.AddColumn(Base, "FimSerie", each
        let f = [Data Fim] ?? Hoje in if f > Hoje then Hoje else f, type date),
    Valido = Table.SelectRows(ComFim, each [FimSerie] >= [Data Início]),

    // uma linha por mês em que o projeto esteve aberto
    ComMeses = Table.AddColumn(Valido, "Mês", each
        List.Generate(
            () => Date.StartOfMonth([Data Início]),
            each _ <= Date.StartOfMonth([FimSerie]),
            each Date.AddMonths(_, 1)), type list),
    Explodido = Table.ExpandListColumn(ComMeses, "Mês"),

    ComRef = Table.AddColumn(Explodido, "Data Referência", each
        List.Min({Date.EndOfMonth([Mês]), [FimSerie]}), type date),

    // em que status o projeto estava NAQUELE mês
    ComStatus = Table.AddColumn(ComRef, "Status no Mês", each
        let
            ref = [Data Referência],
            etapas = {
                [o = 1, s = "AGUARDANDO INÍCIO",   d = [Data Início]],
                [o = 2, s = "PROSPECÇÃO",          d = [Data Início Prospecção] ?? [Data de Início do Projeto]],
                [o = 3, s = "CDA",                 d = [Data Inicio Processo de CDA]],
                [o = 4, s = "AV. TÉCNICA INICIAL", d = [#"DATA - Inicio avaliação técnica inicial"]],
                [o = 5, s = "AV. MARKETING",       d = [#"DATA - Inicio avaliação marketing"]],
                [o = 6, s = "NEGOCIAÇÃO",          d = [#"DATA - Inicio Negociações com parceiro"]],
                [o = 7, s = "APROVAÇÃO SUMMARY",   d = [Data de Início Summary]],
                [o = 8, s = "TERM SHEET",          d = [Data inicio elaboração Term Sheet]],
                [o = 9, s = "CONTRATO",            d = [Início discussão contratual]]},
            atingidas = List.Select(etapas, each _[d] <> null and _[d] <= ref),
            maior = if List.Count(atingidas) = 0 then null
                    else List.Max(List.Transform(atingidas, each _[o])),
            achado = if maior = null then null else List.Select(etapas, each _[o] = maior){0}[s]
        in  achado ?? [Status NN], type text),

    E1 = Table.AddColumn(ComStatus, "Entrou no Mês", each
        Date.StartOfMonth([Data Início]) = [Mês], type logical),
    E2 = Table.AddColumn(E1, "Saiu no Mês", each
        [Data Fim] <> null and Date.StartOfMonth([Data Fim]) = [Mês], type logical),
    E3 = Table.AddColumn(E2, "Ativo no Fim do Mês", each not [Saiu no Mês], type logical),
    E4 = Table.AddColumn(E3, "Ano", each Date.Year([Mês]), Int64.Type),
    E5 = Table.AddColumn(E4, "Ano-Mês", each
        Text.From(Date.Year([Mês])) & "-" & Text.PadStart(Text.From(Date.Month([Mês])), 2, "0"), type text),
    E6 = Table.AddColumn(E5, "Ordem Status Mês", each
        List.PositionOf({"AGUARDANDO INÍCIO","PROSPECÇÃO","CDA","AV. TÉCNICA INICIAL","AV. MARKETING",
            "NEGOCIAÇÃO","APROVAÇÃO SUMMARY","TERM SHEET","CONTRATO"}, [Status no Mês]) + 1, Int64.Type),

    Final = Table.SelectColumns(E6, {
        "ProjetoID","Arquivo","Responsável","Gerência","Mês","Ano","Ano-Mês","Data Referência",
        "Status no Mês","Ordem Status Mês","Entrou no Mês","Saiu no Mês","Ativo no Fim do Mês",
        "Categoria Padrão","Unidade de Negócio","Franquia","Motivo","Situação","Complexidade",
        "Molécula","Fornecedor / Parceiro","Fim Estimado"}, MissingField.UseNull)
in
    Final
