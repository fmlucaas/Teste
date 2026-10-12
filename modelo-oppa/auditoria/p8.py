# -*- coding: utf-8 -*-
"""Auditoria 8 — a aba Preço.

Dez testes. Cada um muda UMA célula, recalcula a planilha inteira no LibreOffice
e confere o efeito, inclusive onde o efeito tem de ser NENHUM — invariante vale
tanto quanto resultado.
"""
import sys, shutil, subprocess, glob, openpyxl

BASE = sys.argv[1]
TMP  = "/tmp/claude-0/-home-user-Teste/42d647a1-c445-511e-84b4-a900542f847f/scratchpad/audit/_p8.xlsx"
REC  = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
n = lambda x: x if isinstance(x, (int, float)) else 0


def lin(ws, t, col=1, exato=False):
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, col).value
        if isinstance(v, str) and ((v.strip() == t) if exato else t in v):
            return r
    raise KeyError(f"{ws.title}: {t}")


def roda(mut):
    shutil.copy(BASE, TMP)
    wb = openpyxl.load_workbook(TMP)
    mut(wb)
    wb.save(TMP)
    o = subprocess.run(["python3", REC, TMP, "420"], capture_output=True, text=True)
    assert '"status": "success"' in o.stdout, o.stdout[:400]
    return openpyxl.load_workbook(TMP, data_only=True)


COL = {"lanc": 2, "m6": 3, "m12": 4, "fim": 5}


def ler(wb):
    PR, RS = wb["Preço"], wb["Resumo"]
    def g(rot, c="fim"):
        return n(PR.cell(lin(PR, rot), COL[c]).value)
    def t(rot, c="fim", exato=False):
        return PR.cell(lin(PR, rot, exato=exato), COL[c]).value
    return dict(
        chk_custo=max(abs(g("✔ Conferência do custo contra a DRE", c)) for c in COL),
        chk_nuvem=max(abs(g("✔ Conferência da nuvem", c)) for c in COL),
        pag=g("Assinantes pagantes"), pag12=g("Assinantes pagantes", "m12"),
        cvar=g("(=) CUSTO VARIÁVEL POR ASSINANTE"),
        cfix=g("(=) CUSTO FIXO DO MÊS"),
        cf_unit=g("Custo fixo dividido pelos assinantes"),
        ctot=g("(=) CUSTO TOTAL POR ASSINANTE"),
        nuvem=g("Nuvem — do próprio assinante"),
        rho=g("(=) FICA PARA A EMPRESA"),
        empata=g("Preço médio por assinante que apenas EMPATA"),
        p_sug=g("Preço médio por assinante COM a margem desejada"),
        fator=g("Fator do mix"),
        ess=g("Plano Essencial — preço necessário"),
        pre=g("Plano Premium — preço necessário"),
        fam=g("Plano Família — preço necessário"),
        ess_hoje=g("Plano Essencial — preço de hoje"),
        mult=g("Quantas vezes o preço de hoje"),
        sobra=g("(=) SOBRA POR ASSINANTE"),
        marg_teste=g("Margem EBITDA a esse preço"),
        nuv_emp=g("Nuvem por assinante que esse preço suporta — para empatar"),
        nuv_marg=g("Nuvem por assinante que esse preço suporta — com a margem"),
        ver=t("VEREDICTO"),
        mes12=t("Mês", "m12", exato=True),
        recon_fl=max(abs(n(wb["Análise Fluxo"].cell(
            lin(wb["Análise Fluxo"], "✔ Verificação"), c).value)) for c in range(2, 62)),
    )


def setp(wb, rot, val, cols=(3, 4, 5, 6, 7)):
    P = wb["Premissas"]
    r = lin(P, rot)
    for c in cols:
        P.cell(r, c).value = val


def setpb(wb, rot, val):
    P = wb["Premissas"]
    P.cell(lin(P, rot), 2).value = val


def setpr(wb, rot, val, col=2):
    PR = wb["Preço"]
    PR.cell(lin(PR, rot), col).value = val


base = ler(openpyxl.load_workbook(BASE, data_only=True))
print(f"REFERÊNCIA (dez/2030)  custo/assinante R$ {base['ctot']:,.2f} · "
      f"nuvem R$ {base['nuvem']:,.2f} · preço necessário R$ {base['ess']:,.2f} · "
      f"sobra a 39,90 R$ {base['sobra']:,.2f}\n")

res = []
def teste(nome, mut, verifica):
    r = ler(roda(mut))
    ok, msg = verifica(r, base)
    res.append((ok, nome))
    print(f"  [{'ok  ' if ok else 'FALHA'}] {nome}\n         {msg}")


teste("As duas conferências contra a DRE ficam zeradas nos quatro momentos",
      lambda wb: None,
      lambda r, b: (r["chk_custo"] < 0.01 and r["chk_nuvem"] < 0.01 and r["recon_fl"] < 0.01,
                    f"custo {r['chk_custo']:.2e} · nuvem {r['chk_nuvem']:.2e} · "
                    f"reconciliação do fluxo {r['recon_fl']:.2e}"))

