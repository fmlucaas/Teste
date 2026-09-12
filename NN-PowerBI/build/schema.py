# -*- coding: utf-8 -*-
"""Esquema declarado do modelo: colunas, tipos, relacionamentos."""

S, D, I, N, B = "string", "dateTime", "int64", "double", "boolean"

# tabela -> [(coluna, tipo, formato|None, sortBy|None)]
COLUMNS = {
"Mapeamento": [
    ("ProjetoID", S, None, None), ("Arquivo", S, None, None),
    ("Responsável Final", S, None, None), ("Gerência", S, None, None),
    ("Entrada", S, None, None), ("Molécula", S, None, None),
    ("Código CI", S, None, None), ("Marca do Referência BR", S, None, None),
    ("Fornecedor / Parceiro", S, None, None), ("País Fornecedor", S, None, None),
    ("Categoria Padrão", S, None, None), ("Coligada Padrão", S, None, None),
    ("Área Terapêutica", S, None, None), ("Franquia", S, None, None),
    ("Sub-área Terapêutica", S, None, None), ("Fase Oportunidade NN", S, None, None),
    ("Indicação", S, None, None), ("Forma Farmacêutica", S, None, None),
    ("Status NN", S, None, None), ("Situação", S, None, None),
    ("Atividade", S, None, None), ("Motivo Padrão", S, None, None),
    ("Detalhamento do cancelamento", S, None, None), ("CDA Status", S, None, None),
    ("Moeda", S, None, None),
    ("Data de Entrada", D, "dd/mm/yyyy", None),
    ("Data de Início do Projeto", D, "dd/mm/yyyy", None),
    ("Data de Finalização do Projeto em NN", D, "dd/mm/yyyy", None),
    ("Data Início Efetiva", D, "dd/mm/yyyy", None),
    ("Data Fim Efetiva", D, "dd/mm/yyyy", None),
    ("Última Data Registrada", D, "dd/mm/yyyy", None),
    ("Data de recebimento da primeira proposta comercial", D, "dd/mm/yyyy", None),
    ("Dias em NN", I, "#,0", None),
    ("Fim Estimado?", B, None, None),
    ("Preço de Fornecimento", N, "#,0.00", None),
    ("Margem Bruta (%)", N, "0.0%", None),
    ("VPL (R$)", N, '"R$" #,0', None),
    ("Fat. Líq. (Peak Sales, R$)", N, '"R$" #,0', None),
    ("Fat. Líq. DRE (Ano1)", N, '"R$" #,0', None),
    ("Fat. Líq. DRE (Ano2)", N, '"R$" #,0', None),
    ("Fat. Líq. DRE (Ano3)", N, '"R$" #,0', None),
    ("Fat. Líq. DRE (Ano4)", N, '"R$" #,0', None),
    ("Fat. Líq. DRE (Ano5)", N, '"R$" #,0', None),
],
"Carregamento Mensal": [
    ("ProjetoID", S, None, None), ("Arquivo", S, None, None),
    ("Responsável Final", S, None, None), ("Gerência", S, None, None),
    ("Mês", D, "mmm/yyyy", None), ("Data Referência", D, "dd/mm/yyyy", None),
    ("ChaveMes", I, "0", None),
    ("Status no Mês", S, None, "Ordem Status Mês"),
    ("Entrou no Mês", B, None, None), ("Saiu no Mês", B, None, None),
    ("Ativo no Fim do Mês", B, None, None),
    ("Categoria Padrão", S, None, None), ("Coligada Padrão", S, None, None),
    ("Franquia", S, None, None), ("Motivo Padrão", S, None, None),
    ("Atividade", S, None, None), ("Situação", S, None, None),
    ("Fim Estimado?", B, None, None),
],
"Calendário": [
    ("Data", D, "dd/mm/yyyy", None), ("Ano", I, "0", None),
    ("Nº Mês", I, "0", None), ("Mês", S, None, "Nº Mês"),
    ("Mês Abrev", S, None, "Nº Mês"), ("Ano-Mês", S, None, "ChaveMes"),
    ("ChaveMes", I, "0", None), ("Trimestre", S, None, None),
    ("Ano-Trimestre", S, None, None),
    ("Início do Mês", D, "dd/mm/yyyy", None), ("Fim do Mês", D, "dd/mm/yyyy", None),
    ("É Mês Atual", B, None, None), ("É Ano Atual", B, None, None),
    ("Passado ou Hoje", B, None, None),
],
"Status NN": [
    ("Status", S, None, "Ordem"), ("Ordem", I, "0", None),
    ("Grupo", S, None, None), ("Em Uso", B, None, None),
],
"Complexidade": [
    ("Categoria Padrão", S, None, None),
    ("Complexidade", S, None, "Ordem Complexidade"),
    ("Ordem Complexidade", I, "0", None),
],
"Esforço": [
    ("Status", S, None, None), ("Complexidade", S, None, None),
    ("Horas Mês", N, "#,0.0", None), ("ChaveEsforco", S, None, None),
],
"Unidade Referência": [
    ("Coligada Padrão", S, None, None), ("Unidade", S, None, "Ordem"), ("Ordem", I, "0", None),
],
"Faturamento Projetado": [
    ("ProjetoID", S, None, None), ("Ano do DRE", I, "0", None),
    ("Ano Projetado", S, None, "Ano do DRE"), ("Valor", N, '"R$" #,0', None),
],
"Equipe": [
    ("Pessoa", S, None, None), ("Nome", S, None, None),
    ("Gerência", S, None, None), ("Projetos Totais", I, "#,0", None),
    ("Capacidade Mensal (h)", N, "#,0", None),
],
"Unidade de Negócio": [
    ("Coligada Padrão", S, None, None),
    ("Unidade de Negócio", S, None, "Ordem"), ("Ordem", I, "0", None),
],
"Motivo Cancelamento": [
    ("Motivo Padrão", S, None, None), ("Motivo", S, None, None), ("Bloco", S, None, None),
],
"País": [ ("País", S, None, None), ("ISO3", S, None, None) ],
"Solicitações": [
    ("Arquivo", S, None, None), ("Área Técnica", S, None, None),
    ("Solicitante", S, None, None), ("Molécula", S, None, None),
    ("Status Solicitação", S, None, None),
    ("Data Solicitação", D, "dd/mm/yyyy", None),
    ("Data Previsão", D, "dd/mm/yyyy", None),
    ("Data Recebimento", D, "dd/mm/yyyy", None),
    ("Dias de Resposta", I, "#,0", None),
    ("Dentro do Prazo", B, None, None),
    ("Viabilidade Padrão", S, None, None), ("OBS", S, None, None),
],
"Qualidade de Dados": [
    ("ProjetoID", S, None, None), ("Arquivo", S, None, None),
    ("Responsável Final", S, None, None), ("Molécula", S, None, None),
    ("Fornecedor / Parceiro", S, None, None), ("Status NN", S, None, None),
    ("Situação", S, None, None), ("Regra", S, None, None),
    ("Gravidade", S, None, None), ("Impacto", S, None, None), ("Peso", I, "0", None),
],
"Histórico Snapshots": [
    ("ProjetoID", S, None, None), ("Data Snapshot", D, "dd/mm/yyyy", None),
    ("Responsável Final", S, None, None), ("Status NN", S, None, None),
    ("Situação", S, None, None), ("Coligada Padrão", S, None, None),
    ("Categoria Padrão", S, None, None), ("Motivo Padrão", S, None, None),
    ("Molécula", S, None, None),
],
}

