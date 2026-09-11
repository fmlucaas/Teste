// =====================================================================
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
    Renomeado
