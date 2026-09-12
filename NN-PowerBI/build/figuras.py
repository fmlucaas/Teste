# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui_kit import *

FIGS = {}
def reg(nome, legenda):
    def deco(fn):
        FIGS[nome] = (fn, legenda); return fn
    return deco

# =====================================================================
@reg("01_mapa_tela", "As cinco áreas da tela do Power BI Desktop")
def f01():
    f = Fig(1100, 760)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Inserir","Modelagem","Exibição","Otimizar","Ajuda"], 1)
    f.rect((0,y,f.w,y+76), fill=CHROME, outline=BORDA)
    for i,(r,ic) in enumerate([("Colar","📋"),("Obter\ndados","▤"),("Pasta de\ntrabalho do Excel","▦"),
                    ("Transformar\ndados","⚙"),("Atualizar","⟳"),("Novo\nvisual","▥"),
                    ("Nova\nmedida","∑"),("Publicar","⇧")]):
        f.botao_faixa(14+i*112, y+7, r, icone=ic)
    topo = y+76

    # barra de modos (esquerda)
    UTIL = f.h - 118
    f.rect((0,topo,54,UTIL), fill=(247,247,247), outline=BORDA)
    for i,(ic,nome) in enumerate([("▥","Relatório"),("▦","Tabela"),("⛓","Modelo")]):
        cy = topo+22+i*62
        cor = ACENTO if i==0 else TEXTO3
        f.txtc((6,cy,48,cy+26), ic, 21, cor=cor)
        f.txtc((0,cy+24,54,cy+38), nome, 8, cor=cor)
        if i==0: f.rect((0,cy-6,4,cy+40), fill=ACENTO)

    # tela do relatório
    f.rect((54,topo,700,UTIL), fill=(234,236,240))
    f.rr((78,topo+22,676,UTIL-28), 6, fill=(255,255,255), outline=BORDA)
    f.txtc((78,topo+40,676,topo+70), "área do relatório (as páginas)", 14, cor=TEXTO3)
    # abas de página
    for i,p in enumerate(["1. Visão Geral","2. Carregamento","+"]):
        x = 78+i*128
        f.rr((x,UTIL-24,x+118 if i<2 else x+30,UTIL-2), 3,
             fill=(255,255,255) if i==0 else (243,243,243), outline=BORDA)
        f.txtc((x,UTIL-24,x+118 if i<2 else x+30,UTIL-2), p, 10, i==0)

    f.painel((700,topo,890,UTIL), "Visualizações",
             ["Tipos de gráfico:","  (os ícones)","","Campos do visual:","  Eixo X","  Eixo Y","  Legenda"])
    f.painel((890,topo,1100,UTIL), "Dados",
             ["▾ Mapeamento","  Molécula","  Status NN","  Situação","▾ Carregamento Mensal",
              "  Status no Mês","▾ Calendário","  Ano-Mês"])

    f.marca((0,30,f.w,topo), 1, dx=f.w/2, dy=-2)
    f.marca((0,topo,54,UTIL), 2, dx=27, dy=UTIL-topo-14)
    f.marca((60,topo+6,694,UTIL-6), 3, dx=317, dy=-2)
    f.marca((700,topo,890,UTIL), 4, dx=95, dy=UTIL-topo-14)
    f.marca((890,topo,1100,UTIL), 5, dx=105, dy=UTIL-topo-14)
    f.legenda(["FAIXA DE OPÇÕES — os menus e botões do topo. Muda conforme a aba escolhida.",
               "BARRA DE MODOS — alterna entre Relatório (gráficos), Tabela (dados) e Modelo (ligações).",
               "ÁREA DO RELATÓRIO — onde os gráficos ficam. As abas de baixo são as páginas.",
               "PAINEL VISUALIZAÇÕES — escolhe o tipo de gráfico e define quais campos ele usa.",
               "PAINEL DADOS — a lista das tabelas e colunas. É daqui que você arrasta os campos."])
    return f

# =====================================================================
@reg("02_opcoes_menu", "Como chegar na janela de Opções")
def f02():
    f = Fig(1100, 430)
    f.titulo_janela("Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Inserir","Modelagem"], 0)
    # menu Arquivo aberto
    f.rect((0,y,300,f.h), fill=(250,250,250), outline=BORDA)
    itens = ["Página Inicial","Novo","Abrir relatório","Salvar","Salvar como",
             "Obter dados","Importar","Exportar","Publicar","Opções e configurações"]
    for i,it in enumerate(itens):
        cy = y+14+i*34
        sel = it=="Opções e configurações"
        if sel: f.rect((6,cy-4,294,cy+28), fill=(230,240,250))
        f.txt((22,cy+12), it, 13, sel, TEXTO if sel else TEXTO2, anchor="lm")
    # submenu
    f.rect((300,y+300,560,y+374), fill=(255,255,255), outline=BORDA)
    f.rect((306,y+306,554,y+336), fill=(230,240,250))
    f.txt((318,y+321), "Opções", 13, True, TEXTO, anchor="lm")
    f.txt((318,y+355), "Configurações da fonte de dados", 13, False, TEXTO2, anchor="lm")
    f.marca((8,y+12,60,y+46), 1, dx=-16, dy=0)
    f.marca((6,y+318,294,y+350), 2, dx=-16, dy=0)
    f.marca((306,y+306,554,y+336), 3, dx=-16, dy=0)
    f.legenda(["Clique em Arquivo (o primeiro da faixa, canto superior esquerdo)",
               "Clique em Opções e configurações",
               "Clique em Opções — abre a janela grande de configurações"])
    return f

# =====================================================================
@reg("03_opcoes_privacidade", "Janela Opções — Privacidade")
def f03():
    f = Fig(1000, 560)
    f.rect((0,0,f.w,f.h), fill=(255,255,255), outline=BORDA)
    f.titulo_janela("Opções")
    lista_g = ["Global","  Carregamento de Dados","  Power Query Editor","  Segurança",
               "  Privacidade","  Idioma de consulta"]
    lista_a = ["ARQUIVO ATUAL","  Carregamento de Dados","  Conexões da Web","  Privacidade",
               "  Idioma regional","  Recursos de visualização"]
    f.rect((0,30,290,f.h), fill=(248,249,250), outline=BORDA)
    yy = 48
    for it in lista_g+[""]+lista_a:
        if it=="": yy += 10; continue
        cab = not it.startswith("  ")
        sel = it=="  Privacidade" and yy>240
        if sel: f.rect((6,yy-4,284,yy+24), fill=(230,240,250))
        f.txt((16 if cab else 34, yy+10), it.strip(), 12, cab or sel,
              TEXTO if (cab or sel) else TEXTO2, anchor="lm")
        if sel: alvo=(6,yy-4,284,yy+24)
        yy += 30
    f.txt((316,54), "Níveis de Privacidade", 16, True)
    f.txt((316,92), "Os níveis de privacidade protegem os dados contra combinação", 12, cor=TEXTO2)
    f.txt((316,112), "acidental com outras fontes. Como todas as suas planilhas vêm", 12, cor=TEXTO2)
    f.txt((316,132), "da mesma pasta do SharePoint, pode ignorar sem risco.", 12, cor=TEXTO2)
    op = [("Combinar dados de acordo com as configurações de Nível de Privacidade", False),
          ("Combinar dados de acordo com as configurações do arquivo", False),
          ("Sempre ignorar as configurações de nível de Privacidade", True)]
    yy = 180
    for t,marcado in op:
        f.d.ellipse((318,yy,334,yy+16), fill=(255,255,255), outline=(120,130,145), width=2)
        if marcado:
            f.d.ellipse((322,yy+4,330,yy+12), fill=ACENTO)
            f.d.ellipse((318,yy,334,yy+16), outline=ACENTO, width=2)
            alvo2 = (312,yy-6,966,yy+24)
        f.txt((346,yy+8), t, 12, marcado, TEXTO if marcado else TEXTO2, anchor="lm")
        yy += 38
    f.botao((760,f.h-52,860,f.h-18), "OK", True)
    f.botao((870,f.h-52,970,f.h-18), "Cancelar")
    f.marca(alvo, 1, dx=-16, dy=0)
    f.marca(alvo2, 2, dx=-16, dy=0)
    f.marca((760,f.h-52,860,f.h-18), 3, dx=-16, dy=0)
    f.legenda(["Na lista da esquerda, em ARQUIVO ATUAL, clique em Privacidade",
               "Marque a terceira bolinha: Sempre ignorar as configurações de nível de Privacidade",
               "Clique em OK"], y=f.h-64)
    return f