# colunas calculadas: tabela -> [(nome, tipo, expressão, formato, sortBy)]
CALC_COLUMNS = {
"Mapeamento": [
    ("Complexidade", S,
     'COALESCE (\n    LOOKUPVALUE (\n        Complexidade[Complexidade],\n'
     '        Complexidade[Categoria Padrão], Mapeamento[Categoria Padrão]\n    ),\n    "MÉDIO"\n)', None, None),
    ("Horas Mês", N,
     "COALESCE (\n    LOOKUPVALUE (\n        'Esforço'[Horas Mês],\n"
     "        'Esforço'[Status], Mapeamento[Status NN],\n"
     "        'Esforço'[Complexidade], Mapeamento[Complexidade]\n    ),\n    0\n)", "#,0.0", None),
    ("Faixa de Duração", S,
     'VAR d = Mapeamento[Dias em NN]\nRETURN\nSWITCH (\n    TRUE (),\n'
     '    ISBLANK ( d ), "Sem data",\n    d <= 30,  "Até 1 mês",\n    d <= 90,  "1 a 3 meses",\n'
     '    d <= 180, "3 a 6 meses",\n    d <= 365, "6 a 12 meses",\n    d <= 730, "1 a 2 anos",\n'
     '              "Mais de 2 anos"\n)', None, None),
    ("Alerta", S,
     'VAR ultima = Mapeamento[Última Data Registrada]\n'
     'VAR diasParado = IF ( ISBLANK ( ultima ), BLANK (), DATEDIFF ( ultima, TODAY (), DAY ) )\n'
     'RETURN\nSWITCH (\n    TRUE (),\n'
     '    Mapeamento[Situação] <> "EM ANDAMENTO", "⚪ Não ativo",\n'
     '    ISBLANK ( diasParado ),                 "⚫ Sem data",\n'
     '    diasParado <= 30,                       "🟢 Em dia",\n'
     '    diasParado <= 90,                       "🟡 Atenção",\n'
     '                                            "🔴 Parado"\n)', None, None),
],
"Carregamento Mensal": [
    ("Complexidade", S,
     "COALESCE (\n    LOOKUPVALUE (\n        Complexidade[Complexidade],\n"
     "        Complexidade[Categoria Padrão], 'Carregamento Mensal'[Categoria Padrão]\n    ),\n"
     '    "MÉDIO"\n)', None, None),
    ("Horas Mês", N,
     "COALESCE (\n    LOOKUPVALUE (\n        'Esforço'[Horas Mês],\n"
     "        'Esforço'[Status], 'Carregamento Mensal'[Status no Mês],\n"
     "        'Esforço'[Complexidade], 'Carregamento Mensal'[Complexidade]\n    ),\n    0\n)", "#,0.0", None),
    ("Ordem Status Mês", I,
     "COALESCE (\n    LOOKUPVALUE (\n        'Status NN'[Ordem],\n"
     "        'Status NN'[Status], 'Carregamento Mensal'[Status no Mês]\n    ),\n    99\n)", "0", None),
],
}

