# -*- coding: utf-8 -*-
"""Auditoria da aba Sócios: confere a apuração da distribuição."""
import sys, openpyxl
ARQ = sys.argv[1]
V = openpyxl.load_workbook(ARQ, data_only=True)
n = lambda x: x if isinstance(x, (int, float)) else 0
S, D, AF, PE = V["Sócios"], V["DRE Projetada"], V["Análise Fluxo"], V["Pessoas"]
ach = []
def chk(c, o, d=""):
    if not c: ach.append((o, d))
def li(ws, t, col=1):
    for r in range(1, ws.max_row+1):
        v = ws.cell(r, col).value
        if isinstance(v, str) and t in v: return r
    raise KeyError(t)
R = {k: li(S, t) for k, t in [
    ("ll","Lucro líquido do exercício"), ("ll_ac","Lucro acumulado (compensa"),
    ("dist_ant","Distribuições já feitas"), ("ll_disp","Lucro ainda não distribuído"),
    ("caixa","Caixa em dezembro (antes"), ("caixa_dist","(−) Distribuições de anos"),
    ("res","(−) Reserva de caixa"), ("livre","Caixa livre"),
    ("distvel","LUCRO DISTRIBUÍVEL"), ("pct","% aplicado"), ("dist","DISTRIBUÍDO NO ANO"),
    ("dist_ac","Distribuições acumuladas"), ("prol","Pró-labore pago"),
    ("retido","Lucro retido na empresa")]}
C = [2,3,4,5,6]

# 1) lucro do ano bate com a DRE anual
hdrD = li(D, "Demonstração do Resultado")
ll_an = [r for r in range(hdrD, hdrD+20)
         if isinstance(D.cell(r,1).value,str) and "(=) LUCRO LÍQUIDO" in D.cell(r,1).value][0]
for j, c in enumerate(C):
    chk(abs(n(S.cell(R["ll"],c).value) - n(D.cell(ll_an,2+j).value)) < .01,
        f"lucro do ano {2026+j} x DRE")
# 2) acumulados encadeiam certo
ac = 0
for j, c in enumerate(C):
    ac += n(S.cell(R["ll"],c).value)
    chk(abs(n(S.cell(R["ll_ac"],c).value)-ac) < .01, f"lucro acumulado {2026+j}",
        f"{n(S.cell(R['ll_ac'],c).value):,.2f} vs {ac:,.2f}")
da = 0
for j, c in enumerate(C):
    da += n(S.cell(R["dist"],c).value)
    chk(abs(n(S.cell(R["dist_ac"],c).value)-da) < .01, f"distribuições acumuladas {2026+j}",
        f"{n(S.cell(R['dist_ac'],c).value):,.2f} vs {da:,.2f}")
# 3) dist_ant do ano = dist_ac do ano anterior
for j, c in enumerate(C):
    esp = 0 if j == 0 else n(S.cell(R["dist_ac"],c-1).value)
    chk(abs(n(S.cell(R["dist_ant"],c).value)-esp) < .01, f"distribuições anteriores {2026+j}",
        f"{n(S.cell(R['dist_ant'],c).value):,.2f} vs {esp:,.2f}")
# 4) cadeia da apuração
for j, c in enumerate(C):
    g = lambda k: n(S.cell(R[k], c).value)
    chk(abs(g("ll_disp") - max(0, g("ll_ac")-g("dist_ant"))) < .01, f"lucro não distribuído {2026+j}")
    chk(abs(g("caixa_dist") + g("dist_ant")) < .01, f"caixa menos distribuições {2026+j}")
    chk(abs(g("livre") - max(0, g("caixa")+g("caixa_dist")+g("res"))) < .01, f"caixa livre {2026+j}")
    chk(abs(g("distvel") - min(g("ll_disp"), g("livre"))) < .01, f"distribuível {2026+j}")
    chk(abs(g("dist") - g("distvel")*g("pct")) < .01, f"distribuído {2026+j}")
    chk(abs(g("retido") - (g("ll_ac")-g("dist_ac"))) < .01, f"lucro retido {2026+j}")
    chk(g("dist") <= g("livre")+.01, f"não distribui mais que o caixa livre {2026+j}")
    chk(g("dist_ac") <= max(0,g("ll_ac"))+.01, f"não distribui mais que o lucro {2026+j}")
# 5) caixa x Análise Fluxo
cx = li(AF, "CAIXA ACUMULADO")
lano = li(AF, "Ano")
for j, c in enumerate(C):
    col = [cc for cc in range(2,62) if AF.cell(lano,cc).value == 2026+j][-1]
    chk(abs(n(S.cell(R["caixa"],c).value)-n(AF.cell(cx,col).value)) < .01, f"caixa dez/{2026+j}")
# 6) pró-labore x Pessoas
soc = li(PE, "Pró-labore dos sócios (despesa)")
lanoP = li(PE, "Ano")
for j, c in enumerate(C):
    soma = sum(n(PE.cell(soc,cc).value) for cc in range(2,62) if PE.cell(lanoP,cc).value == 2026+j)
    chk(abs(n(S.cell(R["prol"],c).value)-soma) < .01, f"pró-labore {2026+j}")
# 7) rateio por sócio
q_ini = li(S, "Sócio") + 1
p_hdr = li(S, "Distribuição de lucros por sócio")   # não a sub-tabela "Total recebido"
tot_pct = 0.0
for r in range(q_ini, q_ini+14):
    if S.cell(r,1).value == "TOTAL": break          # não somar a linha de total
    tot_pct += n(S.cell(r,3).value)
chk(abs(tot_pct-1) < 1e-6, "participações somam 100%", f"{tot_pct:.6f}")
soma_por_socio = 0.0
for r in range(p_hdr+1, p_hdr+15):
    if not S.cell(r,7).value: break
    soma_por_socio += n(S.cell(r,7).value)
chk(abs(soma_por_socio-n(S.cell(R["dist"],7).value)) < .02,
    "soma por sócio x total distribuído", f"{soma_por_socio:,.2f} vs {n(S.cell(R['dist'],7).value):,.2f}")

print("="*80)
if ach:
    print(f"ABA SÓCIOS — {len(ach)} falha(s):")
    for o, d in ach: print(f"   {o:<44} {d}")
else:
    print("ABA SÓCIOS: apuração consistente, nenhuma falha.")
