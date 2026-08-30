# -*- coding: utf-8 -*-
"""Auditoria 4 — comportamento: muda premissa, recalcula, confere a reacao."""
import sys, shutil, subprocess, glob, openpyxl
BASE = sys.argv[1]
TMP = "/tmp/claude-0/-home-user-Teste/42d647a1-c445-511e-84b4-a900542f847f/scratchpad/audit/_t.xlsx"
RECALC = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
n = lambda x: x if isinstance(x, (int, float)) else 0

def lin(ws, txt, col=1):
    for r in range(1, ws.max_row+1):
        v = ws.cell(r, col).value
        if isinstance(v, str) and txt in v: return r
    raise KeyError(txt)

def rodar(mut):
    shutil.copy(BASE, TMP)
    wb = openpyxl.load_workbook(TMP)
    mut(wb)
    wb.save(TMP)
    out = subprocess.run(["python3", RECALC, TMP, "420"], capture_output=True, text=True)
    assert '"status": "success"' in out.stdout, out.stdout[:400]
    return openpyxl.load_workbook(TMP, data_only=True)

def ler(wb):
    R, CE, U, PE, AP = wb["Resumo"], wb["Cenários"], wb["Usuários"], wb["Pessoas"], wb["Aportes"]
    bl = {int(CE.cell(r,1).value.split()[1]): r for r in range(1, CE.max_row+1)
          if isinstance(CE.cell(r,1).value, str) and CE.cell(r,1).value.startswith("CENÁRIO ")}
    rl = lambda t: lin(R, t, col=2)
    return dict(
        base30=n(U["BI"+str(lin(U,"Base de usuários — fim"))].value),
        rec26=n(R["D"+str(rl("Receita bruta de 2026"))].value),
        rec_tot=n(R["D"+str(rl("Receita bruta acumulada"))].value),
        vpl=n(R["D"+str(rl("VPL —"))].value),
        capital=n(AP["C"+str(lin(AP,"CAPITAL TOTAL CONSIDERADO",col=2))].value),
        pessoal30=n(PE["BI"+str(lin(PE,"TOTAL DE PESSOAL"))].value),
        b2b=n(CE["BJ"+str(bl[2]+15)].value),
        recon=max(abs(n(wb["Análise Fluxo"].cell(lin(wb["Análise Fluxo"],"✔ Verificação"), c).value))
                  for c in range(2,62)),
        # estas seguem o CENÁRIO ATIVO (o Resumo mostra sempre os três lado a lado)
        rec_ativo=n(wb["Faturamento"]["BJ"+str(lin(wb["Faturamento"],"RECEITA BRUTA TOTAL"))].value),
        fcl_ativo=n(wb["Análise Fluxo"]["BJ"+str(lin(wb["Análise Fluxo"],"FLUXO DE CAIXA LIVRE"))].value),
    )

base = ler(openpyxl.load_workbook(BASE, data_only=True))
print(f"REFERÊNCIA  base dez/30 {base['base30']:,.0f} · receita 2026 {base['rec26']:,.0f} · "
      f"VPL {base['vpl']:,.0f} · capital {base['capital']:,.0f}\n")

testes = []
def teste(nome, mut, verifica):
    r = ler(rodar(mut))
    ok, msg = verifica(r, base)
    testes.append((ok, nome, msg))
    print(f"  [{'ok  ' if ok else 'FALHA'}] {nome}\n         {msg}")

def setp(wb, rot, val, col=2):
    P = wb["Premissas"]; P.cell(lin(P, rot), col).value = val

teste("Trocar o cenário ativo para Conservador propaga para as abas de detalhe",
      lambda wb: setp(wb, "Cenário ativo  (1", 1),
      lambda r, b: (r["rec_ativo"] < b["rec_ativo"]*0.5 and r["fcl_ativo"] < b["fcl_ativo"]
                    and r["recon"] < .01 and r["rec_tot"] == b["rec_tot"],
                    f"Faturamento {b['rec_ativo']:,.0f} → {r['rec_ativo']:,.0f}; "
                    f"FCL {b['fcl_ativo']:,.0f} → {r['fcl_ativo']:,.0f}; "
                    f"reconciliação {r['recon']}; Resumo (mostra os 3) inalterado ✓"))

