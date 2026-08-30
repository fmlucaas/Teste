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

# Definicao ordenada do bloco: a POSICAO na lista e o offset da linha dentro do
# bloco do cenario. Quem consome (Usuarios, Faturamento, Analise Fluxo, DRE,
# Resumo) referencia pelo NOME em OFF, nunca pelo numero — assim inserir uma
# linha no meio do bloco nao quebra nenhuma outra aba.
#         nome          rotulo                                         fmt   modo      neg.  dest.
LINHAS = [
 ("_hdr",        "",                                                   BRL,  "nada",   False, False),
 ("novos",       "Novos usuários captados",                            INT,  "soma",   False, False),
 ("base_ini",    "Base de usuários — início do mês",                   INT,  "ultimo", False, False),
 ("churn",       "(−) Usuários perdidos (churn)",                      INT,  "soma",   False, False),
 ("base",        "Base de usuários — fim do mês",                      INT,  "ultimo", True,  False),
 ("conv",        "Taxa de conversão (pagantes ÷ base)",                PCT,  "ultimo", False, False),
 ("pag",         "Usuários pagantes",                                  INT,  "ultimo", True,  False),
 ("pag_ess",     "Pagantes — Plano Essencial",                         INT,  "ultimo", False, False),
 ("pag_pre",     "Pagantes — Plano Premium",                           INT,  "ultimo", False, False),
 ("pag_fam",     "Pagantes — Plano Família",                           INT,  "ultimo", False, False),
 ("painel",      "Usuários no painel de dados (com consentimento)",     INT,  "ultimo", False, False),
 ("rec_ess",     "Receita — Plano Essencial",                          BRL,  "soma",   False, False),
 ("rec_pre",     "Receita — Plano Premium",                            BRL,  "soma",   False, False),
 ("rec_fam",     "Receita — Plano Família",                            BRL,  "soma",   False, False),
 ("assinaturas", "Receita de assinaturas",                             BRL,  "soma",   True,  False),
 ("marketplace", "Receita de marketplace (comissões)",                 BRL,  "soma",   False, False),
 ("parcerias",   "Receita B2B — parcerias estratégicas",               BRL,  "soma",   False, False),
 ("dados",       "Receita B2B — venda de dados",                       BRL,  "soma",   False, False),
 ("outras_b2b",  "Receita B2B — outras iniciativas",                   BRL,  "soma",   False, False),
 ("bruta",       "RECEITA BRUTA TOTAL",                                BRL,  "soma",   True,  True),
 ("rbt12",       "RBT12 — base de cálculo do Simples",                 BRL,  "ultimo", False, False),
 ("aliquota",    "Alíquota efetiva de impostos",                       PCT2, "media",  False, False),
 ("impostos",    "(−) Impostos sobre a receita",                       BRL,  "soma",   False, False),
 ("lojas",       "(−) Comissão das lojas de aplicativos",              BRL,  "soma",   False, False),
 ("pgto",        "(−) Taxas de meios de pagamento",                    BRL,  "soma",   False, False),
 ("liquida",     "RECEITA LÍQUIDA",                                    BRL,  "soma",   True,  True),
 ("nuvem",       "(−) Infraestrutura e nuvem",                         BRL,  "soma",   False, False),
 ("suporte",     "(−) Suporte ao cliente",                             BRL,  "soma",   False, False),
 ("pessoal",     "(−) Pessoal (equipe PJ + pró-labore)",               BRL,  "soma",   False, False),
 ("marketing",   "(−) Marketing e aquisição",                          BRL,  "soma",   False, False),
 ("admin",       "(−) Despesas administrativas",                       BRL,  "soma",   False, False),
 ("ebitda",      "EBITDA",                                             BRL,  "soma",   True,  True),
 ("capex",       "(−) Investimentos (CAPEX)",                          BRL,  "soma",   False, False),
 ("fcl",         "FLUXO DE CAIXA LIVRE (FCL)",                         BRL,  "soma",   True,  True),
 ("fcld",        "FCL descontado",                                     BRL,  "soma",   False, False),
 ("fcld_ac",     "FCL descontado acumulado",                           BRL,  "ultimo", False, False),
 ("fcl_ac",      "FCL acumulado (nominal)",                            BRL,  "ultimo", False, False),
 ("flag_eb",     "Marcador — EBITDA já ficou positivo",                INT,  "ultimo", False, False),
 ("aportes",     "(+) Aportes de sócios",                              BRL,  "soma",   False, False),
 ("fluxo",       "Fluxo de caixa do período",                          BRL,  "soma",   False, False),
 ("caixa",       "CAIXA ACUMULADO",                                    BRL,  "ultimo", True,  True),
 ("mk_pb",       "Marcador — mês com FCL acumulado negativo",          INT,  "ultimo", False, False),
 ("mk_pbd",      "Marcador — mês com FCL descontado negativo",         INT,  "ultimo", False, False),
]
OFF      = {nome: i for i, (nome, *_) in enumerate(LINHAS)}


