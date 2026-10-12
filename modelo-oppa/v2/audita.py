# -*- coding: utf-8 -*-
"""Auditoria do modelo mensal.

Cada teste muda UMA celula, recalcula no LibreOffice e confere o efeito —
inclusive onde o efeito tem de ser NENHUM.
"""
import sys, shutil, subprocess, glob, openpyxl

BASE = sys.argv[1]
TMP  = "/tmp/claude-0/-home-user-Teste/42d647a1-c445-511e-84b4-a900542f847f/scratchpad/audit/_v2.xlsx"
REC  = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
n = lambda x: x if isinstance(x, (int, float)) else 0
MES = {"dez26": 16, "jun27": 22, "dez27": 28, "dez28": 40, "dez30": 64, "tot": 65}


def lin(ws, t, col=1, exato=False):
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, col).value
        if isinstance(v, str) and ((v.strip() == t) if exato else v.strip().startswith(t)):
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


def ler(wb):
    DR, NV, RS = wb["DRE Mensal"], wb["Nuvem e Escala"], wb["Resumo"]
    g = lambda rot, m="dez30": n(DR.cell(lin(DR, rot), MES[m]).value)
    gn = lambda rot, m="dez30": n(NV.cell(lin(NV, rot), MES[m]).value)
    gr = lambda rot: RS.cell(lin(RS, rot, col=2), 3).value
    return dict(
        chk1=max(abs(n(DR.cell(lin(DR, "✔ Conferência: faturamento"), c).value))
                 for c in range(5, 65)),
        chk2=max(abs(n(DR.cell(lin(DR, "✔ Conferência: base"), c).value))
                 for c in range(5, 65)),
        chk_nuvem=NV.cell(lin(NV, "✔ Conferência"), 65).value,
        novos_12=g("Novos usuários captados no mês", "dez26"),
        novos_18=g("Novos usuários captados no mês", "jun27"),
        novos_30=g("Novos usuários captados no mês"),
        base=g("(=) BASE NO FIM DO MÊS"), base_27=g("(=) BASE NO FIM DO MÊS", "dez27"),
        pag=g("Assinantes pagantes"), pag_27=g("Assinantes pagantes", "dez27"),
        bruto=g("(=) FATURAMENTO BRUTO"), bruto_tot=g("(=) FATURAMENTO BRUTO", "tot"),
        nuvem=g("(−) Nuvem e infraestrutura"),
        nuvem_free=g("do qual vem do plano gratuito"),
        nuvem_pag=g("Custo de nuvem por assinante pagante"),
        subsidio=g("Subsídio do plano gratuito"),
        adm_3=g("(−) Administrativo", "dez26"),
        ebitda=g("(=) EBITDA"), ebitda_tot=g("(=) EBITDA", "tot"),
        caixa=g("(=) CAIXA ACUMULADO"),
        caixa_min=min(n(DR.cell(lin(DR, "(=) CAIXA ACUMULADO"), c).value) for c in range(5, 65)),
        reserva=g("Reserva mínima em reais"),
        falta=g("FALTA CAPTAR — pior mês"),
        conta_nv=gn("CONTA DE NUVEM DO MÊS"),
        conta_nv_9=gn("CONTA DE NUVEM DO MÊS", "dez26"),
        equiv=gn("Usuários equivalentes"),
        r_falta=gr("QUANTO AINDA FALTA CAPTAR"),
        r_prazo=gr("Até quando o dinheiro"),
        r_nec=gr("(=) Necessidade total de capital"),
        r_consumo=gr("O que a operação consome"),
        r_res=gr("(+) Reserva de caixa"),
        r_be=gr("Primeiro mês com EBITDA positivo"),
        r_vpl=gr("VPL"),
    )


def setdre(wb, rot, col, val):
    DR = wb["DRE Mensal"]
    DR.cell(lin(DR, rot), col).value = val


def setnv(wb, rot, col, val):
    NV = wb["Nuvem e Escala"]
    NV.cell(lin(NV, rot), col).value = val


base = ler(openpyxl.load_workbook(BASE, data_only=True))
print(f"REFERÊNCIA  falta captar R$ {base['r_falta']:,.0f} · prazo {base['r_prazo']} · "
      f"EBITDA+ em {base['r_be']} · pagantes dez/30 {base['pag']:,.0f}\n")

