# -*- coding: utf-8 -*-
"""Organiza as abas: ordem, cor, visibilidade e um mapa na primeira aba.

Treze abas sem hierarquia visual e sem porta de entrada viram labirinto. Aqui a
regra e: a cor da aba diz o que fazer com ela, a ordem segue o fluxo de trabalho
e a primeira aba e um mapa de uma tela.

  vermelho  comece aqui
  azul      leia o resultado
  amarelo   digite
  verde     o resultado em detalhe
  laranja   ajuste e acompanhamento posterior
  cinza     motor e apoio — ocultas
"""
from openpyxl.styles import Alignment
from comum import *

VERMELHO_T = "C00000"
AZUL_T     = "1F3864"
AMARELO_T  = "FFC000"
VERDE_T    = "1F7040"
LARANJA_T  = "ED7D31"
CINZA_T    = "A6A6A6"

# aba, cor, visivel, grupo, para que serve, voce digita?
PLANO = [
    ("Como usar",     VERMELHO_T, True,  "comece",  "O mapa. Esta tela.", "não"),
    ("Resumo",        AZUL_T,     True,  "leia",
     "Os três cenários lado a lado e o diagnóstico. É a aba para mostrar a um sócio ou "
     "investidor.", "não"),
    ("Preço",         AZUL_T,     True,  "leia",
     "De onde sai o valor da assinatura: nuvem, suporte, pessoas, marketing, administrativo, "
     "impostos, comissão da loja e margem. Tem um campo para testar um preço.", "só 3 campos"),
    ("Premissas",     AMARELO_T,  True,  "digite",
     "Todos os números do negócio: preços, conversão, churn, custos, tributação. É aqui que "
     "você passa a maior parte do tempo.", "SIM"),
    ("DRE Projetada", VERDE_T,    True,  "resultado",
     "O resultado mês a mês, de jan/2026 a dez/2030 — colunas B até BI. A soma por ano fica "
     "no rodapé, depois do detalhe mensal.", "não"),
    ("Análise Fluxo", VERDE_T,    True,  "resultado",
     "O caixa mês a mês, mais VPL, TIR e payback. Traz a linha de verificação que precisa "
     "ficar zerada.", "não"),
    ("Pessoas",       LARANJA_T,  True,  "ajuste",
     "O time, linha a linha, com data de entrada e de saída de cada pessoa.", "SIM"),
    ("Aportes",       LARANJA_T,  True,  "ajuste",
     "Todo o capital: quem aportou, quanto, quando e em que status.", "SIM"),
    ("Investimentos", LARANJA_T,  True,  "ajuste",
     "Cronograma de equipamentos, marca e certificações.", "SIM"),
    ("Sócios",        LARANJA_T,  True,  "ajuste",
     "Lucro distribuível e rateio por participação. Os percentuais ainda são provisórios.",
     "SIM"),
    ("Faturamento",   CINZA_T,    False, "motor",
     "A receita aberta por linha de negócio. Mesma informação da DRE, em outro corte.", "não"),
    ("Usuários",      CINZA_T,    False, "motor",
     "O funil de usuários e as métricas de unidade (CAC, LTV, churn).", "não"),
    ("Cenários",      CINZA_T,    False, "motor",
     "O motor. Os três cenários rodam aqui e todas as outras abas leem daqui. Nunca edite.",
     "não"),
    ("Tributos",      CINZA_T,    False, "motor",
     "As tabelas do Simples Nacional (Anexos III e V) e o Fator R.", "não"),
]

GRUPOS = [
    ("comece",    "COMECE AQUI",                        VERMELHO_T),
    ("leia",      "LEIA O RESULTADO",                   AZUL_T),
    ("digite",    "DIGITE AQUI",                        AMARELO_T),
    ("resultado", "O RESULTADO EM DETALHE",             VERDE_T),
    ("ajuste",    "AJUSTE E ACOMPANHAMENTO POSTERIOR",  LARANJA_T),
    ("motor",     "MOTOR E APOIO — ABAS OCULTAS",       CINZA_T),
]

