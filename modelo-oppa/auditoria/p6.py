# -*- coding: utf-8 -*-
"""Auditoria 6 — comportamento das linhas de receita B2B recem-incluidas."""
import sys, shutil, subprocess, glob, openpyxl
BASE=sys.argv[1]
TMP="/tmp/claude-0/-home-user-Teste/42d647a1-c445-511e-84b4-a900542f847f/scratchpad/audit/_b.xlsx"
RECALC=glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
n=lambda x: x if isinstance(x,(int,float)) else 0
def lin(ws,t,col=1):
    for r in range(1,ws.max_row+1):
        v=ws.cell(r,col).value
        if isinstance(v,str) and t in v: return r
    raise KeyError(t)
def tab_b2b(P):
    return next(r for r in range(1,P.max_row+1)
                if P.cell(r,1).value=="Iniciativa" and P.cell(r,2).value=="Categoria")

def rodar(mut):
    shutil.copy(BASE,TMP); wb=openpyxl.load_workbook(TMP); mut(wb); wb.save(TMP)
    o=subprocess.run(["python3",RECALC,TMP,"420"],capture_output=True,text=True)
    assert '"status": "success"' in o.stdout, o.stdout[:300]
    return openpyxl.load_workbook(TMP,data_only=True)

def ler(wb):
    F,CE,U=wb["Faturamento"],wb["Cenários"],wb["Usuários"]
    bl={int(CE.cell(r,1).value.split()[1]):r for r in range(1,CE.max_row+1)
        if isinstance(CE.cell(r,1).value,str) and CE.cell(r,1).value.startswith("CENÁRIO ")}
    S=bl[2]
    def blk(rot):
        for rr in range(S,S+60):
            v=CE.cell(rr,1).value
            if isinstance(v,str) and v.strip().startswith(rot): return rr
        raise KeyError(rot)
    tot=lambda r: sum(n(CE.cell(r,c).value) for c in range(2,62))
    return dict(
        dados=tot(blk("Receita B2B — venda de dados")),
        outras=tot(blk("Receita B2B — outras iniciativas")),
        bruta=tot(blk("RECEITA BRUTA TOTAL")),
        imp=tot(blk("(−) Impostos sobre a receita")),
        lojas=tot(blk("(−) Comissão das lojas")),
        pgto=tot(blk("(−) Taxas de meios de pagamento")),
        nuvem=tot(blk("(−) Infraestrutura e nuvem")),
        painel_fim=n(CE[f"BI{blk('Usuários no painel')}"].value),
        primeiro_mes_dados=next((c-1 for c in range(2,62)
                                 if n(CE.cell(blk("Receita B2B — venda de dados"),c).value)>0), None),
        recon=max(abs(n(wb["Análise Fluxo"].cell(lin(wb["Análise Fluxo"],"✔ Verificação"),c).value))
                  for c in range(2,62)))

base=ler(openpyxl.load_workbook(BASE,data_only=True))
print(f"REFERÊNCIA  dados R$ {base['dados']:,.0f} · painel dez/30 {base['painel_fim']:,.0f} "
      f"· 1º mês com receita de dados: {base['primeiro_mes_dados']}\n")
res=[]
def teste(nome, mut, verifica):
    r=ler(rodar(mut)); ok,msg=verifica(r,base); res.append((ok,nome))
    print(f"  [{'ok  ' if ok else 'FALHA'}] {nome}\n         {msg}")

def setp(wb,rot,val,col=2):
    P=wb["Premissas"]; P.cell(lin(P,rot),col).value=val

teste("Consentimento zero zera o painel e a receita de dados",
      lambda wb: [wb["Premissas"].cell(lin(wb["Premissas"],"% da base que consente"),c).__setattr__("value",0)
                  for c in range(3,8)],
      lambda r,b: (r["painel_fim"]==0 and r["dados"]==0 and b["dados"]>0,
                   f"painel {b['painel_fim']:,.0f}→{r['painel_fim']:,.0f}, dados {b['dados']:,.0f}→{r['dados']:,.0f}"))

teste("Mínimo do painel muito alto adia a receita de dados",
      lambda wb: setp(wb,"Base mínima do painel",900000),
      lambda r,b: (r["dados"]<b["dados"] and (r["primeiro_mes_dados"] is None
                    or r["primeiro_mes_dados"]>b["primeiro_mes_dados"]),
                   f"1º mês {b['primeiro_mes_dados']}→{r['primeiro_mes_dados']}, "
                   f"dados {b['dados']:,.0f}→{r['dados']:,.0f}"))

teste("Mínimo do painel baixo antecipa a receita de dados",
      lambda wb: setp(wb,"Base mínima do painel",5000),
      lambda r,b: (r["primeiro_mes_dados"]<=b["primeiro_mes_dados"] and r["dados"]>=b["dados"],
                   f"1º mês {b['primeiro_mes_dados']}→{r['primeiro_mes_dados']}, "
                   f"dados {b['dados']:,.0f}→{r['dados']:,.0f}"))

def liga_estudo(wb):
    setp(wb,"Considerar iniciativas B2B EM ESTUDO",1)
    P=wb["Premissas"]; h=tab_b2b(P); P.cell(h+3,5).value=18000   # recompra de medicamento
teste("Iniciativa em estudo só entra com o interruptor ligado",
      liga_estudo,
      lambda r,b: (r["outras"]>0 and b["outras"]==0,
                   f"outras iniciativas {b['outras']:,.0f}→{r['outras']:,.0f}"))

def por_usuario(wb):
    P=wb["Premissas"]; h=tab_b2b(P)
    P.cell(h+1,4).value="Por usuário"; P.cell(h+1,5).value=0.50
teste("Modelo 'Por usuário' escala com o tamanho do painel",
      por_usuario,
      lambda r,b: (r["dados"]!=b["dados"] and r["dados"]>0,
                   f"contrato de R$ 0,50/usuário do painel → dados {r['dados']:,.0f}"))

def sem_dados(wb):
    P=wb["Premissas"]; h=tab_b2b(P)
    for k in (1,2): P.cell(h+k,3).value="Descartado"
teste("Receita de dados NÃO paga comissão de loja nem taxa de pagamento",
      sem_dados,
      lambda r,b: (abs(r["lojas"]-b["lojas"])<0.01 and abs(r["pgto"]-b["pgto"])<0.01
                   and r["dados"]==0 and b["dados"]>0,
                   f"lojas {b['lojas']:,.0f}→{r['lojas']:,.0f} (igual ✓), "
                   f"pgto {b['pgto']:,.0f}→{r['pgto']:,.0f} (igual ✓)"))

teste("Receita de dados PAGA imposto sobre receita e custa nuvem",
      sem_dados,
      lambda r,b: (abs(r["imp"])<abs(b["imp"]) and abs(r["nuvem"])<=abs(b["nuvem"]),
                   f"impostos {b['imp']:,.0f}→{r['imp']:,.0f} (caem ✓), "
                   f"nuvem {b['nuvem']:,.0f}→{r['nuvem']:,.0f}"))

teste("Reconciliação segue zerada com as linhas novas",
      lambda wb: setp(wb,"Considerar iniciativas B2B EM ESTUDO",1),
      lambda r,b: (r["recon"]<0.01, f"desvio máximo {r['recon']}"))

print("\n"+"="*92)
f=[t for t in res if not t[0]]
print(f"AUDITORIA 6: {len(res)-len(f)}/{len(res)} testes passaram."
      + ("" if not f else "  FALHAS: "+"; ".join(t[1] for t in f)))
