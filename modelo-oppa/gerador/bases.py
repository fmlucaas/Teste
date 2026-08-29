# -*- coding: utf-8 -*-
"""Abas Tributos, Aportes e Investimentos."""
import datetime as dt
from openpyxl.styles import Alignment
from openpyxl.comments import Comment
from common import *

# =====================================================================
#  TRIBUTOS
# =====================================================================
ANEXO_III = [  # faixa, de, ate, aliquota nominal, parcela a deduzir
    (1,        0.00,  180000.00, 0.0600,      0.00),
    (2,   180000.01,  360000.00, 0.1120,   9360.00),
    (3,   360000.01,  720000.00, 0.1350,  17640.00),
    (4,   720000.01, 1800000.00, 0.1600,  35640.00),
    (5,  1800000.01, 3600000.00, 0.2100, 125640.00),
    (6,  3600000.01, 4800000.00, 0.3300, 648000.00),
]
ANEXO_V = [
    (1,        0.00,  180000.00, 0.1550,      0.00),
    (2,   180000.01,  360000.00, 0.1800,   4500.00),
    (3,   360000.01,  720000.00, 0.1950,   9900.00),
    (4,   720000.01, 1800000.00, 0.2050,  17100.00),
    (5,  1800000.01, 3600000.00, 0.2300,  62100.00),
    (6,  3600000.01, 4800000.00, 0.3050, 540000.00),
]

T = {}

