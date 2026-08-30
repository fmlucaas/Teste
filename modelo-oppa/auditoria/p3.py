# -*- coding: utf-8 -*-
"""Auditoria 3 — valores derivados: DRE, blocos anuais, D&A, cap table, indicadores."""
import sys, openpyxl
from openpyxl.utils import get_column_letter as gcl
ARQ = sys.argv[1]
V = openpyxl.load_workbook(ARQ, data_only=True)
ach = []
def chk(cond, aba, o_que, detalhe=""):
    if not cond:
        ach.append((aba, o_que, detalhe))
    return cond
def n(x): return x if isinstance(x, (int, float)) else 0.0
def blocos(CE):
    """Descobre as linhas iniciais dos tres blocos de cenario na aba Cenarios."""
    m = {}
    for r in range(1, CE.max_row + 1):
        v = CE.cell(r, 1).value
        if isinstance(v, str) and v.startswith("CENÁRIO "):
            m[int(v.split()[1])] = r
    assert len(m) == 3, m
    return m


def lin(ws, txt, col=1, ult=False):
    hits = [r for r in range(1, ws.max_row+1)
            if isinstance(ws.cell(r,col).value, str) and txt in ws.cell(r,col).value]
    if not hits: raise KeyError(f"{ws.title}: {txt}")
    return hits[-1] if ult else hits[0]

D, F, U, AF, CE, PE, IN, AP, R, T = (V["DRE Projetada"], V["Faturamento"], V["Usuários"],
    V["Análise Fluxo"], V["Cenários"], V["Pessoas"], V["Investimentos"], V["Aportes"],
    V["Resumo"], V["Tributos"])
M = range(2, 62)

# ---------------------------------------------------------------- 1. DRE
print("1) DRE — identidades contábeis, mês a mês")
def dl(t, ult=False): return lin(D, t, ult=ult)
rb, rl = dl("(=) RECEITA BRUTA"), dl("(=) RECEITA OPERACIONAL LÍQUIDA")
imp, loj, pgt = dl("(−) Impostos sobre a receita"), dl("(−) Comissão das lojas"), dl("(−) Taxas de meios")
nuv, sup = dl("(−) Infraestrutura e nuvem"), dl("(−) Suporte ao cliente")
lb, eb = dl("(=) LUCRO BRUTO"), dl("(=) EBITDA")
pes, mkt, adm = dl("(−) Pessoal"), dl("(−) Marketing e aquisição"), dl("(−) Despesas administrativas")
da, ebit = dl("(−) Depreciação"), dl("(=) EBIT — resultado")
lair, ll = dl("(=) RESULTADO ANTES"), dl("(=) LUCRO LÍQUIDO")
ass = [dl("Assinaturas — Plano Essencial"), dl("Assinaturas — Plano Premium"),
       dl("Assinaturas — Plano Família"), dl("Marketplace — comissões"),
       dl("B2B — parcerias"), dl("B2B — venda de dados"), dl("B2B — outras iniciativas")]
for c in M:
    g = lambda r: n(D.cell(r, c).value)
    chk(abs(g(rb) - sum(g(x) for x in ass)) < .01, "DRE", f"receita bruta {gcl(c)}")
    chk(abs(g(rl) - (g(rb)+g(imp)+g(loj)+g(pgt))) < .01, "DRE", f"receita líquida {gcl(c)}")
    chk(abs(g(lb) - (g(rl)+g(nuv)+g(sup))) < .01, "DRE", f"lucro bruto {gcl(c)}")
    chk(abs(g(eb) - (g(lb)+g(pes)+g(mkt)+g(adm))) < .01, "DRE", f"EBITDA {gcl(c)}")
    chk(abs(g(ebit) - (g(eb)+g(da))) < .01, "DRE", f"EBIT {gcl(c)}")
    chk(abs(g(ll) - g(lair)) < .01, "DRE", f"lucro líquido {gcl(c)}")
print(f"   {len(ach)} falha(s)")