BANNERS = {
    "Pessoas": "ABA DE AJUSTE  ·  o time muda; revise as datas de entrada e saída e o custo de "
               "cada pessoa sempre que houver contratação ou saída.",
    "Aportes": "ABA DE AJUSTE  ·  cada aporte tem um STATUS, e o status decide se ele entra no "
               "modelo. Realizado e Compromisso entram sempre; Previsto e Em negociação só com "
               "o interruptor ligado na seção 7 de Premissas.",
    "Investimentos": "ABA DE AJUSTE  ·  cronograma de desembolso. Investimento sai do caixa no "
                     "mês da data e é amortizado em 60 meses na DRE — não é despesa do mês.",
    "Sócios": "ABA DE AJUSTE  ·  os percentuais de participação ainda são provisórios. Troque-os "
              "e todo o rateio recalcula. Participação societária depende do valuation de cada "
              "rodada, não da proporção do capital aportado.",
}


def aplica(wb):
    # ---------- banners de acompanhamento ----------
    for aba, txt in BANNERS.items():
        ws = wb[aba]
        c = ws.cell(3, 1, "⚠  " + txt)
        c.font = f(9, True, "833C00")
        c.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        for cc in range(1, 11):
            ws.cell(3, cc).fill = FILL_ALERTA
        ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=10)
        ws.row_dimensions[3].height = 30

    # ---------- cor e visibilidade ----------
    for aba, cor, visivel, *_ in PLANO:
        if aba not in wb.sheetnames:
            continue
        ws = wb[aba]
        ws.sheet_properties.tabColor = cor
        ws.sheet_state = "visible" if visivel else "hidden"

    # ---------- ordem ----------
    ordem = [a for a, *_ in PLANO if a in wb.sheetnames]
    resto = [n for n in wb.sheetnames if n not in ordem]
    wb._sheets = [wb[n] for n in ordem + resto]
    wb.active = 0
    return wb


