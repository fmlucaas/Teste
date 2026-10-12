# -*- coding: utf-8 -*-
"""Monta o modelo mensal da Oppa.

    python3 main.py saida.xlsx

Ordem importa: Nuvem precisa existir antes da DRE para a DRE referenciar a
conta, e a DRE precisa existir antes de Nuvem.liga() fechar o circuito da base
de usuarios.
"""
import sys, openpyxl
import nuvem, quadros, dre, resumo, comecar

OUT = sys.argv[1]
wb = openpyxl.Workbook()
wb.remove(wb.active)

ws_res, CTRL = resumo.controles(wb)
ws_nu, NU    = nuvem.build(wb)
_, E         = quadros.equipe(wb)
_, A         = quadros.aportes(wb)
_, D         = dre.build(wb, CTRL, E, A, NU)
nuvem.liga(ws_nu, NU, D)
R            = resumo.painel(ws_res, CTRL, D, A, NU)
comecar.build(wb)

ordem = ["Começar aqui", "Resumo", "DRE Mensal", "Nuvem e Escala", "Equipe", "Aportes"]
wb._sheets = [wb[n] for n in ordem]
wb.active = 0
wb.save(OUT)
print("salvo:", OUT, "·", len(wb.sheetnames), "abas")