# ---------------------------------------------------------------- 2. anuais
print("2) Blocos anuais conferindo com a soma dos meses")
a0 = len(ach)
def confere_anual(ws, hdr_row, hdr_col, pares, nome):
    anos = [ws.cell(hdr_row, hdr_col+j).value for j in range(5)]
    lano = lin(ws, "Ano")
    for lbl, r_mensal, r_anual in pares:
        for j, ano in enumerate(anos):
            soma = sum(n(ws.cell(r_mensal, c).value) for c in M
                       if ws.cell(lano, c).value == ano)
            val = n(ws.cell(r_anual, hdr_col+j).value)
            chk(abs(val-soma) < .02, nome, f"{lbl} {ano}", f"anual {val:,.2f} vs meses {soma:,.2f}")
hdrD = lin(D, "Demonstração do Resultado")
pares = []
for lbl, rm in [("RECEITA BRUTA", rb), ("Impostos", imp), ("Comissão lojas", loj),
                ("Taxas pgto", pgt), ("RECEITA LÍQUIDA", rl), ("Nuvem", nuv), ("Suporte", sup),
                ("LUCRO BRUTO", lb), ("Pessoal", pes), ("Marketing", mkt), ("Administrativas", adm),
                ("EBITDA", eb), ("D&A", da), ("EBIT", ebit), ("LUCRO LÍQUIDO", ll)]:
    for rr in range(hdrD+1, hdrD+20):
        v = D.cell(rr,1).value
        alvo = lbl.lower().strip("(=)−  ")
        vv = v.lower().strip("(=)−  ") if isinstance(v,str) else ""
        if vv == alvo or (alvo not in ("ebit","ebitda") and alvo in vv):
            pares.append((lbl, rm, rr)); break
confere_anual(D, hdrD, 2, pares, "DRE anual")
hdrF = lin(F, "Ano", ult=True)
confere_anual(F, hdrF, 2, [("Receita bruta", lin(F,"RECEITA BRUTA TOTAL"), hdrF+1),
                           ("Receita líquida", lin(F,"RECEITA LÍQUIDA"), hdrF+2),
                           ("Impostos", lin(F,"(−) Impostos"), hdrF+3),
                           ("Comissão lojas", lin(F,"(−) Comissão"), hdrF+4)], "Faturamento anual")
print(f"   {len(ach)-a0} falha(s)")

# ---------------------------------------------------------------- 3. D&A
print("3) Investimentos — amortização e saldo contábil")
a0 = len(ach)
tot_i, da_i = lin(IN,"TOTAL DE INVESTIMENTOS"), lin(IN,"Depreciação e amortização do mês")
acum_i, sal_i = lin(IN,"Investimento acumulado"), lin(IN,"Saldo contábil")
vida = n(IN.cell(lin(IN,"Vida útil adotada"),2).value)
for k, c in enumerate(M, start=1):
    ac = sum(n(IN.cell(tot_i, cc).value) for cc in range(2, c+1))
    chk(abs(n(IN.cell(acum_i,c).value)-ac) < .01, "Investimentos", f"acumulado {gcl(c)}")
    esp = 0 if k == 1 else sum(n(IN.cell(tot_i,cc).value) for cc in range(2,c))/vida
    chk(abs(n(IN.cell(da_i,c).value)-esp) < .01, "Investimentos", f"D&A {gcl(c)}")
    ant = 0 if k == 1 else n(IN.cell(sal_i,c-1).value)
    chk(abs(n(IN.cell(sal_i,c).value)-(ant+n(IN.cell(tot_i,c).value)-n(IN.cell(da_i,c).value)))<.01,
        "Investimentos", f"saldo {gcl(c)}")
print(f"   {len(ach)-a0} falha(s)")

# ---------------------------------------------------------------- 4. cap table
print("4) Aportes — cap table, compromissos e resumo do capital")
a0 = len(ach)
cap_hdr = lin(AP,"Sócio / Investidor")
tot_cap = None
for r in range(cap_hdr+1, cap_hdr+20):
    if AP.cell(r,1).value == "TOTAL": tot_cap = r; break
soma_cap = sum(n(AP.cell(r,2).value) for r in range(cap_hdr+1, tot_cap))
chk(abs(n(AP.cell(tot_cap,2).value)-soma_cap) < .01, "Aportes", "total do cap table")
chk(abs(n(AP.cell(tot_cap,3).value)-1.0) < 1e-6 or soma_cap == 0,
    "Aportes", "proporções somam 100%", f"{n(AP.cell(tot_cap,3).value):.6f}")
