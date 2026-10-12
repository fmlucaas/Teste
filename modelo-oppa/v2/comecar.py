# -*- coding: utf-8 -*-
"""Aba 'Começar aqui' — cinco abas, meia tela de explicacao."""
from openpyxl.styles import Alignment
from base import *

ABAS = [
 ("Resumo", "1F3864", "A resposta. Começa com quanto a empresa precisa de dinheiro. Troque o "
                      "cenário aqui: um número, e o modelo inteiro responde.", "cenário e TMA"),
 ("DRE Mensal", "1F7040", "O modelo. Uma coluna por mês, de jan/2026 a dez/2030. Dos drivers "
                          "ao EBITDA ao caixa, tudo em uma aba só.", "SIM — colunas B, C e D"),
 ("Nuvem e Escala", "7030A0", "A conta de nuvem. Você digita a conta mensal esperada em cada "
                              "tamanho de base; o custo por usuário sai dividido e cai com a "
                              "escala.", "SIM — coluna B"),
 ("Equipe", "ED7D31", "Uma linha por papel, com mês de entrada e de saída.", "SIM"),
 ("Aportes", "ED7D31", "Todo o capital, com o status de cada linha.", "SIM"),
]


def build(wb):
    ws = wb.create_sheet("Começar aqui")
    ws.sheet_view.showGridLines = False
    for c, w in zip("ABCDE", (3, 20, 88, 22, 3)):
        ws.column_dimensions[c].width = w
    titulo(ws, "OPPA — COMEÇAR AQUI")
    ws["A2"] = "Cinco abas. Você digita em três."
    ws["A2"].font = f(9, False, CINZA, italic=True)
    ws["A2"].alignment = Alignment(vertical="center", indent=1)
    r = 4

    def bloco(t):
        nonlocal r
        c = ws.cell(r, 2, t)
        c.font = f(11, True, "1F3864")
        r += 1

    def livre(t, cor=CINZA, bold=False):
        nonlocal r
        c = ws.cell(r, 2, t)
        c.font = f(9, bold, cor, italic=not bold)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.row_dimensions[r].height = 13 + 11 * (len(t) // 120 + 1)
        r += 1

    bloco("O QUE MUDOU EM RELAÇÃO À VERSÃO ANTERIOR")
    for t in ["Não existe mais premissa anual em lugar nenhum. Toda premissa é mensal: você dá "
              "o valor inicial, a evolução por mês e o mês em que a coisa começa.",
              "O custo de nuvem deixou de ser um número por usuário e passou a ser uma CONTA "
              "mensal que você ancora em alguns tamanhos de base. O custo por usuário é "
              "consequência, e cai com a escala.",
              "A DRE virou uma aba só, com os drivers dentro dela. Você não precisa mais ir e "
              "voltar entre abas para mudar uma premissa e ver o efeito.",
              "Treze abas viraram cinco."]:
        livre("•  " + t)
    r += 1

    bloco("AS CINCO ABAS")
    for j, t in enumerate(["ABA", "PARA QUE SERVE", "VOCÊ DIGITA?"]):
        c = ws.cell(r, 2 + j, t)
        c.font = f(9, True, BRANCO)
        c.fill = F_HDR
        c.alignment = Alignment(horizontal="center" if j == 2 else "left", indent=1)
    r += 1
    for nome, cor, serve, digita in ABAS:
        c = ws.cell(r, 2, nome)
        c.font = f(10, True, cor)
        c.alignment = Alignment(vertical="center", indent=1)
        c2 = ws.cell(r, 3, serve)
        c2.font = f(9, False, "262626")
        c2.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        c3 = ws.cell(r, 4, digita)
        c3.font = f(9, digita.startswith("SIM"), VERM if digita.startswith("SIM") else CINZA)
        c3.alignment = Alignment(horizontal="center", vertical="center")
        for cc in range(2, 5):
            ws.cell(r, cc).border = BORDA
        ws.row_dimensions[r].height = max(17, 13 + 11 * (len(serve) // 95))
        r += 1
    r += 1

    bloco("COMO FUNCIONA UMA LINHA DE PREMISSA, NA DRE MENSAL")
    for t in ["Coluna B — valor inicial: quanto vale no primeiro mês em que a coisa existe.",
              "Coluna C — evolução por mês: quanto cresce ou cai a cada mês. 3% é 3% ao mês, "
              "não ao ano.",
              "Coluna D — mês de início: 1 é jan/2026, 12 é dez/2026, 60 é dez/2030. Antes "
              "disso a linha vale zero.",
              "E o mais útil: digite um número POR CIMA de qualquer mês e a curva passa a "
              "contar dali. Cada mês lê o mês anterior, então mexer em março muda abril até "
              "dezembro de 2030 — e não mexe em janeiro e fevereiro."]:
        livre("•  " + t)
    r += 1

    bloco("AS CORES DAS CÉLULAS")
    for cor, nome, desc in [
        (AZUL, "Azul com fundo creme", "você digita."),
        (AZUL, "Azul com fundo amarelo", "você digita, e esta mexe muito no resultado."),
        (PRETO, "Preto", "calculado na própria aba."),
        (VERDE, "Verde", "vem de outra aba. Mude na origem."),
    ]:
        c = ws.cell(r, 2, nome)
        c.font = f(10, True, cor)
        c.alignment = Alignment(vertical="center", indent=1)
        c2 = ws.cell(r, 3, desc)
        c2.font = f(9, False, "262626")
        c2.alignment = Alignment(vertical="center", indent=1)
        r += 1
    r += 1

    bloco("SE ALGUM NÚMERO PARECER ERRADO")
    livre("O Resumo tem um bloco de conferências no fim. As duas primeiras linhas têm de ser "
          "zero e a terceira tem de dizer 'monotônica'. Se saírem disso, alguma fórmula foi "
          "sobrescrita por um valor digitado — desfaça a última edição.")
    livre("A DRE Mensal traz as mesmas conferências na seção 7, mês a mês, para você achar em "
          "qual mês o problema está.")

    ws.sheet_properties.tabColor = "C00000"
    return ws
