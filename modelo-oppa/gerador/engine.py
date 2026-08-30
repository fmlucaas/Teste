# -*- coding: utf-8 -*-
"""Aba Cenarios: o motor do modelo. Tres blocos mensais identicos, um por cenario."""
from openpyxl.styles import Alignment, PatternFill
from common import *

TEMPO = 4          # linha das datas
LIDX  = TEMPO + 1  # linha do indice do mes
LANO  = TEMPO + 2  # linha do ano
LIDXA = TEMPO + 3  # linha do indice do ano (auxiliar)
BLOCOS = [9, 55, 101]
NOMES = ["CONSERVADOR", "PROVÁVEL", "AGRESSIVO"]
CORES = ["C00000", "1F3864", "1F7040"]

LABELS = [
    "",                                            # 0 header
    "Novos usuários captados",                     # 1
    "Base de usuários — início do mês",            # 2
    "(−) Usuários perdidos (churn)",               # 3
    "Base de usuários — fim do mês",               # 4
    "Taxa de conversão (pagantes ÷ base)",         # 5
    "Usuários pagantes",                           # 6
    "Pagantes — Plano Essencial",                     # 7
    "Pagantes — Plano Premium",              # 8
    "Pagantes — Plano Família",                    # 9
    "Receita — Plano Essencial",                      # 10
    "Receita — Plano Premium",               # 11
    "Receita — Plano Família",                     # 12
    "Receita de assinaturas",                      # 13
    "Receita de marketplace (comissões)",          # 14
    "Receita B2B — parcerias estratégicas",        # 15
    "RECEITA BRUTA TOTAL",                         # 16
    "RBT12 — base de cálculo do Simples",          # 17
    "Alíquota efetiva de impostos",                # 18
    "(−) Impostos sobre a receita",                # 19
    "(−) Comissão das lojas de aplicativos",       # 20
    "(−) Taxas de meios de pagamento",             # 21
    "RECEITA LÍQUIDA",                             # 22
    "(−) Infraestrutura e nuvem",                  # 23
    "(−) Suporte ao cliente",                      # 24
    "(−) Pessoal (equipe PJ + pró-labore)",        # 25
    "(−) Marketing e aquisição",                   # 26
    "(−) Despesas administrativas",                # 27
    "EBITDA",                                      # 28
    "(−) Investimentos (CAPEX)",                   # 29
    "FLUXO DE CAIXA LIVRE (FCL)",                  # 30
    "FCL descontado",                              # 31
    "FCL descontado acumulado",                    # 32
    "FCL acumulado (nominal)",                     # 33
    "Marcador — EBITDA já ficou positivo",         # 34
    "(+) Aportes de sócios",                       # 35
    "Fluxo de caixa do período",                   # 36
    "CAIXA ACUMULADO",                             # 37
    "Marcador — mês com FCL acumulado negativo",    # 38
    "Marcador — mês com FCL descontado negativo",   # 39
]
NL = len(LABELS)   # 38

FMT = {i: BRL for i in range(NL)}
for i in (1, 2, 3, 4, 6, 7, 8, 9, 38, 39):
    FMT[i] = INT
FMT[5] = PCT
FMT[18] = PCT2
FMT[34] = INT
FMT[17] = BRL

MODO = {}                      # como consolidar na coluna TOTAL
for i in range(NL):
    MODO[i] = "soma"
for i in (2, 4, 5, 6, 7, 8, 9, 17, 18, 32, 33, 34, 37, 38, 39):
    MODO[i] = "ultimo"
MODO[0] = "nada"
MODO[18] = "media"

DESTAQUE = {16: FILL_TOTAL, 22: FILL_TOTAL, 28: FILL_TOTAL, 30: FILL_TOTAL, 37: FILL_TOTAL}
NEGRITO = {4, 6, 13, 16, 22, 28, 30, 37}


