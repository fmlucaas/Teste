# -*- coding: utf-8 -*-
import json, sys, re
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name as L
sys.path.insert(0,'/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad')
from molmap import canon, PT
import kb, kb2
SP='/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad/'
OUT='/home/user/Teste/Hikma_Injetaveis_Avaliacao_NN.xlsx'

prods=json.load(open(SP+'products.json')); ev=json.load(open(SP+'evaluation2.json'))
matches=json.load(open(SP+'hist_matches.json'))
wb=xlsxwriter.Workbook(OUT,{'nan_inf_to_errors':True})
F={}
F['title']=wb.add_format({'bold':True,'font_size':17,'font_color':'#0B3D5C'})
F['sub']=wb.add_format({'font_size':10,'font_color':'#5A6B78','text_wrap':True,'valign':'top'})
F['h']=wb.add_format({'bold':True,'font_color':'white','bg_color':'#0B3D5C','border':1,'border_color':'#0B3D5C','text_wrap':True,'valign':'vcenter','align':'center'})
F['hin']=wb.add_format({'bold':True,'font_color':'#3D2B00','bg_color':'#FFD24D','border':1,'border_color':'#B98F00','text_wrap':True,'valign':'vcenter','align':'center'})
F['hcalc']=wb.add_format({'bold':True,'font_color':'white','bg_color':'#1F6F54','border':1,'border_color':'#1F6F54','text_wrap':True,'valign':'vcenter','align':'center'})
F['h2']=wb.add_format({'bold':True,'font_size':12,'font_color':'#0B3D5C','bottom':2,'border_color':'#0B3D5C'})
F['t']=wb.add_format({'text_wrap':True,'valign':'top','border':1,'border_color':'#D8DEE4','font_size':9})
F['tc']=wb.add_format({'text_wrap':True,'valign':'top','align':'center','border':1,'border_color':'#D8DEE4','font_size':9})
F['num']=wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#D8DEE4','font_size':9})
F['inp']=wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#B98F00','font_size':9,'bg_color':'#FFF7DB'})
F['inp2']=wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#B98F00','font_size':9,'bg_color':'#FFF7DB','num_format':'#,##0.00'})
F['calc']=wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#9FC4B5','font_size':9,'bg_color':'#EAF4EF','num_format':'#,##0.00'})
F['calcp']=wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#9FC4B5','font_size':9,'bg_color':'#EAF4EF','num_format':'0%'})
F['calct']=wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#9FC4B5','font_size':9,'bg_color':'#EAF4EF','text_wrap':True,'bold':True})
F['sim']=wb.add_format({'bold':True,'font_color':'#0E6B3D','bg_color':'#DFF3E6','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['nao']=wb.add_format({'bold':True,'font_color':'#8A1C1C','bg_color':'#FBE4E4','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['pa']=wb.add_format({'bold':True,'font_color':'#7A4B00','bg_color':'#FFF0CC','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['bold']=wb.add_format({'bold':True,'valign':'top','text_wrap':True})
F['wrap']=wb.add_format({'text_wrap':True,'valign':'top'})
F['note']=wb.add_format({'italic':True,'font_size':9,'font_color':'#8A1C1C','text_wrap':True,'valign':'top'})
F['kpi']=wb.add_format({'bold':True,'font_size':20,'font_color':'#0B3D5C','align':'center','valign':'vcenter','bg_color':'#EEF4F8','border':1,'border_color':'#C9D6E0'})
F['kpil']=wb.add_format({'font_size':9,'font_color':'#5A6B78','align':'center','valign':'vcenter','bg_color':'#EEF4F8','border':1,'border_color':'#C9D6E0','text_wrap':True})
F['pin']=wb.add_format({'bold':True,'align':'center','valign':'vcenter','border':1,'border_color':'#B98F00','bg_color':'#FFF7DB','font_size':12,'num_format':'#,##0.00'})
F['plab']=wb.add_format({'valign':'vcenter','text_wrap':True,'font_size':10})

# ============ 0. PREMISSAS ============
ws=wb.add_worksheet('0. Premissas (editável)'); P="'0. Premissas (editável)'"
ws.set_column('A:A',3); ws.set_column('B:B',46); ws.set_column('C:C',14); ws.set_column('D:D',72)
ws.write('B2','Premissas da avaliação econômica — edite aqui e a aba 3 recalcula sozinha',F['title'])
ws.write('B3','Estas cinco células comandam as colunas verdes da aba "3. Avaliação por Molécula". Troque pelos seus números e a decisão se refaz.',F['sub'])
for i,h in enumerate(['Premissa','Valor','Por que importa']): ws.write(5,1+i,h,F['h'])
prem=[('Cotação USD → BRL',6.00,'Mesma taxa usada no deck da Comissão (USD = R$ 6,00).'),
 ('Fator de nacionalização do acabado',1.55,'Multiplicador sobre o preço de transferência para chegar ao custo posto no Brasil: frete, seguro, imposto de importação, PIS/COFINS-importação, ICMS, despesas aduaneiras e armazenagem. 1,55 é ponto de partida conservador — calibre com o seu fiscal/logística, porque é a premissa que mais move o resultado.'),
 ('Margem bruta mínima para seguir',0.40,'Abaixo disso o produto acabado importado não paga registro, estoque, força de vendas e risco cambial.'),
 ('Margem bruta de zona cinzenta',0.25,'Entre este valor e o mínimo, a oportunidade só fecha com volume alto ou logística barata.'),
 ('Corte de mercado (R$ MM)',10.0,'Corte que o próprio time usa na lâmina "WarMap | Premissas".')]
r=6
for a,b,c in prem:
    ws.write(r,1,a,F['plab']); ws.write_number(r,2,b,F['pin']); ws.write(r,3,c,F['sub'])
    ws.set_row(r,13*(1+len(c)//72)); r+=1
USD,FAT,MMIN,MMARG,CORTE=[f'{P}!$C${i}' for i in range(7,12)]
r+=1
ws.write(r,1,'Como a decisão é recalculada',F['h2']); r+=1
ws.write(r,1,'Custo posto (R$) = Preço de transferência (US$) × cotação × fator de nacionalização.\n'
  'Margem bruta = (Preço médio NRC − Custo posto) ÷ Preço médio NRC.\n'
  'Veredito econômico = Viável / Marginal / Inviável conforme as duas faixas de margem acima.\n'
  'Decisão recalculada = combina o corte de mercado, o veredito econômico e a triagem qualitativa desta análise.',F['sub'])
ws.set_row(r,58)

# ============ 1. LEIA-ME ============
ws=wb.add_worksheet('1. Leia-me e Metodologia')
ws.set_column('A:A',3); ws.set_column('B:B',122)
ws.write('B2','Catálogo Hikma de Injetáveis 2025 — Avaliação para Licenciamento de Produto Acabado (EMS Non Retail)',F['title'])
r=3
blocos=[('O que mudou nesta versão (v2)',
 'A v1 tratava "molécula já no pipeline do EMS" como motivo para não seguir. Isso está errado para Novos '
 'Negócios: se o Grupo já decidiu que quer a molécula, licenciar o acabado ANTECIPA a entrada em 2 a 5 anos '
 'contra desenvolver internamente. Nesta versão a presença em pipeline/gate virou PONTO POSITIVO (eixo E3) e '
 'aparece como rota "BRIDGE" — entrar com importado agora e migrar para produção própria depois.\n'
 'A v1 também subponderava preço. Como o escopo é licenciamento de PRODUTO ACABADO IMPORTADO, o preço '
 'unitário é a restrição que manda: paracetamol IV pode ser clinicamente ótimo e ainda assim não pagar frete, '
 'imposto e estoque. O eixo econômico virou o de maior peso (0-30) e derrubou paracetamol, clindamicina, '
 'milrinona, nicardipino e outros que a v1 recomendava.'),
('A tese, em uma frase',
 'O catálogo da Hikma é majoritariamente genérico injetável do mercado americano, e essa economia não '
 'atravessa para o Brasil. O valor está concentrado em (a) uma dúzia de itens de nicho e alto valor por '
 'unidade, (b) a plataforma de apresentação pronta para uso, que é conversa de tecnologia e não de importação, '
 'e (c) um CDA já aberto que barateia o custo de descobrir tudo isso.'),
('Os cinco eixos do score',
 'E1 · Economia do acabado importado (0-30) — faixa de preço unitário no hospital brasileiro. É o eixo que decide.\n'
 'E2 · Escassez e barreira técnica (0-20) — poucos fornecedores, histórico de falta, complexidade que defende margem.\n'
 'E3 · Aceleração (0-20) — quantos anos o licenciamento economiza contra desenvolver internamente. Pipeline/gate pontua ALTO.\n'
 'E4 · Diferenciação de apresentação (0-15) — bolsa pronta para uso, seringa preenchida, condição de RLD.\n'
 'E5 · Sinal do histórico (−10 a +15) — relação aberta soma; "cemitério de prospecção" subtrai.'),
('Decisão por regras, não por nota',
 'A recomendação binária não sai de um corte de nota. Ela passa por cinco portas, e basta uma fechada para '
 'virar NÃO: mercado inexistente no Brasil; fora do escopo Non Retail; cemitério de prospecção sem diferencial '
 'novo; economia do acabado que não fecha; e um piso geral de qualidade. Acima disso ainda existe o veto de '
 'especialista, que derruba molécula com nota razoável e tese comercial fraca. Cada porta fechada aparece '
 'escrita na linha, então dá para discordar item a item.'),
('Cemitério de prospecção',
 'Molécula com 4 ou mais parceiros abordados e 70% ou mais dormentes. Não é neutro: é evidência de que o '
 'problema nunca foi achar fornecedor, foi fechar preço. Micafungina (7 parceiros, 86% dormentes) e '
 'bortezomibe (9 parceiros, 78%) caem por aqui — reabrir sem premissa de custo nova é repetir o ciclo.'),
('ATENÇÃO — a faixa de preço é hipótese, não medição',
 'Você disse que a base IQVIA Non-Retail não cabia no anexo, então classifiquei as 136 moléculas em cinco '
 'faixas de preço por conhecimento de mercado. É a premissa mais frágil de todo o arquivo. As colunas amarelas '
 'da aba 3 existem exatamente para você colar o IQVIA por cima: preencheu, as colunas verdes recalculam e a '
 '"DECISÃO RECALCULADA" passa a valer mais que a minha.'),
]
for t,d in blocos:
    ws.write(r,1,t,F['h2']); r+=1
    ws.write(r,1,d,F['note'] if t.startswith('ATENÇÃO') else F['sub'])
    ws.set_row(r,13.5*(1+d.count('\n')+len(d)//118)); r+=2

# ============ 2. RESUMO E CESTAS ============
ws=wb.add_worksheet('2. Resumo e Cestas')
ws.set_column('A:A',3); ws.set_column('B:B',30); ws.set_column('C:C',22); ws.set_column('D:I',15); ws.set_column('J:J',70)
ws.write('B2','Resumo executivo e desenho do negócio',F['title'])
sim=[e for e in ev if e['RECOMENDAÇÃO']=='SIM']
kpis=[('136','moléculas'),('321','apresentações'),(str(len(sim)),'passam na triagem'),
 (str(sum(1 for e in ev if e['Prioridade'].startswith('A'))),'atacar agora'),
 (str(sum(1 for e in ev if e['Viabilidade acabado importado']=='Inviável')),'inviáveis como acabado'),
 (str(sum(1 for e in ev if 'VETO' in e['Override de especialista'])),'vetadas por tese fraca'),
 (str(sum(1 for e in ev if 'CEMITÉRIO' in e['Sinal do histórico'])),'cemitérios'),('1','CDA aberto')]
c=1
for v,l in kpis:
    ws.merge_range(3,c,4,c,v,F['kpi']); ws.merge_range(5,c,6,c,l,F['kpil']); c+=1
r=8
ws.write(r,1,'A leitura crítica',F['h2']); r+=1
for t in [
 'Das 136 moléculas, 114 não são negócio de acabado importado. Não por mérito clínico — por preço unitário. '
 '84 delas estão abaixo de R$ 50 por unidade, faixa em que frete, imposto e estoque comem a margem inteira.',
 'Você tinha razão sobre o paracetamol: na v1 ele era a segunda maior recomendação. Caiu. Mesmo com a bolsa '
 'RLD como diferencial, paracetamol IV é disputado por centavos em licitação. O mesmo veto pegou clindamicina, '
 'milrinona, nicardipino, levocarnitina e gluconato férrico.',
 'Você também tinha razão sobre o pipeline. Corrigido: dexmedetomidina está em Gate no EMS e virou candidata a '
 'BRIDGE — importar da Hikma para entrar agora e migrar para produção própria quando o projeto interno maturar. '
 'É o único jeito de transformar um projeto de 4 anos em receita no ano que vem.',
 'O padrão que emerge: o dinheiro está em nicho de alto valor e baixo volume — Icatibanto, Regadenoson, '
 'Valrubicina, Eribulina, Dantroleno. Preço alto por unidade, poucos competidores, compra por especialidade e '
 'não por pregão de menor preço. É o oposto do perfil do catálogo como um todo.',
 'Dois "não insista": micafungina (7 parceiros, 86% dormentes) e bortezomibe (9 parceiros, 78%). Quando a casa '
 'já bateu nessa porta tantas vezes, o gargalo é preço de origem, e a Hikma não é fornecedor de baixo custo.',
 'A Hikma é multinacional, o que pela lâmina WarMap é "caso a discutir". Some a isso o fato de ser um catálogo '
 'construído para o mercado americano: o preço de transferência tende a vir ancorado em preço americano, que é '
 'o pior ponto de partida possível para competir no não-retail brasileiro. Trate isso como a primeira pergunta, '
 'não como detalhe.',
]:
    ws.write(r,1,'•',F['bold']); ws.merge_range(r,2,r,9,t,F['wrap']); ws.set_row(r,13*(1+len(t)//110)); r+=1

r+=1
ws.write(r,1,'Como eu desenharia o negócio: 4 cestas',F['h2']); r+=1
cestas=[
 ('CESTA 1 — Nicho de alto valor','Onde a economia de acabado importado realmente fecha. É por aqui que se abre a negociação.',
  ['Icatibanto','Regadenoson','Valrubicina','Eribulina','Dantroleno','Dexrazoxano','Tiotepa','Cladribina']),
 ('CESTA 2 — Bridge de aceleração','O EMS já quer a molécula. Importar antecipa a entrada; a produção própria assume depois.',
  ['Dexmedetomidina','Vancomicina']),
 ('CESTA 3 — Dossiê, não acabado','Produto interessa, importar não fecha. Conversa é de transferência de tecnologia — e não é o seu escopo, é o de P&D.',
  ['Paracetamol + Ibuprofeno','Paracetamol','Clindamicina','Linezolida']),
 ('CESTA 4 — Não perseguir','Commodity que o EMS já produz, mercado inexistente no Brasil, ou cemitério de prospecção.',
  ['Micafungina','Bortezomibe','Ceftriaxona','Cefazolina','Meropenem','Ondansetrona','e mais 100']),
]
for i,h in enumerate(['Cesta','Lógica','Moléculas']): ws.write(r,1+i if i<2 else 3,h,F['h'])
ws.set_column('D:D',66); r+=1
for nome,logica,mols in cestas:
    ws.write(r,1,nome,F['bold']); ws.write(r,2,logica,F['t']); ws.write(r,3,', '.join(mols),F['t'])
    ws.set_row(r,13*(1+max(len(logica)//22,len(', '.join(mols))//64))); r+=1

r+=1
ws.write(r,1,'O que pedir à Hikma na próxima conversa (o CDA já cobre)',F['h2']); r+=1
for q in [
 'Price list CIF Santos das 8 moléculas da Cesta 1, em US$ por unidade. Sem isso nada mais importa — é o número que decide tudo.',
 'Brasil está livre? Confirmar se não há distribuidor ou licenciado com direitos na LatAm para esses itens.',
 'Certificado de BPF dos sites que fabricam a Cesta 1, e se já foram inspecionados pela Anvisa.',
 'Dossiês em CTD e disponibilidade de dados para registro por via abreviada — o que encurta o cronograma.',
 'Estabilidade das bolsas pronta-para-uso: shelf life, faixa de temperatura e se suportam transporte marítimo.',
 'Disposição para transferência de tecnologia na Cesta 3 — pergunta diferente da de importação, e provavelmente com outro interlocutor lá dentro.',
 'Volume mínimo por pedido e lead time: em produto de nicho, MOQ alto mata a operação mesmo com preço bom.',
]:
    ws.write(r,1,'→',F['bold']); ws.merge_range(r,2,r,9,q,F['wrap']); ws.set_row(r,13*(1+len(q)//110)); r+=1

r+=1
ws.write(r,1,'Recomendadas — lista completa',F['h2']); r+=1
hdr=['Prioridade','Molécula','Faixa de preço','Score','Rota','Sinal do histórico']
for i,h in enumerate(hdr): ws.write(r,1+i,h,F['h'])
r+=1
ordem={'A - Atacar agora':0,'B - Qualificar':1,'C - Fila':2}
for e in sorted(sim,key=lambda x:(ordem[x['Prioridade']],-x['SCORE TOTAL (0-100)'])):
    pf=F['sim'] if e['Prioridade'].startswith('A') else (F['pa'] if e['Prioridade'].startswith('B') else F['tc'])
    ws.write(r,1,e['Prioridade'],pf); ws.write(r,2,e['Molécula (PT/DCB)'],F['t'])
    ws.write(r,3,e['Faixa de preço (hipótese)'],F['t']); ws.write(r,4,e['SCORE TOTAL (0-100)'],F['num'])
    ws.write(r,5,e['Rota recomendada'],F['t']); ws.write(r,6,e['Sinal do histórico'],F['t']); r+=1

# ============ 3. AVALIAÇÃO ============
base=['Molécula (PT/DCB)','Molécula (EN)','Área terapêutica','RECOMENDAÇÃO','Prioridade','Rota recomendada',
 'SCORE TOTAL (0-100)','E1 Economia do acabado (0-30)','E2 Escassez/barreira (0-20)','E3 Aceleração (0-20)',
 'E4 Diferenciação (0-15)','E5 Sinal do histórico (-10 a 15)','Faixa de preço (hipótese)',
 'Viabilidade acabado importado','Aceleração vs desenv. interno','Relevância (hipótese)','Override de especialista']
inp=['[IQVIA] Mercado NR Brasil (R$ MM)','[IQVIA] Preço médio unitário (R$)','[IQVIA] Nº de competidores',
     '[HIKMA] Preço de transferência (US$/un)']
calc=['Custo posto no Brasil (R$)','Margem bruta estimada','Veredito econômico','Passa corte de mercado?','DECISÃO RECALCULADA']
rest=['Status no Grupo EMS','Detalhe EMS','Sinal do histórico','Já prospectada pela equipe NN',
 'Tipo de match no histórico','Situação do histórico','Prospectada por VOCÊ (Lucas Medina)',
 'Contato prévio com a Hikma','Nº parceiros já abordados','Nº registros no histórico','Parceiros já contatados',
 'Responsáveis NN','Status no histórico','Datas de entrada','Forma farmacêutica','Nº de apresentações (SKUs)',
 'Controlado (Port. 344/98)','Referência (comparable to)','FDA rating','Categoria terapêutica (Hikma)',
 'Produtos no catálogo','NDCs','Páginas no PDF','Justificativa','Riscos e condicionantes']
cols=base+inp+calc+rest
Wd=[26,22,25,14,16,44, 9,11,11,11,11,12, 20,16,16,14,20,  15,15,13,16,  15,12,14,14,20,
    22,32,26,14,16,18,14,14,11,11,44,22,26,22,26,10,12,28,26,30,44,38,12,95,80]
ws=wb.add_worksheet('3. Avaliação por Molécula'); ws.freeze_panes(1,1); ws.set_row(0,44)
i0=len(base); i1=i0+len(inp); i2=i1+len(calc)
for i,h in enumerate(cols):
    f=F['hin'] if i0<=i<i1 else (F['hcalc'] if i1<=i<i2 else F['h'])
    ws.write(0,i,h,f); ws.set_column(i,i,Wd[i])
ordem2={'A - Atacar agora':0,'B - Qualificar':1,'C - Fila':2,'—':3}
data=sorted(ev,key=lambda x:(x['RECOMENDAÇÃO']!='SIM',ordem2[x['Prioridade']],-x['SCORE TOTAL (0-100)']))
for ri,e in enumerate(data,1):
    for c,k in enumerate(base):
        v=e[k]
        f=F['t']
        if k=='RECOMENDAÇÃO': f=F['sim'] if v=='SIM' else F['nao']
        elif k=='Prioridade': f=F['sim'] if v.startswith('A') else (F['pa'] if v.startswith('B') else F['tc'])
        elif k.startswith(('SCORE','E1','E2','E3','E4','E5')): f=F['num']
        elif k=='Viabilidade acabado importado': f=F['sim'] if v=='Viável' else (F['pa'] if v=='Marginal' else F['nao'])
        elif k=='Override de especialista': f=F['nao'] if 'VETO' in v else F['tc']
        ws.write(ri,c,v,f)
    for c in range(i0,i1): ws.write_blank(ri,c,None,F['inp2'] if c>i0 else F['inp'])
    R=ri+1
    MK,PR,NC,TR=[L(i0)+str(R),L(i0+1)+str(R),L(i0+2)+str(R),L(i0+3)+str(R)]
    CP,MG,VE,PC=[L(i1)+str(R),L(i1+1)+str(R),L(i1+2)+str(R),L(i1+3)+str(R)]
    ws.write_formula(ri,i1,  f'=IF({TR}="","",{TR}*{USD}*{FAT})',F['calc'])
    ws.write_formula(ri,i1+1,f'=IF(OR({PR}="",{CP}=""),"",({PR}-{CP})/{PR})',F['calcp'])
    ws.write_formula(ri,i1+2,f'=IF({MG}="","preencher",IF({MG}>={MMIN},"Viável",IF({MG}>={MMARG},"Marginal","Inviável")))',F['calct'])
    ws.write_formula(ri,i1+3,f'=IF({MK}="","preencher",IF({MK}>={CORTE},"PASSA","NÃO PASSA"))',F['calct'])
    ws.write_formula(ri,i1+4,
      f'=IF(AND({MK}="",{PR}=""),"Preencher IQVIA",'
      f'IF(AND({MK}<>"",{MK}<{CORTE}),"NÃO — mercado abaixo do corte",'
      f'IF({VE}="Inviável","NÃO — economia não fecha",'
      f'IF(D{R}="NÃO","NÃO — vetada na triagem",'
      f'IF({VE}="Marginal","REAVALIAR — margem apertada","SIM")))))',F['calct'])
    for c,k in enumerate(rest, start=i2):
        v=e[k]; f=F['t']
        if k in ('Nº parceiros já abordados','Nº registros no histórico','Nº de apresentações (SKUs)'): f=F['num']
        elif k=='Contato prévio com a Hikma': f=F['sim'] if v=='SIM' else F['tc']
        elif k=='Controlado (Port. 344/98)': f=F['pa'] if v=='SIM' else F['tc']
        elif k=='Sinal do histórico': f=F['nao'] if 'CEMITÉRIO' in v else (F['sim'] if 'HIKMA' in v else F['t'])
        ws.write(ri,c,v,f)
ws.autofilter(0,0,len(data),len(cols)-1)

# ============ 4. CATÁLOGO SKU ============
cols4=['Página PDF','Produto (catálogo Hikma)','Molécula (EN)','Molécula (PT/DCB)','Área terapêutica',
 'Categoria terapêutica (Hikma)','Referência (Comparable To)','Descrição do produto','FDA Rating','NDC',
 'Concentração','Conteúdo total de fármaco','Volume de enchimento','Tamanho da unidade','Embalagem',
 'Fechamento (closure)','Forma','Bolsa pronta p/ uso','Faixa de preço','Rota recomendada','Recomendação']
recmap={e['Molécula (EN)']:e for e in ev}
ws=wb.add_worksheet('4. Catálogo Completo (SKU)'); ws.freeze_panes(1,2); ws.set_row(0,34)
W4=[9,46,22,24,25,30,24,34,26,15,20,22,16,16,14,14,10,11,20,44,13]
for i,h in enumerate(cols4): ws.write(0,i,h,F['h']); ws.set_column(i,i,W4[i])
ri=0
for p in sorted(prods,key=lambda x:(x['page'],x['product_name'],x['ndc'])):
    ri+=1; m=canon(p['product_name']); e=recmap[m]
    powder='Pó' if 'powder' in (p['concentration']+p['fill_volume']).lower() else 'Solução'
    bag='SIM' if re.search(r'\bbags?\b',p['pack_quantity'],re.I) or re.search(r'\bin\s+[\d.]+%|Dextrose|NaCl|Sodium Chloride',p['product_name'],re.I) else 'NÃO'
    vals=[p['page'],p['product_name'],m,PT[m],e['Área terapêutica'],p['therapeutic_category'],p['comparable_to'],
     p['product_description'],p['fda_rating'],p['ndc'],p['concentration'],p['total_drug_content'],p['fill_volume'],
     p['unit_size'],p['pack_quantity'],p['closure'],powder,bag,e['Faixa de preço (hipótese)'],
     e['Rota recomendada'],e['RECOMENDAÇÃO']]
    for c,v in enumerate(vals):
        f=F['t']
        if c==0: f=F['num']
        elif c in (16,17): f=F['sim'] if v=='SIM' else F['tc']
        elif c==20: f=F['sim'] if v=='SIM' else F['nao']
        ws.write(ri,c,v,f)
ws.autofilter(0,0,ri,len(cols4)-1)

# ============ 5. HISTÓRICO ============
cols5=['Molécula Hikma (PT)','Tipo de match','Molécula no histórico','Fornecedor / Parceiro','Status','Situação',
 'Responsável','Categoria','Área Terapêutica','Data de Entrada','Início Prospecção','Concl. Prospecção',
 'Início CDA','Concl. CDA','Início Negociações','Concl. Negociações']
ws=wb.add_worksheet('5. Cruzamento Histórico NN'); ws.freeze_panes(1,1); ws.set_row(0,34)
W5=[26,20,34,32,20,18,20,22,24,14,14,14,14,14,14,14]
for i,h in enumerate(cols5): ws.write(0,i,h,F['h']); ws.set_column(i,i,W5[i])
ri=0
for m in sorted(matches,key=lambda x:(x['mol_pt'],x['kind']!='EXATO')):
    ri+=1; h=m['rec']; st=str(h['Status']).strip()
    vals=[m['mol_pt'],m['kind'],str(h['Molécula']),str(h['Fornecedor / Parceiro']),st,
      'PASSIVO (dormente)' if st=='PASSIVO' else 'ATIVO',str(h['Responsável']),str(h['Categoria']),
      str(h['Área Terapêutica']),str(h['Data de Entrada'])[:10],str(h['Data Início Prospecção'])[:10],
      str(h['Data Conclusão Prospecção'])[:10],str(h['Data Inicio Processo de CDA'])[:10],
      str(h['Data de Concl. CDA'])[:10],str(h['DATA - Inicio Negociações com parceiro'])[:10],
      str(h['DATA - Conclusão Negociações com parceiro'])[:10]]
    for c,v in enumerate(vals):
        f=F['t']
        if c==1: f=F['sim'] if v=='EXATO' else F['tc']
        elif c==5: f=F['pa'] if v.startswith('PASSIVO') else F['tc']
        ws.write(ri,c,v,f)
ws.autofilter(0,0,ri,len(cols5)-1)

# ============ 6. EMS ============
cols6=['Bloco','Situação no Grupo EMS','Molécula / Item','No catálogo Hikma?','Leitura para Novos Negócios']
rows6=[]
for m,t in kb.EMS_PORTFOLIO_INJ.items():
    e=recmap[m]; dif='bolsa/seringa' if ('Bolsa' in e['Forma farmacêutica'] or 'Seringa' in e['Forma farmacêutica']) else ''
    rows6.append(['Antibióticos J01 — Non Retail','PORTFÓLIO',t.replace(' Solução injetável',''),'SIM',
      ('Só interessa pela apresentação diferenciada (%s) — e ainda assim como dossiê, não como importado.'%dif) if dif
      else 'EMS já produz. Importar destrói margem. Descartar.'])
for t in kb.EMS_PORTFOLIO_INJ_OUTROS:
    rows6.append(['Antibióticos J01 — Non Retail','PORTFÓLIO',t,'NÃO','Sem correspondente no catálogo Hikma.'])
for t in kb.EMS_ATB_GATE_OUTROS:
    rows6.append(['Antibióticos J01 — Non Retail','PIPELINE / GATE (0-3)',t,'NÃO',
      'Endereçado internamente e a Hikma não cobre — candidato a BRIDGE com OUTRO parceiro.'])
for m,t in kb.EMS_ANEST_PORTFOLIO.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','PORTFÓLIO',t,'SIM','EMS já tem. Controlado 344/98. Descartar.'])
for m,t in kb.EMS_ANEST_PIPELINE.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','PIPELINE',t,'SIM','Escetamina em pipeline; a Hikma oferece cetamina racêmica (controlada). Não substitui.'])
for m,t in kb.EMS_ANEST_GATE.items():
    e=recmap[m]
    rows6.append(['Anestésicos injetáveis (ATC N)','EM AVALIAÇÃO (GATE 0-3)',t,'SIM',
      'BRIDGE: licenciar antecipa 3 a 5 anos. %s'%('Bolsa pronta para uso reforça o caso.' if 'Bolsa' in e['Forma farmacêutica'] else 'Preço baixo enfraquece o caso de importado.')])
for t in kb.EMS_ANEST_GATE_OUTROS:
    rows6.append(['Anestésicos injetáveis (ATC N)','EM AVALIAÇÃO (GATE 0-3)',t,'NÃO','Em gate interno; Hikma não cobre.'])
for t in ['Ciprofol','Adamgammadex','Suzetrigina']:
    rows6.append(['Anestésicos injetáveis (ATC N)','PROSPECÇÃO NOVOS NEGÓCIOS',t,'NÃO','Já em prospecção pelo NN.'])
for m,t in kb.EMS_NOGO.items():
    rows6.append(['Antibióticos — decisões do comitê','NO GO',m,'NÃO',t+' — não reabrir sem fato novo.'])
ws=wb.add_worksheet('6. Portfólio-Pipeline EMS'); ws.freeze_panes(1,0); ws.set_row(0,34)
for i,(h,w) in enumerate(zip(cols6,[34,28,44,18,80])): ws.write(0,i,h,F['h']); ws.set_column(i,i,w)
for ri,row in enumerate(rows6,1):
    for c,v in enumerate(row): ws.write(ri,c,v,F['pa'] if (c==3 and v=='SIM') else F['t'])
ws.autofilter(0,0,len(rows6),len(cols6)-1)

# ============ 7. LACUNAS ============
ws=wb.add_worksheet('7. Lacunas e Perguntas')
ws.set_column('A:A',3); ws.set_column('B:B',34); ws.set_column('C:C',95); ws.set_column('D:D',24)
ws.write('B2','O que ainda falta para fechar a decisão',F['title'])
ws.write('B3','A aba 3 já tem as colunas amarelas prontas para receber o IQVIA. Estas são as lacunas que nem o IQVIA resolve.',F['sub'])
for i,h in enumerate(['Lacuna','Por que trava','Onde buscar']): ws.write(4,1+i,h,F['h'])
gaps=[('Preço de transferência da Hikma','É o número que decide tudo. Sem ele, a coluna de margem fica vazia e toda a priorização continua sendo hipótese minha.','Hikma, sob o CDA vigente'),
 ('Fator real de nacionalização','Usei 1,55 como ponto de partida. Se o número verdadeiro for 1,8, metade da Cesta 1 morre; se for 1,3, a Cesta 2 revive.','Fiscal / Comex / Logística'),
 ('Situação patentária','Eribulina e valrubicina podem ter proteção vigente. É o que separa oportunidade de perda de tempo.','Cortellis — Marcas e Patentes'),
 ('Registro na Anvisa por molécula','Define se é via abreviada, registro novo ou molécula sem precedente no país. Muda o cronograma em anos.','Assuntos Regulatórios'),
 ('Volume real do nicho','Levotiroxina IV e fentolamina podem ter mercado de poucas centenas de unidades/ano — preço alto não salva volume ínfimo.','IQVIA NRC — unidades, não só valor'),
 ('Motivo de perda dos dormentes','290 registros PASSIVO sem justificativa. Sem saber se micafungina caiu por preço, prazo ou qualidade, não dá para decidir se reabre.','Enriquecer a base de NN'),
 ('Exclusividade e território','A Hikma pode já ter compromissos na LatAm para os itens de nicho.','Hikma'),
 ('Posição sobre parceiro multinacional','A lâmina WarMap prioriza empresas não multinacionais. Precisa de aval antes de investir tempo.','Diretoria de Novos Negócios'),
 ('Apetite do hospital pelo RTU','Toda a tese de bolsa pronta para uso depende de o comprador aceitar pagar prêmio. Se não aceitar, a Cesta 2 e 3 caem juntas.','Pesquisa com farmácia hospitalar'),
 ('Capacidade de fill-finish do EMS','Define se a Cesta 3 é transferência de tecnologia viável ou conversa sem lastro.','P&D / Industrial')]
r=5
for a,b,c in gaps:
    ws.write(r,1,a,F['t']); ws.write(r,2,b,F['t']); ws.write(r,3,c,F['t']); ws.set_row(r,13*(1+len(b)//95)); r+=1
r+=1
ws.write(r,1,'Perguntas para você',F['h2']); r+=1
for q in ['Oncologia continua no seu escopo? Cesta 1 é metade oncológica (eribulina, valrubicina, tiotepa, cladribina, dexrazoxano) e o deck de set/26 não trouxe oncologia.',
 'O CDA da vancomicina é seu para ampliar ou é da Livia? Isso muda quem conduz a conversa das outras 21 moléculas.',
 'Existe margem mínima institucional para produto importado? Se for maior que 40%, a Cesta 1 encolhe.',
 'Transferência de tecnologia entra no seu mandato ou você passa a Cesta 3 para P&D?',
 'Qual o apetite para nicho? Icatibanto e valrubicina são mercados de poucos milhões — alto valor unitário, receita total modesta.',
 'Controlados da Portaria 344/98 estão fora por política, ou avaliamos caso a caso?']:
    ws.write(r,1,'?',F['bold']); ws.merge_range(r,2,r,3,q,F['wrap']); ws.set_row(r,13*(1+len(q)//115)); r+=1

# ============ 8. MELHORIAS ============
ws=wb.add_worksheet('8. Melhorias sugeridas')
ws.set_column('A:A',3); ws.set_column('B:B',36); ws.set_column('C:C',100)
ws.write('B2','Melhorias para a próxima versão',F['title'])
for i,h in enumerate(['Melhoria','Como fazer e o que muda']): ws.write(4,1+i,h,F['h'])
mel=[('Trocar as faixas de preço pelo IQVIA','Colar preço médio NRC nas colunas amarelas. O eixo E1 deixa de ser hipótese e a priorização passa a ser defensável no gate.'),
 ('Campo de motivo de perda na base NN','Obrigatório ao mover para PASSIVO. Hoje 290 linhas dormentes sem explicação — é o maior desperdício de inteligência que vocês têm.'),
 ('Marcar parceiro multinacional no cadastro','500 parceiros sem porte nem origem. Com o campo, a regra do WarMap vira filtro automático em vez de discussão caso a caso.'),
 ('Padronizar molécula por DCB','"Vancomicina Injetável" e "VANCOMICINA" são registros distintos; "POLIMIXIN B", "REMIFENTANILA" e "FOSAPREPTANTO" estão com grafia errada. Um campo DCB único acaba com o retrabalho de cruzamento.'),
 ('Registrar preço proposto no histórico','Sem o preço que cada parceiro ofereceu, é impossível saber se a molécula é inviável ou se o parceiro é que era caro.'),
 ('Trazer as decisões do comitê para a base','A coluna STATUS GRUPO EMS do deck (NO GO / GATE / PIPELINE) deveria viver dentro do controle de NN — evita prospectar o que já foi vetado.'),
 ('Rotina anual de re-acesso aos dormentes','Combogesic parou em 2018 e voltou a ser prioridade em 2026. Sem rotina, oportunidades assim só reaparecem por acaso.'),
 ('Separar "molécula" de "apresentação"','O diferencial da Hikma é apresentação, não molécula. Enquanto a base for por molécula, esse tipo de oportunidade continua invisível.')]
r=5
for a,b in mel:
    ws.write(r,1,a,F['t']); ws.write(r,2,b,F['t']); ws.set_row(r,13*(1+len(b)//100)); r+=1

wb.close()
print('OK ->',OUT)
print('SIM:',len(sim),'| moléculas:',len(ev),'| SKUs:',len(prods),'| histórico:',len(matches))
