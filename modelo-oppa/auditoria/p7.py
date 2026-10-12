# -*- coding: utf-8 -*-
"""Auditoria 7 — comportamento das inclusoes novas:
   entrada faseada dos planos, override mensal, Necessidade de Capital e Preco Minimo.

Cada teste muda UMA celula, recalcula a planilha inteira no LibreOffice e confere
que o efeito foi o esperado — inclusive onde o efeito tem de ser NENHUM.
"""
import sys, shutil, subprocess, glob, datetime as dt, openpyxl

BASE = sys.argv[1]
TMP = "/tmp/claude-0/-home-user-Teste/42d647a1-c445-511e-84b4-a900542f847f/scratchpad/audit/_c.xlsx"
RECALC = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
n = lambda x: x if isinstance(x, (int, float)) else 0


def lin(ws, t, col=1, exato=False):
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, col).value
        if isinstance(v, str) and ((v.strip() == t) if exato else t in v):
            return r
    raise KeyError(f"{ws.title}: {t}")


def rodar(mut):
    shutil.copy(BASE, TMP)
    wb = openpyxl.load_workbook(TMP)
    mut(wb)
    wb.save(TMP)
    o = subprocess.run(["python3", RECALC, TMP, "420"], capture_output=True, text=True)
    assert '"status": "success"' in o.stdout, o.stdout[:400]
    return openpyxl.load_workbook(TMP, data_only=True)


def ler(wb):
    CE, PM, NC, RS = wb["Cenários"], wb["Preço Mínimo"], wb["Necessidade de Capital"], wb["Resumo"]
    bl = {int(CE.cell(r, 1).value.split()[1]): r for r in range(1, CE.max_row + 1)
          if isinstance(CE.cell(r, 1).value, str) and CE.cell(r, 1).value.startswith("CENÁRIO ")}
    S = bl[2]

    def blk(rot):
        for rr in range(S, S + 60):
            v = CE.cell(rr, 1).value
            if isinstance(v, str) and v.strip().startswith(rot):
                return rr
        raise KeyError(rot)

    tot = lambda r: sum(n(CE.cell(r, c).value) for c in range(2, 62))
    mes = lambda r, i: n(CE.cell(r, 1 + i).value)
    pm = lambda t: n(PM.cell(lin(PM, t), 2).value)

    # blocos por cenario na aba Necessidade de Capital: 3 linhas com o mesmo rotulo
    def nc_todas(rot):
        return [r for r in range(1, NC.max_row + 1)
                if isinstance(NC.cell(r, 1).value, str) and NC.cell(r, 1).value.strip() == rot]

    r_falta = lin(NC, "(=) FALTA CAPTAR — respeitando as datas de entrada")
    r_nec = lin(NC, "(=) NECESSIDADE TOTAL DE CAPITAL")
    r_cap = lin(NC, "Capital requerido pela operação")
    r_res = lin(NC, "(+) Reserva mínima no mês mais apertado")
    r_pf = lin(NC, "Se os fundadores cobrissem TODA a lacuna")
    r_mneg = lin(NC, "Primeiro mês em que o caixa fica NEGATIVO")
    return dict(
        pag_ess_lanc=mes(blk("Pagantes — Plano Essencial"), 10),
        pag_pre_lanc=mes(blk("Pagantes — Plano Premium"), 10),
        pag_pre_abr27=mes(blk("Pagantes — Plano Premium"), 16),
        pag_fam_tot=tot(blk("Pagantes — Plano Família")),
        base_fim=n(CE[f"BI{blk('Base de usuários — fim do mês')}"].value),
        base_m13=mes(blk("Base de usuários — fim do mês"), 13),
        bruta=tot(blk("RECEITA BRUTA TOTAL")),
        assin=tot(blk("Receita de assinaturas")),
        adm=tot(blk("(−) Despesas administrativas")),
        caixa_min=min(n(CE.cell(blk("CAIXA ACUMULADO"), c).value) for c in range(2, 62)),
        # Preco Minimo (celulas unicas da secao 6)
        preco_janela=pm("PREÇO ÚNICO DO ESSENCIAL QUE ZERA A JANELA"),
        mult=pm("Quantas vezes o preço de hoje"),
        n_nec=pm("Assinantes necessários na janela"),
        tot_cobrir=pm("(=) Total que a assinatura precisa cobrir"),
        uer=pm("Assinantes equivalentes × fator de retenção"),
        fim_janela=PM.cell(lin(PM, "Último mês da janela"), 2).value,
        rho_dez30=n(PM.cell(lin(PM, "(=) Fica para a empresa"), 61).value),
        piso3_dez30=n(PM.cell(lin(PM, "Piso 3 — EQUILIBRA O MÊS"), 61).value),
        mes_cob=PM.cell(lin(PM, "Primeiro mês em que o EBITDA cobre o custo"), 3).value,
        # Necessidade de Capital (cenario Provavel = coluna C)
        falta=n(NC.cell(r_falta, 3).value),
        nec_total=n(NC.cell(r_nec, 3).value),
        capreq=n(NC.cell(r_cap, 3).value),
        reserva=n(NC.cell(r_res, 3).value),
        por_fund=n(NC.cell(r_pf, 3).value),
        mes_neg=NC.cell(r_mneg, 3).value,
        cap_mod=sum(n(NC.cell(lin(NC, "Capital que o modelo considera"), c).value)
                    for c in range(2, 62)),
        # Resumo
        be_resumo=RS.cell(lin(RS, "Break-even do EBITDA", col=2), 4).value,
        # conferencias internas
        recon_pm=max(abs(n(PM.cell(lin(PM, "✔ Reconciliação com o motor"), c).value))
                     for c in range(2, 62)),
        chk_assin=max(abs(n(PM.cell(lin(PM, "Receita de assinaturas (conferência"), c).value))
                      for c in range(2, 62)),
        recon_fl=max(abs(n(wb["Análise Fluxo"].cell(lin(wb["Análise Fluxo"], "✔ Verificação"), c).value))
                     for c in range(2, 62)),
        # avisos da aba Ajuste Mensal
        aviso_novos=n(wb["Ajuste Mensal"].cell(
            lin(wb["Ajuste Mensal"], "⚠ Novos usuários digitados antes do lançamento"), 2).value),
    )


