# -*- coding: utf-8 -*-
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_lib import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = "_Medidas"

H1 = {"fontSize": "18pt", "fontWeight": "bold", "color": "#FFFFFF", "fontFamily": "Segoe UI"}
H2 = {"fontSize": "9pt", "color": "#D8E6F5", "fontFamily": "Segoe UI"}
NOTE = {"fontSize": "8pt", "color": "#5A6672", "fontFamily": "Segoe UI", "fontStyle": "italic"}

X5 = [16, 268, 520, 772, 1024];  W5 = 240
X3 = [16, 436, 856];             W3 = 408
X2 = [16, 646];                  W2 = 618

def header(titulo, sub):
    return [
        shape(0, 0, 1280, 48, AZUL, z=-2, radius=0.0),
        textbox(20, 6, 780, 34, [[(titulo, H1)]], z=-1),
        textbox(820, 14, 444, 24, [[(sub, H2)]], align="right", z=-1),
    ]

def mq(role, measure, q=None):
    q = q or Query(); q.add(role, M, measure, kind="measure"); return q

def cat_measure(entity, col, measure, role_cat="Category", role_y="Y", desc=True):
    q = Query()
    c = q.add(role_cat, entity, col)
    m = q.add(role_y, M, measure, kind="measure")
    return q, c, m

# =====================================================================
# 1. VISÃO GERAL
# =====================================================================
def pagina_visao_geral():
    v = header("Visão Geral | Novos Negócios",
               "Foto de hoje do mapeamento ativo de todo o time")
    v += [
        slicer(X5[0], 56, W5, 40, "Equipe", "Nome", "Responsável"),
        slicer(X5[1], 56, W5, 40, "Unidade de Negócio", "Unidade de Negócio", "Unidade de Negócio"),
        slicer(X5[2], 56, W5, 40, "Mapeamento", "Situação", "Situação"),
        slicer(X5[3], 56, W5, 40, "Status NN", "Status", "Status"),
        slicer(X5[4], 56, W5, 40, "Calendário", "Ano", "Ano de entrada"),
    ]
    kpis = [("Projetos", "OPORTUNIDADES", AZUL), ("Projetos Ativos", "EM ANDAMENTO", VERDE),
            ("Projetos Stand by", "STAND BY", LARANJA), ("Moléculas", "MOLÉCULAS", AZUL_CLR),
            ("Fornecedores", "FORNECEDORES", CINZA)]
    for i, (m, lab, cor) in enumerate(kpis):
        v.append(kpi_card(X5[i], 104, W5, 72, M, m, lab, cor))

    q, c, m = cat_measure("Status NN", "Status", "Projetos")
    v.append(container("clusteredColumnChart", X3[0], 184, W3, 215, q,
                       title="QUANTIDADE DE PROJETOS x STATUS"))

    q, c, m = cat_measure("Mapeamento", "Categoria Padrão", "Projetos")
    v.append(container("clusteredBarChart", X3[1], 184, W3, 215, q,
                       title="PROJETOS x CATEGORIA", order_by=(m, True)))

    q = Query()
    q.add("Category", "País", "País")
    q.add("Size", M, "Projetos", kind="measure")
    v.append(container("map", X3[2], 184, W3, 215, q,
                       title="PROJETOS x PAÍS DO FORNECEDOR"))

    q = Query()
    q.add("Values", "Mapeamento", "Responsável Final")
    q.add("Values", "Mapeamento", "Molécula")
    q.add("Values", "Mapeamento", "Fornecedor / Parceiro")
    q.add("Values", "Mapeamento", "Status NN")
    q.add("Values", "Mapeamento", "Situação")
    q.add("Values", "Mapeamento", "Alerta")
    v.append(container("tableEx", X2[0], 407, W2, 290, q,
                       title="PROJETOS — VISÃO RESUMIDA"))

    q, c, m = cat_measure("Mapeamento", "Coligada Padrão", "Projetos")
    v.append(container("donutChart", X2[1], 407, 300, 290, q,
                       title="% PROJETOS x COLIGADA"))

    q, c, m = cat_measure("Mapeamento", "Situação", "Projetos")
    v.append(container("donutChart", 952, 407, 312, 290, q,
                       title="SITUAÇÃO DOS PROJETOS"))
    return page("SecVisaoGeral", "1. Visão Geral", v, ordinal=0)