def build_tributos(wb, P):
    ws = wb.create_sheet("Tributos")
    titulo(ws, "TRIBUTAÇÃO — SIMPLES NACIONAL E LUCRO PRESUMIDO",
           "Tabelas da LC 123/2006. A 'Tabela Ativa' é a que o modelo usa, conforme o regime "
           "escolhido em Premissas.", largura=8)
    for col, w in zip("ABCDEFGH", (10, 20, 20, 18, 20, 6, 78, 6)):
        ws.column_dimensions[col].width = w

    def tabela(lin, nome, dados, cor):
        secao(ws, lin, nome, 8)
        hdr = ["Faixa", "RBT12 — de", "RBT12 — até", "Alíquota nominal", "Parcela a deduzir"]
        for j, h in enumerate(hdr):
            c = ws.cell(lin + 1, 1 + j, h)
            c.font = f(9, True, BRANCO); c.fill = FILL_HEADER
            c.alignment = Alignment(horizontal="center", wrap_text=True)
        for k, (fx, de, ate, al, ded) in enumerate(dados):
            rr = lin + 2 + k
            ws.cell(rr, 1, fx).number_format = INT
            ws.cell(rr, 2, de).number_format = BRL
            ws.cell(rr, 3, ate).number_format = BRL
            ws.cell(rr, 4, al).number_format = PCT2
            ws.cell(rr, 5, ded).number_format = BRL
            for j in range(1, 6):
                cc = ws.cell(rr, j)
                cc.font = f(9, False, cor); cc.border = BORDA_FINA
                cc.alignment = Alignment(horizontal="center")
        return lin + 2   # primeira linha de dados

    r = 4
    T["a3"] = tabela(r, "ANEXO III — Serviços em geral (alíquota efetiva de 6% a ~19,5%)", ANEXO_III, AZUL_INPUT)
    nota(ws, "G5", "Aplica-se a software/SaaS SOMENTE se o Fator R ≥ 28%.")
    r += 9
    T["a5"] = tabela(r, "ANEXO V — Licenciamento/cessão de uso de software (Fator R < 28%)", ANEXO_V, AZUL_INPUT)
    nota(ws, "G14", "Regra padrão para licenciamento de software quando o Fator R fica abaixo de 28%.")
    r += 9

    # --- Tabela ativa ---------------------------------------------------
    secao(ws, r, "TABELA ATIVA — selecionada pelo regime definido em Premissas", 8)
    hdr = ["Faixa", "RBT12 — de", "Alíquota nominal", "Parcela a deduzir"]
    for j, h in enumerate(hdr):
        c = ws.cell(r + 1, 1 + j, h)
        c.font = f(9, True, BRANCO); c.fill = FILL_HEADER
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    base = r + 2
    for k in range(6):
        rr = base + k
        ws.cell(rr, 1, k + 1).number_format = INT
        ws.cell(rr, 2, f'=IF(Premissas!$B${P["regime"]}=2,B{T["a5"]+k},B{T["a3"]+k})').number_format = BRL
        ws.cell(rr, 3, f'=IF(Premissas!$B${P["regime"]}=2,D{T["a5"]+k},D{T["a3"]+k})').number_format = PCT2
        ws.cell(rr, 4, f'=IF(Premissas!$B${P["regime"]}=2,E{T["a5"]+k},E{T["a3"]+k})').number_format = BRL
        for j in range(1, 5):
            cc = ws.cell(rr, j)
            cc.font = f(9, True, VERDE_LINK); cc.border = BORDA_FINA
            cc.fill = FILL_SUB
            cc.alignment = Alignment(horizontal="center")
    T["ativa_ini"] = base
    T["ativa_fim"] = base + 5
    r = base + 7

    # --- Fator R --------------------------------------------------------
    secao(ws, r, "FATOR R — o teste que decide entre Anexo III e Anexo V", 8); r += 1
    txt = [
        ("Fator R = (folha de salários + pró-labore + encargos dos últimos 12 meses) ÷ RBT12", True),
        ("Fator R ≥ 28%  →  Anexo III (alíquota efetiva a partir de 6%)", False),
        ("Fator R < 28%   →  Anexo V (alíquota efetiva a partir de 15,5%)", False),
        ("", False),
        ("⚠ RISCO MATERIAL PARA A OPPA: pagamento a equipe PJ (prestadores de serviço) NÃO entra no "
         "cálculo do Fator R. Só contam folha CLT e pró-labore dos sócios. Com a estrutura descrita no "
         "brief — equipe PJ e pró-labore zero em 2026 — o Fator R fica próximo de 0% e a empresa cai no "
         "Anexo V, com alíquota inicial de 15,5% em vez de 6%.", False),
        ("", False),
        ("Como reverter: (a) registrar pró-labore relevante para os sócios; (b) contratar parte da equipe "
         "em regime CLT. Ambos aumentam o custo de folha, mas podem valer a pena pela economia tributária. "
         "O quadro abaixo compara os dois anexos no faturamento projetado.", False),
    ]
    for t, b in txt:
        c = ws.cell(r, 1, t)
        c.font = f(9, b, "C00000" if t.startswith("⚠") else CINZA, italic=not b)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
        ws.row_dimensions[r].height = 15 if len(t) < 90 else 44
        r += 1
    T["fator_r_calc"] = r + 1
    r += 1

    # --- Comparativo de anexos ------------------------------------------
    secao(ws, r, "COMPARATIVO — alíquota efetiva por faixa de faturamento anual", 8); r += 1
    for j, h in enumerate(["RBT12", "Anexo III efetivo", "Anexo V efetivo", "Diferença",
                           "Custo anual da diferença"]):
        c = ws.cell(r, 1 + j, h)
        c.font = f(9, True, BRANCO); c.fill = FILL_HEADER
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    r += 1
    for k, rbt in enumerate([180000, 360000, 720000, 1800000, 3600000, 4800000]):
        rr = r + k
        ws.cell(rr, 1, rbt).number_format = BRL
        ws.cell(rr, 2, f'=($A{rr}*INDEX($D${T["a3"]}:$D${T["a3"]+5},MATCH($A{rr},$B${T["a3"]}:$B${T["a3"]+5},1))'
                       f'-INDEX($E${T["a3"]}:$E${T["a3"]+5},MATCH($A{rr},$B${T["a3"]}:$B${T["a3"]+5},1)))/$A{rr}'
               ).number_format = PCT2
        ws.cell(rr, 3, f'=($A{rr}*INDEX($D${T["a5"]}:$D${T["a5"]+5},MATCH($A{rr},$B${T["a5"]}:$B${T["a5"]+5},1))'
                       f'-INDEX($E${T["a5"]}:$E${T["a5"]+5},MATCH($A{rr},$B${T["a5"]}:$B${T["a5"]+5},1)))/$A{rr}'
               ).number_format = PCT2
        ws.cell(rr, 4, f'=$C{rr}-$B{rr}').number_format = PCT2
        ws.cell(rr, 5, f'=$D{rr}*$A{rr}').number_format = BRL
        for j in range(1, 6):
            cc = ws.cell(rr, j)
            cc.font = f(9, False, PRETO); cc.border = BORDA_FINA
            cc.alignment = Alignment(horizontal="center")
        ws.cell(rr, 5).font = f(9, True, "C00000")
    nota(ws, f"G{r}", "Quanto a Oppa paga a mais por ano se cair no Anexo V em vez do Anexo III.")
    return ws, T