cap_total = n(AP.cell(lin(AP,"CAPITAL TOTAL CONSIDERADO",col=2),3).value)
chk(abs(soma_cap-cap_total) < .01, "Aportes", "cap table x capital total",
    f"{soma_cap:,.2f} vs {cap_total:,.2f}")
dif = n(AP.cell(lin(AP,"Capital não atribuído"),2).value)
chk(abs(dif) < .01, "Aportes", "capital não atribuído deve ser zero", f"{dif:,.2f}")
tot_mes = lin(AP,"TOTAL DE APORTES NO MÊS")
chk(abs(sum(n(AP.cell(tot_mes,c).value) for c in M)-cap_total) < .01,
    "Aportes", "cronograma mensal x capital total")
meta = lin(AP,"Fundador",1)
for r in range(meta+1, meta+5):
    if not AP.cell(r,1).value: break
    chk(abs(n(AP.cell(r,5).value)-max(0,10000-n(AP.cell(r,3).value))) < .01,
        "Aportes", f"falta em 2026 — {AP.cell(r,1).value}")
    chk(abs(n(AP.cell(r,6).value)-max(0,n(AP.cell(r,2).value)-n(AP.cell(r,4).value))) < .01,
        "Aportes", f"falta total — {AP.cell(r,1).value}")
print(f"   {len(ach)-a0} falha(s)")

# ---------------------------------------------------------------- 5. indicadores
print("5) Resumo — VPL, TIR, payback, capital requerido, break-even")
a0 = len(ach)
tma_m = n(V["Premissas"].cell(lin(V["Premissas"],"TMA equivalente mensal"),2).value)
BL = blocos(CE)
_S0 = BL[1]
def off(rot):
    """Offset da linha dentro do bloco, localizada pelo rótulo."""
    for rr in range(_S0, min(_S0 + 60, CE.max_row) + 1):
        v = CE.cell(rr, 1).value
        if isinstance(v, str) and v.strip().startswith(rot):
            return rr - _S0
    raise KeyError(rot)
OF = {k: off(v) for k, v in {
    "bruta":"RECEITA BRUTA TOTAL", "ebitda":"EBITDA", "capex":"(−) Investimentos (CAPEX)",
    "fcl":"FLUXO DE CAIXA LIVRE", "fcld_ac":"FCL descontado acumulado",
    "fcl_ac":"FCL acumulado (nominal)", "caixa":"CAIXA ACUMULADO",
}.items()}
def rlin(t): return lin(R, t, col=2)
for k, S in BL.items():
    col = gcl(3+k-1)
    fcl = [n(CE.cell(S+OF['fcl'], c).value) for c in M]
    vpl_esp = sum(f/(1+tma_m)**(i+1) for i, f in enumerate(fcl))
    vpl_xl = n(R[f"{col}{rlin('VPL —')}"].value)
    chk(abs(vpl_xl-vpl_esp) < .5, "Resumo", f"VPL cenário {k}",
        f"{vpl_xl:,.2f} vs {vpl_esp:,.2f}")
    acum, negs = 0.0, []
    for i, f in enumerate(fcl, 1):
        acum += f
        if acum < 0: negs.append(i)
    pb = None if (negs and negs[-1] == len(fcl)) else ((max(negs)+1) if negs else 1)
    if pb is None: pb = "> 60"
    got = R[f"{col}{rlin('Payback simples')}"].value
    chk(pb == got, "Resumo", f"payback simples cenário {k}",
        f"esperado {pb}, obtido {got}")
    capreq = -min(n(CE.cell(S+OF['fcl_ac'], c).value) for c in M)
    chk(abs(n(R[f"{col}{rlin('Capital requerido')}"].value)-capreq) < .01,
        "Resumo", f"capital requerido cenário {k}")
    cmin = min(n(CE.cell(S+OF['caixa'], c).value) for c in M)
    chk(abs(n(R[f"{col}{rlin('Caixa mínimo')}"].value)-cmin) < .01,
        "Resumo", f"caixa mínimo cenário {k}")
    be = next((i for i, c in enumerate(M, 1) if n(CE.cell(S+OF['ebitda'], c).value) > 0), None)
    esp = "não atinge" if be is None else \
        ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"][(be-1)%12] + \
        "/" + str(2026+(be-1)//12)
    got = R[f"{col}{rlin('Break-even')}"].value
    chk(str(got) == esp, "Resumo", f"break-even cenário {k}", f"esperado {esp}, obtido {got}")
    rec_tot = sum(n(CE.cell(S+OF['bruta'], c).value) for c in M)
    chk(abs(n(R[f"{col}{rlin('Receita bruta acumulada')}"].value)-rec_tot) < .01,
        "Resumo", f"receita acumulada cenário {k}")