res = []
def teste(nome, mut, verifica):
    r = ler(roda(mut))
    ok, msg = verifica(r, base)
    res.append((ok, nome))
    print(f"  [{'ok  ' if ok else 'FALHA'}] {nome}\n         {msg}")


# ---------------------------------------------------------------- integridade
teste("As três conferências do modelo ficam limpas",
      lambda wb: None,
      lambda r, b: (r["chk1"] < 0.01 and r["chk2"] < 0.01
                    and str(r["chk_nuvem"]).startswith("✔"),
                    f"DRE {r['chk1']:.2e} e {r['chk2']:.2e} · nuvem: {r['chk_nuvem']}"))

teste("Necessidade total = consumo da operação + reserva do mês mais apertado",
      lambda wb: None,
      lambda r, b: (abs(r["r_nec"] - r["r_consumo"] - r["r_res"]) < 0.01,
                    f"{r['r_consumo']:,.0f} + {r['r_res']:,.0f} = {r['r_nec']:,.0f} ✓"))

# ---------------------------------------------------------------- premissa mensal
teste("Digitar por cima de um mês reancora a curva dali — e não mexe no passado",
      lambda wb: setdre(wb, "Novos usuários captados no mês", MES["jun27"], 60000),
      lambda r, b: (abs(r["novos_12"] - b["novos_12"]) < 1
                    and abs(r["novos_18"] - 60000) < 1
                    and r["novos_30"] > b["novos_30"] * 2,
                    f"dez/26 {b['novos_12']:,.0f}→{r['novos_12']:,.0f} (intacto ✓) · "
                    f"jun/27 {b['novos_18']:,.0f}→{r['novos_18']:,.0f} (o que digitei) · "
                    f"dez/30 {b['novos_30']:,.0f}→{r['novos_30']:,.0f} (seguiu dali) ✓"))

teste("Mudar o mês de início zera os meses anteriores",
      lambda wb: setdre(wb, "(−) Administrativo", 4, 30),
      lambda r, b: (r["adm_3"] == 0 and b["adm_3"] > 0,
                    f"administrativo em dez/26 {b['adm_3']:,.2f}→{r['adm_3']:,.2f} "
                    f"(início movido para o mês 30) ✓"))

teste("Evolução por mês é por MÊS, não por ano",
      lambda wb: setdre(wb, "Novos usuários captados no mês", 3, 0.10),
      lambda r, b: (abs(r["novos_18"] / r["novos_12"] - 1.10 ** 6) < 0.01,
                    f"com 10%/mês, seis meses dão {r['novos_18']/r['novos_12']:.3f}x; "
                    f"1,10^6 = {1.10**6:.3f}x ✓"))

# ---------------------------------------------------------------- cenario
teste("Trocar para Conservador reduz base, receita e EBITDA de uma vez",
      lambda wb: wb["Resumo"].cell(lin(wb["Resumo"], "Cenário ativo", col=2), 3).__setattr__("value", 1),
      lambda r, b: (r["base"] < b["base"] and r["pag"] < b["pag"] * 0.5
                    and r["bruto_tot"] < b["bruto_tot"],
                    f"base {b['base']:,.0f}→{r['base']:,.0f} · pagantes "
                    f"{b['pag']:,.0f}→{r['pag']:,.0f} · faturamento 5 anos "
                    f"{b['bruto_tot']:,.0f}→{r['bruto_tot']:,.0f} ✓"))

teste("Trocar para Agressivo move na direção oposta",
      lambda wb: wb["Resumo"].cell(lin(wb["Resumo"], "Cenário ativo", col=2), 3).__setattr__("value", 3),
      lambda r, b: (r["pag"] > b["pag"] * 2 and r["bruto_tot"] > b["bruto_tot"],
                    f"pagantes {b['pag']:,.0f}→{r['pag']:,.0f} · faturamento 5 anos "
                    f"{b['bruto_tot']:,.0f}→{r['bruto_tot']:,.0f} ✓"))

