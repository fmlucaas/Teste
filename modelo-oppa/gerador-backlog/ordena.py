# -*- coding: utf-8 -*-
"""Ranking: WSJF com DEP calculado do grafo e ordem topologica gulosa."""
import openpyxl
from dados import AVAL, PESOS

ORIG = "/root/.claude/uploads/42d647a1-c445-511e-84b4-a900542f847f/067679df-Validac_a_o_de_prioridade.xlsx"


def carrega_originais():
    ws = openpyxl.load_workbook(ORIG, data_only=True)["Página1"]
    itens, ordem = {}, []
    for r in range(2, ws.max_row + 1):
        pid = ws.cell(r, 1).value
        if not pid:
            continue
        itens[pid] = dict(id=pid, epico=ws.cell(r, 2).value,
                          func=ws.cell(r, 3).value, desc=ws.cell(r, 4).value)
        ordem.append(pid)
    return itens, ordem


def dependentes_transitivos(pre_map):
    """Para cada item, quantos outros ficam bloqueados direta ou indiretamente."""
    filhos = {k: [] for k in pre_map}
    for pid, pres in pre_map.items():
        for p in pres:
            filhos[p].append(pid)
    def alcanca(n, visto):
        for c in filhos[n]:
            if c not in visto:
                visto.add(c)
                alcanca(c, visto)
        return visto
    return {n: len(alcanca(n, set())) for n in pre_map}


def escala(n, maximo):
    """Converte contagem de dependentes para a escala 1-5."""
    if n == 0:  return 1
    if n <= 2:  return 2
    if n <= 5:  return 3
    if n <= max(6, maximo // 2): return 4
    return 5


def calcula():
    itens, ordem_orig = carrega_originais()
    assert not (set(itens) ^ set(AVAL)), "divergência entre planilha e avaliação"

    pre_map = {pid: list(AVAL[pid][4]) for pid in itens}
    for pid, pres in pre_map.items():
        for p in pres:
            assert p in itens, f"{pid} depende de {p}, inexistente"

    dep_bruto = dependentes_transitivos(pre_map)
    mx = max(dep_bruto.values())

    for pid, (vu, obr, mon, esf, pre, just) in AVAL.items():
        it = itens[pid]
        dep_n = dep_bruto[pid]
        dep = escala(dep_n, mx)
        cod = PESOS["VU"]*vu + PESOS["OBR"]*obr + PESOS["MON"]*mon + PESOS["DEP"]*dep
        it.update(VU=vu, OBR=obr, MON=mon, DEP=dep, dep_n=dep_n, ESF=esf,
                  pre=pre, just=just, cod=cod, wsjf=cod/esf)

    # ---- WSJF de cadeia -------------------------------------------------
    # Escolher pelo WSJF proprio e miope: um item barato de valor medio passa na
    # frente de um habilitador que, sozinho, pontua baixo, mas destrava um bloco
    # inteiro de alto valor. O WSJF de cadeia mede o melhor negocio ALCANCAVEL a
    # partir do item: entre todas as sequencias que comecam nele, a de maior
    # (soma de valor / soma de esforco).
    filhos = {k: [] for k in itens}
    for pid, it in itens.items():
        for p in it["pre"]:
            filhos[p].append(pid)

    memo = {}
    def cadeia(n):
        if n in memo:
            return memo[n]
        memo[n] = (itens[n]["cod"], itens[n]["ESF"])          # corta recursao
        melhor = (itens[n]["cod"], itens[n]["ESF"])
        for c in filhos[n]:
            vc, ec = cadeia(c)
            cand = (itens[n]["cod"] + vc, itens[n]["ESF"] + ec)
            if cand[0]/cand[1] > melhor[0]/melhor[1]:
                melhor = cand
        memo[n] = melhor
        return melhor

    for pid, it in itens.items():
        v, e = cadeia(pid)
        it["wsjf_cadeia"] = v / e

    restantes = dict(itens)
    colocados, ordem = set(), []
    while restantes:
        livres = [i for i in restantes.values() if all(p in colocados for p in i["pre"])]
        assert livres, f"ciclo entre {list(restantes)}"
        esc = max(livres, key=lambda i: (i["wsjf_cadeia"], i["wsjf"], i["cod"],
                                         -int(i["id"][-2:])))
        ordem.append(esc["id"]); colocados.add(esc["id"]); del restantes[esc["id"]]

    for pos, pid in enumerate(ordem, 1):
        itens[pid]["rank"] = pos
    for pos, it in enumerate(sorted(itens.values(), key=lambda i: (-i["wsjf"], -i["cod"])), 1):
        it["rank_puro"] = pos
    for it in itens.values():
        it["ajuste"] = it["rank_puro"] - it["rank"]
        it["bloqueia"] = sorted([o for o in itens if it["id"] in itens[o]["pre"]])
    return itens, ordem, ordem_orig


if __name__ == "__main__":
    itens, ordem, _ = calcula()
    print(f"{'#':>3} {'PBI':<8}{'cad':>6}{'WSJF':>6}{'CoD':>6}{'VU':>3}{'OBR':>4}{'MON':>4}{'DEP':>4}"
          f"{'(n)':>5}{'Esf':>4}{'puro':>5}{'aj':>4}  Funcionalidade")
    print("-" * 116)
    for pid in ordem:
        i = itens[pid]
        print(f"{i['rank']:>3} {pid:<8}{i['wsjf_cadeia']:>6.1f}{i['wsjf']:>6.1f}{i['cod']:>6.1f}{i['VU']:>3}{i['OBR']:>4}"
              f"{i['MON']:>4}{i['DEP']:>4}{i['dep_n']:>5}{i['ESF']:>4}{i['rank_puro']:>5}"
              f"{i['ajuste']:>+4}  {i['func'][:46]}")