# =====================================================================
# 2. CARREGAMENTO DO TIME
# =====================================================================
def pagina_carregamento():
    v = header("Carregamento do Time | Capacidade x Demanda",
               "Horas empenhadas hoje, por pessoa, status e complexidade")
    v += [
        slicer(X5[0], 56, W5, 40, "Equipe", "Nome", "Responsável"),
        slicer(X5[1], 56, W5, 40, "Mapeamento", "Atividade", "Atividade (NN / Interno / Parceiro)"),
        slicer(X5[2], 56, W5, 40, "Mapeamento", "Situação", "Situação"),
        slicer(X5[3], 56, W5, 40, "Mapeamento", "Complexidade", "Complexidade"),
        slicer(X5[4], 56, W5, 40, "Unidade de Negócio", "Unidade de Negócio", "Unidade de Negócio"),
    ]
    kpis = [("Projetos Ativos", "PROJETOS ATIVOS", VERDE),
            ("Horas Empenhadas", "HORAS EMPENHADAS", AZUL),
            ("Capacidade (h)", "CAPACIDADE (H)", CINZA),
            ("% Ocupação", "% OCUPAÇÃO", VERMELHO),
            ("Projetos por Pessoa", "PROJETOS / PESSOA", AZUL_CLR)]
    for i, (m, lab, cor) in enumerate(kpis):
        v.append(kpi_card(X5[i], 104, W5, 72, M, m, lab, cor))

    q = Query()
    q.add("Category", "Equipe", "Nome")
    mh = q.add("Y", M, "Horas Empenhadas", kind="measure")
    q.add("Y", M, "Capacidade (h)", kind="measure")
    v.append(container("clusteredBarChart", X2[0], 184, W2, 240, q,
                       title="HORAS EMPENHADAS x CAPACIDADE — POR PESSOA",
                       order_by=(mh, True)))

    q = Query()
    q.add("Y", M, "% Ocupação", kind="measure")
    v.append(container("gauge", X2[1], 184, 300, 240, q,
                       title="% DE OCUPAÇÃO DO TIME"))

    q, c, m = cat_measure("Mapeamento", "Atividade", "Horas Empenhadas")
    v.append(container("donutChart", 952, 184, 312, 240, q,
                       title="HORAS x ATIVIDADE"))

    q = Query()
    q.add("Category", "Status NN", "Status")
    q.add("Series", "Mapeamento", "Complexidade")
    q.add("Y", M, "Projetos Ativos", kind="measure")
    v.append(container("barChart", X2[0], 432, W2, 265, q,
                       title="PROJETOS ATIVOS POR STATUS E COMPLEXIDADE"))

    q = Query()
    q.add("Values", "Equipe", "Nome")
    q.add("Values", M, "Projetos Ativos", kind="measure")
    q.add("Values", M, "Horas Empenhadas", kind="measure")
    q.add("Values", M, "% Ocupação", kind="measure")
    q.add("Values", M, "Status Ocupação", kind="measure")
    v.append(container("tableEx", X2[1], 432, 618, 265, q,
                       title="OCUPAÇÃO POR PESSOA"))
    return page("SecCarregamento", "2. Carregamento do Time", v, ordinal=1)

