// Qualidade de Dados — // uma linha por PROBLEMA encontrado.
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
    ComPeso
