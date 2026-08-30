# -*- coding: utf-8 -*-
"""Aba Como usar: guia de operacao da planilha."""
from openpyxl.styles import Alignment
from common import *


def build(wb, P, PE):
    ws = wb.create_sheet("Como usar")
    ws.sheet_view.showGridLines = False
    titulo(ws, "COMO USAR ESTA PLANILHA",
           "Leia uma vez. Depois é só mexer nas células azuis e ver tudo recalcular.", largura=8)
    for col, w in zip("ABCDEFG", (3, 36, 96, 3, 3, 3, 3)):
        ws.column_dimensions[col].width = w

    r = 4

    def sec(txt):
        nonlocal r
        r += 1
        c = ws.cell(r, 2, txt)
        c.font = f(12, True, BRANCO)
        c.alignment = Alignment(indent=1, vertical="center")
        for cc in range(2, 4):
            ws.cell(r, cc).fill = FILL_SECAO
        ws.cell(r, 3).font = f(12, True, BRANCO)
        ws.row_dimensions[r].height = 22
        r += 1

    def item(titulo_, texto, cor=PRETO, altura=None):
        nonlocal r
        c = ws.cell(r, 2, titulo_)
        c.font = f(10, True, cor)
        c.alignment = Alignment(indent=1, vertical="top", wrap_text=True)
        c2 = ws.cell(r, 3, texto)
        c2.font = f(10, False, "262626")
        c2.alignment = Alignment(vertical="top", wrap_text=True)
        linhas = max(1, (len(texto) // 105) + 1)
        ws.row_dimensions[r].height = altura or max(17, linhas * 14 + 6)
        ws.cell(r, 2).border = Border(top=Side(style="thin", color="D9D9D9"))
        ws.cell(r, 3).border = Border(top=Side(style="thin", color="D9D9D9"))
        r += 1

    def texto_livre(txt, cor=CINZA, bold=False, altura=None):
        nonlocal r
        c = ws.cell(r, 2, txt)
        c.font = f(10, bold, cor)
        c.alignment = Alignment(indent=1, vertical="top", wrap_text=True)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        linhas = max(1, (len(txt) // 140) + 1)
        ws.row_dimensions[r].height = altura or max(17, linhas * 14 + 4)
        r += 1

    # ------------------------------------------------------------------
    sec("EM 30 SEGUNDOS")
    texto_livre("Só existem dois lugares onde você digita: a aba PREMISSAS (todos os números do "
                "negócio) e a aba PESSOAS (o quadro de pessoal). Todo o resto da planilha é "
                "calculado a partir dessas duas. Comece olhando o RESUMO, volte, ajuste, olhe de novo.",
                PRETO, altura=34)
    item("1. Abra o Resumo",
         "Painel executivo com os três cenários lado a lado e o diagnóstico Go / No-Go. É a foto do modelo.")
    item("2. Mude o cenário",
         "Premissas, controle 1.1: digite 1 (Conservador), 2 (Provável) ou 3 (Agressivo). "
         "As abas de detalhe passam todas a mostrar o cenário escolhido. O Resumo mostra os três sempre.")
    item("3. Ajuste o que quiser",
         "Qualquer célula azul. O modelo inteiro recalcula na hora — não há nada para rodar ou atualizar.")
    item("4. Confira",
         "Na Análise Fluxo há uma linha de verificação que compara o detalhamento com o motor de "
         "cenários. Ela tem que ficar zerada. Se aparecer um número diferente de zero, alguma fórmula "
         "foi sobrescrita por engano.")

    # ------------------------------------------------------------------
    sec("AS CORES DIZEM O QUE É CADA CÉLULA")
    item("Azul", "Você digita. É uma premissa sua.", AZUL_INPUT)
    item("Fundo amarelo", "Premissa-chave: mexer nela desloca bastante o resultado. Comece por essas.",
         "BF8F00")
    item("Preto", "Fórmula calculada dentro da própria aba. Não mexa.")
    item("Verde", "Valor que vem de outra aba. Não mexa — mude na origem.", VERDE_LINK)
    item("Marca vermelha no canto",
         "Passe o mouse: há um comentário com a fonte ou a justificativa do número.", "C00000")

    # ------------------------------------------------------------------
    sec("AS PERGUNTAS MAIS COMUNS E ONDE MEXER")
    item("“E se lançarmos mais tarde?”",
         "Premissas → Ano de lançamento e Mês de lançamento. São dois campos separados; a data e o "
         "mês nº da linha do tempo se ajustam sozinhos, e com eles receita, marketing e conversão.")
    item("“Achamos que 5% de pagantes é otimista.”",
         "Premissas → seção 4 → Taxa de conversão. Digite o patamar de 2026 na coluna C e a evolução "
         "anual na coluna B. Lembre que este é o patamar DE REGIME: nos primeiros meses a conversão "
         "sobe pela rampa, então 2026 sai naturalmente mais tímido.")
    item("“Quanto tempo até converter no patamar cheio?”",
         "Premissas → Rampa de maturação da conversão (meses). Com 6, o app leva 6 meses após o "
         "lançamento para atingir o patamar do ano. Coloque 1 se quiser conversão cheia desde o "
         "primeiro mês.")
    item("“Vamos contratar mais gente / menos gente.”",
         "Aba PESSOAS. Uma linha por papel: quantidade, custo por pessoa, mês de início e mês de fim. "
         "Adicione linhas nos espaços em branco no fim da tabela. O custo total do mês é calculado "
         "sozinho e desce para a DRE e para o fluxo de caixa.")
    item("“Quero ver o modelo só com o que já está contratado.”",
         "Premissas → controle “Considerar o plano de contratações?” → digite 0. Some do modelo tudo "
         "que está marcado como Plano na aba Pessoas, sobrando apenas a equipe do MVP.")
    item("“E se os aportes atrasarem?”",
         "Aba APORTES: mude a data de qualquer linha. Veja o efeito na linha Caixa Acumulado da "
         "Análise Fluxo e no indicador “Caixa mínimo” do Resumo.")
    item("“Quero incluir um investidor novo.”",
         "Aba APORTES. Se ele só coloca dinheiro, preencha uma linha em branco da tabela 1: data, "
         "nome, valor, status e tipo. Se ele também traz receita — uma parceria como a da Boston "
         "Scientific — use a tabela 2, que tem campos para o aporte e para a receita mensal "
         "recorrente, com início e fim. Não é preciso mexer em nenhuma fórmula.")
    item("“E se a Boston fechar?”",
         "Aba Aportes, tabela 2: mude o status da linha da Boston para Confirmado, ou ligue o "
         "interruptor “Considerar acordos em negociação” na seção 7 de Premissas para ver todos os "
         "acordos em negociação de uma vez.")
    item("“Quanto cada sócio tem do capital?”",
         "Aba Aportes, seção 5. É a proporção do dinheiro aportado — ponto de partida da conversa "
         "societária, não percentual de equity, que depende do valuation de cada rodada. Ao incluir "
         "um investidor novo, lembre de acrescentar o nome dele também nesta tabela: a linha "
         "“Capital não atribuído” avisa se você esquecer.")
    item("“Queremos incluir uma nova frente de receita B2B.”",
         "Premissas, seção 5, tabela “Iniciativas de receita B2B”. Uma linha por frente: nome, "
         "categoria (Dados ou Outras), status, modelo de cobrança (valor fixo mensal ou por "
         "usuário do painel), valor e período. As duas primeiras linhas são a venda de dados, já "
         "planejada; as demais estão em branco para vocês preencherem.")
    item("“Por que a receita de dados só aparece em 2028?”",
         "Porque o painel precisa de escala. O modelo zera essa receita enquanto a base que "
         "consentiu compartilhar dados não passa do mínimo definido em Premissas — mesmo que a "
         "data do contrato já tenha chegado. Mexa na taxa de consentimento e no mínimo do painel "
         "para ver o efeito.")
    item("“Vamos mudar os preços dos planos.”",
         "Premissas → seção 3. Preços e mix por plano. A ARPPU implícita aparece logo abaixo do mix, "
         "para você conferir o efeito antes de olhar o resultado.")

    # ------------------------------------------------------------------
    sec("AS ABAS, UMA A UMA")
    abas = [
        ("Como usar", "Este guia.", CINZA),
        ("Resumo",
         "Painel executivo. Três cenários lado a lado, teste Go/No-Go em quatro perguntas objetivas, "
         "métricas de unidade e a lista de pontos de atenção que apareceram na modelagem. "
         "É a aba para mostrar a um investidor.", "1F3864"),
        ("Premissas",
         "Todos os números do negócio, em oito seções: controles, tributação, preços e mix, drivers "
         "por cenário, monetização, custos operacionais, Boston Scientific e notas metodológicas. "
         "É aqui que você passa a maior parte do tempo.", "BF8F00"),
        ("Pessoas",
         "O quadro de pessoal, linha a linha. Separa o que está contratado do que é plano, calcula o "
         "headcount mês a mês e o Fator R — o índice que decide se a empresa fica no Anexo III ou no "
         "Anexo V do Simples.", "BF8F00"),
        ("DRE Projetada",
         "A demonstração de resultado em regime de competência, mês a mês e consolidada por ano. "
         "Receita bruta → deduções → receita líquida → lucro bruto → EBITDA → lucro líquido, com as "
         "margens em cada etapa.", "1F7040"),
        ("Análise Fluxo",
         "O fluxo de caixa, na mesma estrutura da sua planilha de Análise de Investimento: Projeto "
         "(investimentos) → Operacionais → Fluxo de Caixa Livre → VPL, TIR e Payback. Traz também a "
         "linha de verificação e o caixa acumulado.", "1F7040"),
        ("Faturamento",
         "A receita aberta por linha de negócio — cada plano, marketplace, B2B — com as deduções e um "
         "resumo anual.", "2E5C8A"),
        ("Usuários",
         "O funil de usuários e as métricas de unidade: CAC, LTV, LTV/CAC, ARPPU, payback do CAC, "
         "queima de caixa e runway. Traz também o painel de dados — quantos usuários consentiram "
         "compartilhar dados, que é o que a receita B2B de dados monetiza.", "2E5C8A"),
        ("Cenários",
         "O motor. Os três cenários rodam aqui, mês a mês, e todas as outras abas leem daqui. "
         "É a aba mais densa e a única fonte de verdade dos números — consulte, não edite.", "7030A0"),
        ("Investimentos",
         "Cronograma de CAPEX (equipamentos, marca, certificações) e a amortização em 60 meses. O "
         "desenvolvimento do app entra aqui vindo da aba Pessoas.", CINZA),
        ("Aportes",
         "Todo o capital da empresa: lançamentos de aporte, investidores estratégicos que trazem "
         "receita recorrente, resumo do capital, controle do compromisso de R$ 20.000 por fundador "
         "e a proporção do capital por sócio. Todas as tabelas têm linhas em branco para você "
         "incluir investidores novos.", "BF8F00"),
        ("Tributos",
         "Tabelas dos Anexos III e V do Simples Nacional, a tabela ativa conforme o regime escolhido, "
         "a explicação do Fator R e quanto custa por ano cair no anexo errado.", CINZA),
    ]
    for nome, desc, cor in abas:
        item(nome, desc, cor)

    # ------------------------------------------------------------------
    sec("O QUE NÃO MEXER")
    texto_livre("Nada quebra de forma irreversível, mas três coisas causam confusão:", PRETO)
    item("A aba Cenários",
         "É o motor. Se você mudar uma fórmula lá, as outras abas passam a mostrar números que não "
         "batem entre si. A linha de verificação da Análise Fluxo vai acusar.")
    item("As linhas de total",
         "Em negrito e com fundo azul-claro. São somas — mude as parcelas, não o total.")
    item("A coluna TOTAL (última à direita)",
         "Em linhas de saldo — base de usuários, caixa acumulado, pagantes — ela mostra o valor do "
         "último mês, não uma soma. Está anotado ao lado de cada uma.")

    # ------------------------------------------------------------------
    sec("SE ALGUM NÚMERO PARECER ERRADO")
    item("Confira a linha de verificação",
         "Análise Fluxo, logo abaixo do Caixa Acumulado. Tem que estar zerada em todos os meses.")
    item("Confira o mix de planos",
         "Premissas, seção 3: a linha de verificação do mix precisa somar 100% em todos os anos.")
    item("Recalcule",
         "No Excel, F9 força o recálculo. Se você abriu o arquivo e os números parecem antigos, "
         "confira se o cálculo automático está ligado em Fórmulas → Opções de Cálculo.")
    item("Cuidado ao sobrescrever fórmulas",
         "Nas seções com evolução anual (drivers por cenário), as colunas de 2027 a 2030 são "
         "calculadas. Digitar por cima é permitido e às vezes desejável — mas aquele ano deixa de "
         "seguir a taxa de evolução, e os anos seguintes passam a contar a partir do que você digitou.")

    r += 1
    texto_livre("As premissas mais sensíveis do modelo, em ordem: taxa de conversão, churn, CAC e "
                "quadro de pessoal. Se for calibrar alguma coisa com os sócios, comece por essas quatro.",
                "C00000", bold=True, altura=32)
    return ws