# =====================================================================
# 3. EVOLUÇÃO DO MÊS  (visão nova: o mês inteiro, não só a foto do dia)
# =====================================================================
def pagina_evolucao():
    v = header("Evolução do Mês | Como transcorreu o carregamento",
               "Entradas, saídas e carteira mês a mês — e não apenas a foto do dia")
    v += [
        slicer(X5[0], 56, W5, 40, "Equipe", "Nome", "Responsável"),
        slicer(X5[1], 56, W5, 40, "Calendário", "Ano", "Ano"),
        slicer(X5[2], 56, W5, 40, "Calendário", "Mês", "Mês"),
        slicer(X5[3], 56, W5, 40, "Unidade de Negócio", "Unidade de Negócio", "Unidade de Negócio"),
        slicer(X5[4], 56, W5, 40, "Carregamento Mensal", "Status no Mês", "Status no mês"),
    ]
    kpis = [("Ativos no Início do Mês", "INÍCIO DO MÊS", CINZA),
            ("Entradas no Mês", "ENTRARAM", VERDE),
            ("Saídas no Mês", "SAÍRAM", VERMELHO),
            ("Ativos no Fim do Mês", "FIM DO MÊS", AZUL),
            ("Diferença Hoje vs Mês", "HOJE vs FIM DO MÊS", LARANJA)]
    for i, (m, lab, cor) in enumerate(kpis):
        v.append(kpi_card(X5[i], 104, W5, 72, M, m, lab, cor))

    q = Query()
    q.add("Category", "Calendário", "Ano-Mês")
    q.add("Y", M, "Ativos no Fim do Mês", kind="measure")
    q.add("Y2", M, "Entradas no Mês", kind="measure")
    q.add("Y2", M, "Saídas no Mês", kind="measure")
    v.append(container("lineClusteredColumnComboChart", X2[0], 184, W2, 245, q,
                       title="CARTEIRA, ENTRADAS E SAÍDAS POR MÊS"))

    q = Query()
    q.add("Category", "Calendário", "Ano-Mês")
    q.add("Y", M, "Saldo do Mês", kind="measure")
    v.append(container("waterfallChart", X2[1], 184, W2, 245, q,
                       title="SALDO DO MÊS (ENTRADAS − SAÍDAS)"))

    q = Query()
    q.add("Rows", "Equipe", "Nome")
    q.add("Columns", "Calendário", "Ano-Mês")
    q.add("Values", M, "Ativos no Fim do Mês", kind="measure")
    v.append(container("pivotTable", X2[0], 437, W2, 190, q,
                       title="CARTEIRA POR PESSOA E MÊS"))

    q = Query()
    q.add("Category", "Calendário", "Ano-Mês")
    q.add("Series", "Carregamento Mensal", "Status no Mês")
    q.add("Y", M, "Projetos no Mês", kind="measure")
    v.append(container("columnChart", X2[1], 437, W2, 190, q,
                       title="COMPOSIÇÃO DO FUNIL AO LONGO DO TEMPO"))

    v.append(kpi_card(16, 635, 1248, 62, M, "Narrativa do Mês", "RESUMO PARA O REPORT", AZUL))
    return page("SecEvolucao", "3. Evolução do Mês", v, ordinal=2)