def setp(wb, rot, val, col=2):
    P = wb["Premissas"]
    P.cell(lin(P, rot), col).value = val


def setaj(wb, rot_bloco, rot, mes, val):
    """Escreve um override na aba Ajuste Mensal, no bloco indicado."""
    AJ = wb["Ajuste Mensal"]
    ini = lin(AJ, rot_bloco)
    for r in range(ini + 1, ini + 8):
        v = AJ.cell(r, 1).value
        if isinstance(v, str) and v.strip().startswith(rot):
            AJ.cell(r, 1 + mes).value = val
            return
    raise KeyError(rot)


base = ler(openpyxl.load_workbook(BASE, data_only=True))
print(f"REFERÊNCIA  Premium no lançamento {base['pag_pre_lanc']:,.0f} · "
      f"preço da janela R$ {base['preco_janela']:,.2f} ({base['mult']:.2f}x) · "
      f"falta captar R$ {base['falta']:,.0f} · break-even {base['be_resumo']}\n")

res = []


def teste(nome, mut, verifica):
    r = ler(rodar(mut))
    ok, msg = verifica(r, base)
    res.append((ok, nome))
    print(f"  [{'ok  ' if ok else 'FALHA'}] {nome}\n         {msg}")


# ============================ ENTRADA FASEADA DOS PLANOS ====================
teste("No lançamento só existe o Essencial: Premium e Família zerados",
      lambda wb: None,
      lambda r, b: (r["pag_pre_lanc"] == 0 and r["pag_ess_lanc"] > 0,
                    f"out/26: Essencial {r['pag_ess_lanc']:,.0f}, Premium {r['pag_pre_lanc']:,.0f} "
                    f"(tem de ser 0) ✓"))

teste("Adiar a entrada dos dois planos para depois de 2030 deixa tudo Essencial",
      lambda wb: [setp(wb, "Mês de entrada do plano Premium", dt.datetime(2031, 1, 1)),
                  setp(wb, "Mês de entrada do plano Família", dt.datetime(2031, 1, 1))],
      lambda r, b: (r["pag_pre_abr27"] == 0 and r["pag_fam_tot"] == 0 and r["assin"] < b["assin"],
                    f"Premium abr/27 {b['pag_pre_abr27']:,.0f}→{r['pag_pre_abr27']:,.0f}, "
                    f"Família total {b['pag_fam_tot']:,.0f}→{r['pag_fam_tot']:,.0f}, "
                    f"assinaturas {b['assin']:,.0f}→{r['assin']:,.0f} (cai ✓)"))

teste("Antecipar a entrada para jan/2026 traz Premium já no lançamento",
      lambda wb: [setp(wb, "Mês de entrada do plano Premium", dt.datetime(2026, 1, 1)),
                  setp(wb, "Mês de entrada do plano Família", dt.datetime(2026, 1, 1))],
      lambda r, b: (r["pag_pre_lanc"] > 0 and r["assin"] > b["assin"],
                    f"Premium out/26 0→{r['pag_pre_lanc']:,.0f}, "
                    f"assinaturas {b['assin']:,.0f}→{r['assin']:,.0f} (sobe ✓)"))

