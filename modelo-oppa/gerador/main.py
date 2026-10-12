# -*- coding: utf-8 -*-
import sys, openpyxl
from common import *
import premissas, bases, pessoas, investimentos, ajuste, engine, detalhe
import capital, preco, resumo, socios, comousar

OUT = sys.argv[1]

wb = openpyxl.Workbook()
wb.remove(wb.active)

_, P   = premissas.build(wb)
_, T   = bases.build_tributos(wb, P)
_, A   = bases.build_aportes(wb, P)
ws_pe, PE = pessoas.build(wb, P)
_, I   = investimentos.build(wb, P, PE)
_, AJ  = ajuste.build(wb, P)
_, BLOCOS, NL = engine.build(wb, P, A, I, T, PE)
_, U   = detalhe.build_usuarios(wb, P, BLOCOS, PE)
_, FAT = detalhe.build_faturamento(wb, P, BLOCOS)
_, FL  = detalhe.build_fluxo(wb, P, A, I, BLOCOS, PE)
_, D   = detalhe.build_dre(wb, P, I, BLOCOS, FL)
pessoas.add_fator_r(ws_pe, P, PE, FAT)
_, CAP, CAPR, CAPK = capital.build(wb, P, A, I, BLOCOS, FL, PE)
_, M, W, SPR = preco.build(wb, P, BLOCOS, FL, D)
_, SO  = socios.build(wb, P, A, FL, D, PE, BLOCOS)
_, R   = resumo.build(wb, P, A, I, BLOCOS, FL, U, CAPR, W, SPR)
comousar.build(wb, P, PE)

ordem = ["Como usar", "Resumo", "Necessidade de Capital", "Preço Mínimo", "Premissas",
         "Ajuste Mensal", "Pessoas", "Sócios", "DRE Projetada", "Análise Fluxo",
         "Faturamento", "Usuários", "Cenários", "Investimentos", "Aportes", "Tributos"]
wb._sheets = [wb[n] for n in ordem]

cores = {"Como usar": "C00000", "Resumo": "1F3864", "Premissas": "FFC000", "Pessoas": "FFC000",
         "Ajuste Mensal": "FFC000", "Necessidade de Capital": "1F3864", "Preço Mínimo": "1F3864",
         "DRE Projetada": "1F7040", "Análise Fluxo": "1F7040", "Faturamento": "2E5C8A",
         "Usuários": "2E5C8A", "Sócios": "1F3864", "Cenários": "7030A0", "Investimentos": "808080",
         "Aportes": "808080", "Tributos": "808080"}
for n, c in cores.items():
    wb[n].sheet_properties.tabColor = c

wb.active = 0
wb.save(OUT)
print("salvo:", OUT)
