# -*- coding: utf-8 -*-
"""Medidas do modelo SIMPLES (3 tabelas). Fonte única para o dossiê."""
INT, DEC, PCT, RS, TXT = "Número inteiro (#.##0)", "1 casa decimal", "Porcentagem, 1 casa", "Moeda R$, 0 casas", "Texto (sem formato)"

# (grupo, nome, dax, formato, para_que_serve)
M = [
("A. Contagens básicas","Projetos","DISTINCTCOUNT ( Mapeamento[ProjetoID] )",INT,
 "Quantas oportunidades existem no filtro atual."),
("A. Contagens básicas","Moléculas","DISTINCTCOUNT ( Mapeamento[Molécula] )",INT,
 "Quantas moléculas diferentes. Uma molécula pode ter vários fornecedores."),
("A. Contagens básicas","Fornecedores","DISTINCTCOUNT ( Mapeamento[Fornecedor / Parceiro] )",INT,
 "Quantas empresas diferentes foram abordadas."),
("A. Contagens básicas","Responsáveis","DISTINCTCOUNT ( Mapeamento[Responsável] )",INT,
 "Quantas pessoas do time aparecem no filtro atual."),
("A. Contagens básicas","Projetos Ativos",
 'CALCULATE ( [Projetos], Mapeamento[Situação] = "Em andamento" )',INT,
 "Só os projetos que estão rodando agora."),
("A. Contagens básicas","Projetos Stand by",
 'CALCULATE ( [Projetos], Mapeamento[Situação] = "Stand by" )',INT,"Projetos pausados."),
("A. Contagens básicas","Projetos Encerrados",
 'CALCULATE ( [Projetos], Mapeamento[Situação] = "Encerrado" )',INT,"Projetos cancelados/finalizados."),
("A. Contagens básicas","% Ativos","DIVIDE ( [Projetos Ativos], [Projetos] )",PCT,
 "Quanto da carteira está de fato rodando."),
("A. Contagens básicas","Projetos por Pessoa","DIVIDE ( [Projetos Ativos], [Responsáveis] )",DEC,
 "Média de projetos ativos por pessoa."),

("B. Carregamento","Capacidade (h)","[Responsáveis] * 168",INT,
 "Horas úteis disponíveis. 168 h por pessoa por mês — troque o número se a régua do time for outra."),
("B. Carregamento","Horas Empenhadas",
 'CALCULATE ( SUMX ( Mapeamento, Mapeamento[Horas Mês] ), Mapeamento[Situação] = "Em andamento" )',DEC,
 "Soma das horas que os projetos ativos consomem por mês. Fica ZERO até a régua ser preenchida."),
("B. Carregamento","Horas Disponíveis","[Capacidade (h)] - [Horas Empenhadas]",DEC,
 "Quanto ainda cabe."),
("B. Carregamento","% Ocupação","DIVIDE ( [Horas Empenhadas], [Capacidade (h)] )",PCT,
 "Acima de 100% = time sobrecarregado."),
("B. Carregamento","Aviso Régua",
 'IF (\n    [Horas Empenhadas] = 0,\n'
 '    "A régua de horas ainda não foi preenchida — veja a Parte 4.4 do dossiê.",\n'
 '    BLANK ()\n)',TXT,
 "Texto que aparece na tela 2 enquanto a régua estiver zerada. Some sozinho quando você preencher."),
("B. Carregamento","Status Ocupação",
 'VAR o = [% Ocupação]\nRETURN\nSWITCH (\n    TRUE (),\n'
 '    [Horas Empenhadas] = 0, "Régua não preenchida",\n'
 '    o > 1.1,  "Sobrecarregado",\n    o > 0.9,  "No limite",\n'
 '    o > 0.6,  "Saudável",\n              "Com folga"\n)',TXT,
 "Classificação em palavras, para a tabela por pessoa."),

("C. Evolução do mês","Projetos no Mês","DISTINCTCOUNT ( 'Carregamento Mensal'[ProjetoID] )",INT,
 "Quantos projetos passaram pelo mês selecionado."),
("C. Evolução do mês","Ativos no Fim do Mês",
 "CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Ativo no Fim do Mês] = TRUE () )",INT,
 "A carteira na virada do mês. É o número do report."),
("C. Evolução do mês","Entradas no Mês",
 "CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Entrou no Mês] = TRUE () )",INT,
 "Quantos projetos NOVOS entraram naquele mês."),
("C. Evolução do mês","Saídas no Mês",
 "CALCULATE ( [Projetos no Mês], 'Carregamento Mensal'[Saiu no Mês] = TRUE () )",INT,
 "Quantos saíram (cancelados, stand by ou concluídos)."),
("C. Evolução do mês","Saldo do Mês","[Entradas no Mês] - [Saídas no Mês]",INT,
 "Positivo = a carteira cresceu. Negativo = encolheu."),
("C. Evolução do mês","Ativos no Início do Mês","[Ativos no Fim do Mês] - [Saldo do Mês]",INT,
 "Com quantos o mês começou."),
("C. Evolução do mês","Ativos Mês Anterior",
 "CALCULATE ( [Ativos no Fim do Mês], DATEADD ( 'Calendário'[Data], -1, MONTH ) )",INT,
 "O mesmo número, um mês antes."),
("C. Evolução do mês","Variação vs Mês Anterior",
 "VAR anterior = [Ativos Mês Anterior]\nRETURN\n    IF ( NOT ISBLANK ( anterior ), [Ativos no Fim do Mês] - anterior )",INT,
 "Cresceu ou caiu quanto."),
("C. Evolução do mês","Diferença Hoje vs Mês","[Projetos Ativos] - [Ativos no Fim do Mês]",INT,
 "A diferença entre a foto de hoje e o fechamento do mês. É o ponto que você levantou no report."),
("C. Evolução do mês","Narrativa do Mês",
 'VAR ini = [Ativos no Início do Mês]\nVAR ent = [Entradas no Mês]\n'
 'VAR sai = [Saídas no Mês]\nVAR fim = [Ativos no Fim do Mês]\n'
 'VAR quem = IF ( HASONEVALUE ( Mapeamento[Responsável] ), SELECTEDVALUE ( Mapeamento[Responsável] ), "O time" )\n'
 'VAR mes  = IF ( HASONEVALUE ( \'Calendário\'[Ano-Mês] ), SELECTEDVALUE ( \'Calendário\'[Ano-Mês] ), "o período" )\n'
 'RETURN\n    IF (\n        ISBLANK ( fim ),\n        "Sem movimentação no período.",\n'
 '        quem & " começou " & mes & " com " & FORMAT ( ini, "0" ) & " projetos, recebeu "\n'
 '            & FORMAT ( ent, "0" ) & ", encerrou " & FORMAT ( sai, "0" )\n'
 '            & " e terminou com " & FORMAT ( fim, "0" ) & " em carteira."\n    )',TXT,
 "Frase pronta para colar no report mensal. Muda sozinha conforme os filtros."),

("D. Funil e ciclo","Dias Médios em NN","AVERAGE ( Mapeamento[Dias em NN] )",INT,
 "Quanto tempo, em média, um projeto fica com o time."),
("D. Funil e ciclo","Dias Médios até 1ª Proposta",
 "AVERAGEX (\n    FILTER (\n        Mapeamento,\n"
 "        NOT ISBLANK ( Mapeamento[Data de recebimento da primeira proposta comercial] )\n"
 "            && NOT ISBLANK ( Mapeamento[Data Início] )\n    ),\n"
 "    DATEDIFF (\n        Mapeamento[Data Início],\n"
 "        Mapeamento[Data de recebimento da primeira proposta comercial],\n        DAY\n    )\n)",INT,
 "Da entrada até o parceiro mandar preço."),
("D. Funil e ciclo","% da Etapa",
 "DIVIDE (\n    [Projetos],\n    CALCULATE ( [Projetos], REMOVEFILTERS ( Mapeamento[Status NN] ) )\n)",PCT,
 "Quanto cada etapa representa do funil."),
("D. Funil e ciclo","Taxa de Conversão até Contrato",
 "DIVIDE (\n    CALCULATE (\n        [Projetos],\n        Mapeamento[Ordem Status] >= 8,\n"
 "        REMOVEFILTERS ( Mapeamento[Status NN] )\n    ),\n"
 "    CALCULATE ( [Projetos], REMOVEFILTERS ( Mapeamento[Status NN] ) )\n)",PCT,
 "Quantos chegam a Term Sheet ou Contrato."),

("E. Cancelamentos","Cancelados + Stand by",
 'CALCULATE ( [Projetos], Mapeamento[Situação] IN { "Encerrado", "Stand by" } )',INT,
 "Tudo que saiu do fluxo, por qualquer motivo."),
("E. Cancelamentos","% do Motivo",
 "DIVIDE (\n    [Cancelados + Stand by],\n"
 "    CALCULATE ( [Cancelados + Stand by], REMOVEFILTERS ( Mapeamento[Motivo] ) )\n)",PCT,
 "Peso de cada motivo no total."),
("E. Cancelamentos","Motivo nº 1",
 'VAR t =\n    ADDCOLUMNS (\n        FILTER ( VALUES ( Mapeamento[Motivo] ), Mapeamento[Motivo] <> "(Sem motivo registrado)" ),\n'
 '        "@q", [Cancelados + Stand by]\n    )\n'
 'VAR topo = TOPN ( 1, FILTER ( t, [@q] > 0 ), [@q], DESC )\n'
 'RETURN\n    CONCATENATEX ( topo, Mapeamento[Motivo] )',TXT,
 "O motivo mais frequente, em texto. Vai direto para o cartão do one-page."),

("F. Report por unidade","Unidade Selecionada",
 'SELECTEDVALUE ( Mapeamento[Unidade de Negócio], "Todas as unidades" )',TXT,
 "Mostra qual unidade está filtrada."),
("F. Report por unidade","Moléculas (Todas as Unidades)",
 "CALCULATE ( [Moléculas], REMOVEFILTERS ( Mapeamento[Unidade de Negócio] ) )",INT,
 "O total de NN, ignorando o filtro de unidade. Serve de denominador."),
("F. Report por unidade","% da Unidade no Total",
 "DIVIDE ( [Moléculas], [Moléculas (Todas as Unidades)] )",PCT,
 "A frase 'esta BU representou X% do que NN avaliou'."),
("F. Report por unidade","Novas no Período",
 "CALCULATE (\n    [Moléculas],\n    NOT ISBLANK ( Mapeamento[Data de Entrada] )\n)",INT,
 "Moléculas carregadas no ano/período filtrado (use o filtro Ano de Entrada)."),
("F. Report por unidade","Resumo da Unidade",
 'VAR part = [% da Unidade no Total]\n'
 'VAR ativas = [Projetos Ativos]\nVAR paradas = [Cancelados + Stand by]\n'
 'RETURN\n    IF (\n        ISBLANK ( [Projetos] ),\n'
 '        "Sem oportunidades para os filtros selecionados.",\n'
 '        [Unidade Selecionada] & " representa " & FORMAT ( part, "0,0%" )\n'
 '            & " das moléculas avaliadas por Novos Negócios no período. "\n'
 '            & FORMAT ( ativas, "0" ) & " em andamento e " & FORMAT ( paradas, "0" )\n'
 '            & " canceladas ou em stand by. Principal motivo: " & [Motivo nº 1] & "."\n    )',TXT,
 "Parágrafo pronto para o slide da unidade de negócio."),

("G. Financeiro","VPL Total","SUM ( Mapeamento[VPL (R$)] )",RS,"Soma do valor presente líquido."),
("G. Financeiro","Peak Sales","SUM ( Mapeamento[Fat. Líq. (Peak Sales, R$)] )",RS,"Pico de faturamento previsto."),
("G. Financeiro","Faturamento 5 Anos",
 "SUM ( Mapeamento[Fat. Líq. DRE (Ano1)] )\n    + SUM ( Mapeamento[Fat. Líq. DRE (Ano2)] )\n"
 "    + SUM ( Mapeamento[Fat. Líq. DRE (Ano3)] )\n    + SUM ( Mapeamento[Fat. Líq. DRE (Ano4)] )\n"
 "    + SUM ( Mapeamento[Fat. Líq. DRE (Ano5)] )",RS,"Soma dos 5 anos do DRE."),
("G. Financeiro","Margem Bruta Média","AVERAGE ( Mapeamento[Margem Bruta (%)] )",PCT,"Margem média dos projetos que têm o dado."),
("G. Financeiro","Projetos com VPL",
 "CALCULATE ( [Projetos], NOT ISBLANK ( Mapeamento[VPL (R$)] ) )",INT,"Quantos têm número financeiro."),
("G. Financeiro","% Cobertura Financeira",
 'DIVIDE (\n    [Projetos com VPL],\n'
 '    CALCULATE ( [Projetos], Mapeamento[Situação] IN { "Em andamento", "Stand by" } )\n)',PCT,
 "Quanto do funil tem número. Hoje é baixo — mostra o tamanho do buraco."),

("H. Qualidade da base","Sem Data de Fim",
 'CALCULATE (\n    [Projetos],\n    Mapeamento[Situação] <> "Em andamento",\n'
 '    ISBLANK ( Mapeamento[Data de Finalização do Projeto em NN] )\n)',INT,
 "Projetos que saíram sem registrar quando. É a pendência nº 1."),
("H. Qualidade da base","% Sem Data de Fim",
 'DIVIDE (\n    [Sem Data de Fim],\n'
 '    CALCULATE ( [Projetos], Mapeamento[Situação] <> "Em andamento" )\n)',PCT,
 "Em percentual."),
("H. Qualidade da base","Sem Motivo",
 'CALCULATE (\n    [Projetos],\n    Mapeamento[Situação] = "Encerrado",\n'
 '    Mapeamento[Motivo] = "(Sem motivo registrado)"\n)',INT,
 "Encerrados sem justificativa registrada."),
("H. Qualidade da base","Sem Unidade de Negócio",
 'CALCULATE ( [Projetos], Mapeamento[Unidade de Negócio] = "(Não informado)" )',INT,
 "Não aparecem em nenhum report de BU."),
("H. Qualidade da base","Sem Categoria",
 'CALCULATE ( [Projetos], Mapeamento[Categoria Padrão] = "(NÃO INFORMADO)" )',INT,
 "Sem categoria não há complexidade nem cálculo de horas."),
("H. Qualidade da base","Sem Área Terapêutica",
 'CALCULATE ( [Projetos], Mapeamento[Franquia] = "(NÃO INFORMADO)" )',INT,
 "Somem dos cortes por franquia."),
("H. Qualidade da base","Total de Pendências",
 "[Sem Data de Fim] + [Sem Motivo] + [Sem Unidade de Negócio]\n    + [Sem Categoria] + [Sem Área Terapêutica]",INT,
 "Soma das pendências. Quanto menor, melhor."),
("H. Qualidade da base","Projetos Parados",
 'CALCULATE ( [Projetos], Mapeamento[Alerta] = "3. Parado" )',INT,
 "Ativos sem nenhuma data nova há mais de 90 dias."),

("I. Apoio","Atualizado em",
 '"Dados atualizados em " & FORMAT ( NOW (), "dd/mm/yyyy HH:mm" )',TXT,
 "Carimbo da última atualização. Coloque no rodapé de cada página."),
]

