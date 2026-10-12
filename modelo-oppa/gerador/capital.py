# -*- coding: utf-8 -*-
"""Aba Necessidade de Capital: quanto a empresa precisa, e de quem.

A pergunta tem duas respostas e elas nao sao iguais:

  1. Quanto a OPERACAO consome antes de se sustentar — o pico do fluxo de caixa
     livre acumulado negativo. Ignora quando o dinheiro chega.
  2. Quanto FALTA CAPTAR — mes a mes, com o capital entrando nas datas em que
     esta previsto entrar. Dinheiro certo na data errada nao paga conta.

A segunda e sempre a que manda, e e sempre maior ou igual a primeira menos o
capital ja previsto. Esta aba mostra as duas e a diferenca entre elas.

Os tres cenarios tem bloco proprio. Um numero de cenario calculado a partir de
outro cenario e o tipo de erro que passa despercebido porque a celula mostra
algo plausivel.
"""
from openpyxl.styles import Alignment, PatternFill
from common import *
from engine import O
from detalhe import mk_sel

TEMPO, LIDX, LANO, LIDXA = 4, 5, 6, 7
COLS = ["B", "C", "D"]
NOMES = ["CONSERVADOR", "PROVÁVEL", "AGRESSIVO"]
CORES = ["C00000", "1F3864", "1F7040"]


