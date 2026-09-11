// Ordem do funil + agrupamento + sinalização do que está em desuso.
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
    Tipado
