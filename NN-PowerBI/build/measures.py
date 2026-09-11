# -*- coding: utf-8 -*-
"""Fonte única de verdade das medidas DAX."""

FMT_INT = "#,0"
FMT_DEC = "#,0.0"
FMT_PCT = "0.0%"
FMT_RS  = '"R$" #,0'
FMT_TXT = None

# (nome, expressão, formato, pasta)
MEASURES = [
# ---------------- 01 Visão Geral ----------------
("Projetos", "DISTINCTCOUNT ( Mapeamento[ProjetoID] )", FMT_INT, "01 Visão Geral"),
("Moléculas", "DISTINCTCOUNT ( Mapeamento[Molécula] )", FMT_INT, "01 Visão Geral"),
("Fornecedores", "DISTINCTCOUNT ( Mapeamento[Fornecedor / Parceiro] )", FMT_INT, "01 Visão Geral"),
("Países", "DISTINCTCOUNT ( Mapeamento[País Fornecedor] )", FMT_INT, "01 Visão Geral"),
("Projetos Ativos", 'CALCULATE ( [Projetos], Mapeamento[Situação] = "EM ANDAMENTO" )', FMT_INT, "01 Visão Geral"),
("Projetos Stand by", 'CALCULATE ( [Projetos], Mapeamento[Situação] = "STAND BY" )', FMT_INT, "01 Visão Geral"),
("Projetos Encerrados", 'CALCULATE ( [Projetos], Mapeamento[Situação] = "ENCERRADO" )', FMT_INT, "01 Visão Geral"),
("% Ativos", "DIVIDE ( [Projetos Ativos], [Projetos] )", FMT_PCT, "01 Visão Geral"),
("Projetos por Pessoa", "DIVIDE ( [Projetos Ativos], DISTINCTCOUNT ( Mapeamento[Responsável Final] ) )", FMT_DEC, "01 Visão Geral"),

# ---------------- 02 Carregamento ----------------
("Horas Empenhadas",
 'CALCULATE (\n    SUMX ( Mapeamento, Mapeamento[Horas Mês] ),\n    Mapeamento[Situação] = "EM ANDAMENTO"\n)', FMT_DEC, "02 Carregamento"),
("Horas Empenhadas (com Stand by)",
 'CALCULATE (\n    SUMX ( Mapeamento, Mapeamento[Horas Mês] ),\n    Mapeamento[Situação] IN { "EM ANDAMENTO", "STAND BY" }\n)', FMT_DEC, "02 Carregamento"),
("Capacidade (h)",
 "SUMX ( VALUES ( Equipe[Pessoa] ), CALCULATE ( MAX ( Equipe[Capacidade Mensal (h)] ) ) )", FMT_DEC, "02 Carregamento"),
("% Ocupação", "DIVIDE ( [Horas Empenhadas], [Capacidade (h)] )", FMT_PCT, "02 Carregamento"),
("Horas Disponíveis", "[Capacidade (h)] - [Horas Empenhadas]", FMT_DEC, "02 Carregamento"),
("Status Ocupação",
 'VAR o = [% Ocupação]\nRETURN\nSWITCH (\n    TRUE (),\n    ISBLANK ( o ), "Sem dados",\n    o > 1.10,      "🔴 Sobrecarregado",\n    o > 0.90,      "🟠 No limite",\n    o > 0.60,      "🟢 Saudável",\n                   "🔵 Folga"\n)', FMT_TXT, "02 Carregamento"),

# ---------------- 03 Evolução do Mês ----------------
("Projetos no Mês", "DISTINCTCOUNT ( 'Carregamento Mensal'[ProjetoID] )", FMT_INT, "03 Evolução do Mês"),
("Ativos no Fim do Mês",
 "CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Ativo no Fim do Mês] = TRUE () )", FMT_INT, "03 Evolução do Mês"),
("Entradas no Mês",
 "CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Entrou no Mês] = TRUE () )", FMT_INT, "03 Evolução do Mês"),
("Saídas no Mês",
 "CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Saiu no Mês] = TRUE () )", FMT_INT, "03 Evolução do Mês"),
("Saldo do Mês", "[Entradas no Mês] - [Saídas no Mês]", FMT_INT, "03 Evolução do Mês"),
("Ativos no Início do Mês", "[Ativos no Fim do Mês] - [Saldo do Mês]", FMT_INT, "03 Evolução do Mês"),
("Ativos Mês Anterior",
 "CALCULATE ( [Ativos no Fim do Mês], DATEADD ( 'Calendário'[Data], -1, MONTH ) )", FMT_INT, "03 Evolução do Mês"),
("Variação vs Mês Anterior",
 "VAR atual = [Ativos no Fim do Mês]\nVAR anterior = [Ativos Mês Anterior]\nRETURN\n    IF ( NOT ISBLANK ( anterior ), atual - anterior )", FMT_INT, "03 Evolução do Mês"),
("% Variação vs Mês Anterior",
 "DIVIDE ( [Variação vs Mês Anterior], [Ativos Mês Anterior] )", FMT_PCT, "03 Evolução do Mês"),
("Pico do Mês",
 "MAXX ( VALUES ( 'Carregamento Mensal'[ChaveMes] ), [Projetos no Mês] )", FMT_INT, "03 Evolução do Mês"),
("Horas Empenhadas no Mês",
 "SUMX ( 'Carregamento Mensal', 'Carregamento Mensal'[Horas Mês] )", FMT_DEC, "03 Evolução do Mês"),
("% Ocupação no Mês", "DIVIDE ( [Horas Empenhadas no Mês], [Capacidade (h)] )", FMT_PCT, "03 Evolução do Mês"),
("Diferença Hoje vs Mês", "[Projetos Ativos] - [Ativos no Fim do Mês]", FMT_INT, "03 Evolução do Mês"),
("Narrativa do Mês",
 'VAR ini = [Ativos no Início do Mês]\n'
 'VAR ent = [Entradas no Mês]\n'
 'VAR sai = [Saídas no Mês]\n'
 'VAR fim = [Ativos no Fim do Mês]\n'
 'VAR pessoa = IF ( HASONEVALUE ( Equipe[Nome] ), SELECTEDVALUE ( Equipe[Nome] ), "O time" )\n'
 'VAR mes = IF ( HASONEVALUE ( \'Calendário\'[Ano-Mês] ), SELECTEDVALUE ( \'Calendário\'[Ano-Mês] ), "o período" )\n'
 'RETURN\n'
 '    IF (\n'
 '        ISBLANK ( fim ),\n'
 '        "Sem movimentação no período.",\n'
 '        pessoa & " começou " & mes & " com " & FORMAT ( ini, "0" ) & " projetos, "\n'
 '            & "recebeu " & FORMAT ( ent, "0" ) & " novo(s), encerrou " & FORMAT ( sai, "0" )\n'
 '            & " e terminou com " & FORMAT ( fim, "0" ) & " em carteira."\n'
 '    )', FMT_TXT, "03 Evolução do Mês"),

# ---------------- 04 Funil e Ciclo ----------------
("Projetos no Funil",
 'CALCULATE ( [Projetos], Mapeamento[Situação] IN { "EM ANDAMENTO", "STAND BY" } )', FMT_INT, "04 Funil e Ciclo"),
("Dias Médios em NN", "AVERAGEX ( Mapeamento, Mapeamento[Dias em NN] )", FMT_INT, "04 Funil e Ciclo"),
("Dias Médios até 1ª Proposta",
 "AVERAGEX (\n    FILTER (\n        Mapeamento,\n        NOT ISBLANK ( Mapeamento[Data de recebimento da primeira proposta comercial] )\n            && NOT ISBLANK ( Mapeamento[Data Início Efetiva] )\n    ),\n    DATEDIFF (\n        Mapeamento[Data Início Efetiva],\n        Mapeamento[Data de recebimento da primeira proposta comercial],\n        DAY\n    )\n)", FMT_INT, "04 Funil e Ciclo"),
("% da Etapa",
 "DIVIDE ( [Projetos], CALCULATE ( [Projetos], REMOVEFILTERS ( 'Status NN' ) ) )", FMT_PCT, "04 Funil e Ciclo"),
("Taxa de Conversão até Contrato",
 "DIVIDE (\n    CALCULATE ( [Projetos], 'Status NN'[Ordem] >= 8 ),\n    CALCULATE ( [Projetos], REMOVEFILTERS ( 'Status NN' ) )\n)", FMT_PCT, "04 Funil e Ciclo"),

# ---------------- 05 Cancelamentos ----------------
("Cancelados + Stand by",
 'CALCULATE ( [Projetos], Mapeamento[Situação] IN { "ENCERRADO", "STAND BY" } )', FMT_INT, "05 Cancelamentos"),
("% do Motivo",
 "DIVIDE (\n    [Cancelados + Stand by],\n    CALCULATE ( [Cancelados + Stand by], REMOVEFILTERS ( 'Motivo Cancelamento' ) )\n)", FMT_PCT, "05 Cancelamentos"),
("Motivo nº 1",
 'VAR t =\n    ADDCOLUMNS ( VALUES ( \'Motivo Cancelamento\'[Motivo] ), "@q", [Cancelados + Stand by] )\nVAR topo =\n    TOPN ( 1, FILTER ( t, [@q] > 0 ), [@q], DESC )\nRETURN\n    CONCATENATEX ( topo, \'Motivo Cancelamento\'[Motivo] )', FMT_TXT, "05 Cancelamentos"),
("Cancelados no Mês",
 "CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Saiu no Mês] = TRUE () )", FMT_INT, "05 Cancelamentos"),

# ---------------- 06 Financeiro ----------------
("VPL Total", "SUM ( Mapeamento[VPL (R$)] )", FMT_RS, "06 Financeiro"),
("VPL Médio", "AVERAGE ( Mapeamento[VPL (R$)] )", FMT_RS, "06 Financeiro"),
("Peak Sales", "SUM ( Mapeamento[Fat. Líq. (Peak Sales, R$)] )", FMT_RS, "06 Financeiro"),
("Faturamento 5 Anos",
 "SUM ( Mapeamento[Fat. Líq. DRE (Ano1)] )\n    + SUM ( Mapeamento[Fat. Líq. DRE (Ano2)] )\n    + SUM ( Mapeamento[Fat. Líq. DRE (Ano3)] )\n    + SUM ( Mapeamento[Fat. Líq. DRE (Ano4)] )\n    + SUM ( Mapeamento[Fat. Líq. DRE (Ano5)] )", FMT_RS, "06 Financeiro"),
("Margem Bruta Média", "AVERAGE ( Mapeamento[Margem Bruta (%)] )", FMT_PCT, "06 Financeiro"),
("Projetos com VPL",
 "CALCULATE ( [Projetos], NOT ISBLANK ( Mapeamento[VPL (R$)] ) )", FMT_INT, "06 Financeiro"),
("% Cobertura Financeira", "DIVIDE ( [Projetos com VPL], [Projetos no Funil] )", FMT_PCT, "06 Financeiro"),
("VPL de Projetos Ativos",
 'CALCULATE ( [VPL Total], Mapeamento[Situação] = "EM ANDAMENTO" )', FMT_RS, "06 Financeiro"),
("Valor em Risco (Stand by)",
 'CALCULATE ( [VPL Total], Mapeamento[Situação] = "STAND BY" )', FMT_RS, "06 Financeiro"),

# ---------------- 07 Qualidade da Base ----------------
("Problemas", "COUNTROWS ( 'Qualidade de Dados' )", FMT_INT, "07 Qualidade da Base"),
("Problemas Graves",
 'CALCULATE ( [Problemas], \'Qualidade de Dados\'[Gravidade] = "Alta" )', FMT_INT, "07 Qualidade da Base"),
("Projetos com Problema",
 "DISTINCTCOUNT ( 'Qualidade de Dados'[ProjetoID] )", FMT_INT, "07 Qualidade da Base"),
("Índice de Qualidade",
 "VAR pesoMax = [Projetos] * 11 * 3\nVAR pesoReal =\n    SUMX ( 'Qualidade de Dados', 'Qualidade de Dados'[Peso] )\nRETURN\n    1 - DIVIDE ( pesoReal, pesoMax )", FMT_PCT, "07 Qualidade da Base"),
("% Projetos Sem Data de Fim",
 'DIVIDE (\n    CALCULATE (\n        [Projetos],\n        Mapeamento[Situação] <> "EM ANDAMENTO",\n        ISBLANK ( Mapeamento[Data de Finalização do Projeto em NN] )\n    ),\n    CALCULATE ( [Projetos], Mapeamento[Situação] <> "EM ANDAMENTO" )\n)', FMT_PCT, "07 Qualidade da Base"),

# ---------------- 08 Solicitações Técnicas ----------------
("Solicitações", "COUNTROWS ( 'Solicitações' )", FMT_INT, "08 Solicitações Técnicas"),
("SLA Médio (dias)", "AVERAGE ( 'Solicitações'[Dias de Resposta] )", FMT_DEC, "08 Solicitações Técnicas"),
("% no Prazo",
 "DIVIDE (\n    CALCULATE ( [Solicitações], 'Solicitações'[Dentro do Prazo] = TRUE () ),\n    CALCULATE ( [Solicitações], NOT ISBLANK ( 'Solicitações'[Dentro do Prazo] ) )\n)", FMT_PCT, "08 Solicitações Técnicas"),
("% Viável",
 'DIVIDE (\n    CALCULATE ( [Solicitações], \'Solicitações\'[Viabilidade Padrão] = "Viável" ),\n    CALCULATE ( [Solicitações], \'Solicitações\'[Viabilidade Padrão] <> "(Sem parecer)" )\n)', FMT_PCT, "08 Solicitações Técnicas"),
("Solicitações em Aberto",
 "CALCULATE ( [Solicitações], ISBLANK ( 'Solicitações'[Data Recebimento] ) )", FMT_INT, "08 Solicitações Técnicas"),

# ---------------- 09 Auxiliares ----------------
("Atualizado em",
 '"Dados até " & FORMAT ( TODAY (), "dd/mm/yyyy" )', FMT_TXT, "09 Auxiliares"),
("Título Ocupação",
 '"Capacidade: " & FORMAT ( [Horas Empenhadas], "#,0.0" ) & " h de "\n    & FORMAT ( [Capacidade (h)], "#,0" ) & " h  ("\n    & FORMAT ( [% Ocupação], "0.0%" ) & ")"', FMT_TXT, "09 Auxiliares"),
("Sem Seleção",
 'IF ( ISBLANK ( [Projetos] ), "Nenhum projeto atende aos filtros selecionados.", BLANK () )', FMT_TXT, "09 Auxiliares"),
]