def build(wb, P, A, I, T, PE):
    ws = wb.create_sheet("Cenários")
    titulo(ws, "MOTOR DE CENÁRIOS — CONSERVADOR · PROVÁVEL · AGRESSIVO",
           "Os três cenários rodam sempre, lado a lado. As demais abas mostram em detalhe o cenário "
           "selecionado em Premissas. Esta aba é a única fonte de verdade dos números.")
    largura_padrao(ws, col_a=42)
    cabecalho_tempo(ws, linha_data=TEMPO, congelar="B9", anos_row=P["anos"])

    ANOS_R = P["anos"]

    def yr(key, L):
        """Driver anual `key` na coluna L, via indice de ano pre-calculado."""
        r = P[key]
        return f'INDEX(Premissas!$C${r}:$G${r},{L}${LIDXA})' 

    ai, af = T["ativa_ini"], T["ativa_fim"]

    for s, S in enumerate(BLOCOS, start=1):
        # ---- cabecalho do bloco ---------------------------------------
        c = ws.cell(S, 1, f"CENÁRIO {s} — {NOMES[s-1]}")
        c.font = f(11, True, BRANCO)
        fill = PatternFill("solid", fgColor=CORES[s-1])
        for cc in range(1, COL_PCT + 1):
            ws.cell(S, cc).fill = fill
        ws.row_dimensions[S].height = 20

        for off in range(1, NL):
            r = S + off
            rotulo(ws, r, LABELS[off], 1 if off not in NEGRITO else 0,
                   bold=(off in NEGRITO),
                   color=CINZA if off == 34 else PRETO)

        def prev(i):
            return gcl(COL0 + i - 2)

        FORM = {
            1:  lambda i, L: f'=IF({L}${TEMPO}<Premissas!$B${P["lancamento"]},0,{yr(f"novos_{s}", L)})',
            2:  lambda i, L: '=0' if i == 1 else f'={prev(i)}{S+4}',
            3:  lambda i, L: f'=-{L}{S+2}*{yr(f"churn_{s}", L)}',
            4:  lambda i, L: f'={L}{S+2}+{L}{S+3}+{L}{S+1}',
            5:  lambda i, L: (f'=IF({L}${TEMPO}<Premissas!$B${P["lancamento"]},0,'
                          f'{yr(f"conv_{s}", L)}*MIN(1,MAX(0,'
                          f'({L}${LIDX}-Premissas!$B${P["lanc_idx"]}+1)'
                          f'/Premissas!$B${P["rampa_conv"]})))'),
            6:  lambda i, L: f'=ROUND({L}{S+4}*{L}{S+5},0)',
            7:  lambda i, L: f'=ROUND({L}{S+6}*{yr("mix_b", L)},0)',
            8:  lambda i, L: f'=ROUND({L}{S+6}*{yr("mix_i", L)},0)',
            9:  lambda i, L: f'={L}{S+6}-{L}{S+7}-{L}{S+8}',
            10: lambda i, L: (f'={L}{S+7}*Premissas!$B${P["p_basico"]}'
                              f'*(1+Premissas!$B${P["reajuste"]})^({L}${LANO}-2026)'),
            11: lambda i, L: (f'={L}{S+8}*Premissas!$B${P["p_inter"]}'
                              f'*(1+Premissas!$B${P["reajuste"]})^({L}${LANO}-2026)'),
            12: lambda i, L: (f'={L}{S+9}*Premissas!$B${P["p_premium"]}'
                              f'*(1+Premissas!$B${P["reajuste"]})^({L}${LANO}-2026)'),
            13: lambda i, L: f'=SUM({L}{S+10}:{L}{S+12})',
            14: lambda i, L: (f'={L}{S+4}*{yr("attach_mp", L)}*Premissas!$B${P["ticket_mp"]}'
                              f'*Premissas!$B${P["com_mp"]}'),
            15: lambda i, L: f'=Aportes!{L}{A["b2b"]}',
            16: lambda i, L: f'=SUM({L}{S+13}:{L}{S+15})',
            17: lambda i, L: (f'={L}{S+16}*12' if i == 1 else
                              (f'=SUM($B{S+16}:{prev(i)}{S+16})/{i-1}*12' if i <= 12 else
                               f'=SUM({gcl(COL0+i-13)}{S+16}:{prev(i)}{S+16})')),
            18: lambda i, L: (
                f'=IF(Premissas!$B${P["regime"]}=3,Premissas!$B${P["lp"]},'
                f'IF({L}{S+17}>Premissas!$B${P["teto_simples"]},Premissas!$B${P["lp"]},'
                f'IFERROR(MAX(Tributos!$C${ai},'
                f'(INDEX(Tributos!$C${ai}:$C${af},MATCH({L}{S+17},Tributos!$B${ai}:$B${af},1))*{L}{S+17}'
                f'-INDEX(Tributos!$D${ai}:$D${af},MATCH({L}{S+17},Tributos!$B${ai}:$B${af},1)))/{L}{S+17}),'
                f'Tributos!$C${ai})))'),
            19: lambda i, L: f'=-{L}{S+16}*{L}{S+18}',
            20: lambda i, L: f'=-{L}{S+13}*Premissas!$B${P["taxa_loja"]}*{yr("share_loja", L)}',
            21: lambda i, L: (f'=-({L}{S+13}*(1-{yr("share_loja", L)})+{L}{S+14})'
                              f'*Premissas!$B${P["taxa_pgto"]}'),
            22: lambda i, L: f'={L}{S+16}+SUM({L}{S+19}:{L}{S+21})',
            23: lambda i, L: (f'=-({L}{S+6}*{yr("cloud_pag", L)}'
                              f'+({L}{S+4}-{L}{S+6})*{yr("cloud_free", L)}'
                              f'+IF({L}${TEMPO}>=Premissas!$B${P["cloud_ini"]},{yr("cloud_fixo", L)},0))'),
            24: lambda i, L: f'=-{L}{S+6}*{yr("sup_var", L)}',
            25: lambda i, L: f'=-Pessoas!{L}{PE["despesa"]}',
            26: lambda i, L: (f'=-({L}{S+1}*(1-{yr("organico", L)})*{yr(f"cac_{s}", L)}'
                              f'+IF({L}${TEMPO}>=Premissas!$B${P["mkt_ini"]},{yr("mkt_rec", L)},0)'
                              f'+IF({L}${TEMPO}=DATE(YEAR(Premissas!$B${P["mkt_lanc_mes"]}),'
                              f'MONTH(Premissas!$B${P["mkt_lanc_mes"]}),1),Premissas!$B${P["mkt_lanc"]},0))'),
            27: lambda i, L: f'=-IF({L}${TEMPO}>=Premissas!$B${P["adm_ini"]},{yr("admin", L)},0)',
            28: lambda i, L: f'=SUM({L}{S+22}:{L}{S+27})',
            29: lambda i, L: f'=-Investimentos!{L}{I["total"]}',
            30: lambda i, L: f'={L}{S+28}+{L}{S+29}',
            31: lambda i, L: f'={L}{S+30}/(1+Premissas!$B${P["tma_m"]})^{L}${LIDX}',
            32: lambda i, L: f'={L}{S+31}' if i == 1 else f'={prev(i)}{S+32}+{L}{S+31}',
            33: lambda i, L: f'={L}{S+30}' if i == 1 else f'={prev(i)}{S+33}+{L}{S+30}',
            34: lambda i, L: (f'=IF({L}{S+28}>0,1,0)' if i == 1 else
                              f'=IF({prev(i)}{S+34}=1,1,IF({L}{S+28}>0,1,0))'),
            35: lambda i, L: f'=Aportes!{L}{A["total"]}',
            36: lambda i, L: f'={L}{S+30}+{L}{S+35}',
            37: lambda i, L: f'={L}{S+36}' if i == 1 else f'={prev(i)}{S+37}+{L}{S+36}',
            # Marcadores de payback. A conta antiga era COUNTIF(acumulado<0)+1, que só vale
            # se os meses negativos forem os PRIMEIROS. Com jan-mar/2026 em zero (nem
            # negativos), ela subestimava o payback. Aqui guardamos o índice do mês enquanto
            # o acumulado ainda está negativo; o payback é o maior desses índices, mais um.
            38: lambda i, L: f'=IF({L}{S+33}<0,{L}${LIDX},0)',
            39: lambda i, L: f'=IF({L}{S+32}<0,{L}${LIDX},0)',
        }

        for off in range(1, NL):
            r = S + off
            fmt = FMT[off]
            bold = off in NEGRITO
            for i in range(1, N_MESES + 1):
                L = col_mes(i)
                cel = ws[f"{L}{r}"]
                cel.value = FORM[off](i, L)
                cel.number_format = fmt
                cel.font = f(9, bold, CINZA if off == 34 else PRETO)
                if off in DESTAQUE:
                    cel.fill = DESTAQUE[off]
            # coluna TOTAL
            ct = ws[f"{L_TOT}{r}"]
            if MODO[off] == "soma":
                ct.value = f"=SUM(B{r}:{L_FIM}{r})"
            elif MODO[off] == "ultimo":
                ct.value = f"={L_FIM}{r}"
            elif MODO[off] == "media":
                ct.value = f"=IFERROR(-{L_TOT}{S+19}/{L_TOT}{S+16},0)"
            ct.number_format = fmt
            ct.font = f(9, True, PRETO)
            ct.fill = FILL_TOTAL
        # legenda da coluna TOTAL para linhas de estoque
        for off in (2, 4, 6, 7, 8, 9, 17, 32, 33, 37):
            nota(ws, f"{L_PCT}{S+off}", "Saldo no último mês (dez/2030), não soma.")
        for off in (38, 39):
            nota(ws, f"{L_PCT}{S+off}", "Auxiliar do payback: guarda o nº do mês enquanto o "
                                        "acumulado está negativo. O payback é o maior valor, mais um.")
        nota(ws, f"{L_PCT}{S+18}", "Alíquota efetiva média ponderada do período.")

    return ws, BLOCOS, NL