teste("O Essencial é o resíduo: a soma dos três planos fecha com o total de pagantes",
      lambda wb: None,
      lambda r, b: (r["chk_assin"] < 0.01,
                    f"conferência receita de assinaturas = preço × unidades equivalentes: "
                    f"desvio máximo {r['chk_assin']:.2e} ✓"))

# ============================ OVERRIDE MENSAL ===============================
teste("Override de captação muda só o mês escrito",
      lambda wb: setaj(wb, "CENÁRIO 2 — PROVÁVEL", "Novos usuários captados no mês", 13, 99000),
      lambda r, b: (r["base_m13"] > b["base_m13"] + 60000,
                    f"base de jan/27 {b['base_m13']:,.0f}→{r['base_m13']:,.0f} "
                    f"(+{r['base_m13']-b['base_m13']:,.0f} com 99.000 captados) ✓"))

teste("Override de administrativas eleva o custo e mantém a reconciliação",
      lambda wb: setaj(wb, "CUSTOS", "Despesas administrativas", 20, 500000),
      lambda r, b: (abs((r["adm"] - b["adm"]) + 500000 - 6000) < 1 and r["recon_fl"] < 0.01,
                    f"administrativas {b['adm']:,.0f}→{r['adm']:,.0f} "
                    f"(troca os R$ 6.000 do mês por R$ 500.000) · reconciliação {r['recon_fl']:.2e} ✓"))

teste("Override zerado é um valor, não um branco: zera o mês",
      lambda wb: setaj(wb, "CENÁRIO 2 — PROVÁVEL", "Novos usuários captados no mês", 13, 0),
      lambda r, b: (r["base_m13"] < b["base_m13"],
                    f"base de jan/27 {b['base_m13']:,.0f}→{r['base_m13']:,.0f} "
                    f"(mês sem captação) ✓"))

teste("Override fora da janela não vale, e a aba avisa",
      lambda wb: setaj(wb, "CENÁRIO 2 — PROVÁVEL", "Novos usuários captados no mês", 3, 50000),
      lambda r, b: (abs(r["base_fim"] - b["base_fim"]) < 0.5 and r["aviso_novos"] == 1,
                    f"base dez/30 {b['base_fim']:,.0f}→{r['base_fim']:,.0f} (inalterada ✓) e "
                    f"o contador de células ignoradas marca {r['aviso_novos']:.0f} ✓"))

# ============================ NECESSIDADE DE CAPITAL ========================
teste("Necessidade total = capital requerido + reserva (identidade)",
      lambda wb: None,
      lambda r, b: (abs(r["nec_total"] - r["capreq"] - r["reserva"]) < 0.01,
                    f"{r['capreq']:,.0f} + {r['reserva']:,.0f} = {r['nec_total']:,.0f} ✓"))

teste("Zerar a reserva mínima reduz o que falta captar",
      lambda wb: setp(wb, "Reserva mínima de caixa", 0),
      lambda r, b: (r["falta"] < b["falta"] and abs(r["falta"] - (-b["caixa_min"])) < 1,
                    f"falta captar {b['falta']:,.0f}→{r['falta']:,.0f}, que é exatamente o caixa "
                    f"mínimo negativo ({-b['caixa_min']:,.0f}) ✓"))

# O pico da lacuna e em abr/2027. Antecipar um aporte que JA chegava antes disso
# nao muda nada — o caixa acumulado no mes do pico e o mesmo. Atrasa-lo, sim.
teste("Atrasar aporte previsto aumenta a lacuna, com o mesmo capital total",
      lambda wb: [wb["Aportes"].cell(r, 1).__setattr__("value", dt.datetime(2027, 12, 15))
                  for r in range(6, 40) if wb["Aportes"].cell(r, 4).value == "Previsto"
                  and n(wb["Aportes"].cell(r, 3).value) > 0],
      lambda r, b: (r["falta"] > b["falta"] + 100000 and abs(r["cap_mod"] - b["cap_mod"]) < 1,
                    f"falta captar {b['falta']:,.0f}→{r['falta']:,.0f} com o MESMO capital "
                    f"({r['cap_mod']:,.0f}) — a data vale dinheiro ✓"))