# =====================================================================
@reg("04_opcoes_carregamento", "Janela Opções — Carregamento de Dados")
def f04():
    f = Fig(1000, 560)
    f.rect((0,0,f.w,f.h), fill=(255,255,255), outline=BORDA)
    f.titulo_janela("Opções")
    f.rect((0,30,290,f.h), fill=(248,249,250), outline=BORDA)
    itens = ["GLOBAL","  Carregamento de Dados","  Segurança","  Privacidade","",
             "ARQUIVO ATUAL","  Carregamento de Dados","  Conexões da Web","  Privacidade"]
    yy = 48; alvo=None
    for it in itens:
        if it=="": yy += 12; continue
        cab = not it.startswith("  ")
        sel = it=="  Carregamento de Dados" and yy>200
        if sel:
            f.rect((6,yy-4,284,yy+24), fill=(230,240,250)); alvo=(6,yy-4,284,yy+24)
        f.txt((16 if cab else 34, yy+10), it.strip(), 12, cab or sel,
              TEXTO if (cab or sel) else TEXTO2, anchor="lm")
        yy += 30
    f.txt((316,54), "Relações", 15, True)
    checks = [("Detectar automaticamente novas relações depois que os dados forem carregados", False, True),
              ("Atualizar ou excluir relações ao atualizar dados", True, False),
              ("Importar relações de fontes de dados na primeira carga", True, False)]
    yy = 92; alvos=[]
    for t, marcado, destacar in checks:
        f.rr((318,yy,334,yy+16), 3, fill=(255,255,255), outline=(120,130,145), width=2)
        if marcado: f.txtc((318,yy,334,yy+16), "✓", 13, True, ACENTO)
        f.txt((346,yy+8), t, 11.5, destacar, TEXTO if destacar else TEXTO2, anchor="lm")
        if destacar: alvos.append((312,yy-6,978,yy+24))
        yy += 34
    f.txt((316,yy+16), "Inteligência de tempo", 15, True)
    yy += 54
    f.rr((318,yy,334,yy+16), 3, fill=(255,255,255), outline=(120,130,145), width=2)
    f.txtc((318,yy,334,yy+16), "✓", 13, True, ACENTO)
    f.txt((346,yy+8), "Data/hora automática para novos arquivos", 11.5, True, TEXTO, anchor="lm")
    alvos.append((312,yy-6,978,yy+24))
    f.botao((760,f.h-52,860,f.h-18), "OK", True)
    f.botao((870,f.h-52,970,f.h-18), "Cancelar")
    f.marca(alvo, 1, dx=-16, dy=0)
    f.marca(alvos[0], 2, dx=-16, dy=0)
    f.marca(alvos[1], 3, dx=-16, dy=0)
    f.marca((760,f.h-52,860,f.h-18), 4, dx=-16, dy=0)
    f.legenda(["Ainda em ARQUIVO ATUAL, clique em Carregamento de Dados",
               "DESMARQUE 'Detectar automaticamente novas relações' (se estiver marcada)",
               "DESMARQUE 'Data/hora automática para novos arquivos'",
               "Clique em OK. Pode ser que ele peça para reabrir o arquivo — aceite."], y=f.h-84)
    return f

# =====================================================================
@reg("05_transformar_dados", "Onde fica o botão Transformar dados")
def f05():
    f = Fig(1100, 300)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Inserir","Modelagem","Exibição","Ajuda"], 1)
    f.rect((0,y,f.w,y+86), fill=CHROME, outline=BORDA)
    alvo=None
    for i,(r,ic) in enumerate([("Colar","📋"),("Obter\ndados","▤"),("Excel","▦"),
                    ("Hub de\ndados","☁"),("Inserir dados","⌨"),("Transformar\ndados","⚙"),
                    ("Atualizar","⟳")]):
        b = f.botao_faixa(16+i*118, y+10, r, larg=108, alt=66, icone=ic)
        if r.startswith("Transformar"): alvo=b
    f.marca(alvo, 1, dx=-14, dy=-14)
    f.seta((alvo[0]-90, alvo[1]+100), (alvo[0]+30, alvo[3]+6))
    f.nota((alvo[0]-96, alvo[1]+104), "clique aqui", cor=DEST, sz=14)
    f.legenda(["Aba Página Inicial → botão Transformar dados. Abre uma JANELA NOVA "
               "chamada Editor do Power Query."], y=f.h-44)
    return f

# =====================================================================
@reg("06_consulta_nula", "Editor do Power Query — criar uma Consulta Nula")
def f06():
    f = Fig(1100, 560)
    f.titulo_janela("Sem Título - Editor do Power Query")
    y = f.faixa(["Arquivo","Página Inicial","Transformar","Adicionar Coluna","Exibição","Ferramentas"], 1)
    f.rect((0,y,f.w,y+80), fill=CHROME, outline=BORDA)
    alvo=None
    for i,(r,ic) in enumerate([("Fechar e\nAplicar","✓"),("Nova\nFonte","＋"),("Fontes\nRecentes","🕐"),
                    ("Inserir\nDados","⌨"),("Gerenciar\nParâmetros","⚙"),("Atualizar\nVisualização","⟳"),
                    ("Editor\nAvançado","✎")]):
        b = f.botao_faixa(16+i*116, y+8, r, larg=106, alt=64, icone=ic)
        if r.startswith("Nova"): alvo=b
    topo = y+80
    f.painel((0,topo,250,f.h-56), "Consultas [0]", ["(ainda vazio)"])
    f.rect((250,topo,f.w,f.h-56), fill=(250,250,250), outline=BORDA)
    # menu suspenso do Nova Fonte
    mx, my = alvo[0], alvo[3]
    f.rect((mx,my,mx+260,my+236), fill=(255,255,255), outline=BORDA)
    for i,it in enumerate(["Pasta de Trabalho do Excel","Texto/CSV","Web","SharePoint",
                           "SQL Server","Mais...","Consulta Nula"]):
        cy = my+10+i*32
        sel = it=="Consulta Nula"
        if sel:
            f.rect((mx+4,cy-4,mx+256,cy+26), fill=(230,240,250)); alvo2=(mx+4,cy-4,mx+256,cy+26)
        f.txt((mx+18,cy+11), it, 12, sel, TEXTO if sel else TEXTO2, anchor="lm")
    f.marca(alvo, 1, dx=-14, dy=-14)
    f.marca(alvo2, 2, dx=-14, dy=0)
    f.legenda(["Página Inicial → Nova Fonte",
               "Role o menu até o fim e clique em Consulta Nula (é o último item)"], y=f.h-52)
    return f