# =====================================================================
#  APORTES
# =====================================================================
APORTES = [
    # data, socio, valor, status, tipo
    (dt.date(2026, 4, 16), "Paulo Kapp",        10000, "Realizado", "Fundador"),
    (dt.date(2026, 7,  4), "Lucas Medina",       5000, "Realizado", "Fundador"),
    (dt.date(2026, 8, 20), "Paulo Kapp",        10000, "Realizado", "Fundador"),
    (dt.date(2026, 8, 20), "Felipe Toescher",    3000, "Realizado", "Fundador"),
    (dt.date(2026, 8, 20), "Lucas Iung",         2000, "Realizado", "Fundador"),
    (dt.date(2026, 8, 29), "Lucas Iung",         3000, "Realizado", "Fundador"),
    (dt.date(2026,12, 15), "Lucas Medina",       5000, "Compromisso","Fundador"),
    (dt.date(2026,12, 15), "Felipe Toescher",    7000, "Compromisso","Fundador"),
    (dt.date(2026,12, 15), "Lucas Iung",         5000, "Compromisso","Fundador"),
    (dt.date(2027, 6, 15), "Lucas Medina",       5000, "Compromisso","Fundador"),
    (dt.date(2027, 6, 15), "Felipe Toescher",    5000, "Compromisso","Fundador"),
    (dt.date(2027, 6, 15), "Lucas Iung",         5000, "Compromisso","Fundador"),
    (dt.date(2027,12, 15), "Lucas Medina",       5000, "Compromisso","Fundador"),
    (dt.date(2027,12, 15), "Felipe Toescher",    5000, "Compromisso","Fundador"),
    (dt.date(2027,12, 15), "Lucas Iung",         5000, "Compromisso","Fundador"),
    (dt.date(2026,10, 15), "C-ioT",             40000, "Previsto",  "Novo sócio"),
    (dt.date(2026,10, 15), "Felipe Martinelli", 40000, "Previsto",  "Novo sócio"),
    (dt.date(2026,11, 15), "Shaiane",           40000, "Previsto",  "Novo sócio"),
]
FUNDADORES = ["Paulo Kapp", "Lucas Medina", "Felipe Toescher", "Lucas Iung"]

A = {}