def build(wb, P, A, I, BLOCOS, FL, PE):
    ws = wb.create_sheet("Necessidade de Capital")
    sel, yr, yr_cen, ov_cen = mk_sel(P, BLOCOS)
    titulo(ws, "NECESSIDADE DE CAPITAL — QUANTO A EMPRESA PRECISA E DE QUEM",
           "Mês a mês, porque no começo é o mês que decide. O ano fecha positivo e a empresa "
           "quebra em março: é isso que a visão anual esconde.")
    largura_padrao(ws, col_a=56, col_mes_w=13)
    cabecalho_tempo(ws, linha_data=TEMPO, congelar="B9", anos_row=P["anos"])

    C = {}
    r = 8

    def linha(lbl, fn, key, fmt=BRL, bold=False, nivel=1, destaque=False,
              obs=None, cor=PRETO, total=True):
        nonlocal r
        rotulo(ws, r, lbl, 0 if bold else nivel, bold=bold, color=cor)
        preencher_linha(ws, r, fn, fmt, bold=bold, color=cor, total=total)
        if destaque:
            for i in range(1, N_MESES + 1):
                ws[f"{col_mes(i)}{r}"].fill = FILL_TOTAL
        if obs:
            nota(ws, f"{L_PCT}{r}", obs)
        C[key] = r
        r += 1
        return C[key]

    def prev(i):
        return gcl(COL0 + i - 2)

    # =================================================================
    secao(ws, r, "1. O CAPITAL QUE JÁ ESTÁ NA MESA, POR STATUS — vale para os três cenários",
          COL_PCT)
    r += 1
    ai, af = A["ini"], A["fim"]

    def _status(st, L):
        return (f'SUMPRODUCT((Aportes!$D${ai}:$D${af}="{st}")'
                f'*(Aportes!$A${ai}:$A${af}>={L}${TEMPO})'
                f'*(Aportes!$A${ai}:$A${af}<=EOMONTH({L}${TEMPO},0))'
                f'*Aportes!$C${ai}:$C${af})')

    for st, key, obs in [
        ("Realizado", "st_real", "Dinheiro que já entrou na conta da empresa."),
        ("Compromisso", "st_comp", "Fundadores já se comprometeram; ainda não integralizaram."),
        ("Previsto", "st_prev", "Negociação em curso, sem assinatura. Ligado/desligado em Premissas."),
        ("Em negociação", "st_negoc", "Sem compromisso nenhum. Desligado por padrão."),
    ]:
        linha(st, lambda i, L, s=st: f'={_status(s, L)}', key, obs=obs)
    ei, ef = A["est_ini"], A["est_fim"]
    linha("Investidores estratégicos (tabela 2 da aba Aportes)",
          lambda i, L: (f'=SUMPRODUCT((Aportes!$D${ei}:$D${ef}>={L}${TEMPO})'
                        f'*(Aportes!$D${ei}:$D${ef}<=EOMONTH({L}${TEMPO},0))'
                        f'*Aportes!$C${ei}:$C${ef})'), "st_estr")
    linha("Capital de todos os status, somado",
          lambda i, L: f'=SUM({L}{C["st_real"]}:{L}{C["st_estr"]})', "cap_todos", bold=True)
    linha("Capital que o modelo considera (depois dos interruptores)",
          lambda i, L: f'=Aportes!{L}{A["total"]}', "cap_mod", cor=VERDE_LINK, bold=True,
          obs="É este que entra no caixa. A diferença para a linha acima é o que está desligado.")
    linha("Capital considerado — acumulado",
          lambda i, L: f'=Aportes!{L}{A["acum"]}', "cap_ac", cor=VERDE_LINK, total=False)
    r += 2

    # =================================================================
    # Um bloco por cenario. O que muda de cenario para cenario: o FCL, o caixa
    # e a nuvem (que depende do numero de usuarios). Pessoas, marketing
    # recorrente e administrativas sao iguais nos tres.
    # =================================================================
    fixo_comum = "+".join(f"'Análise Fluxo'!{{L}}{FL[k]}"
                          for k in ("equipe", "clt", "prolab", "mkt_rec", "adm"))
    K = []
    for s, S in enumerate(BLOCOS):
        c = ws.cell(r, 1, f"CENÁRIO {s+1} — {NOMES[s]}")
        c.font = f(11, True, BRANCO)
        fill = PatternFill("solid", fgColor=CORES[s])
        for cc in range(1, COL_PCT + 1):
            ws.cell(r, cc).fill = fill
        ws.row_dimensions[r].height = 20
        r += 1
        k = {}

        def L_(lbl, fn, key, **kw):
            k[key] = linha(lbl, fn, f"{key}_{s}", **kw)
            return k[key]

        L_("Fluxo de caixa livre do mês (FCL)",
           lambda i, L: f"='Cenários'!{L}{S+O.fcl}", "fcl", cor=VERDE_LINK,
           obs="Não inclui aporte: aporte é financiamento, não geração de caixa.")
        L_("Buraco do mês (quanto a operação queimou)",
           lambda i, L: f'=IF({L}{k["fcl"]}<0,-{L}{k["fcl"]},0)', "buraco")
        r_bac = r
        L_("Buraco acumulado",
           lambda i, L: (f'={L}{k["buraco"]}' if i == 1
                         else f'={prev(i)}{r_bac}+{L}{k["buraco"]}'), "buraco_ac", total=False,
           obs="Soma de todos os meses negativos, sem compensar com os positivos.")
        L_("FCL acumulado (os positivos já abatendo os negativos)",
           lambda i, L: f"='Cenários'!{L}{S+O.fcl_ac}", "fcl_ac", cor=VERDE_LINK, total=False,
           bold=True, obs="O fundo do poço desta linha é o capital requerido pela operação.")
        L_("Custo fixo do mês (nuvem, pessoas, marketing recorrente, administrativas)",
           lambda i, L: ("=-('Cenários'!" + f"{L}{S+O.nuvem}+" + fixo_comum.replace("{L}", L) + ")"),
           "cf", cor=VERDE_LINK,
           obs="Sem aquisição paga, imposto, loja e meio de pagamento: esses variam com a "
               "operação, não com a existência dela.")
        L_("Reserva mínima desejada",
           lambda i, L: (f'=MAX(SUMPRODUCT((B${LIDX}:{L_FIM}${LIDX}>{L}${LIDX})'
                         f'*(B${LIDX}:{L_FIM}${LIDX}<={L}${LIDX}+Premissas!$B${P["reserva_meses"]})'
                         f'*B${k["cf"]}:{L_FIM}${k["cf"]}),'
                         f'Premissas!$B${P["reserva_meses"]}*{L}{k["cf"]})'), "reserva",
           total=False,
           obs="Custo fixo dos próximos meses. Nos últimos meses do horizonte não há 'próximos', "
               "então cai para o custo fixo do mês vezes o número de meses — senão a reserva "
               "sumiria justamente onde a empresa é maior.")
        L_("Caixa projetado no fim do mês",
           lambda i, L: f"='Cenários'!{L}{S+O.caixa}", "caixa", cor=VERDE_LINK, bold=True,
           destaque=True, total=False)
        L_("Caixa acima (ou abaixo) da reserva",
           lambda i, L: f'={L}{k["caixa"]}-{L}{k["reserva"]}', "folga", total=False,
           obs="Negativo aqui já é sinal amarelo, mesmo com o caixa no positivo.")
        L_("FALTA CAPTAR neste mês",
           lambda i, L: f'=MAX(0,{L}{k["reserva"]}-{L}{k["caixa"]})', "falta", bold=True,
           destaque=True, total=False,
           obs="Quanto teria de estar em caixa neste mês e não está.")
        L_("FALTA CAPTAR — pior caso até aqui (cronograma de captação)",
           lambda i, L: f'=MAX($B{k["falta"]}:{L}{k["falta"]})', "falta_ac", bold=True,
           total=False, obs="Só sobe. É a meta de captação que precisa estar fechada até este mês.")
        L_("Marcador — mês com caixa negativo",
           lambda i, L: f'=IF({L}{k["caixa"]}<0,{L}${LIDX},9999)', "mk_neg", fmt=INT,
           total=False, cor=CINZA,
           obs="Auxiliar: guarda o nº do mês quando o caixa fica negativo. O menor valor é o "
               "primeiro mês sem fundo.")
        L_("Meses de caixa restantes (runway)",
           lambda i, L: (f'=IFERROR(IF({L}{k["cf"]}<=0,"",'
                         f'MAX(0,{L}{k["caixa"]})/{L}{k["cf"]}),"")'), "runway",
           fmt='0.0;;"–"', total=False, cor=CINZA,
           obs="Caixa dividido pelo custo fixo do mês. Abaixo de 3 é zona de risco.")
        K.append(k)
        r += 1

    r += 1

    # =================================================================
    secao(ws, r, "RESPOSTA POR CENÁRIO", COL_PCT); r += 1
    ws.cell(r, 1, "QUANTO A EMPRESA PRECISA").font = f(10, True, BRANCO)
    ws.cell(r, 1).fill = FILL_HEADER
    ws.cell(r, 1).alignment = Alignment(indent=1, vertical="center")
    for j, col in enumerate(COLS):
        c = ws[f"{col}{r}"]
        c.value = NOMES[j]
        c.font = f(10, True, BRANCO)
        c.fill = PatternFill("solid", fgColor=CORES[j])
        c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[r].height = 22
    r += 1

    R = {}

    def res(lbl, fx, key=None, fmt=BRL, bold=False, obs=None, cor=PRETO):
        nonlocal r
        c = ws.cell(r, 1, lbl)
        c.font = f(10, bold, cor)
        c.alignment = Alignment(indent=1, vertical="center")
        for j, col in enumerate(COLS):
            cc = ws[f"{col}{r}"]
            cc.value = fx(j, col)
            cc.number_format = fmt
            cc.font = f(10, bold, cor)
            cc.alignment = Alignment(horizontal="center")
            cc.border = BORDA_FINA
            if bold:
                cc.fill = FILL_TOTAL
        if obs:
            c2 = ws.cell(r, 6, obs)
            c2.font = f(8, False, CINZA, italic=True)
            c2.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
            ws.merge_cells(start_row=r, start_column=6, end_row=r, end_column=15)
            ws.row_dimensions[r].height = max(15, 13 + 11 * (len(obs) // 115))
        if key:
            R[key] = r
        r += 1
        return r - 1

    def rng(j, key):
        x = K[j][key]
        return f"$B${x}:${L_FIM}${x}"

    res("Capital requerido pela operação (pico do FCL acumulado negativo)",
        lambda j, col: f"=-MIN(0,MIN({rng(j, 'fcl_ac')}))", "capreq", bold=True,
        obs="Quanto a operação consome antes de virar. Ignora a data em que o dinheiro chega.")
    res("(+) Reserva mínima no mês mais apertado",
        lambda j, col: (f"=INDEX({rng(j, 'reserva')},"
                        f"MATCH(MIN({rng(j, 'caixa')}),{rng(j, 'caixa')},0))"), "res_pico")
    res("(=) NECESSIDADE TOTAL DE CAPITAL",
        lambda j, col: f"={col}{R['capreq']}+{col}{R['res_pico']}", "nec_total", bold=True)
    res("(−) Já realizado", lambda j, col: f"=-Aportes!$C${A['res_real']}", "r_real")
    res("(−) Compromisso dos fundadores a integralizar",
        lambda j, col: f"=-Aportes!$C${A['res_comp']}", "r_comp")
    res("(−) Previsto (negociação em curso)",
        lambda j, col: f"=-Aportes!$C${A['res_prev']}", "r_prev",
        obs="Entra como zero se o interruptor de aportes previstos estiver desligado em Premissas.")
    res("(=) FALTA CAPTAR — ignorando as datas de entrada",
        lambda j, col: (f"=MAX(0,{col}{R['nec_total']}+{col}{R['r_real']}"
                        f"+{col}{R['r_comp']}+{col}{R['r_prev']})"), "falta_simples",
        obs="Serve para a conversa de rodada: o tamanho do cheque, supondo o dinheiro "
            "disponível desde o primeiro mês.")
    res("(=) FALTA CAPTAR — respeitando as datas de entrada",
        lambda j, col: f"=MAX({rng(j, 'falta')})", "falta_real", bold=True,
        obs="Esta é a que manda: a pior lacuna de qualquer mês, com cada aporte entrando na "
            "data prevista e a reserva mínima respeitada.")
    res("Mês em que essa lacuna aparece", lambda j, col: (
            f'=CHOOSE(MOD(MATCH(MAX({rng(j, "falta")}),{rng(j, "falta")},0)-1,12)+1,'
            f'"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez")&"/"&'
            f'(2026+INT((MATCH(MAX({rng(j, "falta")}),{rng(j, "falta")},0)-1)/12))'),
        "falta_mes", fmt=TXT)
    res("Caixa mínimo projetado", lambda j, col: f"=MIN({rng(j, 'caixa')})", "caixa_min",
        obs="Negativo significa conta sem fundo naquele mês — não é um aviso, é a operação parando.")
    res("Mês do caixa mínimo", lambda j, col: (
            f'=CHOOSE(MOD(MATCH(MIN({rng(j, "caixa")}),{rng(j, "caixa")},0)-1,12)+1,'
            f'"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez")&"/"&'
            f'(2026+INT((MATCH(MIN({rng(j, "caixa")}),{rng(j, "caixa")},0)-1)/12))'),
        "caixa_min_mes", fmt=TXT,
        obs="Prazo real da captação: o dinheiro precisa estar na conta ANTES deste mês.")
    res("Primeiro mês em que o caixa fica NEGATIVO", lambda j, col: (
            f'=IF(MIN({rng(j, "mk_neg")})=9999,"nunca",'
            f'CHOOSE(MOD(MIN({rng(j, "mk_neg")})-1,12)+1,'
            f'"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez")&"/"&'
            f'(2026+INT((MIN({rng(j, "mk_neg")})-1)/12)))'),
        "primeiro_mes", fmt=TXT, bold=True,
        obs="O prazo que não se negocia. Antes deste mês o dinheiro tem de estar na conta — "
            "pode ser bem antes do mês do fundo do poço.")
    r += 1

    # =================================================================
    secao(ws, r, "QUANTO SAI DE CADA SÓCIO", COL_PCT); r += 1
    fi, ff = A["fund_ini"], A["fund_fim"]
    i, fim = A["ini"], A["fim"]
    res("Fundadores no quadro",
        lambda j, col: f'=COUNTIF(Aportes!$A${fi}:$A${ff},"?*")', "n_fund", fmt=INT,
        obs="Lido da tabela de compromisso dos fundadores, na aba Aportes.")
    res("Compromisso total dos fundadores",
        lambda j, col: f"=SUM(Aportes!$B${fi}:$B${ff})", "meta_fund",
        obs="R$ 20 mil cada, conforme o acordo em curso.")
    res("Já integralizado pelos fundadores",
        lambda j, col: (f'=SUMIFS(Aportes!$C${i}:$C${fim},Aportes!$E${i}:$E${fim},"Fundador",'
                        f'Aportes!$D${i}:$D${fim},"Realizado")'), "pago_fund")
    res("Ainda por integralizar do compromisso atual",
        lambda j, col: (f'=SUMIFS(Aportes!$C${i}:$C${fim},Aportes!$E${i}:$E${fim},"Fundador",'
                        f'Aportes!$D${i}:$D${fim},"Compromisso")'), "falta_fund", bold=True,
        obs="Já está dentro do capital que o modelo considera. Não é captação nova.")
    res("Se os fundadores cobrissem TODA a lacuna, quanto sai de cada um",
        lambda j, col: f"=IFERROR({col}{R['falta_real']}/{col}{R['n_fund']},0)", "por_fund",
        bold=True,
        obs="Além do compromisso que já existe. É a conta de quanto cada um teria de pôr para "
            "não precisar de dinheiro de fora e não diluir ninguém.")
    res("Quantas vezes o que cada fundador já integralizou",
        lambda j, col: (f"=IFERROR({col}{R['por_fund']}/({col}{R['pago_fund']}"
                        f"/{col}{R['n_fund']}),0)"), "mult_fund", fmt=MULT,
        obs="Régua de realismo: serve para saber se a conta cabe no bolso dos quatro ou se a "
            "captação externa é inevitável.")
    res("Capital externo necessário, se os fundadores só honrarem o compromisso",
        lambda j, col: f"={col}{R['falta_real']}", "externo", bold=True,
        obs="O compromisso dos fundadores já está contado no caixa projetado, então a lacuna "
            "que sobra é exatamente o que precisa vir de fora.")
    res("Diluição implícita desse capital externo",
        lambda j, col: (f"=IFERROR({col}{R['externo']}/(Aportes!$C${A['capital_total']}"
                        f"+{col}{R['externo']}),0)"), "diluicao", fmt=PCT,
        obs="Participação que o dinheiro novo compraria se o preço fosse o capital aportado — "
            "é piso, não preço: valuation de verdade se negocia, não se calcula aqui. Com um "
            "valuation pré-dinheiro maior, a diluição cai na mesma proporção.")
    r += 2

    for txt, cor in [
        ("Por que as duas respostas de 'falta captar' diferem: a primeira soma o buraco total "
         "e desconta todo o capital previsto, como se o dinheiro estivesse disponível desde "
         "janeiro. A segunda percorre os 60 meses e pergunta, em cada um, se o saldo cobre a "
         "reserva. Quando a segunda é maior, o problema não é o tamanho do capital — é a data.",
         CINZA),
        ("A reserva mínima é o que separa as duas. Zere a célula em Premissas e a necessidade "
         "cai para o mínimo matemático: o capital que apenas evita o saldo negativo, sem "
         "nenhuma folga. É um número para medir o piso, não para operar.", CINZA),
    ]:
        c = ws.cell(r, 1, txt)
        c.font = f(9, False, cor, italic=True)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=12)
        ws.row_dimensions[r].height = 44
        r += 1

    return ws, C, R, K