# =====================================================================
@reg("07_editor_avancado", "Editor Avançado — onde o texto é colado")
def f07():
    f = Fig(1100, 660)
    f.rect((0,0,f.w,f.h), fill=(255,255,255), outline=BORDA)
    f.titulo_janela("Editor Avançado")
    f.txt((20,50), "Consulta1", 15, True)
    cx = (20, 78, f.w-20, f.h-186)
    f.rect(cx, fill=(252,252,252), outline=BORDA)
    linhas = ['let','    SITE       = "https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS",',
              '    BIBLIOTECA = "Documentos Compartilhados",',
              '    PASTA      = "DEMANDAS NN - ALIANÇA/DEMANDAS NN - ALIANÇAS",',
              '    ABA        = "Mapeamento NN",','','    fnTexto = (v as any) as nullable text =>',
              '        let t = if v = null then null else Text.Trim(', '        ...',
              '','    Final = Table.RemoveColumns(ComID, {"Seq"})','in','    Final']
    yy = cx[1]+14
    for i,l in enumerate(linhas):
        f.txt((cx[0]+44, yy), l, 11.5, False, TEXTO2, mono=True)
        f.txt((cx[0]+14, yy), str(i+1).rjust(2), 10.5, False, TEXTO3, mono=True)
        yy += 19
    f.rect((cx[0],cx[3]-34,cx[2],cx[3]), fill=(246,248,250), outline=BORDA)
    f.txt((cx[0]+14, cx[3]-17), "✓  Nenhum erro de sintaxe foi detectado.", 12, False, (20,120,70), anchor="lm")
    f.botao((f.w-260,f.h-172,f.w-150,f.h-138), "Concluído", True)
    f.botao((f.w-140,f.h-172,f.w-30,f.h-138), "Cancelar")
    f.marca(cx, 1, dx=-14, dy=-14)
    f.marca((cx[0],cx[3]-34,cx[2],cx[3]), 2, dx=-14, dy=0)
    f.marca((f.w-260,f.h-172,f.w-150,f.h-138), 3, dx=-14, dy=0)
    f.legenda(["Clique dentro desta caixa branca, aperte Ctrl+A (seleciona tudo), "
               "Delete, e depois Ctrl+V para colar o texto da consulta",
               "Confira esta linha: precisa dizer 'Nenhum erro de sintaxe foi detectado'. "
               "Se acusar erro, você colou pela metade — refaça o Ctrl+A / Ctrl+V",
               "Clique em Concluído"], y=f.h-104)
    return f

# =====================================================================
@reg("08_renomear", "Renomear a consulta")
def f08():
    f = Fig(1000, 460)
    f.titulo_janela("Editor do Power Query")
    y = f.faixa(["Arquivo","Página Inicial","Transformar","Adicionar Coluna"], 1)
    topo = y+8
    f.painel((0,topo,280,f.h-84), "Consultas [1]", [])
    f.rect((8,topo+36,272,topo+64), fill=(230,240,250))
    f.txt((22,topo+50), "Consulta1", 13, True, TEXTO, anchor="lm")
    mx, my = 120, topo+64
    f.rect((mx,my,mx+250,my+232), fill=(255,255,255), outline=BORDA)
    for i,it in enumerate(["Copiar","Colar","Excluir","Renomear","Duplicar",
                           "Referência","Habilitar carga"]):
        cy = my+10+i*31
        sel = it=="Renomear"
        if sel:
            f.rect((mx+4,cy-4,mx+246,cy+25), fill=(230,240,250)); alvo=(mx+4,cy-4,mx+246,cy+25)
        if it=="Habilitar carga":
            f.txtc((mx+10,cy,mx+26,cy+22), "✓", 13, True, ACENTO)
        f.txt((mx+34,cy+11), it, 12, sel, TEXTO if sel else TEXTO2, anchor="lm")
    f.marca((8,topo+36,272,topo+64), 1, dx=-14, dy=0)
    f.marca(alvo, 2, dx=-14, dy=0)
    f.rr((560,topo+40,860,topo+72), 4, fill=(255,255,255), outline=ACENTO, width=2)
    f.txt((574,topo+56), "Mapeamento", 14, True, TEXTO, anchor="lm")
    f.marca((560,topo+40,860,topo+72), 3, dx=-14, dy=0)
    f.legenda(["Clique com o BOTÃO DIREITO no nome da consulta (lado esquerdo)",
               "Escolha Renomear",
               "Apague tudo e digite o nome exato. Depois aperte Enter."], y=f.h-76)
    return f

# =====================================================================
@reg("09_credenciais", "Entrar na conta do SharePoint")
def f09():
    f = Fig(940, 470)
    f.rect((0,0,f.w,f.h), fill=(255,255,255), outline=BORDA)
    f.titulo_janela("Acessar conteúdo do SharePoint")
    f.rect((0,30,300,f.h-84), fill=(248,249,250), outline=BORDA)
    for i,(it,sel) in enumerate([("Anônimo",False),("Windows",False),("Conta organizacional",True)]):
        cy = 56+i*46
        if sel:
            f.rect((6,cy-6,294,cy+30), fill=(230,240,250)); alvo=(6,cy-6,294,cy+30)
            f.rect((6,cy-6,10,cy+30), fill=ACENTO)
        f.txt((26,cy+12), it, 13, sel, TEXTO if sel else TEXTO2, anchor="lm")
    f.txt((326,58), "Conta organizacional", 16, True)
    f.txt((326,98), "Use o e-mail da EMS. É o mesmo login do seu computador.", 12, cor=TEXTO2)
    f.botao((326,136,466,172), "Entrar", True)
    f.txt((326,206), "Selecione o nível ao qual aplicar estas configurações:", 12, cor=TEXTO2)
    f.rr((326,232,900,268), 4, fill=(255,255,255), outline=BORDA)
    f.txt((340,250), "https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS", 12, False, TEXTO, anchor="lm", mono=True)
    f.txtc((872,232,900,268), "▾", 13, cor=TEXTO2)
    f.botao((f.w-250,f.h-64,f.w-140,f.h-28), "Conectar", True)
    f.botao((f.w-130,f.h-64,f.w-20,f.h-28), "Cancelar")
    f.marca(alvo, 1, dx=-14, dy=0)
    f.marca((326,136,466,172), 2, dx=-14, dy=0)
    f.marca((f.w-250,f.h-64,f.w-140,f.h-28), 3, dx=-14, dy=0)
    f.legenda(["Clique em Conta organizacional (lado esquerdo)",
               "Clique em Entrar e faça login com o e-mail da EMS",
               "Depois que seu nome aparecer, clique em Conectar"], y=f.h-76)
    return f

# =====================================================================
@reg("10_fechar_aplicar", "Fechar e Aplicar — carrega tudo para o relatório")
def f10():
    f = Fig(1000, 300)
    f.titulo_janela("Editor do Power Query")
    y = f.faixa(["Arquivo","Página Inicial","Transformar","Adicionar Coluna","Exibição"], 1)
    f.rect((0,y,f.w,y+86), fill=CHROME, outline=BORDA)
    b = f.botao_faixa(16, y+10, "Fechar e\nAplicar", larg=110, alt=66, icone="✓")
    for i,(r,ic) in enumerate([("Nova\nFonte","＋"),("Gerenciar\nParâmetros","⚙"),
                               ("Atualizar\nVisualização","⟳"),("Editor\nAvançado","✎")]):
        f.botao_faixa(140+i*116, y+10, r, larg=106, alt=66, icone=ic)
    topo = y+86
    f.painel((0,topo,250,f.h-46), "Consultas [3]",
             ["Mapeamento","Carregamento Mensal","Calendário"])
    f.marca(b, 1, dx=-14, dy=-14)
    f.marca((0,topo,250,f.h-46), 2, dx=125, dy=-12)
    f.legenda(["Depois das 3 consultas prontas, clique em Fechar e Aplicar",
               "Antes de clicar, confira: precisa haver EXATAMENTE estas 3 consultas, "
               "com estes nomes e acentos"], y=f.h-52)
    return f

