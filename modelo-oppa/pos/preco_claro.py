# -*- coding: utf-8 -*-
"""Acrescenta a aba PREÇO: de onde sai o preco, componente por componente.

A pergunta que a aba responde: quanto custa atender UM assinante por mes, e que
preco esse custo exige depois de imposto, loja e meio de pagamento.

A resposta depende do MOMENTO, e e isso que a aba deixa visivel. Custo fixo
dividido por 90 assinantes da um numero absurdo; dividido por 37 mil, da alguns
reais. Por isso a tabela tem quatro colunas, nao uma: lancamento, seis meses,
doze meses e regime.
"""
from openpyxl.styles import Alignment
from comum import *

ABA = "Preço"


def build(wb):
    if ABA in wb.sheetnames:
        del wb[ABA]
    ws = wb.create_sheet(ABA)
    P, CE, AF = wb["Premissas"], wb["Cenários"], wb["Análise Fluxo"]

    # ---------- localiza tudo por rotulo ----------
    def p(rot):
        return linha_por_rotulo(P, rot)

    def af(rot):
        return linha_por_rotulo(AF, rot)

    L_cen       = p("Cenário ativo  (1")
    L_lanc_idx  = p("Mês nº do lançamento")
    L_p_ess     = p("Plano Essencial (R$/mês)")
    L_p_pre     = p("Plano Premium (R$/mês)")
    L_p_fam     = p("Plano Família (R$/mês)")
    L_reaj      = p("Reajuste anual de preços")
    L_loja      = p("Taxa das lojas de aplicativos")
    L_share     = p("% da receita de assinaturas cobrada")
    L_pgto      = p("Taxa de meio de pagamento")
    L_painel_c  = p("Custo de processamento do painel")
    L_cl_fix    = p("Nuvem — custo fixo mensal")
    L_cl_pag    = p("Nuvem — custo variável por usuário PAGANTE")
    L_cl_free   = p("Nuvem — custo variável por usuário GRATUITO")
    L_cl_ini    = p("Início dos custos de nuvem")
    L_sup       = p("Suporte — ferramentas")
    L_organ     = p("Aquisição orgânica")
    # mix: as linhas de mix sao as que tem SO o nome do plano na coluna A
    L_mix_e = linha_por_rotulo(P, "Plano Essencial", exato=True)
    L_mix_p = linha_por_rotulo(P, "Plano Premium", exato=True)
    L_mix_f = linha_por_rotulo(P, "Plano Família", exato=True)
    # drivers por cenario: a linha do cenario fica abaixo do rotulo do driver
    def drv(rot_driver, cen):
        base = p(rot_driver)
        nome = {1: "Conservador", 2: "Provável", 3: "Agressivo"}[cen]
        return linha_por_rotulo(P, nome, inicio=base + 1, fim=base + 4, exato=True)

    MOT = linhas_do_motor(wb, [
        "Base de usuários — fim do mês", "Usuários pagantes",
        "Pagantes — Plano Essencial", "Pagantes — Plano Premium", "Pagantes — Plano Família",
        "Usuários no painel de dados", "Receita de assinaturas",
        "Alíquota efetiva de impostos", "EBITDA", "RECEITA BRUTA TOTAL"])

    AF_R = {k: af(v) for k, v in {
        "nuvem": "Infraestrutura e nuvem", "sup": "Suporte ao cliente",
        "pj": "Equipe PJ", "clt": "Equipe CLT", "prolab": "Pró-labore dos sócios",
        "mkt_perf": "Marketing de performance", "mkt_rec": "Marketing recorrente",
        "mkt_lanc": "Propaganda de lançamento", "adm": "Despesas administrativas"}.items()}

    # ---------- layout ----------
    ws.column_dimensions["A"].width = 58
    for col in "BCDE":
        ws.column_dimensions[col].width = 17
    ws.column_dimensions["F"].width = 3
    for col in "GHIJKLMN":
        ws.column_dimensions[col].width = 9

    titulo(ws, "PREÇO — DE ONDE SAI O VALOR DA ASSINATURA",
           "Custo de atender um assinante por mês, componente por componente, e o preço que esse "
           "custo exige. Quatro momentos, porque o custo por assinante cai com a escala: o que é "
           "caro com 90 assinantes é barato com 37 mil.")
    ws["A3"] = '=" Cenário ativo: "&Premissas!$B$' + str(L_cen) + '&"   ·   todos os valores em R$ por assinante por mês, salvo onde indicado"'
    ws["A3"].font = f(9, True, VERDE_LINK)
    ws.row_dimensions[3].height = 15

    COLS = ["B", "C", "D", "E"]
    R = {}
    r = 5

    def bloco(txt):
        nonlocal r
        secao(ws, r, txt, 14)
        r += 1

    def L(rot, formulas, key=None, fmt=BRL2, bold=False, nivel=1, destaque=False,
          obs=None, cor=PRETO, entrada=False, unico=False):
        """Uma linha com os quatro momentos. `formulas` recebe a letra da coluna.
        `unico`: o valor e digitado so na coluna B e as outras espelham, para nao
        haver quatro celulas da mesma premissa saindo de sincronia."""
        nonlocal r
        c = ws.cell(r, 1, rot)
        c.font = f(10, bold, cor)
        c.alignment = Alignment(indent=0 if bold else nivel, vertical="center")
        for col in COLS:
            cc = ws[f"{col}{r}"]
            if unico and col != "B":
                cc.value = f"=$B${r}"
            else:
                cc.value = formulas(col) if callable(formulas) else formulas
            cc.number_format = fmt
            espelho = unico and col != "B"
            cc.font = f(10, bold, cor if espelho else (AZUL_INPUT if entrada else cor))
            cc.alignment = Alignment(horizontal="center")
            cc.border = BORDA
            if entrada and not espelho:
                cc.fill = FILL_INPUT
            elif destaque:
                cc.fill = FILL_TOTAL
        if obs:
            nota(ws, r, obs)
        if key:
            R[key] = r
        r += 1
        return r - 1

    # =============== 1. OS QUATRO MOMENTOS ===============
    bloco("1. OS QUATRO MOMENTOS DA TABELA")
    idx = L("Mês nº na linha do tempo (1 = jan/2026 · 60 = dez/2030)",
            lambda col: {"B": f"=Premissas!$B${L_lanc_idx}",
                         "C": f"=MIN(60,Premissas!$B${L_lanc_idx}+6)",
                         "D": f"=MIN(60,Premissas!$B${L_lanc_idx}+12)",
                         "E": "=60"}[col], "idx", INT, entrada=True,
            obs="Lançamento, +6 meses, +12 meses e o último mês do modelo. Digite por cima "
                "para olhar qualquer outro mês — é a única célula desta aba que você precisa mexer.")
    I = {col: f"{col}${idx}" for col in COLS}

    def eng(rot, col):
        """Valor do motor no cenário ativo, no mês da coluna."""
        alvos = ",".join(f"INDEX('Cenários'!$B${x}:${L_FIM}${x},{I[col]})"
                         for x in MOT[rot])
        return f"CHOOSE(Premissas!$B${L_cen},{alvos})"

    def flx(key, col):
        """Valor da aba Análise Fluxo (já é o cenário ativo) no mês da coluna."""
        x = AF_R[key]
        return f"INDEX('Análise Fluxo'!$B${x}:${L_FIM}${x},{I[col]})"

    def ano(col):
        return f"INDEX('Cenários'!$B$7:${L_FIM}$7,{I[col]})"

    def prem_ano(linha, col):
        return f"INDEX(Premissas!$C${linha}:$G${linha},{ano(col)})"

    L("Mês", lambda col: f"=INDEX('Cenários'!$B$4:${L_FIM}$4,{I[col]})", "data", MES, bold=True)
    L("Base total de usuários (pagantes + gratuitos)",
      lambda col: f"={eng('Base de usuários — fim do mês', col)}", "base", INT, cor=VERDE_LINK)
    pag = L("Assinantes pagantes", lambda col: f"={eng('Usuários pagantes', col)}", "pag", INT,
            bold=True, cor=VERDE_LINK,
            obs="É por este número que todo o custo fixo é dividido. É a variável que manda no preço.")
    L("Receita de assinaturas no mês",
      lambda col: f"={eng('Receita de assinaturas', col)}", "assin", BRL, cor=VERDE_LINK)
    L("Receita média por assinante hoje (ARPPU)",
      lambda col: f"=IFERROR({eng('Receita de assinaturas', col)}/{col}${pag},0)", "arppu",
      BRL2, bold=True,
      obs="Média do que cada assinante paga, considerando o mix de planos daquele mês.")
    r += 1

    # =============== 2. CUSTO VARIÁVEL ===============
    bloco("2. CUSTO VARIÁVEL — o que cada assinante a mais custa (R$ por assinante/mês)")
    L("Nuvem — do próprio assinante", lambda col: f"={prem_ano(L_cl_pag, col)}", "cv_nuvem",
      obs="Premissas, seção 6: 'Nuvem — custo variável por usuário PAGANTE'. É o maior item "
          "variável e por isso o mais sensível: cada real aqui pede cerca de R$ 1,39 de preço.")
    L("Nuvem — rateio dos usuários do plano gratuito",
      lambda col: (f"=IFERROR(({eng('Base de usuários — fim do mês', col)}"
                   f"-{col}${pag})*{prem_ano(L_cl_free, col)}/{col}${pag},0)"), "cv_free",
      obs="O plano gratuito não paga e consome. Quem assina sustenta quem não assina.")
    L("Nuvem — processamento do painel de dados",
      lambda col: (f"=IFERROR({eng('Usuários no painel de dados', col)}"
                   f"*Premissas!$B${L_painel_c}/{col}${pag},0)"), "cv_painel")
    L("Suporte ao cliente", lambda col: f"={prem_ano(L_sup, col)}", "cv_sup")
    L("Marketing — custo de conquistar um assinante (CAC)",
      lambda col: (f"=IFERROR((1-{prem_ano(L_organ, col)})"
                   f"*CHOOSE(Premissas!$B${L_cen},"
                   + ",".join(prem_ano(drv("CAC — custo de aquisição", k), col) for k in (1, 2, 3))
                   + ")/CHOOSE(Premissas!$B${},".format(L_cen)
                   + ",".join(prem_ano(drv("Taxa de conversão (pagantes", k), col) for k in (1, 2, 3))
                   + "),0)"), "cac_pag", BRL2, cor=CINZA,
      obs="Gasto para trazer um ASSINANTE: o CAC por usuário captado, dividido pela taxa de "
          "conversão do ano. Não é custo mensal — é de uma vez só, na entrada.")
    L("Marketing — o CAC diluído na vida do assinante",
      lambda col: (f"={col}{R['cac_pag']}*CHOOSE(Premissas!$B${L_cen},"
                   + ",".join(prem_ano(drv("Churn mensal da base", k), col) for k in (1, 2, 3))
                   + ")"), "cv_cac",
      obs="Vida esperada do assinante = 1 ÷ churn. Multiplicar o CAC pelo churn é espalhá-lo "
          "por essa vida — é assim que ele entra num preço mensal.")
    cvar = L("(=) CUSTO VARIÁVEL POR ASSINANTE",
             lambda col: (f"={col}{R['cv_nuvem']}+{col}{R['cv_free']}+{col}{R['cv_painel']}"
                          f"+{col}{R['cv_sup']}+{col}{R['cv_cac']}"), "cvar", BRL2,
             bold=True, destaque=True)
    r += 1

    # =============== 3. CUSTO FIXO ===============
    bloco("3. CUSTO FIXO — o que a empresa gasta mesmo sem um assinante a mais (R$ no mês)")
    L("Pessoas — equipe PJ, CLT e pró-labore",
      lambda col: f"=-({flx('pj', col)}+{flx('clt', col)}+{flx('prolab', col)})", "cf_pes", BRL,
      cor=VERDE_LINK, obs="Da aba Pessoas, linha a linha. É o maior custo fixo em todos os meses.")
    L("Nuvem — parcela fixa (ambiente, licenças, banco de dados)",
      lambda col: (f"=IF({col}{R['data']}>=Premissas!$B${L_cl_ini},{prem_ano(L_cl_fix, col)},0)"),
      "cf_nuvem", BRL)
    L("Marketing recorrente e propaganda de lançamento",
      lambda col: f"=-({flx('mkt_rec', col)}+{flx('mkt_lanc', col)})", "cf_mkt", BRL,
      cor=VERDE_LINK)
    L("Administrativo — contabilidade, jurídico, ferramentas",
      lambda col: f"=-{flx('adm', col)}", "cf_adm", BRL, cor=VERDE_LINK,
      obs="Premissas, seção 6. A célula é MENSAL. Hoje está como 2000/12, 5000/12 e assim por "
          "diante, o que dá R$ 167 por mês em 2027 — para contabilidade, jurídico e ferramentas "
          "de uma empresa no Simples isso é baixo. Vale conferir: só o contador costuma custar "
          "entre R$ 300 e R$ 800 por mês.")
    cfix = L("(=) CUSTO FIXO DO MÊS",
             lambda col: (f"={col}{R['cf_pes']}+{col}{R['cf_nuvem']}+{col}{R['cf_mkt']}"
                          f"+{col}{R['cf_adm']}"), "cfix", BRL, bold=True, destaque=True)
    L("Custo fixo dividido pelos assinantes",
      lambda col: f"=IFERROR({col}{cfix}/{col}${pag},0)", "cf_unit", BRL2, bold=True,
      obs="É esta linha que faz o preço parecer impossível no lançamento e razoável depois. "
          "Não é o custo que muda — é o número de pessoas dividindo a conta.")
    r += 1

    ctot = L("(=) CUSTO TOTAL POR ASSINANTE  ·  variável + fixo rateado",
             lambda col: f"={col}{cvar}+{col}{R['cf_unit']}", "ctot", BRL2, bold=True,
             destaque=True)
    L("✔ Conferência do custo contra a DRE, sem o marketing (deve ser zero)",
      lambda col: (f"=({col}{R['cv_nuvem']}+{col}{R['cv_free']}+{col}{R['cv_painel']}"
                   f"+{col}{R['cv_sup']})*{col}${pag}+{col}{cfix}"
                   f"+({flx('nuvem', col)}+{flx('sup', col)}+{flx('pj', col)}"
                   f"+{flx('clt', col)}+{flx('prolab', col)}+{flx('mkt_rec', col)}"
                   f"+{flx('mkt_lanc', col)}+{flx('adm', col)})"), "chk1", BRL2,
      cor=CINZA,
      obs="Compara nuvem, suporte, pessoas, marketing recorrente e administrativo com o que a "
          "DRE gasta nos mesmos itens. O marketing de AQUISIÇÃO fica fora de propósito: aqui "
          "ele entra diluído na vida do assinante, na DRE entra no mês do desembolso.")
    L("✔ Conferência da nuvem: esta aba × assinantes − nuvem da DRE (deve ser zero)",
      lambda col: (f"=({col}{R['cv_nuvem']}+{col}{R['cv_free']}+{col}{R['cv_painel']})"
                   f"*{col}${pag}+{col}{R['cf_nuvem']}+{flx('nuvem', col)}"), "chk2", BRL2,
      cor=CINZA,
      obs="Prova que a decomposição da nuvem nesta aba é a mesma conta que a DRE usa. "
          "Se der diferente de zero, não confie no preço desta aba.")
    r += 1

    # =============== 4. O QUE INCIDE SOBRE O PREÇO ===============
    bloco("4. O QUE SAI DE CADA REAL COBRADO — antes de sobrar para pagar o custo")
    L("(−) Imposto sobre a receita (Simples / Lucro Presumido)",
      lambda col: f"={eng('Alíquota efetiva de impostos', col)}", "d_imp", PCT2, cor=VERDE_LINK,
      obs="Alíquota efetiva do mês, da tabela do Simples. Sobe conforme o faturamento dos "
          "últimos 12 meses.")
    L("(−) Comissão da loja de aplicativos (Apple / Google)",
      lambda col: f"=Premissas!$B${L_loja}*{prem_ano(L_share, col)}", "d_loja", PCT2,
      obs="15% sobre a parte cobrada dentro do app. Cobrar fora do app evita a comissão, "
          "mas o aplicativo precisa estar nas lojas para existir.")
    L("(−) Taxa do meio de pagamento (cartão, PIX, boleto)",
      lambda col: f"=Premissas!$B${L_pgto}*(1-{prem_ano(L_share, col)})", "d_pgto", PCT2)
    L("(=) Total que sai do preço",
      lambda col: f"={col}{R['d_imp']}+{col}{R['d_loja']}+{col}{R['d_pgto']}", "d_tot", PCT2,
      bold=True)
    rho = L("(=) FICA PARA A EMPRESA, de cada R$ 1 cobrado",
            lambda col: f"=1-{col}{R['d_tot']}", "rho", PCT2, bold=True, destaque=True,
            obs="Cobrar R$ 1 não é receber R$ 1. Todo preço desta aba é o custo dividido por "
                "esta porcentagem — é o que faz o preço subir mais do que o custo.")
    r += 1

    # =============== 5. O PREÇO ===============
    bloco("5. O PREÇO QUE O CUSTO EXIGE")
    L("Margem EBITDA desejada", "=0.2", "margem", PCT, entrada=True, unico=True,
      obs="Digite a margem que você quer que sobre depois de pagar tudo. Com 0%, o preço "
          "apenas empata.")
    L("Preço médio por assinante que apenas EMPATA (margem zero)",
      lambda col: f"=IFERROR({col}{ctot}/{col}{rho},0)", "p_empata", BRL2, bold=True)
    psug = L("Preço médio por assinante COM a margem desejada",
             lambda col: f"=IFERROR({col}{ctot}/({col}{rho}*(1-{col}{R['margem']})),0)",
             "p_sug", BRL2, bold=True, destaque=True,
             obs="É a ARPPU necessária: a média ponderada dos três planos. Abaixo, traduzida "
                 "para o preço de cada plano.")
    L("Receita média por assinante hoje (para comparar)",
      lambda col: f"={col}{R['arppu']}", "arppu2", BRL2, cor=CINZA)
    L("Margem EBITDA que o preço de hoje entrega",
      lambda col: (f"=IFERROR(({col}{R['arppu']}*{col}{rho}-{col}{ctot})"
                   f"/({col}{R['arppu']}*{col}{rho}),0)"), "margem_hoje", PCT, bold=True,
      obs="Difere da margem EBITDA da DRE de propósito: aqui o marketing de aquisição entra "
          "diluído na vida do assinante, e marketplace e B2B não entram. É a margem da "
          "ASSINATURA, não a da empresa.")
    r += 1

    fator = L("Fator do mix (quanto a ARPPU vale em preços de Essencial)",
              lambda col: (f"={prem_ano(L_mix_e, col)}+{prem_ano(L_mix_p, col)}"
                           f"*IFERROR(Premissas!$B${L_p_pre}/Premissas!$B${L_p_ess},0)"
                           f"+{prem_ano(L_mix_f, col)}"
                           f"*IFERROR(Premissas!$B${L_p_fam}/Premissas!$B${L_p_ess},0)"),
              "fator", MULT, cor=CINZA,
              obs="Converte a ARPPU necessária em preço do Essencial, mantendo a razão de "
                  "preço atual entre os três planos. Cuidado: mexer no preço de UM plano em "
                  "Premissas muda a razão, e com ela esta tradução — a ARPPU necessária, que "
                  "vem do custo, não muda.")
    L("Plano Essencial — preço necessário",
      lambda col: f"=IFERROR({col}{psug}/{col}{fator},0)", "pe_sug", BRL2, bold=True,
      destaque=True)
    L("Plano Premium — preço necessário",
      lambda col: (f"={col}{R['pe_sug']}"
                   f"*IFERROR(Premissas!$B${L_p_pre}/Premissas!$B${L_p_ess},0)"), "pp_sug",
      BRL2, bold=True, destaque=True)
    L("Plano Família — preço necessário",
      lambda col: (f"={col}{R['pe_sug']}"
                   f"*IFERROR(Premissas!$B${L_p_fam}/Premissas!$B${L_p_ess},0)"), "pf_sug",
      BRL2, bold=True, destaque=True)
    L("Plano Essencial — preço de hoje, em Premissas",
      lambda col: (f"=Premissas!$B${L_p_ess}"
                   f"*(1+N(Premissas!$B${L_reaj}))^(INDEX('Cenários'!$B$6:${L_FIM}$6,{I[col]})-2026)"),
      "pe_hoje", BRL2, cor=CINZA)
    L("Quantas vezes o preço de hoje",
      lambda col: f"=IFERROR({col}{R['pe_sug']}/{col}{R['pe_hoje']},0)", "mult", MULT, bold=True,
      obs="Acima de 1,0x o preço de hoje não cobre o custo daquele mês. Acima de ~1,5x o preço "
          "deixa de ser vendável e a resposta passa a ser escala, não preço.")
    r += 1

    # =============== 6. TESTAR UM PREÇO ===============
    bloco("6. TESTAR UM PREÇO — digite o valor e veja se ele fecha")
    teste = L("Preço do Essencial que você quer testar", "=39.9", "teste", BRL2,
              entrada=True, unico=True,
              obs="O cálculo do sócio. Premium e Família seguem a mesma proporção de hoje.")
    L("Receita média por assinante a esse preço",
      lambda col: f"={col}{teste}*{col}{fator}", "t_arppu", BRL2)
    L("O que sobra depois de imposto, loja e meio de pagamento",
      lambda col: f"={col}{R['t_arppu']}*{col}{rho}", "t_liq", BRL2)
    L("(−) Custo total por assinante",
      lambda col: f"=-{col}{ctot}", "t_custo", BRL2)
    L("(=) SOBRA POR ASSINANTE, NO MÊS",
      lambda col: f"={col}{R['t_liq']}+{col}{R['t_custo']}", "t_sobra", BRL2, bold=True,
      destaque=True)
    L("Margem EBITDA a esse preço",
      lambda col: f"=IFERROR({col}{R['t_sobra']}/{col}{R['t_liq']},0)", "t_margem", PCT,
      bold=True)
    L("Assinantes necessários, a esse preço, para o mês fechar no zero",
      lambda col: (f"=IF({col}{R['t_liq']}-{col}{cvar}<=0,\"\","
                   f"ROUNDUP({col}{cfix}/({col}{R['t_liq']}-{col}{cvar}),0))"), "t_n", INT,
      bold=True,
      obs="Custo fixo do mês dividido pelo que cada assinante deixa depois do custo variável. "
          "Vazio significa que nenhum volume fecha: a esse preço o assinante não cobre nem o "
          "próprio custo variável.")
    L("Assinantes projetados naquele mês",
      lambda col: f"={col}${pag}", "t_proj", INT, cor=CINZA)
    r += 1
    L("Nuvem por assinante que esse preço suporta — para empatar",
      lambda col: (f"={col}{R['t_liq']}-({col}{R['cv_free']}+{col}{R['cv_painel']}"
                   f"+{col}{R['cv_sup']}+{col}{R['cv_cac']})-{col}{R['cf_unit']}"),
      "t_nuvem_max", BRL2, bold=True, destaque=True,
      obs="A conta ao contrário: fixado o preço, quanto a nuvem pode custar por assinante. "
          "Compare com a linha 'Nuvem — do próprio assinante' no bloco 2.")
    L("Nuvem por assinante que esse preço suporta — com a margem desejada",
      lambda col: (f"={col}{R['t_liq']}*(1-{col}{R['margem']})-({col}{R['cv_free']}"
                   f"+{col}{R['cv_painel']}+{col}{R['cv_sup']}+{col}{R['cv_cac']})"
                   f"-{col}{R['cf_unit']}"), "t_nuvem_marg", BRL2, bold=True, destaque=True,
      obs="Se este número ficar abaixo de zero, o preço testado não paga nem o resto do custo "
          "variável — nuvem zero não salvaria.")
    L("Diferença contra a nuvem que está em Premissas hoje",
      lambda col: f"={col}{R['t_nuvem_marg']}-{col}{R['cv_nuvem']}", "t_nuvem_dif", BRL2,
      bold=True,
      obs="Negativo: a nuvem premissada é mais cara do que o preço testado suporta. "
          "Positivo: sobra folga.")
    r += 1
    L("VEREDICTO",
      lambda col: (f'=IF({col}{R["t_liq"]}-{col}{cvar}<=0,"✗ não fecha com nenhum volume",'
                   f'IF({col}{R["t_sobra"]}>0,"✓ fecha e sobra "&TEXT({col}{R["t_sobra"]},"R$ 0.00")'
                   f'&" por assinante",'
                   f'"✗ faltam "&TEXT({col}{R["t_n"]}-{col}${pag},"#,##0")&" assinantes"))'),
      "t_ver", TXT, bold=True)
    r += 2

    # =============== leitura ===============
    textos = [
        ("COMO LER ESTA ABA", None, True),
        ("O preço não é um número só: ele depende de quantas pessoas estão dividindo o custo "
         "fixo. Compare as quatro colunas e isso fica evidente — o custo variável por "
         "assinante quase não muda, o custo fixo por assinante despenca.", CINZA, False),
        ("Nos primeiros meses nenhum preço de mercado cobre o custo. Isso não é defeito de "
         "precificação: é a conta de uma assinatura mensal com base pequena. Esses meses são "
         "pagos por capital, não por preço. Preço alto no lançamento derruba a conversão e "
         "piora o caixa.", CINZA, False),
        ("Os dois itens que mais mexem no preço são a NUVEM POR ASSINANTE PAGANTE e a COMISSÃO "
         "DA LOJA. Cada R$ 1 de nuvem por assinante exige cerca de R$ 1,39 de preço, porque "
         "imposto, loja e meio de pagamento levam quase 30% do que se cobra.", VERMELHO, False),
        ("Hoje a premissa de nuvem por assinante pagante está em R$ 31,90, escrita na célula "
         "como 6,40 × 5. Nos quatro momentos da tabela, o preço de R$ 39,90 só se paga se essa "
         "nuvem ficar perto de R$ 6,40 — exatamente o número antes da multiplicação. Vale "
         "conferir de onde vem o 5: se for usuário por conta, o custo já está por assinante e "
         "não deveria ser multiplicado; se for cinco anos, é custo acumulado e não mensal.",
         VERMELHO, False),
        ("A linha de conferência da nuvem existe para você poder confiar nesta aba: ela compara "
         "a decomposição daqui com o número que a DRE usa. Se um dia ela sair de zero, alguma "
         "fórmula foi sobrescrita.", CINZA, False),
    ]
    for txt, cor, bold in textos:
        c = ws.cell(r, 1, txt)
        c.font = f(10 if bold else 9, bold, cor or PRETO, italic=not bold)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        ws.row_dimensions[r].height = 18 if bold else 42
        r += 1

    ws.freeze_panes = "B6"
    ws.sheet_properties.tabColor = "1F3864"
    return ws, R
