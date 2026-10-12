# -*- coding: utf-8 -*-
"""Aplica os ajustes na planilha do usuario, preservando as edicoes dele.

   python3 aplica.py entrada.xlsx saida.xlsx

Nao regera nada: abre o arquivo, acrescenta a aba Preco, reescreve a aba Como
usar como mapa e reorganiza ordem, cor e visibilidade das abas.
"""
import sys, openpyxl
import preco_claro, reorganiza

ENT, SAI = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(ENT)
antes = list(wb.sheetnames)

preco_claro.build(wb)
reorganiza.mapa(wb)
reorganiza.aplica(wb)

wb.save(SAI)
visiveis = [n for n in wb.sheetnames if wb[n].sheet_state == "visible"]
ocultas = [n for n in wb.sheetnames if wb[n].sheet_state != "visible"]
print("abas antes :", len(antes))
print("abas agora :", len(wb.sheetnames))
print("visíveis   :", ", ".join(visiveis))
print("ocultas    :", ", ".join(ocultas))
print("salvo      :", SAI)