# =====================================================================
@reg("11_modelo_ligacoes", "Exibição de Modelo — criar as duas ligações")
def f11():
    f = Fig(1100, 620)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Modelagem","Exibição","Ajuda"], 0)
    UTIL = f.h - 130
    f.rect((0,y,54,UTIL), fill=(247,247,247), outline=BORDA)
    for i,(ic,nome) in enumerate([("▥","Relatório"),("▦","Tabela"),("⛓","Modelo")]):
        cy = y+22+i*62
        cor = ACENTO if i==2 else TEXTO3
        f.txtc((6,cy,48,cy+26), ic, 21, cor=cor)
        f.txtc((0,cy+24,54,cy+38), nome, 8, cor=cor)
        if i==2: f.rect((0,cy-6,4,cy+40), fill=ACENTO); alvo_modo=(0,cy-8,54,cy+42)
    f.rect((54,y,f.w,UTIL), fill=(238,240,244))

    def tabela(x, yy, titulo, campos, larg=250):
        f.rr((x,yy,x+larg,yy+34+len(campos)*24), 5, fill=(255,255,255), outline=BORDA)
        f.rect((x,yy,x+larg,yy+30), fill=(240,243,247))
        f.txt((x+12,yy+15), titulo, 13, True, TEXTO, anchor="lm")
        pos={}
        for i,c in enumerate(campos):
            cy = yy+34+i*24
            f.txt((x+16,cy+11), c, 11.5, c.startswith("*"), TEXTO2 if not c.startswith("*") else TEXTO, anchor="lm")
            pos[c]=(x,cy+11,x+larg)
        return pos

    p1 = tabela(100, y+70, "Carregamento Mensal",
        ["*ProjetoID","*Data Referência","Status no Mês","Entrou no Mês","Saiu no Mês","Ativo no Fim do Mês"])
    p2 = tabela(470, y+70, "Mapeamento",
        ["*ProjetoID","Molécula","Status NN","Situação","Unidade de Negócio"])
    p3 = tabela(810, y+250, "Calendário", ["*Data","Ano","Ano-Mês","Mês"], larg=220)

    a = p1["*ProjetoID"]; b = p2["*ProjetoID"]
    f.seta((a[2]+6, a[1]), (b[0]-6, b[1]))
    c = p1["*Data Referência"]; d = p3["*Data"]
    f.seta((c[2]+6, c[1]), (d[0]-6, d[1]))
    f.marca((a[0]+8, a[1]-13, a[2]-8, a[1]+13), 2, dx=-14, dy=0)
    f.marca((c[0]+8, c[1]-13, c[2]-8, c[1]+13), 3, dx=-48, dy=0)
    f.marca(alvo_modo, 1, dx=27, dy=-16)
    f.nota((362, a[1]-8), "arraste →", cor=DEST, sz=12)
    f.nota((370, c[1]+16), "arraste ↘", cor=DEST, sz=12)
    f.legenda(["Clique no terceiro ícone da barra da esquerda: Modelo",
               "Segure o campo ProjetoID da tabela Carregamento Mensal e arraste "
               "até o campo ProjetoID da tabela Mapeamento. Solte.",
               "Segure Data Referência (Carregamento Mensal) e arraste até Data (Calendário). Solte.",
               "Confira: cada ligação deve mostrar '*' do lado do Carregamento Mensal e '1' do outro lado."])
    return f

# =====================================================================
@reg("12_marcar_data", "Marcar o Calendário como tabela de data")
def f12():
    f = Fig(1100, 360)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Modelagem","Exibição","Ferramentas de tabela"], 4)
    f.rect((0,y,f.w,y+82), fill=CHROME, outline=BORDA)
    alvo=None
    for i,(r,ic) in enumerate([("Nova\nmedida","∑"),("Nova\ncoluna","▤"),("Nova\ntabela","▦"),
                               ("Gerenciar\nrelações","⛓"),("Marcar como\ntabela de data","📅")]):
        b=f.botao_faixa(16+i*124, y+8, r, larg=114, alt=64, icone=ic)
        if r.startswith("Marcar"): alvo=b
    topo=y+82
    f.painel((f.w-250,topo,f.w,f.h-96), "Dados",
             ["▾ Mapeamento","▾ Carregamento Mensal","▾ Calendário","  Data","  Ano","  Mês"])
    f.rect((f.w-244,topo+78,f.w-6,topo+100), fill=(230,240,250))
    f.marca((f.w-244,topo+78,f.w-6,topo+100), 1, dx=-14, dy=0)
    f.marca(alvo, 2, dx=-14, dy=-14)
    f.rect((300,topo+40,760,topo+140), fill=(255,255,255), outline=BORDA)
    f.txt((316,topo+62), "Marcar como tabela de data", 14, True)
    f.txt((316,topo+92), "Coluna de data:", 12, cor=TEXTO2)
    f.rr((430,topo+82,700,topo+112), 4, fill=(255,255,255), outline=ACENTO, width=2)
    f.txt((444,topo+97), "Data", 12, True, TEXTO, anchor="lm")
    f.marca((430,topo+82,700,topo+112), 3, dx=-14, dy=0)
    f.legenda(["No painel Dados (direita), clique na tabela Calendário para selecioná-la",
               "Aparece a aba Ferramentas de tabela no topo → Marcar como tabela de data",
               "Em 'Coluna de data' escolha Data e clique OK"], y=f.h-86)
    return f

# =====================================================================
@reg("13_classificar_coluna", "Classificar uma coluna de texto por outra coluna")
def f13():
    f = Fig(1100, 340)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Modelagem","Exibição","Ferramentas de coluna"], 4)
    f.rect((0,y,f.w,y+82), fill=CHROME, outline=BORDA)
    alvo=None
    for i,(r,ic) in enumerate([("Formato","Aa"),("Resumo\npadrão","∑"),("Categoria\nde dados","▦"),
                               ("Classificar por\ncoluna","↕")]):
        b=f.botao_faixa(16+i*130, y+8, r, larg=120, alt=64, icone=ic)
        if r.startswith("Classificar"): alvo=b
    topo=y+82
    f.painel((f.w-250,topo,f.w,f.h-88), "Dados",
             ["▾ Mapeamento","  Status NN","  Ordem Status","▾ Calendário","  Mês","  Nº Mês"])
    f.rect((f.w-244,topo+36,f.w-6,topo+58), fill=(230,240,250))
    f.marca((f.w-244,topo+36,f.w-6,topo+58), 1, dx=-14, dy=0)
    f.marca(alvo, 2, dx=-14, dy=-14)
    mx,my = alvo[0], alvo[3]
    f.rect((mx,my,mx+250,my+96), fill=(255,255,255), outline=BORDA)
    for i,it in enumerate(["Molécula","Ordem Status","Situação"]):
        cy=my+8+i*29; sel = it=="Ordem Status"
        if sel:
            f.rect((mx+4,cy-4,mx+246,cy+24), fill=(230,240,250)); alvo2=(mx+4,cy-4,mx+246,cy+24)
        f.txt((mx+18,cy+10), it, 12, sel, TEXTO if sel else TEXTO2, anchor="lm")
    f.marca(alvo2, 3, dx=-14, dy=0)
    f.legenda(["Clique na COLUNA que quer ordenar (aqui: Status NN)",
               "Aba Ferramentas de coluna → Classificar por coluna",
               "Escolha a coluna de números que define a ordem (aqui: Ordem Status)"], y=f.h-78)
    return f