# =====================================================================
# 4. REPORT POR UNIDADE DE NEGÓCIO  (substitui o PDF NR e o PPT SNC)
# =====================================================================
def pagina_bu():
    v = header("One Page Report | Unidade de Negócio",
               "Selecione a unidade e o ano — o report que hoje é feito à mão")
    v += [
        slicer(X5[0], 56, W5, 40, "Unidade de Negócio", "Unidade de Negócio", "Unidade de Negócio"),
        slicer(X5[1], 56, W5, 40, "Mapeamento", "Franquia", "Franquia / Classe terapêutica"),
        slicer(X5[2], 56, W5, 40, "Calendário", "Ano", "Ano de entrada"),
        slicer(X5[3], 56, W5, 40, "Mapeamento", "Categoria Padrão", "Categoria"),
        slicer(X5[4], 56, W5, 40, "Equipe", "Nome", "Responsável"),
    ]
    kpis = [("Moléculas", "MOLÉCULAS AVALIADAS", AZUL),
            ("Projetos", "OPORTUNIDADES", AZUL_CLR),
            ("Projetos Ativos", "EM ANDAMENTO", VERDE),
            ("Cancelados + Stand by", "CANCELADAS / STAND BY", VERMELHO),
            ("Motivo nº 1", "PRINCIPAL MOTIVO", CINZA)]
    for i, (m, lab, cor) in enumerate(kpis):
        v.append(kpi_card(X5[i], 104, W5, 72, M, m, lab, cor))

    q, c, m = cat_measure("Status NN", "Status", "Projetos Ativos")
    v.append(container("hundredPercentStackedBarChart", X3[0], 184, W3, 250, q,
                       title="ESTÁGIO DAS OPORTUNIDADES EM ANDAMENTO"))

    q, c, m = cat_measure("Unidade de Negócio", "Unidade de Negócio", "Projetos")
    v.append(container("clusteredBarChart", X3[1], 184, W3, 250, q,
                       title="FRANQUIAS DE ATUAÇÃO DE NOVOS NEGÓCIOS", order_by=(m, True)))

    q, c, m = cat_measure("Motivo Cancelamento", "Motivo", "Cancelados + Stand by")
    v.append(container("clusteredBarChart", X3[2], 184, W3, 250, q,
                       title="MOTIVOS DE CANCELAMENTO / STAND BY", order_by=(m, True)))

    q, c, m = cat_measure("Mapeamento", "Categoria Padrão", "Moléculas")
    v.append(container("donutChart", X3[0], 442, W3, 255, q,
                       title="CATEGORIA DAS MOLÉCULAS"))

    q, c, m = cat_measure("Mapeamento", "Fase Oportunidade NN", "Moléculas")
    v.append(container("clusteredBarChart", X3[1], 442, W3, 255, q,
                       title="MATURIDADE (FASE DA OPORTUNIDADE)", order_by=(m, True)))

    q = Query()
    q.add("Values", "Mapeamento", "Molécula")
    q.add("Values", "Mapeamento", "Fornecedor / Parceiro")
    q.add("Values", "Mapeamento", "Fase Oportunidade NN")
    q.add("Values", "Mapeamento", "Indicação")
    q.add("Values", "Mapeamento", "Status NN")
    q.add("Values", "Mapeamento", "Situação")
    v.append(container("tableEx", X3[2], 442, W3, 255, q,
                       title="OPORTUNIDADES EM DESTAQUE"))
    return page("SecBU", "4. Report por Unidade de Negócio", v, ordinal=3)