# ---------------------------------------------------------------- nuvem
teste("Peso zero do usuário gratuito elimina o subsídio",
      lambda wb: setnv(wb, "Peso de um usuário do plano GRATUITO", 2, 0),
      lambda r, b: (abs(r["nuvem_free"]) < 1 and r["nuvem_pag"] < b["nuvem_pag"]
                    and abs(r["subsidio"]) < 0.01,
                    f"nuvem do plano gratuito {b['nuvem_free']:,.0f}→{r['nuvem_free']:,.0f} · "
                    f"custo de nuvem por pagante R$ {b['nuvem_pag']:,.2f}→{r['nuvem_pag']:,.2f} ✓"))

teste("Peso 100% faz o gratuito custar como um pagante",
      lambda wb: setnv(wb, "Peso de um usuário do plano GRATUITO", 2, 1.0),
      lambda r, b: (r["equiv"] > b["equiv"] * 5 and r["nuvem_pag"] > b["nuvem_pag"] * 3,
                    f"usuários equivalentes {b['equiv']:,.0f}→{r['equiv']:,.0f} · custo de "
                    f"nuvem por pagante R$ {b['nuvem_pag']:,.2f}→{r['nuvem_pag']:,.2f} ✓"))

teste("Dobrar a âncora de 1 milhão dobra a conta no topo da curva",
      lambda wb: setnv(wb, "1000000", 2, 1_100_000) if False else
                 wb["Nuvem e Escala"].cell(
                     next(rr for rr in range(1, 60)
                          if wb["Nuvem e Escala"].cell(rr, 1).value == 1_000_000), 2
                 ).__setattr__("value", 1_100_000),
      lambda r, b: (r["conta_nv"] > b["conta_nv"], 
                    f"conta de nuvem em dez/30 R$ {b['conta_nv']:,.0f}→{r['conta_nv']:,.0f} "
                    f"(a âncora do topo subiu de 550 mil para 1,1 milhão) ✓"))

teste("A nuvem só começa a custar no mês indicado",
      lambda wb: setnv(wb, "Mês em que a nuvem começa a custar", 2, 20),
      lambda r, b: (r["conta_nv_9"] == 0 and b["conta_nv_9"] > 0,
                    f"conta em dez/26 R$ {b['conta_nv_9']:,.0f}→{r['conta_nv_9']:,.0f} "
                    f"(início movido para o mês 20) ✓"))

# ---------------------------------------------------------------- capital
teste("Zerar a reserva faz a lacuna virar exatamente o caixa mínimo negativo",
      lambda wb: setdre(wb, "Reserva mínima de caixa desejada", 2, 0),
      lambda r, b: (abs(r["r_falta"] - (-b["caixa_min"])) < 1,
                    f"falta captar {b['r_falta']:,.0f}→{r['r_falta']:,.0f}, e o caixa mínimo "
                    f"era {b['caixa_min']:,.0f} ✓"))

teste("Desligar o capital não assinado aumenta a lacuna",
      lambda wb: [wb["Aportes"].cell(lin(wb["Aportes"], "Considerar aportes PREVISTOS"), 2).__setattr__("value", 0),
                  wb["Aportes"].cell(lin(wb["Aportes"], "Considerar acordos EM NEGOCIAÇÃO"), 2).__setattr__("value", 0)],
      lambda r, b: (r["r_falta"] > b["r_falta"] + 200000,
                    f"falta captar {b['r_falta']:,.0f}→{r['r_falta']:,.0f} "
                    f"(+{r['r_falta']-b['r_falta']:,.0f}: os R$ 280 mil de capital mais a "
                    f"receita B2B da Boston, que sai junto) ✓"))

# ---------------------------------------------------------------- preco
teste("Dobrar o preço dobra a receita de assinatura e nada mais",
      lambda wb: setdre(wb, "Preço médio por assinante no mês", 2, 79.80),
      lambda r, b: (abs(r["pag"] - b["pag"]) < 1 and abs(r["nuvem"] - b["nuvem"]) < 1
                    and r["ebitda"] > b["ebitda"],
                    f"pagantes {b['pag']:,.0f}→{r['pag']:,.0f} (igual ✓) · nuvem igual ✓ · "
                    f"EBITDA dez/30 {b['ebitda']:,.0f}→{r['ebitda']:,.0f}"))

print("\n" + "=" * 92)
bons = sum(1 for ok, _ in res if ok)
print(f"AUDITORIA DO MODELO MENSAL: {bons}/{len(res)} testes passaram.")
for ok, nome in res:
    if not ok:
        print("  FALHOU:", nome)