def mapa(wb):
    """Reescreve a aba Como usar como um mapa de uma tela."""
    if "Como usar" in wb.sheetnames:
        del wb["Como usar"]
    ws = wb.create_sheet("Como usar")
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (3, 20, 86, 16, 3)):
        ws.column_dimensions[col].width = w

    titulo(ws, "OPPA — O MAPA DA PLANILHA", largura=5)
    ws["A2"] = ("Catorze abas, mas você só precisa de quatro no dia a dia. A cor da aba diz o "
                "que fazer com ela.")
    ws["A2"].font = f(9, False, CINZA, italic=True)
    ws["A2"].alignment = Alignment(vertical="center", indent=1)
    r = 4

    # ---- o caminho curto ----
    ws.cell(r, 2, "O CAMINHO MAIS CURTO").font = f(11, True, AZUL_T)
    r += 1
    for n, txt in enumerate([
        "Abra o RESUMO e veja onde o negócio está nos três cenários.",
        "Abra PREÇO para entender de onde sai o valor da assinatura e testar um preço.",
        "Mude o que quiser em PREMISSAS. Tudo recalcula sozinho — não há nada para rodar.",
        "Volte ao RESUMO e compare.",
    ], start=1):
        c = ws.cell(r, 2, f"{n}.")
        c.font = f(10, True, PRETO)
        c.alignment = Alignment(horizontal="right")
        c2 = ws.cell(r, 3, txt)
        c2.font = f(10, False, PRETO)
        c2.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[r].height = 16
        r += 1
    r += 1

    # ---- as abas ----
    ws.cell(r, 2, "ABA").font = f(9, True, BRANCO)
    ws.cell(r, 3, "PARA QUE SERVE").font = f(9, True, BRANCO)
    ws.cell(r, 4, "VOCÊ DIGITA?").font = f(9, True, BRANCO)
    for c in range(2, 5):
        ws.cell(r, c).fill = FILL_HEADER
        ws.cell(r, c).alignment = Alignment(horizontal="center" if c == 4 else "left", indent=1)
    ws.row_dimensions[r].height = 18
    r += 1

    for chave, rotulo_g, cor in GRUPOS:
        c = ws.cell(r, 2, rotulo_g)
        c.font = f(9, True, BRANCO)
        fill = PatternFill("solid", fgColor=cor)
        for cc in range(2, 5):
            ws.cell(r, cc).fill = fill
        c.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[r].height = 16
        r += 1
        for aba, cor_aba, visivel, grupo, serve, digita in PLANO:
            if grupo != chave:
                continue
            c = ws.cell(r, 2, aba)
            c.font = f(10, True, cor_aba if cor_aba != CINZA_T else CINZA)
            c.alignment = Alignment(vertical="center", indent=1)
            c2 = ws.cell(r, 3, serve)
            c2.font = f(9, False, "262626")
            c2.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
            c3 = ws.cell(r, 4, digita)
            c3.font = f(9, digita == "SIM", VERMELHO if digita == "SIM" else CINZA)
            c3.alignment = Alignment(horizontal="center", vertical="center")
            for cc in range(2, 5):
                ws.cell(r, cc).border = BORDA
            ws.row_dimensions[r].height = max(16, 13 + 11 * (len(serve) // 95))
            r += 1
    r += 1

    def txt_livre(t, cor=CINZA, bold=False, titulo_=False):
        nonlocal r
        c = ws.cell(r, 2, t)
        c.font = f(11 if titulo_ else 9, bold or titulo_, cor, italic=not (bold or titulo_))
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.row_dimensions[r].height = 18 if titulo_ else max(15, 12 + 11 * (len(t) // 118))
        r += 1

    txt_livre("PARA VER UMA ABA OCULTA", AZUL_T, titulo_=True)
    txt_livre("Clique com o botão direito em qualquer aba na barra de baixo e escolha "
              "'Reexibir' (Excel) ou 'Mostrar planilha' (LibreOffice). Elas estão ocultas "
              "porque são o motor e o apoio — nada se perde, e nada ali precisa ser editado.")
    r += 1

    txt_livre("AS CORES DAS CÉLULAS", AZUL_T, titulo_=True)
    for cor, nome, desc in [
        (AZUL_INPUT, "Azul", "você digita — é uma premissa sua."),
        ("BF8F00", "Fundo amarelo", "premissa-chave: mexer nela desloca bastante o resultado."),
        (PRETO, "Preto", "fórmula calculada na própria aba. Não mexa."),
        (VERDE_LINK, "Verde", "valor que vem de outra aba. Mude na origem."),
    ]:
        c = ws.cell(r, 2, nome)
        c.font = f(10, True, cor)
        c.alignment = Alignment(vertical="center", indent=1)
        c2 = ws.cell(r, 3, desc)
        c2.font = f(9, False, "262626")
        c2.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[r].height = 15
        r += 1
    r += 1

    txt_livre("SE ALGUM NÚMERO PARECER ERRADO", VERMELHO, titulo_=True)
    for t in [
        "Na ANÁLISE FLUXO há uma linha de verificação que compara o detalhe com o motor. "
        "Ela tem de ficar zerada em todos os meses.",
        "Na aba PREÇO há duas linhas de conferência que comparam a decomposição de custo com "
        "a DRE. Também têm de ficar zeradas.",
        "Em PREMISSAS, a linha 'Verificação do mix' tem de somar 100% em todos os anos.",
        "Se alguma delas sair de zero, uma fórmula foi sobrescrita por um valor digitado. "
        "Desfaça a última edição ou peça o arquivo novo.",
    ]:
        txt_livre("•  " + t)

    ws.sheet_properties.tabColor = VERMELHO_T
    return ws
