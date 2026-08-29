# -*- coding: utf-8 -*-
"""Aba Premissas: todos os inputs do modelo, com registro de linhas."""
import datetime as dt
from openpyxl.styles import Alignment
from openpyxl.comments import Comment
from common import *

ANOS = [2026, 2027, 2028, 2029, 2030]
C_ANO = {a: gcl(3 + i) for i, a in enumerate(ANOS)}   # C..G
CA, CG = "C", "G"

P = {}   # chave -> linha


def _in(ws, lin, col, val, fmt, key=None, chave=False, fonte=None):
    c = ws.cell(lin, col, val)
    c.number_format = fmt
    c.font = f(10, False, AZUL_INPUT)
    c.fill = FILL_INPUT if chave else FILL_SUB
    c.border = BORDA_FINA
    c.alignment = Alignment(horizontal="center")
    if fonte:
        c.comment = Comment(fonte, "Modelo Oppa", height=110, width=330)
    return c


def linha_input(ws, lin, label, valores, fmt, key, nivel=1, chave=False,
                fonte=None, obs=None):
    """Linha com 5 colunas anuais (C..G)."""
    rotulo(ws, lin, label, nivel)
    for i, a in enumerate(ANOS):
        v = valores[i] if isinstance(valores, (list, tuple)) else valores
        _in(ws, lin, 3 + i, v, fmt, chave=chave, fonte=fonte)
    if obs:
        nota(ws, f"I{lin}", obs)
    P[key] = lin
    return lin


def linha_unica(ws, lin, label, valor, fmt, key, nivel=1, chave=False,
                fonte=None, obs=None, formula=False):
    rotulo(ws, lin, label, nivel)
    c = ws.cell(lin, 2, valor)
    c.number_format = fmt
    c.font = f(10, formula, PRETO if formula else AZUL_INPUT)
    c.fill = None if formula else (FILL_INPUT if chave else FILL_SUB)
    c.border = BORDA_FINA
    c.alignment = Alignment(horizontal="center")
    if fonte:
        c.comment = Comment(fonte, "Modelo Oppa", height=120, width=340)
    if obs:
        nota(ws, f"D{lin}", obs)
    P[key] = lin
    return lin