print(f"   {len(ach)-a0} falha(s)")

# ---------------------------------------------------------------- 6. usuarios
print("6) Usuários — métricas de unidade")
a0 = len(ach)
ul = lambda t: lin(U, t)
for c in M:
    pag = n(U.cell(ul("Usuários pagantes"), c).value)
    base = n(U.cell(ul("Base de usuários — fim"), c).value)
    chk(abs(n(U.cell(ul("Usuários gratuitos"),c).value)-(base-pag)) < .01, "Usuários", f"gratuitos {gcl(c)}")
    if pag:
        mc = n(U.cell(ul("Margem de contribuição"),c).value)
        ltv = n(U.cell(ul("LTV —"),c).value)
        cacp = n(U.cell(ul("CAC por usuário PAGANTE"),c).value)
        if cacp:
            chk(abs(n(U.cell(ul("LTV ÷ CAC"),c).value)-ltv/cacp) < 1e-6, "Usuários", f"LTV/CAC {gcl(c)}")
        if mc:
            chk(abs(n(U.cell(ul("Payback do CAC"),c).value)-cacp/mc) < 1e-6, "Usuários", f"payback CAC {gcl(c)}")
print(f"   {len(ach)-a0} falha(s)")

# ---------------------------------------------------------------- 7. tributos / fator R
print("7) Tributos e Fator R")
a0 = len(ach)
a3 = lin(T,"ANEXO III"); a5 = lin(T,"ANEXO V")
cmp0 = lin(T,"RBT12",1) if False else None
for r in range(1, T.max_row+1):
    rbt = T.cell(r,1).value
    if isinstance(rbt,(int,float)) and rbt >= 180000 and isinstance(T.cell(r,5).value,(int,float)):
        def ef(tab):
            nom, ded = None, None
            for k in range(6):
                de = T.cell(tab+2+k,2).value
                if rbt >= de: nom, ded = T.cell(tab+2+k,4).value, T.cell(tab+2+k,5).value
            return (rbt*nom-ded)/rbt
        chk(abs(n(T.cell(r,2).value)-ef(a3)) < 1e-9, "Tributos", f"efetiva Anexo III em {rbt:,.0f}")
        chk(abs(n(T.cell(r,3).value)-ef(a5)) < 1e-9, "Tributos", f"efetiva Anexo V em {rbt:,.0f}")
        chk(abs(n(T.cell(r,5).value)-(n(T.cell(r,3).value)-n(T.cell(r,2).value))*rbt) < .01,
            "Tributos", f"custo da diferença em {rbt:,.0f}")
fr = lin(PE,"FATOR R  (folha")
folha = lin(PE,"Folha do Fator R")
rec = lin(PE,"Receita bruta do ano")
for j in range(5):
    c = 2+j
    rr = n(PE.cell(rec,c).value)
    esp = n(PE.cell(folha,c).value)/rr if rr else 0
    chk(abs(n(PE.cell(fr,c).value)-esp) < 1e-9, "Pessoas", f"Fator R coluna {gcl(c)}")
print(f"   {len(ach)-a0} falha(s)")

print("\n" + "="*92)
if not ach:
    print("AUDITORIA 3: nenhuma inconsistência.")
else:
    print(f"AUDITORIA 3 — {len(ach)} falha(s):\n")
    for aba, o, d in ach[:40]:
        print(f"  {aba:<20} {o:<44} {d}")
    if len(ach) > 40: print(f"  ... e mais {len(ach)-40}")