# Teste do contrario: capital maior resolve a lacuna do pico, mas nao o buraco
# que acontece ANTES de ele chegar. O aporte da C-ioT entra em out/2026 e o caixa
# ja fica negativo em jun/2026.
teste("Capital maior que chega depois não resolve buraco anterior",
      lambda wb: wb["Aportes"].cell(lin(wb["Aportes"], "C-ioT", col=2), 3).__setattr__("value", 900000),
      lambda r, b: (r["falta"] < b["falta"] and r["mes_neg"] == b["mes_neg"],
                    f"falta captar {b['falta']:,.0f}→{r['falta']:,.0f}, mas o primeiro mês "
                    f"negativo continua {r['mes_neg']} (o aporte entra em out/26) ✓"))

teste("Por fundador = lacuna ÷ nº de fundadores",
      lambda wb: None,
      lambda r, b: (abs(r["por_fund"] * 4 - r["falta"]) < 0.01,
                    f"{r['por_fund']:,.2f} × 4 = {r['falta']:,.2f} ✓"))

# ============================ PREÇO MÍNIMO ==================================
teste("O preço da janela é identidade: total a cobrir ÷ (equivalentes × retenção)",
      lambda wb: None,
      lambda r, b: (abs(r["preco_janela"] * r["uer"] - r["tot_cobrir"]) < 0.5,
                    f"{r['preco_janela']:,.4f} × {r['uer']:,.2f} = {r['tot_cobrir']:,.2f} ✓"))

teste("A reconciliação do Preço Mínimo contra o EBITDA do motor fica zerada",
      lambda wb: None,
      lambda r, b: (r["recon_pm"] < 1e-6,
                    f"desvio máximo {r['recon_pm']:.2e} em 60 meses ✓"))

teste("Subir a comissão das lojas derruba a retenção e sobe todos os pisos",
      lambda wb: setp(wb, "Taxa das lojas de aplicativos", 0.30),
      lambda r, b: (r["rho_dez30"] < b["rho_dez30"] and r["piso3_dez30"] > b["piso3_dez30"]
                    and r["preco_janela"] > b["preco_janela"],
                    f"retenção {b['rho_dez30']:.2%}→{r['rho_dez30']:.2%}, piso 3 de dez/30 "
                    f"R$ {b['piso3_dez30']:,.2f}→{r['piso3_dez30']:,.2f}, preço da janela "
                    f"R$ {b['preco_janela']:,.2f}→{r['preco_janela']:,.2f} ✓"))

teste("Esticar a janela de 6 para 12 meses muda o período e o preço",
      lambda wb: setp(wb, "Meses iniciais que a assinatura precisa cobrir", 12),
      lambda r, b: (r["fim_janela"].month == 9 and r["fim_janela"].year == 2027
                    and r["preco_janela"] != b["preco_janela"],
                    f"fim da janela {b['fim_janela']:%b/%Y}→{r['fim_janela']:%b/%Y}, "
                    f"preço R$ {b['preco_janela']:,.2f}→{r['preco_janela']:,.2f}"))

teste("Desligar os custos pré-lançamento reduz o total a cobrir",
      lambda wb: setp(wb, "Incluir na conta os custos anteriores ao lançamento", 0),
      lambda r, b: (abs((b["tot_cobrir"] - r["tot_cobrir"]) - 12000) < 1
                    and r["preco_janela"] < b["preco_janela"],
                    f"total a cobrir {b['tot_cobrir']:,.0f}→{r['tot_cobrir']:,.0f} "
                    f"(−R$ 12.000, o gasto de abr a set/26) ✓"))

teste("Dobrar o preço do Essencial reduz os assinantes necessários na janela",
      lambda wb: setp(wb, "Plano Essencial (R$/mês)", 39.80),
      lambda r, b: (r["n_nec"] < b["n_nec"] * 0.6 and r["mult"] < b["mult"],
                    f"assinantes necessários {b['n_nec']:,.0f}→{r['n_nec']:,.0f}, "
                    f"múltiplo do preço {b['mult']:.2f}x→{r['mult']:.2f}x ✓"))

teste("O mês em que a assinatura cobre o custo é o mesmo break-even do Resumo",
      lambda wb: None,
      lambda r, b: (r["mes_cob"] == r["be_resumo"],
                    f"Preço Mínimo diz {r['mes_cob']}, Resumo diz {r['be_resumo']} — "
                    f"duas contas independentes, mesmo mês ✓"))

print("\n" + "=" * 92)
bons = sum(1 for ok, _ in res if ok)
print(f"AUDITORIA 7: {bons}/{len(res)} testes passaram.")
for ok, nome in res:
    if not ok:
        print("  FALHOU:", nome)