def build(wb):
    ws = wb.create_sheet("Premissas")
    titulo(ws, "OPPA — PREMISSAS DO MODELO",
           "Células AZUIS são entradas editáveis · fundo AMARELO = premissa-chave · "
           "PRETO = fórmula. Passe o mouse sobre as células com marca vermelha para ver a fonte de cada número.",
           largura=12)
    ws.column_dimensions["A"].width = 54
    ws.column_dimensions["B"].width = 16
    for a in ANOS:
        ws.column_dimensions[C_ANO[a]].width = 14
    ws.column_dimensions["H"].width = 3
    ws.column_dimensions["I"].width = 70

    r = 4
    # ------------------------------------------------------------------
    secao(ws, r, "1. CONTROLES DO MODELO", 12); r += 1
    rotulo(ws, r, "Ano →", 0, bold=True)
    for a in ANOS:
        c = ws.cell(r, 3 + ANOS.index(a), a)
        c.font = f(10, True, BRANCO); c.fill = FILL_HEADER
        c.alignment = Alignment(horizontal="center")
        c.number_format = '0'
    P["anos"] = r
    r += 1

    linha_unica(ws, r, "Cenário ativo  (1 = Conservador · 2 = Provável · 3 = Agressivo)",
                2, '0', "cenario", chave=True,
                obs="Troque este número para recalcular todo o modelo no cenário desejado."); r += 1
    rotulo(ws, r, "Cenário ativo — nome", 1)
    c = ws.cell(r, 2, f'=CHOOSE($B${P["cenario"]},"CONSERVADOR","PROVÁVEL","AGRESSIVO")')
    c.font = f(10, True, VERDE_LINK); c.alignment = Alignment(horizontal="center")
    P["cenario_nome"] = r; r += 1

    linha_unica(ws, r, "Data de início do modelo", dt.datetime(2026, 1, 1), DATA, "inicio"); r += 1
    linha_unica(ws, r, "Horizonte de projeção (meses)", 60, INT, "horizonte"); r += 1
    linha_unica(ws, r, "Mês de lançamento do app ao público", dt.datetime(2026, 10, 1), MES,
                "lancamento", chave=True,
                obs="Brief: 'app majoritariamente pronto em Outubro'."); r += 1
    linha_unica(ws, r, "TMA — taxa mínima de atratividade (a.a.)", 0.25, PCT, "tma", chave=True,
                fonte=("Taxa de desconto. A planilha original usava 16% a.a. Para uma startup pré-receita "
                       "a faixa usual é 25%–40% a.a. (custo de capital de venture early-stage). "
                       "25% a.a. adotado como premissa central — ajustável."),
                obs="Original usava 16% a.a.; 25% reflete risco de startup pré-receita."); r += 1
    rotulo(ws, r, "TMA equivalente mensal", 1)
    c = ws.cell(r, 2, f'=(1+$B${P["tma"]})^(1/12)-1'); c.number_format = PCT2
    c.font = f(10, True, PRETO); c.alignment = Alignment(horizontal="center")
    P["tma_m"] = r; r += 1
    linha_unica(ws, r, "Payback desejado (meses) — critério de decisão", 36, INT, "payback_alvo",
                obs="Critério Go/No-Go, herdado da planilha de viabilidade da EMS."); r += 2

    # ------------------------------------------------------------------
    secao(ws, r, "2. TRIBUTAÇÃO", 12); r += 1
    linha_unica(ws, r, "Regime  (1 = Simples Anexo III · 2 = Simples Anexo V · 3 = Lucro Presumido)",
                1, '0', "regime", chave=True,
                fonte=("ATENÇÃO — Fator R. Licenciamento/cessão de uso de software é Anexo V, "
                       "migrando para Anexo III somente se o Fator R (folha de salários + pró-labore "
                       "dos últimos 12 meses ÷ RBT12) for >= 28%. Pagamento a equipe PJ NÃO conta "
                       "como folha para esse cálculo. Veja a aba Tributos."),
                obs="Ver aba Tributos: com equipe PJ o Fator R tende a ficar < 28% → Anexo V."); r += 1
    linha_unica(ws, r, "Alíquota Lucro Presumido / acima do teto do Simples", 0.1633, PCT2, "lp",
                fonte=("Serviços: PIS 0,65% + COFINS 3,00% + ISS 5,00% + IRPJ 4,80% (32% de presunção × 15%) "
                       "+ CSLL 2,88% (32% × 9%) = 16,33% sobre a receita bruta. Sem o adicional de IRPJ. "
                       "ISS varia de 2% a 5% conforme o município."),
                obs="PIS 0,65 + COFINS 3,00 + ISS 5,00 + IRPJ 4,80 + CSLL 2,88 = 16,33%"); r += 1
    linha_unica(ws, r, "Teto do Simples Nacional (RBT12)", 4800000, BRL, "teto_simples",
                obs="LC 123/2006. Acima disso o modelo passa automaticamente ao Lucro Presumido."); r += 2

    # ------------------------------------------------------------------
    secao(ws, r, "3. PREÇOS E MIX DE PLANOS", 12); r += 1
    linha_unica(ws, r, "Plano Básico (R$/mês)", 19.90, BRL2, "p_basico", chave=True); r += 1
    linha_unica(ws, r, "Plano Intermediário (R$/mês)", 39.90, BRL2, "p_inter", chave=True); r += 1
    linha_unica(ws, r, "Plano Premium (R$/mês)", 79.90, BRL2, "p_premium", chave=True); r += 1
    linha_unica(ws, r, "Reajuste anual de preços (a.a.)", 0.045, PCT, "reajuste",
                obs="Reajuste inflacionário aplicado a partir de 2027 (IPCA projetado ~4,5%)."); r += 1

    rotulo(ws, r, "Mix de pagantes por plano (% dos assinantes)", 0, bold=True); r += 1
    linha_input(ws, r, "Plano Básico", [0.75, 0.72, 0.68, 0.64, 0.60], PCT, "mix_b", chave=True,
        fonte=("Em assinatura B2C de ticket baixo a decisão é 'pagar ou não pagar', não 'qual plano' — "
               "o degrau de entrada concentra a base. Referências de mercado mostram o plano individual/"
               "entrada com 60–75% dos assinantes. O efeito compromisso / center-stage (Simonson & Tversky, "
               "1992) puxa parte da base para o plano do meio ao longo do tempo, à medida que o produto "
               "ganha funcionalidades. Por isso o mix migra de 75/20/5 (2026) para 60/28/12 (2030)."),
        obs="Efeito compromisso (Simonson & Tversky, 1992) + padrão de assinatura B2C de ticket baixo."); r += 1
    linha_input(ws, r, "Plano Intermediário", [0.20, 0.22, 0.24, 0.26, 0.28], PCT, "mix_i", chave=True,
        obs="Plano-ponte: cresce conforme o Premium ganha valor percebido (efeito center-stage)."); r += 1
    linha_input(ws, r, "Plano Premium", [0.05, 0.06, 0.08, 0.10, 0.12], PCT, "mix_p", chave=True,
        obs="Fatia menor mas crescente — ancoragem de preço que sustenta o Intermediário."); r += 1
    rotulo(ws, r, "Verificação do mix (deve somar 100%)", 2, italic=True)
    for i, a in enumerate(ANOS):
        L = C_ANO[a]
        c = ws.cell(r, 3 + i, f'=SUM({L}{P["mix_b"]}:{L}{P["mix_p"]})')
        c.number_format = PCT; c.font = f(9, True, PRETO)
        c.alignment = Alignment(horizontal="center")
    P["mix_chk"] = r; r += 1
    rotulo(ws, r, "ARPPU implícita (receita média por assinante pagante)", 2, italic=True)
    for i, a in enumerate(ANOS):
        L = C_ANO[a]
        c = ws.cell(r, 3 + i,
            f'=({L}{P["mix_b"]}*$B${P["p_basico"]}+{L}{P["mix_i"]}*$B${P["p_inter"]}'
            f'+{L}{P["mix_p"]}*$B${P["p_premium"]})*(1+$B${P["reajuste"]})^({L}${P["anos"]}-2026)')
        c.number_format = BRL2; c.font = f(9, True, VERDE_LINK)
        c.alignment = Alignment(horizontal="center")
    P["arppu"] = r; r += 2

    # ------------------------------------------------------------------
    secao(ws, r, "4. DRIVERS POR CENÁRIO", 12); r += 1
    nota(ws, f"A{r}", "Cada driver tem 3 linhas: Conservador / Provável / Agressivo. "
                      "O modelo usa a linha do cenário ativo (controle 1.1).")
    ws[f"A{r}"].alignment = Alignment(indent=1); r += 1

    rotulo(ws, r, "Novos usuários captados por mês (média do ano)", 0, bold=True); r += 1
    linha_input(ws, r, "Conservador", [10860, 13200, 27000, 42000, 57000], INT, "novos_1"); r += 1
    linha_input(ws, r, "Provável",    [18100, 22000, 45000, 70000, 95000], INT, "novos_2", chave=True,
        fonte=("Calibrado para a meta do brief: ~50.000 usuários na base ao final de 2026. "
               "Com lançamento em out/2026 e churn de 8%/mês, 18.100 novos/mês em out+nov+dez "
               "resulta em base de ~50.100 em dez/2026."),
        obs="Calibrado para atingir a meta de ~50.000 usuários em dez/2026."); r += 1
    linha_input(ws, r, "Agressivo",   [25340, 33000, 68000, 105000, 143000], INT, "novos_3"); r += 1

    rotulo(ws, r, "Churn mensal da base de usuários", 0, bold=True); r += 1
    linha_input(ws, r, "Conservador", [0.100, 0.095, 0.090, 0.085, 0.080], PCT, "churn_1"); r += 1
    linha_input(ws, r, "Provável",    [0.080, 0.075, 0.070, 0.065, 0.060], PCT, "churn_2", chave=True,
        fonte=("Benchmarks 2025/2026 de apps de assinatura em Saúde & Fitness: churn mensal de 7% a 10% "
               "(mediana ~9,2%); os melhores apps ficam abaixo de 5%. Adotado 8% em 2026 caindo a 6% em 2030, "
               "assumindo que monitoramento de saúde retém melhor que fitness (necessidade médica, não motivação). "
               "Fonte: RevenueCat State of Subscription Apps 2025; Business of Apps Health & Fitness Benchmarks."),
        obs="Saúde & Fitness: 7–10%/mês de churn (mediana 9,2%). Monitoramento retém melhor que fitness."); r += 1
    linha_input(ws, r, "Agressivo",   [0.060, 0.055, 0.050, 0.048, 0.045], PCT, "churn_3"); r += 1

    rotulo(ws, r, "Taxa de conversão (pagantes ÷ base ativa)", 0, bold=True); r += 1
    linha_input(ws, r, "Conservador", [0.030, 0.035, 0.038, 0.042, 0.045], PCT, "conv_1"); r += 1
    linha_input(ws, r, "Provável",    [0.050, 0.055, 0.060, 0.065, 0.070], PCT, "conv_2", chave=True,
        fonte=("Premissa do brief: 5% de pagantes. Benchmarks de freemium: mediana 2,2%–2,6%, faixa típica "
               "2%–5%, quartil superior 5%–8%. 5% posiciona a Oppa no quartil superior — defensável para "
               "app de saúde com feature paga clara (histórico de dados), mas é premissa agressiva. "
               "Fontes: RevenueCat 2025; Userpilot; Geneo Freemium Benchmarks."),
        obs="Premissa do brief (5%). Benchmark freemium: mediana 2,2%; quartil superior 5–8%."); r += 1
    linha_input(ws, r, "Agressivo",   [0.070, 0.080, 0.085, 0.090, 0.100], PCT, "conv_3"); r += 1

    rotulo(ws, r, "CAC — custo de aquisição por novo usuário (R$)", 0, bold=True); r += 1
    linha_input(ws, r, "Conservador", [4.00, 5.00, 6.00, 7.00, 8.00], BRL2, "cac_1"); r += 1
    linha_input(ws, r, "Provável",    [2.50, 3.00, 3.50, 4.00, 4.50], BRL2, "cac_2", chave=True,
        fonte=("CPI (custo por instalação) no Brasil em Meta/Google Ads para apps de saúde: R$ 1,50–4,00. "
               "Adotado R$ 2,50 em 2026, subindo até R$ 4,50 em 2030 conforme se esgotam as audiências baratas. "
               "A agência da Shaiane reduz o custo de produção criativa, não o custo de mídia."),
        obs="CPI Brasil saúde: R$ 1,50–4,00. Sobe com a escala (audiências baratas se esgotam)."); r += 1
    linha_input(ws, r, "Agressivo",   [1.50, 1.80, 2.20, 2.60, 3.00], BRL2, "cac_3"); r += 1

    linha_input(ws, r, "Aquisição orgânica (% dos novos usuários, sem custo de mídia)",
                [0.30, 0.32, 0.35, 0.38, 0.40], PCT, "organico", nivel=0,
        obs="Boca a boca + conteúdo da agência da Shaiane. Reduz a fatia de novos usuários paga com mídia."); r += 2

    # ------------------------------------------------------------------
    secao(ws, r, "5. MONETIZAÇÃO — CANAIS E TAXAS", 12); r += 1
    linha_unica(ws, r, "Taxa das lojas de aplicativos (App Store / Google Play)", 0.15, PCT, "taxa_loja",
        chave=True,
        fonte=("Google Play cobra 15% em TODAS as assinaturas auto-renováveis desde o 1º dia. "
               "Apple cobra 30%, reduzidos a 15% no App Store Small Business Program (receita anual < US$ 1 mi) "
               "ou a partir do 2º ano de assinatura. Acima de US$ 1 mi/ano a Apple volta a 30% — "
               "risco a monitorar a partir de 2028."),
        obs="Google Play 15% desde o 1º dia; Apple 15% no Small Business Program (< US$ 1 mi/ano)."); r += 1
    linha_input(ws, r, "% da receita de assinaturas cobrada pelas lojas",
                [0.85, 0.80, 0.75, 0.72, 0.70], PCT, "share_loja",
        obs="Migração gradual para checkout web/PIX próprio, que não paga comissão de loja."); r += 1
    linha_unica(ws, r, "Taxa de meio de pagamento (venda direta web/PIX)", 0.045, PCT, "taxa_pgto",
        obs="Média ponderada cartão (~4,99%) e PIX (~1,0%)."); r += 1

    rotulo(ws, r, "Marketplace de dispositivos", 0, bold=True); r += 1
    linha_unica(ws, r, "Comissão média sobre GMV", 0.10, PCT, "com_mp", chave=True,
        obs="Brief: faixa de 5% a 15% de comissão. Adotado o ponto médio."); r += 1
    linha_unica(ws, r, "Ticket médio do dispositivo (R$)", 350.00, BRL2, "ticket_mp",
        obs="Oxímetro ~R$150, smartwatch de saúde ~R$400, balança/pressão ~R$250."); r += 1
    linha_input(ws, r, "Taxa de compra mensal (% da base ativa que compra no mês)",
                [0.000, 0.0015, 0.0025, 0.0040, 0.0050], '0.00%', "attach_mp",
        obs="Marketplace só entra no ar em 2027. Compra de device é evento raro e de alto ticket."); r += 2

    # ------------------------------------------------------------------
    secao(ws, r, "6. CUSTOS OPERACIONAIS", 12); r += 1
    linha_unica(ws, r, "Início dos custos de nuvem", dt.datetime(2026, 5, 1), MES, "cloud_ini",
        obs="Primeiro gasto real registrado: R$ 532,29 em 04/05/2026."); r += 1
    linha_input(ws, r, "Nuvem — custo fixo mensal (R$)", [600, 2500, 8000, 18000, 30000], BRL, "cloud_fixo",
        fonte=("Ancorado no gasto real de R$ 532,29 em 04/05/2026 (pré-lançamento). "
               "Cresce com ambientes, observabilidade, banco gerenciado e redundância."),
        obs="Base: gasto real de R$ 532,29 em 04/05/2026."); r += 1
    linha_input(ws, r, "Nuvem — custo variável por usuário PAGANTE (R$/mês)",
                [1.50, 1.35, 1.15, 1.00, 0.90], BRL2, "cloud_pag", chave=True,
        fonte=("Usuário pagante tem histórico: série temporal de sinais vitais armazenada e consultável. "
               "Custo de banco time-series + storage + processamento. Cai com escala (compressão, "
               "tiering de armazenamento, contratos de volume)."),
        obs="Só o pagante gera histórico (série temporal armazenada) — premissa do brief."); r += 1
    linha_input(ws, r, "Nuvem — custo variável por usuário GRATUITO (R$/mês)",
                [0.02, 0.02, 0.018, 0.015, 0.015], BRL2, "cloud_free",
        fonte=("O brief assume custo ~zero para o usuário gratuito, pois não há histórico. "
               "Não é exatamente zero: a ingestão em tempo real e as chamadas de API consomem compute "
               "mesmo sem persistência. R$ 0,02/mês (R$ 0,24/ano) é o custo residual dessa pipeline."),
        obs="Não é zero: ingestão em tempo real e API consomem compute mesmo sem persistir histórico."); r += 1
    linha_input(ws, r, "Suporte — custo por usuário pagante (R$/mês)",
                [0.35, 0.35, 0.30, 0.28, 0.25], BRL2, "sup_var",
        obs="Autoatendimento + chatbot; humano só na exceção."); r += 1
    linha_input(ws, r, "Suporte — custo fixo mensal (R$)", [0, 3000, 15000, 45000, 90000], BRL, "sup_fixo"); r += 1

    linha_unica(ws, r, "Início da equipe PJ recorrente", dt.datetime(2026, 11, 1), MES, "equipe_ini",
        obs="Após a entrega do MVP (out/2026), a equipe passa de projeto para manutenção/evolução."); r += 1
    linha_input(ws, r, "Equipe PJ recorrente (R$/mês)", [4000, 25000, 90000, 220000, 420000], BRL, "equipe",
        chave=True,
        fonte=("O orçamento de R$ 21.000 do brief é o custo TOTAL do MVP (ago–out/2026) e está na aba "
               "Investimentos. Esta linha é a equipe recorrente pós-lançamento, que o brief não dimensiona. "
               "PREMISSA A VALIDAR: uma base de 50 mil usuários exige engenharia contínua."),
        obs="⚠ Não está no brief. Escalonado com o porte da operação — em 2030 equivale a ~14% da receita."); r += 1
    linha_unica(ws, r, "Início do pró-labore dos sócios", dt.datetime(2027, 1, 1), MES, "prolab_ini"); r += 1
    linha_input(ws, r, "Pró-labore total dos sócios (R$/mês)", [0, 15000, 40000, 80000, 140000], BRL, "prolab",
        obs="Zero em 2026 (sócios sem retirada). Também é a base do Fator R — ver aba Tributos."); r += 1

    linha_unica(ws, r, "Início das despesas administrativas", dt.datetime(2026, 4, 1), MES, "adm_ini",
        obs="A partir da constituição da empresa / primeiro aporte (16/04/2026)."); r += 1
    linha_input(ws, r, "Administrativas (contabilidade, jurídico, ferramentas) — R$/mês",
                [1500, 6000, 25000, 60000, 110000], BRL, "admin"); r += 1
    linha_input(ws, r, "Marketing recorrente — agência/conteúdo (R$/mês)",
                [3000, 15000, 60000, 140000, 250000], BRL, "mkt_rec",
        fonte=("Reduzido pela entrada da Shaiane, sócia com agência de marketing própria, que absorve "
               "produção criativa e gestão. Não elimina o custo: ferramentas, mídia de conteúdo, "
               "influenciadores e produção seguem sendo desembolso."),
        obs="Reduzido pela agência da Shaiane, mas não eliminado (ferramentas, mídia, produção)."); r += 1
    linha_unica(ws, r, "Início do marketing recorrente", dt.datetime(2026, 10, 1), MES, "mkt_ini"); r += 1
    linha_unica(ws, r, "Propaganda de lançamento — valor único (R$)", 25000, BRL, "mkt_lanc"); r += 1
    linha_unica(ws, r, "Mês da propaganda de lançamento", dt.datetime(2026, 10, 1), MES, "mkt_lanc_mes"); r += 2

    # ------------------------------------------------------------------
    secao(ws, r, "7. BOSTON SCIENTIFIC (cenário opcional — desligado por padrão)", 12); r += 1
    linha_unica(ws, r, "Acordo ativo?  (1 = Sim · 0 = Não)", 0, '0', "boston_on", chave=True,
        fonte=("Acordo NÃO confirmado. Mantido fora do caso-base para que a viabilidade não dependa "
               "de receita não contratada. Ligue esta célula (=1) para dimensionar o upside."),
        obs="⚠ Desligado por padrão. Mude para 1 para ver o impacto do acordo."); r += 1
    linha_unica(ws, r, "Aporte da Boston Scientific (R$)", 500000, BRL, "boston_val",
        obs="Brief: 'casa dos seis dígitos'. Adotado o ponto médio da faixa R$ 100 mil – R$ 999 mil."); r += 1
    linha_unica(ws, r, "Mês do aporte", dt.datetime(2027, 7, 1), MES, "boston_mes"); r += 1
    linha_unica(ws, r, "Receita B2B recorrente (R$/mês, a partir do mês do aporte)", 80000, BRL,
                "boston_rec",
        obs="Monitoramento de pacientes pós-operatórios. Contrapartida: exclusividade B2B hospitalar."); r += 2

    # ------------------------------------------------------------------
    secao(ws, r, "8. NOTAS METODOLÓGICAS", 12); r += 1
    notas = [
        "FCL (Fluxo de Caixa Livre) NÃO inclui aportes de sócios. Aporte é financiamento, não geração de "
        "caixa — incluí-lo infla VPL e TIR artificialmente. A planilha original somava o aporte à receita; "
        "aqui os dois fluxos estão separados (ver aba Análise Fluxo).",
        "VPL, TIR e Payback são calculados sobre o FCL. Caixa Acumulado e Runway usam FCL + Aportes.",
        "Rendimento financeiro do caixa não é considerado (premissa conservadora).",
        "Investimentos (desenvolvimento do app, equipamentos, marca, certificações) saem do caixa no mês do "
        "desembolso e são amortizados linearmente em 60 meses na DRE — por isso EBITDA da DRE e FCL diferem.",
        "Propaganda de lançamento é tratada como despesa de marketing (regime de competência), não como "
        "investimento — diferente da planilha original, que a colocava em 'Projeto'.",
        "O modelo troca automaticamente do Simples para o Lucro Presumido quando o RBT12 ultrapassa "
        "R$ 4,8 milhões, sem intervenção manual.",
        "Todas as células azuis são editáveis; o modelo inteiro recalcula a partir delas.",
    ]
    for n in notas:
        c = ws.cell(r, 1, "•  " + n)
        c.font = f(9, False, CINZA)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
        ws.row_dimensions[r].height = 28
        r += 1

    return ws, P