class _Off:
    """Offsets por atributo: O.assinaturas em vez de OFF["assinaturas"].
    Sem aspas, cabe dentro de qualquer f-string."""
    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, v)


O = _Off(OFF)
NL       = len(LINHAS)
LABELS   = [l[1] for l in LINHAS]
FMT      = {i: l[2] for i, l in enumerate(LINHAS)}
MODO     = {i: l[3] for i, l in enumerate(LINHAS)}
NEGRITO  = {i for i, l in enumerate(LINHAS) if l[4]}
DESTAQUE = {i: FILL_TOTAL for i, l in enumerate(LINHAS) if l[5]}


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

        bi, bf = P["b2b_ini"], P["b2b_fim"]

        def _b2b(L, categoria, S, exige_painel):
            """Soma os contratos da tabela B2B ativos no mês, por categoria."""
            cond = (f'(Premissas!$B${bi}:$B${bf}="{categoria}")'
                    f'*((Premissas!$C${bi}:$C${bf}="Planejado")'
                    f'+(Premissas!$C${bi}:$C${bf}="Em estudo")*Premissas!$B${P["inc_estudo"]})'
                    f'*(Premissas!$F${bi}:$F${bf}<={L}${TEMPO})'
                    f'*(Premissas!$G${bi}:$G${bf}>={L}${TEMPO})')
            fixo = (f'SUMPRODUCT({cond}*(Premissas!$D${bi}:$D${bf}="Fixo mensal")'
                    f'*Premissas!$E${bi}:$E${bf})')
            porusu = (f'SUMPRODUCT({cond}*(Premissas!$D${bi}:$D${bf}="Por usuário")'
                      f'*Premissas!$E${bi}:$E${bf})*{L}{S+O.painel}')
            corpo = f'{fixo}+{porusu}'
            if exige_painel:
                return f'=IF({L}{S+O.painel}=0,0,{corpo})'
            return f'={corpo}'

        FORM = {
            O.novos:  lambda i, L: f'=IF({L}${TEMPO}<Premissas!$B${P["lancamento"]},0,{yr(f"novos_{s}", L)})',
            O.base_ini:  lambda i, L: '=0' if i == 1 else f'={prev(i)}{S+O.base}',
            O.churn:  lambda i, L: f'=-{L}{S+O.base_ini}*{yr(f"churn_{s}", L)}',
            O.base:  lambda i, L: f'={L}{S+O.base_ini}+{L}{S+O.churn}+{L}{S+O.novos}',
            O.conv:  lambda i, L: (f'=IF({L}${TEMPO}<Premissas!$B${P["lancamento"]},0,'
                          f'{yr(f"conv_{s}", L)}*MIN(1,MAX(0,'
                          f'({L}${LIDX}-Premissas!$B${P["lanc_idx"]}+1)'
                          f'/Premissas!$B${P["rampa_conv"]})))'),
            O.pag:  lambda i, L: f'=ROUND({L}{S+O.base}*{L}{S+O.conv},0)',
            O.pag_ess:  lambda i, L: f'=ROUND({L}{S+O.pag}*{yr("mix_b", L)},0)',
            O.pag_pre:  lambda i, L: f'=ROUND({L}{S+O.pag}*{yr("mix_i", L)},0)',
            O.pag_fam:  lambda i, L: f'={L}{S+O.pag}-{L}{S+O.pag_ess}-{L}{S+O.pag_pre}',
            O.rec_ess: lambda i, L: (f'={L}{S+O.pag_ess}*Premissas!$B${P["p_basico"]}'
                              f'*(1+Premissas!$B${P["reajuste"]})^({L}${LANO}-2026)'),
            O.rec_pre: lambda i, L: (f'={L}{S+O.pag_pre}*Premissas!$B${P["p_inter"]}'
                              f'*(1+Premissas!$B${P["reajuste"]})^({L}${LANO}-2026)'),
            O.rec_fam: lambda i, L: (f'={L}{S+O.pag_fam}*Premissas!$B${P["p_premium"]}'
                              f'*(1+Premissas!$B${P["reajuste"]})^({L}${LANO}-2026)'),
            O.assinaturas: lambda i, L: f'=SUM({L}{S+O.rec_ess}:{L}{S+O.rec_fam})',
            O.marketplace: lambda i, L: (f'={L}{S+O.base}*{yr("attach_mp", L)}*Premissas!$B${P["ticket_mp"]}'
                              f'*Premissas!$B${P["com_mp"]}'),
            O.parcerias: lambda i, L: f'=Aportes!{L}{A["b2b"]}',
            O.bruta: lambda i, L: f'=SUM({L}{S+O.assinaturas}:{L}{S+O.outras_b2b})',
            # Painel de dados: base × consentimento, zerado enquanto não atingir a escala mínima
            O.painel: lambda i, L: (
                f'=IF(ROUND({L}{S+O.base}*{yr("consent", L)},0)>=Premissas!$B${P["painel_min"]},'
                f'ROUND({L}{S+O.base}*{yr("consent", L)},0),0)'),
            # Receita de dados: contratos da tabela B2B com categoria "Dados".
            # Sem painel comercializável, nenhum contrato fatura, mesmo já iniciado.
            O.dados:      lambda i, L: _b2b(L, "Dados", S, True),
            O.outras_b2b: lambda i, L: _b2b(L, "Outras", S, False),
            O.rbt12: lambda i, L: (f'={L}{S+O.bruta}*12' if i == 1 else
                              (f'=SUM($B{S+O.bruta}:{prev(i)}{S+O.bruta})/{i-1}*12' if i <= 12 else
                               f'=SUM({gcl(COL0+i-13)}{S+O.bruta}:{prev(i)}{S+O.bruta})')),
            O.aliquota: lambda i, L: (
                f'=IF(Premissas!$B${P["regime"]}=3,Premissas!$B${P["lp"]},'
                f'IF({L}{S+O.rbt12}>Premissas!$B${P["teto_simples"]},Premissas!$B${P["lp"]},'
                f'IFERROR(MAX(Tributos!$C${ai},'
                f'(INDEX(Tributos!$C${ai}:$C${af},MATCH({L}{S+O.rbt12},Tributos!$B${ai}:$B${af},1))*{L}{S+O.rbt12}'
                f'-INDEX(Tributos!$D${ai}:$D${af},MATCH({L}{S+O.rbt12},Tributos!$B${ai}:$B${af},1)))/{L}{S+O.rbt12}),'
                f'Tributos!$C${ai})))'),
            O.impostos: lambda i, L: f'=-{L}{S+O.bruta}*{L}{S+O.aliquota}',
            O.lojas: lambda i, L: f'=-{L}{S+O.assinaturas}*Premissas!$B${P["taxa_loja"]}*{yr("share_loja", L)}',
            O.pgto: lambda i, L: (f'=-({L}{S+O.assinaturas}*(1-{yr("share_loja", L)})+{L}{S+O.marketplace})'
                              f'*Premissas!$B${P["taxa_pgto"]}'),
            O.liquida: lambda i, L: f'={L}{S+O.bruta}+SUM({L}{S+O.impostos}:{L}{S+O.pgto})',
            O.nuvem: lambda i, L: (f'=-({L}{S+O.pag}*{yr("cloud_pag", L)}'
                              f'+({L}{S+O.base}-{L}{S+O.pag})*{yr("cloud_free", L)}'
                              f'+{L}{S+O.painel}*Premissas!$B${P["custo_painel"]}'
                              f'+IF({L}${TEMPO}>=Premissas!$B${P["cloud_ini"]},{yr("cloud_fixo", L)},0))'),
            O.suporte: lambda i, L: f'=-{L}{S+O.pag}*{yr("sup_var", L)}',
            O.pessoal: lambda i, L: f'=-Pessoas!{L}{PE["despesa"]}',
            O.marketing: lambda i, L: (f'=-({L}{S+O.novos}*(1-{yr("organico", L)})*{yr(f"cac_{s}", L)}'
                              f'+IF({L}${TEMPO}>=Premissas!$B${P["mkt_ini"]},{yr("mkt_rec", L)},0)'
                              f'+IF({L}${TEMPO}=DATE(YEAR(Premissas!$B${P["mkt_lanc_mes"]}),'
                              f'MONTH(Premissas!$B${P["mkt_lanc_mes"]}),1),Premissas!$B${P["mkt_lanc"]},0))'),
            O.admin: lambda i, L: f'=-IF({L}${TEMPO}>=Premissas!$B${P["adm_ini"]},{yr("admin", L)},0)',
            O.ebitda: lambda i, L: f'=SUM({L}{S+O.liquida}:{L}{S+O.admin})',
            O.capex: lambda i, L: f'=-Investimentos!{L}{I["total"]}',
            O.fcl: lambda i, L: f'={L}{S+O.ebitda}+{L}{S+O.capex}',
            O.fcld: lambda i, L: f'={L}{S+O.fcl}/(1+Premissas!$B${P["tma_m"]})^{L}${LIDX}',
            O.fcld_ac: lambda i, L: f'={L}{S+O.fcld}' if i == 1 else f'={prev(i)}{S+O.fcld_ac}+{L}{S+O.fcld}',
            O.fcl_ac: lambda i, L: f'={L}{S+O.fcl}' if i == 1 else f'={prev(i)}{S+O.fcl_ac}+{L}{S+O.fcl}',
            O.flag_eb: lambda i, L: (f'=IF({L}{S+O.ebitda}>0,1,0)' if i == 1 else
                              f'=IF({prev(i)}{S+O.flag_eb}=1,1,IF({L}{S+O.ebitda}>0,1,0))'),
            O.aportes: lambda i, L: f'=Aportes!{L}{A["total"]}',
            O.fluxo: lambda i, L: f'={L}{S+O.fcl}+{L}{S+O.aportes}',
            O.caixa: lambda i, L: f'={L}{S+O.fluxo}' if i == 1 else f'={prev(i)}{S+O.caixa}+{L}{S+O.fluxo}',
            # Marcadores de payback. A conta antiga era COUNTIF(acumulado<0)+1, que só vale
            # se os meses negativos forem os PRIMEIROS. Com jan-mar/2026 em zero (nem
            # negativos), ela subestimava o payback. Aqui guardamos o índice do mês enquanto
            # o acumulado ainda está negativo; o payback é o maior desses índices, mais um.
            O.mk_pb: lambda i, L: f'=IF({L}{S+O.fcl_ac}<0,{L}${LIDX},0)',
            O.mk_pbd: lambda i, L: f'=IF({L}{S+O.fcld_ac}<0,{L}${LIDX},0)',
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
