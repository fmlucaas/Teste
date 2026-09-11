let
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
    Tipado