# =====================================================================
# 5. FINANCEIRO
# =====================================================================
def pagina_financeiro():
    v = header("Visão Financeira | Valor do Pipeline",
               "VPL, faturamento projetado e margem dos projetos avaliados")
    v += [
        slicer(X5[0], 56, W5, 40, "Unidade de Negócio", "Unidade de Negócio", "Unidade de Negócio"),
        slicer(X5[1], 56, W5, 40, "Equipe", "Nome", "Responsável"),
        slicer(X5[2], 56, W5, 40, "Mapeamento", "Situação", "Situação"),
        slicer(X5[3], 56, W5, 40, "Status NN", "Status", "Status"),
        slicer(X5[4], 56, W5, 40, "Calendário", "Ano", "Ano de entrada"),
    ]
    kpis = [("VPL Total", "VPL TOTAL", VERDE), ("Peak Sales", "PEAK SALES", AZUL),
            ("Faturamento 5 Anos", "FAT. LÍQ. 5 ANOS", AZUL_CLR),
            ("Margem Bruta Média", "MARGEM BRUTA MÉDIA", LARANJA),
            ("% Cobertura Financeira", "% COM DADO FINANCEIRO", VERMELHO)]
    for i, (m, lab, cor) in enumerate(kpis):
        v.append(kpi_card(X5[i], 104, W5, 72, M, m, lab, cor))

    q = Query()
    q.add("Category", "Mapeamento", "Molécula")
    mv = q.add("Y", M, "VPL Total", kind="measure")
    v.append(container("clusteredBarChart", X2[0], 184, W2, 245, q,
                       title="VPL POR MOLÉCULA", order_by=(mv, True), top=15))

    q = Query()
    q.add("Category", "Unidade de Negócio", "Unidade de Negócio")
    mv = q.add("Y", M, "VPL Total", kind="measure")
    v.append(container("clusteredColumnChart", X2[1], 184, W2, 245, q,
                       title="VPL POR UNIDADE DE NEGÓCIO", order_by=(mv, True)))

    q = Query()
    q.add("Values", "Mapeamento", "Molécula")
    q.add("Values", "Mapeamento", "Fornecedor / Parceiro")
    q.add("Values", "Mapeamento", "Moeda")
    q.add("Values", M, "VPL Total", kind="measure")
    q.add("Values", M, "Peak Sales", kind="measure")
    q.add("Values", M, "Margem Bruta Média", kind="measure")
    q.add("Values", M, "Faturamento 5 Anos", kind="measure")
    v.append(container("tableEx", X2[0], 437, W2, 260, q,
                       title="PROJETOS COM DADOS FINANCEIROS"))

    q, c, m = cat_measure("Status NN", "Status", "VPL Total")
    v.append(container("clusteredColumnChart", X2[1], 437, W2, 260, q,
                       title="VPL POR ESTÁGIO DO FUNIL"))
    return page("SecFinanceiro", "5. Financeiro", v, ordinal=4)

# =====================================================================
# 6. MAPEAMENTO COMPLETO  (o consolidado que hoje precisa ser pedido)
# =====================================================================
def pagina_completo():
    v = header("Mapeamento Ativo Completo | Consolidado de todo o time",
               "Todas as colunas, todos os responsáveis — exportável em Excel")
    linha1 = [("Equipe", "Nome", "Responsável"),
              ("Unidade de Negócio", "Unidade de Negócio", "Unidade de Negócio"),
              ("Status NN", "Status", "Status"),
              ("Mapeamento", "Situação", "Situação"),
              ("Mapeamento", "Categoria Padrão", "Categoria")]
    linha2 = [("Mapeamento", "Franquia", "Franquia"),
              ("Mapeamento", "Entrada", "Origem da oportunidade"),
              ("Mapeamento", "Atividade", "Atividade"),
              ("Motivo Cancelamento", "Motivo", "Motivo cancelamento"),
              ("Calendário", "Ano", "Ano de entrada")]
    for i, (e, c, t) in enumerate(linha1):
        v.append(slicer(X5[i], 56, W5, 40, e, c, t))
    for i, (e, c, t) in enumerate(linha2):
        v.append(slicer(X5[i], 102, W5, 40, e, c, t))

    q = Query()
    for col in ["Responsável Final", "Gerência", "Entrada", "Molécula", "Código CI",
                "Marca do Referência BR", "Fornecedor / Parceiro", "País Fornecedor",
                "Categoria Padrão", "Coligada Padrão", "Área Terapêutica",
                "Fase Oportunidade NN", "Indicação", "Forma Farmacêutica",
                "Status NN", "Situação", "Atividade", "Motivo Padrão",
                "Detalhamento do cancelamento", "Data de Entrada",
                "Data Início Efetiva", "Data Fim Efetiva", "Dias em NN",
                "Complexidade", "Faixa de Duração", "Alerta"]:
        q.add("Values", "Mapeamento", col)
    v.append(container("tableEx", 16, 152, 1248, 545, q,
                       title="MAPEAMENTO ATIVO — BASE COMPLETA"))
    return page("SecCompleto", "6. Mapeamento Completo", v, ordinal=5)