# =====================================================================
@reg("14_nova_medida", "Criar uma medida")
def f14():
    f = Fig(1100, 420)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Inserir","Modelagem","Exibição"], 3)
    f.rect((0,y,f.w,y+82), fill=CHROME, outline=BORDA)
    alvo=None
    for i,(r,ic) in enumerate([("Gerenciar\nrelações","⛓"),("Nova\nmedida","∑"),
                               ("Nova\ncoluna","▤"),("Nova\ntabela","▦")]):
        b=f.botao_faixa(16+i*124, y+8, r, larg=114, alt=64, icone=ic)
        if r.startswith("Nova\nm"): alvo=b
    topo=y+82
    # barra de fórmulas
    f.rect((54,topo,f.w-250,topo+92), fill=(250,250,250), outline=BORDA)
    f.txtc((58,topo+4,86,topo+34), "✓", 15, True, (20,130,70))
    f.txtc((88,topo+4,116,topo+34), "✗", 15, True, (180,60,60))
    f.rect((124,topo+8,f.w-268,topo+80), fill=(255,255,255), outline=ACENTO, width=2)
    f.txt((136,topo+22), "Projetos = DISTINCTCOUNT ( Mapeamento[ProjetoID] )", 13, False, TEXTO, mono=True)
    f.txt((136,topo+50), "↑ nome da medida      ↑ obrigatório o sinal de igual", 11, False, TEXTO3)
    f.painel((f.w-250,topo,f.w,f.h-88), "Dados",
             ["▾ _Medidas","  ∑ Projetos","▾ Mapeamento","▾ Carregamento Mensal"])
    f.rect((f.w-244,topo+36,f.w-6,topo+58), fill=(230,240,250))
    f.marca(alvo, 1, dx=-14, dy=-14)
    f.marca((124,topo+8,f.w-268,topo+80), 2, dx=-14, dy=0)
    f.marca((f.w-244,topo+36,f.w-6,topo+58), 3, dx=-14, dy=0)
    f.legenda(["Selecione a tabela _Medidas no painel Dados, depois clique em "
               "Modelagem → Nova medida",
               "Apague o texto que aparece e cole a medida inteira (nome, sinal de = e a fórmula). "
               "Aperte Enter.",
               "A medida nova aparece aqui com o símbolo de somatório. "
               "Se aparecer em outra tabela, arraste-a para _Medidas."], y=f.h-78)
    return f