teste("Trocar o cenário ativo para Agressivo propaga na direção oposta",
      lambda wb: setp(wb, "Cenário ativo  (1", 3),
      lambda r, b: (r["rec_ativo"] > b["rec_ativo"] and r["recon"] < .01,
                    f"Faturamento {b['rec_ativo']:,.0f} → {r['rec_ativo']:,.0f}; "
                    f"reconciliação {r['recon']}"))

teste("Adiar o lançamento de out para dez/2026 derruba a receita de 2026",
      lambda wb: setp(wb, "Mês de lançamento", 12),
      lambda r, b: (r["rec26"] < b["rec26"]*0.35,
                    f"receita 2026 {b['rec26']:,.0f} → {r['rec26']:,.0f}"))

teste("Zerar o churn faz a base crescer muito acima do caso-base",
      lambda wb: [wb["Premissas"].cell(lin(wb["Premissas"],"Churn mensal da base")+2, c).__setattr__("value", 0)
                  for c in range(2, 8)],
      lambda r, b: (r["base30"] > b["base30"]*2,
                    f"base dez/30 {b['base30']:,.0f} → {r['base30']:,.0f}"))

teste("Desligar o plano de contratações zera o pessoal a partir de nov/2026",
      lambda wb: setp(wb, "Considerar o plano de contratações", 0),
      lambda r, b: (r["pessoal30"] == 0 and b["pessoal30"] > 0,
                    f"pessoal dez/30 {b['pessoal30']:,.0f} → {r['pessoal30']:,.0f}"))

teste("Desligar os aportes previstos derruba o capital para o dos fundadores",
      lambda wb: setp(wb, "Considerar aportes PREVISTOS", 0),
      lambda r, b: (abs(r["capital"] - 80000) < 1,
                    f"capital {b['capital']:,.0f} → {r['capital']:,.0f} (esperado 80.000)"))

teste("Ligar os acordos em negociação traz a Boston: capital e receita B2B",
      lambda wb: setp(wb, "Considerar acordos EM NEGOCIAÇÃO", 1),
      lambda r, b: (abs(r["capital"]-700000) < 1 and r["b2b"] > 0 and b["b2b"] == 0,
                    f"capital {r['capital']:,.0f}, receita B2B acumulada {r['b2b']:,.0f}"))

teste("Subir a TMA de 25% para 60% reduz o VPL",
      lambda wb: setp(wb, "TMA — taxa mínima", 0.60),
      lambda r, b: (r["vpl"] < b["vpl"],
                    f"VPL {b['vpl']:,.0f} → {r['vpl']:,.0f}"))

teste("Zerar a conversão zera a receita de assinatura, mas não a de marketplace",
      lambda wb: [wb["Premissas"].cell(lin(wb["Premissas"],"Taxa de conversão (pagantes")+2, c).__setattr__("value", 0)
                  for c in range(2, 8)],
      lambda r, b: (0 < r["rec_tot"] < b["rec_tot"]*0.15,
                    f"receita 5 anos {b['rec_tot']:,.0f} → {r['rec_tot']:,.0f} (sobra o marketplace)"))

teste("Trocar o regime para Anexo III reduz os impostos e aumenta o VPL",
      lambda wb: setp(wb, "Regime  (1 = Simples", 1),
      lambda r, b: (r["vpl"] > b["vpl"],
                    f"VPL {b['vpl']:,.0f} → {r['vpl']:,.0f}"))

print("\n" + "="*92)
falhas = [t for t in testes if not t[0]]
print(f"AUDITORIA 4: {len(testes)-len(falhas)}/{len(testes)} testes de comportamento passaram."
      + ("" if not falhas else "  FALHAS: " + "; ".join(t[1] for t in falhas)))