# =====================================================================
# 7. QUALIDADE DA BASE
# =====================================================================
def pagina_qualidade():
    v = header("Qualidade da Base | O que falta preencher",
               "Cada linha aqui é um campo que impede uma análise")
    v += [
        slicer(X5[0], 56, W5, 40, "Equipe", "Nome", "Responsável"),
        slicer(X5[1], 56, W5, 40, "Qualidade de Dados", "Gravidade", "Gravidade"),
        slicer(X5[2], 56, W5, 40, "Qualidade de Dados", "Regra", "Regra"),
        slicer(X5[3], 56, W5, 40, "Unidade de Negócio", "Unidade de Negócio", "Unidade de Negócio"),
        slicer(X5[4], 56, W5, 40, "Mapeamento", "Situação", "Situação"),
    ]
    kpis = [("Índice de Qualidade", "ÍNDICE DE QUALIDADE", VERDE),
            ("Problemas", "PENDÊNCIAS", LARANJA),
            ("Problemas Graves", "PENDÊNCIAS GRAVES", VERMELHO),
            ("Projetos com Problema", "PROJETOS AFETADOS", AZUL),
            ("% Projetos Sem Data de Fim", "% SEM DATA DE FIM", VERMELHO)]
    for i, (m, lab, cor) in enumerate(kpis):
        v.append(kpi_card(X5[i], 104, W5, 72, M, m, lab, cor))

    q, c, m = cat_measure("Qualidade de Dados", "Regra", "Problemas")
    v.append(container("clusteredBarChart", X2[0], 184, W2, 245, q,
                       title="PENDÊNCIAS POR REGRA", order_by=(m, True)))

    q, c, m = cat_measure("Equipe", "Nome", "Problemas")
    v.append(container("clusteredBarChart", X2[1], 184, W2, 245, q,
                       title="PENDÊNCIAS POR RESPONSÁVEL", order_by=(m, True)))

    q = Query()
    q.add("Values", "Qualidade de Dados", "Responsável Final")
    q.add("Values", "Qualidade de Dados", "Molécula")
    q.add("Values", "Qualidade de Dados", "Fornecedor / Parceiro")
    q.add("Values", "Qualidade de Dados", "Regra")
    q.add("Values", "Qualidade de Dados", "Gravidade")
    q.add("Values", "Qualidade de Dados", "Impacto")
    v.append(container("tableEx", 16, 437, 1248, 260, q,
                       title="PENDÊNCIAS — DETALHE POR PROJETO"))
    return page("SecQualidade", "7. Qualidade da Base", v, ordinal=6)


def build():
    pages = [pagina_visao_geral(), pagina_carregamento(), pagina_evolucao(),
             pagina_bu(), pagina_financeiro(), pagina_completo(), pagina_qualidade()]
    layout = {
        "id": 0,
        "resourcePackages": [{"resourcePackage": {
            "name": "SharedResources", "type": 2, "disabled": False,
            "items": [{"type": 202, "path": "BaseThemes/CY24SU10.json", "name": "CY24SU10"}]}}],
        "config": json.dumps({
            "version": "5.43",
            "themeCollection": {"baseTheme": {"name": "CY24SU10", "version": "5.55", "type": 2}},
            "activeSectionIndex": 0,
            "defaultDrillFilterOtherVisuals": True,
            "settings": {"useStylableVisualContainerHeader": True,
                         "allowChangeFilterTypes": True,
                         "useNewFilterPaneExperience": True},
            "objects": {"outspacePane": [{"properties": {"expanded": {"expr": {
                "Literal": {"Value": "false"}}}}}]},
        }, ensure_ascii=False),
        "layoutOptimization": 0,
        "sections": pages,
        "filters": "[]",
        "publicCustomVisuals": [],
    }
    out = os.path.join(ROOT, "modelo", "Layout.json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(layout, ensure_ascii=False, indent=1))
    n = sum(len(p["visualContainers"]) for p in pages)
    print(f"OK  Layout.json -> {out}")
    print(f"    páginas={len(pages)}  visuais={n}")
    return layout

if __name__ == "__main__":
    build()