COLUNA_CALCULADA_HORAS = '''Horas Mês =
// ===================================================================
// RÉGUA DE ESFORÇO — preencha quando o time definir (Parte 4.4)
// Troque cada 0 pelo número de HORAS POR MÊS que um projeto naquele
// status e complexidade consome. Aceita decimais: use 1,5 e não 1.5
// ===================================================================
VAR c = Mapeamento[Complexidade]
VAR s = Mapeamento[Status NN]
RETURN
SWITCH (
    TRUE (),
    s = "AGUARDANDO INÍCIO"   && c = "BAIXO", 0,
    s = "AGUARDANDO INÍCIO"   && c = "MÉDIO", 0,
    s = "AGUARDANDO INÍCIO"   && c = "ALTO",  0,
    s = "PROSPECÇÃO"          && c = "BAIXO", 0,
    s = "PROSPECÇÃO"          && c = "MÉDIO", 0,
    s = "PROSPECÇÃO"          && c = "ALTO",  0,
    s = "CDA"                 && c = "BAIXO", 0,
    s = "CDA"                 && c = "MÉDIO", 0,
    s = "CDA"                 && c = "ALTO",  0,
    s = "AV. TÉCNICA INICIAL" && c = "BAIXO", 0,
    s = "AV. TÉCNICA INICIAL" && c = "MÉDIO", 0,
    s = "AV. TÉCNICA INICIAL" && c = "ALTO",  0,
    s = "AV. MARKETING"       && c = "BAIXO", 0,
    s = "AV. MARKETING"       && c = "MÉDIO", 0,
    s = "AV. MARKETING"       && c = "ALTO",  0,
    s = "NEGOCIAÇÃO"          && c = "BAIXO", 0,
    s = "NEGOCIAÇÃO"          && c = "MÉDIO", 0,
    s = "NEGOCIAÇÃO"          && c = "ALTO",  0,
    s = "APROVAÇÃO SUMMARY"   && c = "BAIXO", 0,
    s = "APROVAÇÃO SUMMARY"   && c = "MÉDIO", 0,
    s = "APROVAÇÃO SUMMARY"   && c = "ALTO",  0,
    s = "TERM SHEET"          && c = "BAIXO", 0,
    s = "TERM SHEET"          && c = "MÉDIO", 0,
    s = "TERM SHEET"          && c = "ALTO",  0,
    s = "CONTRATO"            && c = "BAIXO", 0,
    s = "CONTRATO"            && c = "MÉDIO", 0,
    s = "CONTRATO"            && c = "ALTO",  0,
    0
)'''