# (tabelaDim, colunaDim, tabelaFato, colunaFato, ativo)
RELATIONSHIPS = [
    ("Equipe", "Pessoa", "Mapeamento", "Responsável Final", True),
    ("Status NN", "Status", "Mapeamento", "Status NN", True),
    ("Complexidade", "Categoria Padrão", "Mapeamento", "Categoria Padrão", True),
    ("Unidade de Negócio", "Coligada Padrão", "Mapeamento", "Coligada Padrão", True),
    ("Motivo Cancelamento", "Motivo Padrão", "Mapeamento", "Motivo Padrão", True),
    ("País", "País", "Mapeamento", "País Fornecedor", True),
    ("Mapeamento", "ProjetoID", "Carregamento Mensal", "ProjetoID", True),
    ("Mapeamento", "ProjetoID", "Qualidade de Dados", "ProjetoID", True),
    ("Mapeamento", "ProjetoID", "Faturamento Projetado", "ProjetoID", True),
    ("Calendário", "Data", "Carregamento Mensal", "Data Referência", True),
    ("Calendário", "Data", "Mapeamento", "Data de Entrada", False),
    ("Calendário", "Data", "Mapeamento", "Data Fim Efetiva", False),
    ("Calendário", "Data", "Solicitações", "Data Solicitação", True),
    ("Equipe", "Pessoa", "Solicitações", "Solicitante", True),
    ("Calendário", "Data", "Histórico Snapshots", "Data Snapshot", True),
    ("Equipe", "Pessoa", "Histórico Snapshots", "Responsável Final", True),
]

# parâmetros: (nome, expressão M)
PARAMETERS = [
 ("pSiteSharePoint", '"https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'),
 ("pBiblioteca", '"Documentos Compartilhados" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'),
 ("pPastaMapeamentos", '"DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'),
 ("pPastaHistorico", '"DEMANDAS NN - ALIANÇA/HISTORICO" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false]'),
 ("pAbaMapeamento", '"Mapeamento NN" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'),
 ("pAbaSolicitacoes", '"Solicitações" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false]'),
 ("pArquivoRegua", '"Regua_Esforco_NN.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false]'),
 ("pCapacidadeMensalHoras", '168 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=true]'),
 ("pAnoMinimo", '2022 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=false]'),
 ("pEstimarFimQuandoAusente", 'true meta [IsParameterQuery=true, Type="Logical", IsParameterQueryRequired=false]'),
]

# consultas que viram TABELA (arquivo em M/queries)
TABLE_QUERIES = {
 "Mapeamento": "Mapeamento", "Carregamento Mensal": "Carregamento Mensal",
 "Calendário": "Calendario", "Status NN": "Status NN",
 "Complexidade": "Complexidade", "Esforço": "Esforco", "Equipe": "Equipe",
 "Unidade de Negócio": "Unidade de Negocio", "Motivo Cancelamento": "Motivo Cancelamento",
 "País": "Pais", "Solicitações": "Solicitações",
 "Qualidade de Dados": "Qualidade de Dados", "Histórico Snapshots": "Historico Snapshots",
 "Faturamento Projetado": "Faturamento Projetado",
 "Unidade Referência": "Unidade Referencia",
}

# consultas auxiliares (não viram tabela): função e navegação
HELPER_QUERIES = {"fnUtil": "fnUtil", "Fonte_Arquivos": "Fonte_Arquivos",
                  "Fonte_Regua": "Fonte_Regua"}