def build_aportes(wb, P):
    ws = wb.create_sheet("Aportes")
    titulo(ws, "APORTES DE SÓCIOS — CRONOGRAMA E CAP TABLE",
           "Fatos em azul vêm do brief. 'Compromisso' = regra dos R$ 20.000 por fundador "
           "(R$ 10.000 ainda em 2026, saldo até 2027). 'Previsto' = negociação em curso, não assinada.")
    largura_padrao(ws, col_a=30, col_mes_w=11)
    for col, w in zip("ABCDEF", (16, 24, 16, 16, 16, 4)):
        ws.column_dimensions[col].width = w

    # --- Lista de aportes -----------------------------------------------
    r = 4
    secao(ws, r, "LANÇAMENTOS", 6); r += 1
    for j, h in enumerate(["Data", "Sócio", "Valor", "Status", "Tipo"]):
        c = ws.cell(r, 1 + j, h)
        c.font = f(9, True, BRANCO); c.fill = FILL_HEADER
        c.alignment = Alignment(horizontal="center")
    r += 1
    A["ini"] = r
    for (d, s, v, st, tp) in sorted(APORTES, key=lambda x: x[0]):
        ws.cell(r, 1, dt.datetime(d.year, d.month, d.day)).number_format = DATA
        ws.cell(r, 2, s)
        ws.cell(r, 3, v).number_format = BRL
        ws.cell(r, 4, st)
        ws.cell(r, 5, tp)
        cor = AZUL_INPUT if st == "Realizado" else ("000000" if st == "Compromisso" else "BF8F00")
        for j in range(1, 6):
            cc = ws.cell(r, j)
            cc.font = f(9, st == "Realizado", cor)
            cc.border = BORDA_FINA
            cc.alignment = Alignment(horizontal="center" if j != 2 else "left", indent=1 if j == 2 else 0)
            if st == "Realizado":
                cc.fill = FILL_OK
            elif st == "Previsto":
                cc.fill = FILL_ALERTA
        r += 1
    A["fim"] = r - 1
    ws.cell(r, 2, "TOTAL").font = f(10, True)
    c = ws.cell(r, 3, f'=SUM(C{A["ini"]}:C{A["fim"]})')
    c.number_format = BRL; c.font = f(10, True); c.fill = FILL_TOTAL
    A["total_geral"] = r
    r += 2

    # --- Resumo por status ----------------------------------------------
    secao(ws, r, "RESUMO", 6); r += 1
    resumo = [
        ("Realizado até 29/08/2026", '"Realizado"'),
        ("Compromisso de fundadores a integralizar", '"Compromisso"'),
        ("Previsto — novos sócios (não assinado)", '"Previsto"'),
    ]
    for lbl, cond in resumo:
        ws.cell(r, 2, lbl).font = f(9)
        c = ws.cell(r, 3, f'=SUMIFS($C${A["ini"]}:$C${A["fim"]},$D${A["ini"]}:$D${A["fim"]},{cond})')
        c.number_format = BRL; c.font = f(9, True)
        r += 1
    ws.cell(r, 2, "Capital total do caso-base (sem Boston Scientific)").font = f(10, True)
    c = ws.cell(r, 3, f'=SUM(C{A["ini"]}:C{A["fim"]})')
    c.number_format = BRL; c.font = f(10, True); c.fill = FILL_TOTAL
    r += 1
    ws.cell(r, 2, "(+) Aporte Boston Scientific, se ativo").font = f(9, italic=True)
    c = ws.cell(r, 3, f'=Premissas!$B${P["boston_on"]}*Premissas!$B${P["boston_val"]}')
    c.number_format = BRL; c.font = f(9, False, VERDE_LINK)
    r += 2

    # --- Compromissos por fundador --------------------------------------
    secao(ws, r, "CONTROLE DO COMPROMISSO DOS FUNDADORES (R$ 20.000 cada · R$ 10.000 ainda em 2026)", 6)
    r += 1
    for j, h in enumerate(["Fundador", "Meta total", "Aportado até 2026", "Aportado total",
                           "Falta em 2026", "Falta total"]):
        c = ws.cell(r, 1 + j, h)
        c.font = f(9, True, BRANCO); c.fill = FILL_HEADER
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.column_dimensions["F"].width = 16
    r += 1
    A["meta"] = r
    for nome in FUNDADORES:
        ws.cell(r, 1, nome).font = f(9, True)
        ws.cell(r, 2, 20000).number_format = BRL
        ws.cell(r, 2).font = f(9, False, AZUL_INPUT)
        ws.cell(r, 3, f'=SUMIFS($C${A["ini"]}:$C${A["fim"]},$B${A["ini"]}:$B${A["fim"]},$A{r},'
                      f'$A${A["ini"]}:$A${A["fim"]},"<="&DATE(2026,12,31))').number_format = BRL
        ws.cell(r, 4, f'=SUMIFS($C${A["ini"]}:$C${A["fim"]},$B${A["ini"]}:$B${A["fim"]},$A{r})'
               ).number_format = BRL
        ws.cell(r, 5, f'=MAX(0,10000-$C{r})').number_format = BRL
        ws.cell(r, 6, f'=MAX(0,$B{r}-$D{r})').number_format = BRL
        for j in range(1, 7):
            cc = ws.cell(r, j)
            if j > 2:
                cc.font = f(9, False, PRETO)
            cc.border = BORDA_FINA
            cc.alignment = Alignment(horizontal="center" if j > 1 else "left", indent=1)
        r += 1
    nota(ws, f"H{A['meta']}", "Paulo Kapp já integralizou os R$ 20.000. Os demais têm saldo a aportar.")
    r += 1

    # --- Cronograma mensal ----------------------------------------------
    r += 1
    cabecalho_tempo(ws, linha_data=r, congelar=f"B{r+5}")
    A["tempo"] = r
    r += 4
    rotulo(ws, r, "Aportes de fundadores", 1)
    preencher_linha(ws, r, lambda i, L: (
        f'=SUMIFS($C${A["ini"]}:$C${A["fim"]},$E${A["ini"]}:$E${A["fim"]},"Fundador",'
        f'$A${A["ini"]}:$A${A["fim"]},">="&{L}${A["tempo"]},'
        f'$A${A["ini"]}:$A${A["fim"]},"<="&EOMONTH({L}${A["tempo"]},0))'), BRL)
    A["fund"] = r; r += 1
    rotulo(ws, r, "Aportes de novos sócios", 1)
    preencher_linha(ws, r, lambda i, L: (
        f'=SUMIFS($C${A["ini"]}:$C${A["fim"]},$E${A["ini"]}:$E${A["fim"]},"Novo sócio",'
        f'$A${A["ini"]}:$A${A["fim"]},">="&{L}${A["tempo"]},'
        f'$A${A["ini"]}:$A${A["fim"]},"<="&EOMONTH({L}${A["tempo"]},0))'), BRL)
    A["novos"] = r; r += 1
    rotulo(ws, r, "Aporte Boston Scientific (se ativo)", 1)
    preencher_linha(ws, r, lambda i, L: (
        f'=IF(AND(Premissas!$B${P["boston_on"]}=1,'
        f'{L}${A["tempo"]}=DATE(YEAR(Premissas!$B${P["boston_mes"]}),MONTH(Premissas!$B${P["boston_mes"]}),1)),'
        f'Premissas!$B${P["boston_val"]},0)'), BRL, color=VERDE_LINK)
    A["boston"] = r; r += 1
    rotulo(ws, r, "TOTAL DE APORTES NO MÊS", 0, bold=True)
    preencher_linha(ws, r, lambda i, L: f'=SUM({L}{A["fund"]}:{L}{A["boston"]})', BRL, bold=True)
    for i in range(1, N_MESES + 1):
        ws[f"{col_mes(i)}{r}"].fill = FILL_TOTAL
    A["total"] = r; r += 1
    rotulo(ws, r, "Capital acumulado", 1, italic=True)
    preencher_linha(ws, r, lambda i, L: (
        f'={A["total"]and L}{A["total"]}' if i == 1 else f'={gcl(COL0+i-2)}{r}+{L}{A["total"]}'),
        BRL, color=CINZA, total=False)
    ws[f"B{r}"] = f'=B{A["total"]}'
    A["acum"] = r
    return ws, A