teste("Custo total = variável + fixo rateado (identidade)",
      lambda wb: None,
      lambda r, b: (abs(r["ctot"] - r["cvar"] - r["cf_unit"]) < 0.005
                    and abs(r["cf_unit"] - r["cfix"] / r["pag"]) < 0.005,
                    f"{r['cvar']:,.2f} + {r['cf_unit']:,.2f} = {r['ctot']:,.2f}, e o fixo "
                    f"rateado é {r['cfix']:,.0f} ÷ {r['pag']:,.0f} ✓"))

teste("Cada R$ 1 de nuvem por assinante pede cerca de R$ 1,39 de preço",
      lambda wb: setp(wb, "Nuvem — custo variável por usuário PAGANTE", 32.90),
      lambda r, b: (abs((r["empata"] - b["empata"]) - 1 / b["rho"]) < 0.02,
                    f"+R$ 1,00 de nuvem → preço de equilíbrio {b['empata']:,.2f}→"
                    f"{r['empata']:,.2f} (+{r['empata']-b['empata']:,.2f}); "
                    f"1 ÷ {b['rho']:.1%} = {1/b['rho']:,.2f} ✓"))

teste("Pôr a nuvem no valor que a aba diz suportar zera a sobra a R$ 39,90",
      lambda wb: setp(wb, "Nuvem — custo variável por usuário PAGANTE", base["nuv_emp"]),
      lambda r, b: (abs(r["sobra"]) < 0.02,
                    f"nuvem = R$ {b['nuv_emp']:,.2f} → sobra R$ {r['sobra']:,.4f} "
                    f"(a conta ao contrário fecha) ✓"))

teste("Pôr a nuvem no valor com margem entrega exatamente a margem desejada",
      lambda wb: setp(wb, "Nuvem — custo variável por usuário PAGANTE", base["nuv_marg"]),
      lambda r, b: (abs(r["marg_teste"] - 0.20) < 0.001,
                    f"nuvem = R$ {b['nuv_marg']:,.2f} → margem {r['marg_teste']:.2%} "
                    f"(desejada 20%) ✓"))

teste("Margem desejada zero iguala o preço sugerido ao de equilíbrio",
      lambda wb: setpr(wb, "Margem EBITDA desejada", 0),
      lambda r, b: (abs(r["p_sug"] - r["empata"]) < 0.005,
                    f"sugerido {r['p_sug']:,.2f} = equilíbrio {r['empata']:,.2f} ✓"))

teste("Subir a comissão da loja derruba a retenção e sobe o preço necessário",
      lambda wb: setpb(wb, "Taxa das lojas de aplicativos", 0.30),
      lambda r, b: (r["rho"] < b["rho"] and r["ess"] > b["ess"],
                    f"retenção {b['rho']:.2%}→{r['rho']:.2%}, Essencial necessário "
                    f"R$ {b['ess']:,.2f}→{r['ess']:,.2f} ✓"))

teste("A ARPPU necessária vem do custo, não do preço digitado",
      lambda wb: setpb(wb, "Plano Essencial (R$/mês)", 49.90),
      lambda r, b: (abs(r["p_sug"] - b["p_sug"]) / b["p_sug"] < 0.03
                    and abs(r["ess"] * r["fator"] - r["p_sug"]) < 0.02
                    and r["mult"] > b["mult"],
                    f"ARPPU necessária {b['p_sug']:,.2f}→{r['p_sug']:,.2f} (praticamente igual; "
                    f"a sobra é o imposto, que muda de faixa) · o Essencial necessário cai para "
                    f"{r['ess']:,.2f} porque a RAZÃO entre os planos mudou: "
                    f"{r['ess']:,.2f} × {r['fator']:.3f} = {r['p_sug']:,.2f} ✓ · "
                    f"múltiplo {b['mult']:.2f}x→{r['mult']:.2f}x"))

teste("Trocar o mês de referência muda a coluna inteira",
      lambda wb: setpr(wb, "Mês nº na linha do tempo", 36, col=4),
      lambda r, b: (r["pag12"] != b["pag12"] and r["mes12"].year == 2028
                    and r["mes12"].month == 12,
                    f"coluna '+12 meses' passou a dez/2028: assinantes "
                    f"{b['pag12']:,.0f}→{r['pag12']:,.0f} ✓"))

teste("Os três planos mantêm a razão de preço entre si",
      lambda wb: None,
      lambda r, b: (abs(r["pre"] / r["ess"] - 89.9 / 79.9) < 0.001
                    and abs(r["fam"] / r["ess"] - 109.0 / 79.9) < 0.001,
                    f"Essencial {r['ess']:,.2f} · Premium {r['pre']:,.2f} "
                    f"({r['pre']/r['ess']:.3f}x) · Família {r['fam']:,.2f} "
                    f"({r['fam']/r['ess']:.3f}x) — mesma razão de Premissas ✓"))

teste("Com a nuvem em R$ 6,40 o veredicto do R$ 39,90 vira positivo",
      lambda wb: setp(wb, "Nuvem — custo variável por usuário PAGANTE", 6.40),
      lambda r, b: (str(r["ver"]).startswith("✓") and r["sobra"] > 0,
                    f"veredicto: {r['ver']} · margem {r['marg_teste']:.1%}"))

print("\n" + "=" * 92)
bons = sum(1 for ok, _ in res if ok)
print(f"AUDITORIA 8: {bons}/{len(res)} testes passaram.")
for ok, nome in res:
    if not ok:
        print("  FALHOU:", nome)
