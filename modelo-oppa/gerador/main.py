# -*- coding: utf-8 -*-
import sys, openpyxl
from openpyxl.styles import Alignment
from common import *
import premissas, bases, investimentos, engine, detalhe, resumo

OUT = sys.argv[1]

wb = openpyxl.Workbook()
wb.remove(wb.active)

_, P = premissas.build(wb)
_, T = bases.build_tributos(wb, P)
_, A = bases.build_aportes(wb, P)
_, I = investimentos.build(wb, P)
_, BLOCOS, NL = engine.build(wb, P, A, I, T)
_, U = detalhe.build_usuarios(wb, P, BLOCOS)
_, FAT = detalhe.build_faturamento(wb, P, BLOCOS)
_, FL = detalhe.build_fluxo(wb, P, A, I, BLOCOS)
_, D = detalhe.build_dre(wb, P, I, BLOCOS, FL)
_, R = resumo.build(wb, P, A, I, BLOCOS, FL, U)

# ordem final das abas
ordem = ["Resumo", "Premissas", "DRE Projetada", "Análise Fluxo", "Faturamento",
         "Usuários", "Cenários", "Investimentos", "Aportes", "Tributos"]
wb._sheets = [wb[n] for n in ordem]

# cor das guias
cores = {"Resumo": "1F3864", "Premissas": "FFC000", "DRE Projetada": "1F7040",
         "Análise Fluxo": "1F7040", "Faturamento": "2E5C8A", "Usuários": "2E5C8A",
         "Cenários": "7030A0", "Investimentos": "808080", "Aportes": "808080",
         "Tributos": "808080"}
for n, c in cores.items():
    wb[n].sheet_properties.tabColor = c

wb.active = 0
wb.save(OUT)
print("salvo:", OUT)
import json
print(json.dumps({"P_len": len(P), "blocos": BLOCOS, "linhas_bloco": NL}, ensure_ascii=False))