# =====================================================================
@reg("15_painel_visualizacoes", "O painel Visualizações — qual ícone é qual gráfico")
def f15():
    f = Fig(1100, 700)
    f.rect((0,0,f.w,f.h), fill=(255,255,255))
    f.txt((20,18), "Painel VISUALIZAÇÕES — os ícones que você vai usar neste dossiê", 15, True)
    f.txt((20,44), "Os ícones ficam no painel da direita, em grade. Passe o mouse em cima "
                   "e o nome aparece.", 12, cor=TEXTO2)
    usados = [
        ("▥","Gráfico de barras empilhadas","Barras deitadas, empilhadas por legenda"),
        ("▤","Gráfico de barras clusterizado","Barras deitadas, uma ao lado da outra"),
        ("▦","Gráfico de colunas empilhadas","Colunas em pé, empilhadas"),
        ("▧","Gráfico de colunas clusterizado","Colunas em pé, uma ao lado da outra"),
        ("▨","Gráfico de barras 100% empilhadas","Barras que sempre somam 100%"),
        ("╱","Gráfico de linhas","Linha ao longo do tempo"),
        ("◤","Gráfico de área empilhada","Linha com preenchimento, empilhada"),
        ("▮","Gráfico de colunas e linhas","Colunas e linha no mesmo gráfico"),
        ("⊿","Gráfico em cascata","Sobe e desce — bom para saldo do mês"),
        ("◕","Gráfico de rosca","Pizza com buraco no meio"),
        ("▭","Cartão","Um número grande e sozinho"),
        ("☰","Segmentação de dados","O filtro que o usuário mexe"),
        ("▤","Tabela","Linhas e colunas"),
        ("⊞","Matriz","Tabela cruzada (linhas × colunas)"),
        ("◉","Medidor","Velocímetro — usado no % de ocupação"),
    ]
    cols, cw, ch = 2, 530, 40
    for i,(ic,nome,desc) in enumerate(usados):
        cx = 20 + (i%cols)*cw; cy = 76 + (i//cols)*ch
        f.rr((cx,cy,cx+34,cy+34), 4, fill=(248,249,251), outline=BORDA)
        f.txtc((cx,cy,cx+34,cy+34), ic, 17, cor=ACENTO)
        f.txt((cx+44,cy+9), nome, 12, True)
        f.txt((cx+44,cy+24), desc, 10.5, cor=TEXTO2)
    yy = 76 + ((len(usados)+1)//cols)*ch + 16
    f.rect((20,yy,f.w-20,yy+108), fill=DEST_BG, outline=(240,190,175))
    f.txt((36,yy+16), "Se você não achar o ícone", 13, True, DEST)
    for i,l in enumerate([
        "Os ícones não têm nome escrito — só desenho. Passe o mouse em cima de cada um e espere",
        "meio segundo: aparece uma tarja preta com o nome exato. É assim que você confere.",
        "Existe também o botão '...' (três pontinhos) no canto do painel, que lista mais tipos."]):
        f.txt((36,yy+42+i*20), l, 11.5, cor=TEXTO2)
    return f

# =====================================================================
@reg("16_pocos_campos", "Onde arrastar cada campo dentro de um visual")
def f16():
    f = Fig(1100, 560)
    f.rect((0,0,f.w,f.h), fill=(255,255,255))
    f.txt((20,18), "Depois de inserir o gráfico, o painel mostra os 'poços' de campos", 15, True)
    f.txt((20,44), "Cada gráfico tem poços diferentes. Você ARRASTA a coluna do painel Dados "
                   "(direita) para dentro do poço certo.", 12, cor=TEXTO2)
    # visual selecionado
    f.rr((20,76,470,420), 6, fill=(250,251,252), outline=ACENTO, width=2)
    f.txt((36,96), "QUANTIDADE DE PROJETOS × STATUS", 12, True, ACENTO)
    for i,(h,l) in enumerate([(60,"Prospecção"),(110,"Av. Técnica"),(45,"Negociação"),(30,"CDA"),(18,"Contrato")]):
        bx = 56+i*82
        f.rr((bx,380-h*2.2,bx+56,380), 4, fill=(42,120,214))
        f.txtc((bx,356-h*2.2,bx+56,376-h*2.2), str(h), 11, True, TEXTO2)
        f.txtc((bx-8,384,bx+64,400), l, 9, cor=TEXTO2)
    # painel visualizações
    f.painel((500,76,790,f.h-96), "Visualizações")
    f.txt((514,112), "Criar visual", 11, True, TEXTO2)
    f.campo_visual((514,138,776,0), "Eixo X", ["Status NN"])
    f.campo_visual((514,206,776,0), "Eixo Y", ["Projetos"])
    f.campo_visual((514,274,776,0), "Legenda", [])
    f.campo_visual((514,342,776,0), "Dicas de ferramenta", [])
    # painel dados
    f.painel((800,76,f.w,f.h-96), "Dados",
             ["▾ _Medidas","  ∑ Projetos","  ∑ Projetos Ativos","▾ Mapeamento","  Status NN",
              "  Situação","  Unidade de Negócio","  Molécula"])
    f.marca((514,152,776,178), 1, dx=-14, dy=0)
    f.marca((514,220,776,246), 2, dx=-14, dy=0)
    f.seta((900,232),(790,232))
    f.seta((900,150),(790,166))
    f.legenda(["EIXO X = o que aparece embaixo do gráfico (a categoria). "
               "Arraste aqui a coluna de texto, ex.: Mapeamento → Status NN",
               "EIXO Y = o que é medido (a altura das barras). "
               "Arraste aqui a medida, ex.: _Medidas → Projetos",
               "Em gráficos de BARRAS DEITADAS os nomes trocam: a categoria vai no Eixo Y "
               "e o número no Eixo X. O dossiê sempre diz qual é qual."], y=f.h-86)
    return f

# =====================================================================
@reg("17_editar_interacoes", "Fazer um filtro NÃO afetar um gráfico específico")
def f17():
    f = Fig(1100, 520)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Inserir","Modelagem","Formato"], 4)
    f.rect((0,y,f.w,y+80), fill=CHROME, outline=BORDA)
    alvo=None
    for i,(r,ic) in enumerate([("Trazer para\na frente","⬆"),("Alinhar","≡"),
                               ("Agrupar","▣"),("Editar\ninterações","⇄")]):
        b=f.botao_faixa(16+i*126, y+8, r, larg=116, alt=64, icone=ic)
        if r.startswith("Editar"): alvo=b
    topo = y+88
    f.rr((30,topo,250,topo+96), 6, fill=(255,255,255), outline=ACENTO, width=3)
    f.txt((44,topo+14), "UNIDADE DE NEGÓCIO", 10, True, TEXTO2)
    f.rr((44,topo+38,236,topo+68), 4, fill=(250,250,250), outline=BORDA)
    f.txt((56,topo+53), "Non-Retail", 12, False, TEXTO, anchor="lm")
    f.txtc((214,topo+38,236,topo+68), "▾", 12, cor=TEXTO2)
    f.nota((30,topo+104), "este é o filtro selecionado", cor=DEST, sz=11)

    def mini(x, yy, titulo, marcado):
        f.rr((x,yy,x+250,yy+150), 6, fill=(255,255,255), outline=BORDA)
        f.txt((x+14,yy+16), titulo, 10, True, ACENTO)
        for i,h in enumerate([90,64,40,22]):
            f.rr((x+18+i*56,yy+126-h,x+18+i*56+40,yy+126), 3, fill=(42,120,214))
        # ícones de interação
        bx = x+250-78
        for j,(ic,ativo) in enumerate([("⧉", marcado==0),("⊘", marcado==1)]):
            cx = bx+j*34
            f.d.ellipse((cx,yy-14,cx+28,yy+14), fill=ACENTO if ativo else (255,255,255),
                        outline=ACENTO, width=2)
            f.txtc((cx,yy-14,cx+28,yy+14), ic, 14, True, (255,255,255) if ativo else ACENTO)
        return (bx+34, yy-14, bx+62, yy+14)

    mini(320, topo+30, "ESTÁGIO DAS OPORTUNIDADES", 0)
    alvo2 = mini(620, topo+30, "FRANQUIAS DE ATUAÇÃO DE NN", 1)
    mini(320, topo+210, "MOTIVOS DE CANCELAMENTO", 0)
    f.marca(alvo, 1, dx=-14, dy=-14)
    f.marca((30,topo,250,topo+96), 2, dx=-14, dy=0)
    f.marca(alvo2, 3, dx=-14, dy=-26)
    f.legenda(["Selecione o gráfico/filtro que vai MANDAR o filtro, depois "
               "aba Formato → Editar interações",
               "Aqui selecionamos a segmentação Unidade de Negócio",
               "Aparecem dois botõezinhos em cima de cada gráfico: ⧉ = filtrar (padrão), "
               "⊘ = nenhum. Clique em ⊘ no gráfico 'Franquias de Atuação' para ele "
               "continuar mostrando todas as unidades."], y=f.h-86)
    return f

# =====================================================================
def _wire(titulo, kpis, blocos, nome_pagina):
    """Desenha o rascunho de layout de uma página do relatório."""
    f = Fig(1100, 700)
    f.rect((0,0,f.w,f.h), fill=(238,240,244))
    f.rect((0,0,f.w,52), fill=(31,95,169))
    f.txt((22,26), titulo, 16, True, (255,255,255), anchor="lm")
    f.txt((f.w-22,26), "página: " + nome_pagina, 11, False, (200,220,245), anchor="rm")
    # filtros
    f.rr((16,62,f.w-16,104), 5, fill=(255,255,255), outline=BORDA)
    f.txt((28,74), "SEGMENTAÇÕES (filtros)", 9, True, TEXTO3)
    for i in range(5):
        bx = 28+i*212
        f.rr((bx,84,bx+196,98), 3, fill=(248,249,251), outline=BORDA2)
    # kpis
    for i,(rot,cor) in enumerate(kpis):
        bx = 16+i*(1068/len(kpis))
        bw = 1068/len(kpis)-10
        f.rr((bx,114,bx+bw,182), 5, fill=(255,255,255), outline=BORDA)
        f.rect((bx,114,bx+bw,118), fill=cor)
        f.txtc((bx,126,bx+bw,144), rot, 9, True, TEXTO3)
        f.txtc((bx,146,bx+bw,176), "000", 24, True, cor)
    # blocos
    for (x,y,w,h,tipo,rot) in blocos:
        f.rr((x,y,x+w,y+h), 6, fill=(255,255,255), outline=BORDA)
        f.txt((x+14,y+16), rot, 10.5, True, ACENTO)
        f.txt((x+14,y+34), "[" + tipo + "]", 9.5, False, TEXTO3)
        # esbocinho
        cx0, cy0, cx1, cy1 = x+16, y+50, x+w-16, y+h-14
        if "barra" in tipo.lower() or "100%" in tipo:
            n = min(6, max(3,int((cy1-cy0)//22)))
            for i in range(n):
                yy = cy0+i*((cy1-cy0)/n)
                f.rr((cx0+64, yy+3, cx0+64+(cx1-cx0-70)*(1-i*0.13), yy+((cy1-cy0)/n)-8), 3,
                     fill=(42,120,214) if i%2==0 else (90,160,230))
                f.rr((cx0, yy+5, cx0+56, yy+((cy1-cy0)/n)-10), 2, fill=(232,236,242))
        elif "coluna" in tipo.lower() or "cascata" in tipo.lower():
            n = 9 if "linha" in tipo.lower() else 7
            topos=[]
            for i in range(n):
                hh = (cy1-cy0)*(0.25+0.62*abs(((i*3)%n)/n))
                bx = cx0+i*((cx1-cx0)/n)
                cor = (27,175,122) if "linha" in tipo.lower() else (42,120,214)
                f.rr((bx+4, cy1-hh, bx+((cx1-cx0)/n)-8, cy1), 3, fill=cor)
                topos.append((bx+((cx1-cx0)/n)/2, cy1-hh-14))
            if "linha" in tipo.lower():
                f.d.line(topos, fill=(42,120,214), width=3)
                for p in topos: f.d.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4), fill=(42,120,214))
        elif "área" in tipo.lower() or "area" in tipo.lower():
            import math
            faixas=[(42,120,214),(235,104,52),(27,175,122),(237,161,0)]
            base=[cy1]*13
            for k,cor in enumerate(faixas):
                pts=[]
                for i in range(13):
                    alt=(cy1-cy0)*(0.09+0.07*abs(math.sin(i/2.0+k)))
                    pts.append((cx0+i*((cx1-cx0)/12), base[i]-alt))
                poly=pts+[(cx0+12*((cx1-cx0)/12), base[12]),(cx0, base[0])]
                f.d.polygon(poly, fill=cor)
                base=[p[1] for p in pts]
        elif "rosca" in tipo.lower():
            r = min((cx1-cx0)/2, (cy1-cy0)/2)-6
            mx, my = (cx0+cx1)/2, (cy0+cy1)/2
            f.d.ellipse((mx-r,my-r,mx+r,my+r), fill=(42,120,214))
            f.d.pieslice((mx-r,my-r,mx+r,my+r), 300, 30, fill=(235,104,52))
            f.d.pieslice((mx-r,my-r,mx+r,my+r), 30, 95, fill=(27,175,122))
            f.d.ellipse((mx-r*0.55,my-r*0.55,mx+r*0.55,my+r*0.55), fill=(255,255,255))
        elif "linha" in tipo.lower():
            import math
            pts=[(cx0+i*((cx1-cx0)/12), cy1-(cy1-cy0)*(0.3+0.55*abs(math.sin(i/2.1))))
                 for i in range(13)]
            f.d.line(pts, fill=(42,120,214), width=3)
            for i in range(0,13,2):
                bx=pts[i][0]
                f.rr((bx-6,cy1-26,bx+6,cy1), 2, fill=(27,175,122))
        elif "tabela" in tipo.lower() or "matriz" in tipo.lower():
            f.rect((cx0,cy0,cx1,cy0+18), fill=(31,95,169))
            for i in range(1, int((cy1-cy0)//18)):
                yy = cy0+i*18
                if yy+16>cy1: break
                f.rect((cx0,yy,cx1,yy+17), fill=(250,251,252) if i%2 else (255,255,255), outline=BORDA2)
        elif "medidor" in tipo.lower():
            r = min((cx1-cx0)/2, (cy1-cy0))-8
            mx, my = (cx0+cx1)/2, cy1-6
            f.d.pieslice((mx-r,my-r,mx+r,my+r), 180, 360, fill=(232,236,242))
            f.d.pieslice((mx-r,my-r,mx+r,my+r), 180, 300, fill=(214,64,32))
            f.d.ellipse((mx-r*0.62,my-r*0.62,mx+r*0.62,my+r*0.62), fill=(255,255,255))
        elif "cartão" in tipo.lower():
            f.txtc((cx0,cy0,cx1,cy1), "texto dinâmico da medida", 12, cor=TEXTO3)
    # abas de página
    f.rect((0,f.h-34,f.w,f.h), fill=(243,243,243), outline=BORDA)
    for i,p in enumerate(["1. Visão Geral","2. Carregamento","3. Evolução","4. Report BU",
                          "5. Carteira","6. Financeiro","7. Completo","8. Qualidade"]):
        bx = 12+i*134
        at = p == nome_pagina
        f.rr((bx,f.h-29,bx+128,f.h-5), 3, fill=(255,255,255) if at else (236,236,236), outline=BORDA)
        f.txtc((bx,f.h-29,bx+128,f.h-5), p, 9.5, at)
    return f

AZ=(42,120,214); VD=(27,175,122); VM=(214,64,32); LR=(235,152,26); RX=(74,58,167); CZ=(96,106,120)

@reg("20_tela1", "Rascunho da Tela 1 — Visão Geral")
def f20(): return _wire("1. Visão Geral | Novos Negócios",
    [("OPORTUNIDADES",AZ),("EM ANDAMENTO",VD),("STAND BY",LR),("MOLÉCULAS",RX),("FORNECEDORES",CZ)],
    [(16,192,350,220,"Colunas clusterizado","QUANTIDADE DE PROJETOS × STATUS"),
     (376,192,350,220,"Barras clusterizado","PROJETOS × CATEGORIA"),
     (736,192,348,220,"Barras clusterizado","ORIGEM DA OPORTUNIDADE"),
     (16,422,700,200,"Tabela","PROJETOS — VISÃO RESUMIDA"),
     (726,422,358,200,"Barras clusterizado","PROJETOS POR COLIGADA")], "1. Visão Geral")

@reg("21_tela2", "Rascunho da Tela 2 — Carregamento do Time")
def f21(): return _wire("2. Carregamento do Time",
    [("PROJETOS ATIVOS",VD),("HORAS EMPENHADAS",AZ),("CAPACIDADE (H)",CZ),("HORAS DISPONÍVEIS",LR),("% OCUPAÇÃO",VM)],
    [(16,192,530,220,"Barras clusterizado","HORAS E PROJETOS POR PESSOA"),
     (556,192,250,220,"Medidor","% DE OCUPAÇÃO DO TIME"),
     (816,192,268,220,"Rosca","ONDE O TEMPO É GASTO (ATIVIDADE)"),
     (16,422,530,170,"Barras empilhadas","PROJETOS ATIVOS POR STATUS E COMPLEXIDADE"),
     (556,422,528,170,"Tabela","CARGA POR PESSOA"),
     (16,602,1068,20,"Cartão","AVISO DA RÉGUA")], "2. Carregamento")

@reg("22_tela3", "Rascunho da Tela 3 — Evolução do Mês")
def f22(): return _wire("3. Evolução do Mês",
    [("INÍCIO DO MÊS",CZ),("ENTRARAM",VD),("SAÍRAM",VM),("FIM DO MÊS",AZ),("HOJE vs FIM DO MÊS",LR)],
    [(16,192,640,230,"Colunas e linhas","CARTEIRA, ENTRADAS E SAÍDAS POR MÊS"),
     (666,192,418,230,"Cascata","SALDO DO MÊS (ENTRADAS − SAÍDAS)"),
     (16,432,640,150,"Área empilhada","COMPOSIÇÃO DO FUNIL AO LONGO DO TEMPO"),
     (666,432,418,150,"Matriz","RESUMO MÊS A MÊS"),
     (16,592,1068,32,"Cartão","NARRATIVA DO MÊS (frase pronta para o report)")], "3. Evolução")

@reg("23_tela4", "Rascunho da Tela 4 — Report por Unidade de Negócio")
def f23(): return _wire("4. Report por Unidade de Negócio",
    [("MOLÉCULAS",AZ),("% DO TOTAL DE NN",RX),("EM ANDAMENTO",VD),("CANCELADAS/STAND BY",VM),("NOVAS NO PERÍODO",LR)],
    [(16,192,350,200,"Barras 100% empilhadas","ESTÁGIO DAS OPORTUNIDADES"),
     (376,192,350,200,"Barras clusterizado","FRANQUIAS DE ATUAÇÃO DE NN"),
     (736,192,348,200,"Barras clusterizado","MOTIVOS DE CANCELAMENTO"),
     (16,402,350,180,"Rosca","CATEGORIA DAS MOLÉCULAS"),
     (376,402,350,180,"Barras clusterizado","MATURIDADE (FASE)"),
     (736,402,348,180,"Barras clusterizado","ÁREA TERAPÊUTICA"),
     (16,592,1068,32,"Cartão","RESUMO DA UNIDADE (parágrafo para o slide)")], "4. Report BU")

@reg("24_tela5", "Rascunho da Tela 5 — Carteira da Unidade")
def f24(): return _wire("5. Carteira da Unidade",
    [("MOLÉCULAS",AZ),("CARREGADAS",VD),("ENCERRADAS",VM),("DIAS MÉDIOS EM NN",CZ),("PRINCIPAL MOTIVO",LR)],
    [(16,192,530,190,"Colunas clusterizado","CARREGAMENTO DE MOLÉCULAS POR MÊS"),
     (556,192,528,190,"Barras empilhadas","ÁREA TERAPÊUTICA × SITUAÇÃO"),
     (16,392,1068,232,"Tabela","OPORTUNIDADES DA UNIDADE")], "5. Carteira")

@reg("25_tela6", "Rascunho da Tela 6 — Financeiro")
def f25(): return _wire("6. Financeiro",
    [("VPL TOTAL",VD),("PEAK SALES",AZ),("FAT. 5 ANOS",RX),("MARGEM MÉDIA",LR),("% COM DADO",VM)],
    [(16,192,530,220,"Barras clusterizado","VPL POR MOLÉCULA (10 maiores)"),
     (556,192,528,220,"Colunas clusterizado","FATURAMENTO PROJETADO (DRE 5 ANOS)"),
     (16,422,1068,200,"Tabela","PROJETOS COM DADOS FINANCEIROS")], "6. Financeiro")

@reg("26_tela7", "Rascunho da Tela 7 — Mapeamento Completo")
def f26(): return _wire("7. Mapeamento Completo",
    [("LINHAS EXIBIDAS",AZ),("MOLÉCULAS",RX),("FORNECEDORES",VD),("PAÍSES",LR),("ÁREAS TERAP.",CZ)],
    [(16,192,1068,430,"Tabela","MAPEAMENTO ATIVO — BASE COMPLETA (exporta para Excel)")], "7. Completo")

@reg("27_tela8", "Rascunho da Tela 8 — Qualidade da Base")
def f27(): return _wire("8. Qualidade da Base",
    [("SEM DATA DE FIM",VM),("% SEM DATA DE FIM",VM),("SEM MOTIVO",LR),("SEM UNIDADE",LR),("PARADOS >90 DIAS",CZ)],
    [(16,192,530,220,"Barras clusterizado","PENDÊNCIAS POR TIPO"),
     (556,192,528,220,"Barras clusterizado","PENDÊNCIAS POR RESPONSÁVEL"),
     (16,422,1068,200,"Tabela","PENDÊNCIAS — DETALHE POR PROJETO")], "8. Qualidade")

# =====================================================================
@reg("30_publicar", "Publicar o relatório para a nuvem")
def f30():
    f = Fig(1000, 420)
    f.titulo_janela("Dashboard Novos Negocios - Power BI Desktop")
    y = f.faixa(["Arquivo","Página Inicial","Inserir","Modelagem","Exibição"], 1)
    f.rect((0,y,f.w,y+82), fill=CHROME, outline=BORDA)
    alvo=None
    for i,(r,ic) in enumerate([("Colar","📋"),("Obter\ndados","▤"),("Transformar\ndados","⚙"),
                               ("Atualizar","⟳"),("Publicar","⇧")]):
        b=f.botao_faixa(16+i*120, y+8, r, larg=110, alt=66, icone=ic)
        if r=="Publicar": alvo=b
    topo=y+96
    f.rect((250,topo,760,topo+220), fill=(255,255,255), outline=BORDA)
    f.txt((270,topo+24), "Publicar no Power BI", 15, True)
    f.txt((270,topo+56), "Selecione um destino", 12, cor=TEXTO2)
    for i,(n,sel) in enumerate([("Meu workspace", False),("Novos Negócios", True)]):
        cy = topo+84+i*40
        if sel:
            f.rect((262,cy-6,748,cy+30), fill=(230,240,250)); alvo2=(262,cy-6,748,cy+30)
        f.txt((282,cy+12), n, 13, sel, TEXTO if sel else TEXTO2, anchor="lm")
    f.botao((530,topo+176,640,topo+208), "Selecionar", True)
    f.botao((650,topo+176,748,topo+208), "Cancelar")
    f.marca(alvo, 1, dx=-14, dy=-14)
    f.marca(alvo2, 2, dx=-14, dy=0)
    f.marca((530,topo+176,640,topo+208), 3, dx=-14, dy=0)
    f.legenda(["Salve o arquivo primeiro (Ctrl+S). Depois: Página Inicial → Publicar",
               "Escolha o workspace do time (NÃO use 'Meu workspace' — ninguém mais enxerga)",
               "Clique em Selecionar e espere a mensagem de sucesso"], y=f.h-78)
    return f

# =====================================================================
@reg("31_agendamento", "Power BI na web — atualização automática diária")
def f31():
    f = Fig(1100, 680)
    f.rect((0,0,f.w,f.h), fill=(255,255,255))
    f.rect((0,0,f.w,46), fill=(36,41,47))
    f.txt((20,23), "Power BI", 15, True, (255,255,255), anchor="lm")
    f.txt((140,23), "app.powerbi.com  ›  Novos Negócios  ›  Configurações do modelo semântico",
          12, False, (190,196,204), anchor="lm")
    y=70
    f.txt((24,y), "Dashboard Novos Negocios", 17, True); y+=44

    # --- credenciais
    f.rr((24,y,f.w-24,y+150), 6, fill=(250,251,252), outline=BORDA)
    f.txt((44,y+22), "▾  Credenciais da fonte de dados", 14, True)
    f.txt((44,y+54), "SharePoint  —  https://emspocbi.sharepoint.com/sites/NOVOSNEGCIOS",
          12, False, TEXTO2, mono=True)
    f.txt((44,y+80), "Status: falha ao conectar. As credenciais são inválidas.", 12, False, (190,60,50))
    a1 = f.botao((44,y+104,196,y+136), "Editar credenciais", True)
    f.marca(a1, 1, dx=-14, dy=0); y += 172

    # --- atualização agendada
    f.rr((24,y,f.w-24,y+300), 6, fill=(250,251,252), outline=BORDA)
    f.txt((44,y+22), "▾  Atualização agendada", 14, True)
    # toggle
    f.rr((44,y+52,88,y+76), 12, fill=(20,140,90))
    f.d.ellipse((68,y+54,86,y+74), fill=(255,255,255))
    f.txt((100,y+64), "Manter os dados atualizados", 12.5, True, TEXTO, anchor="lm")
    a2=(38,y+46,340,y+82)
    f.txt((44,y+98), "Frequência de atualização", 11.5, True, TEXTO2)
    f.rr((44,y+118,300,y+150), 4, fill=(255,255,255), outline=ACENTO, width=2)
    f.txt((58,y+134), "Diariamente", 12.5, True, TEXTO, anchor="lm")
    f.txtc((272,y+118,300,y+150), "▾", 12, cor=TEXTO2)
    a3=(44,y+118,300,y+150)
    f.txt((360,y+98), "Fuso horário", 11.5, True, TEXTO2)
    f.rr((360,y+118,700,y+150), 4, fill=(255,255,255), outline=BORDA)
    f.txt((374,y+134), "(UTC-03:00) Brasília", 12.5, False, TEXTO, anchor="lm")
    f.txt((44,y+172), "Horário", 11.5, True, TEXTO2)
    for i,h in enumerate(["07:00","13:00"]):
        f.rr((44+i*130,y+192,164+i*130,y+224), 4, fill=(255,255,255), outline=BORDA)
        f.txt((58+i*130,y+208), h, 12.5, False, TEXTO, anchor="lm")
        f.txt((150+i*130,y+208), "✕", 11, False, TEXTO3, anchor="lm")
    f.txt((320,y+208), "+ Adicionar outro horário", 12, False, ACENTO, anchor="lm")
    a4=(38,y+186,300,y+230)
    f.rr((44,y+244,60,y+260), 3, fill=(255,255,255), outline=(120,130,145), width=2)
    f.txtc((44,y+244,60,y+260), "✓", 12, True, ACENTO)
    f.txt((74,y+252), "Enviar e-mail de notificação de falha de atualização para mim",
          12, False, TEXTO, anchor="lm")
    a5=(38,y+238,700,y+266)
    f.marca(a2, 2, dx=-14, dy=0); f.marca(a3, 3, dx=-14, dy=0)
    f.marca(a4, 4, dx=-14, dy=0); f.marca(a5, 5, dx=-14, dy=0)
    f.legenda(["Editar credenciais → Método: OAuth2 → Entrar com o e-mail da EMS → "
               "Nível de privacidade: Organizacional",
               "Ligue a chave 'Manter os dados atualizados'",
               "Frequência: Diariamente",
               "Horário: adicione 07:00 e 13:00. Fuso: (UTC-03:00) Brasília",
               "Marque o aviso por e-mail — assim você descobre se a atualização falhar"],
              y=f.h-108)
    return f
