# -*- coding: utf-8 -*-
"""Visão única: uma linha por NDC, agrupada por molécula (células mescladas),
com as colunas de preenchimento valendo uma vez por molécula."""
import json, sys, re
import xlsxwriter
from collections import defaultdict
sys.path.insert(0,'/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad')
from molmap import canon, PT
import kb
SP='/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad/'
OUT='/home/user/Teste/Hikma_Injetaveis_Base_NN.xlsx'

prods=json.load(open(SP+'products.json')); ev=json.load(open(SP+'final.json'))
matches=json.load(open(SP+'hist_matches.json'))
EV={e['Molécula (EN)']:e for e in ev}
SLIDE={}
for m in kb.EMS_PORTFOLIO_INJ: SLIDE[m]='Slide 25'
for m in list(kb.EMS_ANEST_PORTFOLIO)+list(kb.EMS_ANEST_PIPELINE)+list(kb.EMS_ANEST_GATE): SLIDE[m]='Slide 34'

bymol=defaultdict(list)
for p in prods: bymol[canon(p['product_name'])].append(p)
for m in bymol: bymol[m].sort(key=lambda s:(s['product_name'], s['page'], s['ndc']))

def schedule(n):
    m=re.search(r'\bC-(I{1,3}V?|IV|V)\b', n); return 'C-'+m.group(1) if m else '—'

wb=xlsxwriter.Workbook(OUT,{'nan_inf_to_errors':True})
def hdr(bg,fc='white',bc=None):
    return wb.add_format({'bold':True,'font_color':fc,'bg_color':bg,'border':1,'border_color':bc or bg,
        'text_wrap':True,'valign':'vcenter','align':'center','font_size':9})
def grp(bg,fc='white'):
    return wb.add_format({'bold':True,'font_color':fc,'bg_color':bg,'align':'center','valign':'vcenter','border':1,'font_size':10})
F={}
F['title']=wb.add_format({'bold':True,'font_size':17,'font_color':'#0B3D5C'})
F['sub']=wb.add_format({'font_size':10,'font_color':'#5A6B78','text_wrap':True,'valign':'top'})
F['h2']=wb.add_format({'bold':True,'font_size':12,'font_color':'#0B3D5C','bottom':2,'border_color':'#0B3D5C'})
F['hrec']=hdr('#8A1C1C'); F['hcat']=hdr('#0B3D5C'); F['hems']=hdr('#1F6F54')
F['hnn']=hdr('#5B3A8C'); F['hin']=hdr('#FFD24D','#3D2B00','#B98F00')
GRP_REC=grp('#8A1C1C'); GRP_CAT=grp('#0B3D5C'); GRP_EMS=grp('#1F6F54'); GRP_NN=grp('#5B3A8C'); GRP_IN=grp('#FFD24D','#3D2B00')
B='#C3CBD4'                                   # borda entre blocos de molécula
F['m']   =wb.add_format({'text_wrap':True,'valign':'top','border':1,'border_color':B,'font_size':9,'bg_color':'#F7F9FB'})
F['mc']  =wb.add_format({'text_wrap':True,'valign':'vcenter','align':'center','border':1,'border_color':B,'font_size':9,'bg_color':'#F7F9FB'})
F['mnum']=wb.add_format({'valign':'vcenter','align':'center','border':1,'border_color':B,'font_size':9,'bg_color':'#F7F9FB'})
F['msim']=wb.add_format({'bold':True,'font_color':'#0E6B3D','bg_color':'#DFF3E6','align':'center','valign':'vcenter','border':1,'border_color':B,'font_size':9})
F['mnao']=wb.add_format({'bold':True,'font_color':'#8A1C1C','bg_color':'#FBE4E4','align':'center','valign':'vcenter','border':1,'border_color':B,'font_size':9})
F['mn']  =wb.add_format({'align':'center','valign':'vcenter','border':1,'border_color':B,'font_size':9,'font_color':'#8A93A0','bg_color':'#F7F9FB'})
F['t']   =wb.add_format({'text_wrap':True,'valign':'top','border':1,'border_color':'#E4E9EE','font_size':9})
F['tc']  =wb.add_format({'text_wrap':True,'valign':'top','align':'center','border':1,'border_color':'#E4E9EE','font_size':9})
F['num'] =wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#E4E9EE','font_size':9})
F['ok']  =wb.add_format({'align':'center','valign':'top','border':1,'border_color':'#E4E9EE','font_size':9,'font_color':'#0E6B3D','bold':True})
F['inp'] =wb.add_format({'border':1,'border_color':'#B98F00','bg_color':'#FFF7DB','font_size':9,'valign':'top'})
F['bold']=wb.add_format({'bold':True,'valign':'top','text_wrap':True})

# ================= 1. LEIA-ME =================
ws=wb.add_worksheet('1. Leia-me'); ws.set_column('A:A',3); ws.set_column('B:B',120)
ws.write('B2','Catálogo Hikma de Injetáveis 2025 — base de trabalho',F['title'])
r=3
for t,d in [
 ('O que este arquivo é',
  'O catálogo Hikma 2025 convertido em planilha, com minha recomendação binária por molécula e dois '
  'sinalizadores factuais: se a molécula aparece no portfólio/pipeline do Grupo EMS e se já passou por '
  'Novos Negócios. As colunas de análise de mercado estão em branco para você preencher.'),
 ('Uma aba só, agrupada por molécula',
  'A aba 2 tem uma linha por apresentação (321 no total), mas agrupada: tudo que é da MOLÉCULA — '
  'recomendação, justificativa, sinalizadores e as colunas em branco — está mesclado verticalmente ao longo '
  'das linhas daquela molécula. Você preenche o faturamento da vancomicina uma vez e vale para as 14 '
  'apresentações dela. O que varia por apresentação (NDC, concentração, embalagem, fechamento) fica em '
  'linha própria.'),
 ('Atenção ao ordenar e filtrar',
  'Células mescladas são o preço do agrupamento: o Excel recusa ORDENAR um intervalo que as contenha, e ao '
  'FILTRAR ele considera só a primeira linha de cada bloco. Para trabalhar com filtro, use o filtro do '
  'cabeçalho e leia o bloco inteiro. Se em algum momento preferir ordenar e filtrar livremente, me peça a '
  'versão sem mesclagem — aí o valor da molécula se repete em todas as linhas dela.'),
 ('As cinco faixas de coluna',
  'VERMELHA — minha recomendação e a justificativa (por molécula).\n'
  'AZUL — fatos do catálogo Hikma (por apresentação).\n'
  'VERDE — portfólio/pipeline EMS, da apresentação da Comissão de set/26 (por molécula).\n'
  'ROXA — histórico de Novos Negócios: sim/não e quando (por molécula).\n'
  'AMARELA — em branco, para você preencher (por molécula).'),
 ('Como cheguei ao SIM/NÃO',
  'Regra de negócio, não nota. Recomendo NÃO quando: a molécula não tem uso relevante no Brasil; é de canal '
  'Retail, fora do seu escopo; a casa já abordou quatro ou mais parceiros e quase todos estão dormentes; é '
  'substância da Portaria 344/98 sem preço que justifique a cota de importação; ou o preço unitário no '
  'hospital brasileiro é baixo demais para cobrir frete, imposto, estoque e registro de um acabado '
  'importado. Recomendo SIM quando o preço comporta a importação, ou quando é faixa intermediária com '
  'escassez, apresentação diferenciada ou projeto interno que o licenciamento pode antecipar. '
  'Resultado: 30 SIM e 106 NÃO.'),
 ('O que a recomendação NÃO é',
  'É triagem para você não gastar tempo com as 106, não veredito. A premissa mais frágil é o preço '
  'unitário, que estimei por conhecimento de mercado porque a base IQVIA não coube no anexo. Se o preço '
  'real de uma molécula for muito diferente do que presumi, a recomendação dela vira — por isso cada linha '
  'diz o motivo.'),
 ('Sobre o sinalizador de pipeline',
  'Presença e estágio (PORTFÓLIO, PIPELINE ou EM AVALIAÇÃO/GATE 0-3), com o texto do deck e o slide. '
  'Tratei estar em pipeline como direcional positivo — o Grupo já quis a molécula e licenciar pode '
  'antecipar a entrada — nunca como fator isolado.'),
 ('Sobre o sinalizador de histórico',
  'Só sim/não e quando (primeiro e último registro de entrada), para balizar suas buscas. O detalhe por '
  'parceiro e status está na aba 3. A coluna de contato prévio com a própria Hikma acende em uma molécula: '
  'vancomicina, com CDA vigente.'),
 ('Injetáveis',
  'As 164 fichas do corpo do catálogo (321 apresentações) são todas injetáveis. O índice de distribuidores '
  '(pág. 81) traz 3 NDCs sem ficha, um deles comprimido (mefloquina) — ficaram de fora.'),
 ('Como o PDF foi lido',
  'Extração por coordenada de cada palavra, não leitura de texto corrido, porque o arquivo tem conteúdo '
  'fora da área visível que duplicava a página seguinte. Os 321 NDCs foram reconciliados contra o índice '
  'de distribuidores (págs. 68-83), sem divergência.'),
 ('Fontes',
  'hikmainjectableproductcatalogjune2025.pdf · Apresentação Reunião Portfólio Setembro.pptx (slides 25 e 34) '
  '· data_7.xlsx, aba "data (8)" — 1.038 linhas, 1.029 registros após reparo de 9 quebrados por quebra de linha.'),
]:
    ws.write(r,1,t,F['h2']); r+=1
    ws.write(r,1,d,F['sub']); ws.set_row(r,13.5*(1+d.count('\n')+len(d)//116)); r+=2

# ================= 2. BASE DE TRABALHO =================
MOL=['Molécula (PT/DCB)','Molécula (EN)','Agrupamento terapêutico','RECOMENDAÇÃO','Justificativa','Nº apres.']
SKU=['Produto (catálogo Hikma)','NDC','Concentração','Conteúdo total','Volume de enchimento',
     'Tamanho da unidade','Embalagem','Fechamento','Forma','Bolsa RTU','Seringa','Controle DEA',
     'Categoria terapêutica (Hikma)','Referência (Comparable To)','FDA Rating','Descrição do produto','Pág.']
EMSC=['Está em portfólio/pipeline EMS?','Estágio no Grupo EMS','Texto do deck','Slide']
NNC=['Já avaliada por NN?','Quando','Contato prévio com a Hikma']
INC=['Faturamento NR (R$ MM)','Unidades/ano','Preço por unidade (R$)','Nº de competidores',
     'Registro Anvisa','Situação patentária','Preço de transferência','Sua avaliação','Observações']
cols=MOL+SKU+EMSC+NNC+INC
W=[24,20,24,14,74,7,
   40,15,20,20,15,15,14,13,10,9,9,10,28,24,24,30,6,
   15,19,34,8,
   13,20,14,
   16,14,16,14,17,17,17,18,30]
ws=wb.add_worksheet('2. Base de trabalho'); ws.freeze_panes(2,1)
i0=0; i1=len(MOL); i2=i1+len(SKU); i3=i2+len(EMSC); i4=i3+len(NNC); i5=i4+len(INC)
ws.merge_range(0,i0,0,i1-1,'MOLÉCULA E MINHA RECOMENDAÇÃO  ·  agrupado',GRP_REC)
ws.merge_range(0,i1,0,i2-1,'APRESENTAÇÃO  ·  uma linha por NDC',GRP_CAT)
ws.merge_range(0,i2,0,i3-1,'SINAL · EMS  ·  agrupado',GRP_EMS)
ws.merge_range(0,i3,0,i4-1,'SINAL · NN  ·  agrupado',GRP_NN)
ws.merge_range(0,i4,0,i5-1,'PARA VOCÊ PREENCHER  ·  uma vez por molécula',GRP_IN)
ws.set_row(0,20); ws.set_row(1,44)
for i,h in enumerate(cols):
    f=F['hrec'] if i<i1 else (F['hcat'] if i<i2 else (F['hems'] if i<i3 else (F['hnn'] if i<i4 else F['hin'])))
    ws.write(1,i,h,f); ws.set_column(i,i,W[i])

def put(r1,r2,c,val,fmt):
    if r2>r1: ws.merge_range(r1,c,r2,c,val,fmt)
    else:     ws.write(r1,c,val,fmt)

row=2; nmerge=0
for mol in sorted(bymol, key=lambda m: PT[m]):
    skus=bymol[mol]; e=EV[mol]; n=len(skus); r1=row; r2=row+n-1
    # ---- bloco da molécula (mesclado) ----
    mvals=[(0,e['Molécula (PT/DCB)'],F['m']),(1,e['Molécula (EN)'],F['m']),
           (2,e['Agrupamento terapêutico'],F['m']),
           (3,e['RECOMENDAÇÃO'],F['msim'] if e['RECOMENDAÇÃO']=='SIM' else F['mnao']),
           (4,e['Justificativa'],F['m']),(5,n,F['mnum'])]
    for c,v,f in mvals: put(r1,r2,c,v,f)
    ems=[(i2,e['Está em portfólio/pipeline EMS?'],F['msim'] if e['Está em portfólio/pipeline EMS?']=='SIM' else F['mn']),
         (i2+1,e['Estágio no Grupo EMS'],F['mc']),(i2+2,e['Texto do deck'],F['m']),(i2+3,SLIDE.get(mol,'—'),F['mc'])]
    nn=[(i3,e['Já avaliada por NN?'],F['msim'] if e['Já avaliada por NN?']=='SIM' else F['mn']),
        (i3+1,e['Quando'],F['mc']),
        (i3+2,e['Contato prévio com a Hikma'],F['msim'] if e['Contato prévio com a Hikma']=='SIM' else F['mn'])]
    for c,v,f in ems+nn: put(r1,r2,c,v,f)
    for c in range(i4,i5): put(r1,r2,c,None,F['inp'])
    if n>1: nmerge+=1
    # ---- linhas de apresentação ----
    for k,s in enumerate(skus):
        rr=r1+k
        powder='Pó' if 'powder' in (s['concentration']+s['fill_volume']).lower() else 'Solução'
        bag='SIM' if re.search(r'\bbags?\b',s['pack_quantity'],re.I) or re.search(r'\bin\s+[\d.]+%|Dextrose|NaCl|Sodium Chloride',s['product_name'],re.I) else '—'
        syr='SIM' if re.search(r'\bsyringes?\b',s['pack_quantity']+' '+s['unit_size']+' '+s['product_name'],re.I) else '—'
        vals=[s['product_name'],s['ndc'],s['concentration'],s['total_drug_content'],s['fill_volume'],
              s['unit_size'],s['pack_quantity'],s['closure'],powder,bag,syr,schedule(s['product_name']),
              s['therapeutic_category'],s['comparable_to'],s['fda_rating'],s['product_description'],s['page']]
        for j,v in enumerate(vals):
            c=i1+j; f=F['t']
            if j in (8,11): f=F['tc']
            elif j in (9,10): f=F['ok'] if v=='SIM' else F['tc']
            elif j==16: f=F['num']
            ws.write(rr,c,v,f)
    # ---- altura: a justificativa mesclada precisa caber no bloco ----
    need=-(-len(e['Justificativa'])//72)*12.6
    ws.set_row(r1,None) if False else None
    h=max(15.0, need/n)
    for rr in range(r1,r2+1): ws.set_row(rr,min(h,300))
    row=r2+1
ws.autofilter(1,0,row-1,len(cols)-1)
total_rows=row-2

# ================= 3. HISTÓRICO NN =================
C5=['Molécula Hikma (PT)','Tipo de match','Molécula no histórico','Fornecedor / Parceiro','Status','Situação',
 'Responsável','Categoria','Área Terapêutica','Data de Entrada','Início Prospecção','Concl. Prospecção',
 'Início CDA','Concl. CDA','Início Negociações','Concl. Negociações']
ws=wb.add_worksheet('3. Histórico NN (detalhe)'); ws.freeze_panes(1,1); ws.set_row(0,34)
for i,(h,w) in enumerate(zip(C5,[26,20,34,32,20,18,20,22,24,14,14,14,14,14,14,14])):
    ws.write(0,i,h,F['hnn']); ws.set_column(i,i,w)
ri=0
for m in sorted(matches,key=lambda x:(x['mol_pt'],x['kind']!='EXATO')):
    ri+=1; h=m['rec']; st=str(h['Status']).strip()
    vals=[m['mol_pt'],m['kind'],str(h['Molécula']),str(h['Fornecedor / Parceiro']),st,
      'PASSIVO (dormente)' if st=='PASSIVO' else 'ATIVO',str(h['Responsável']),str(h['Categoria']),
      str(h['Área Terapêutica']),str(h['Data de Entrada'])[:10],str(h['Data Início Prospecção'])[:10],
      str(h['Data Conclusão Prospecção'])[:10],str(h['Data Inicio Processo de CDA'])[:10],
      str(h['Data de Concl. CDA'])[:10],str(h['DATA - Inicio Negociações com parceiro'])[:10],
      str(h['DATA - Conclusão Negociações com parceiro'])[:10]]
    for c,v in enumerate(vals): ws.write(ri,c,v,F['tc'] if c in (1,5) else F['t'])
ws.autofilter(0,0,ri,len(C5)-1)
nhist=ri

# ================= 4. PORTFÓLIO / PIPELINE EMS =================
C6=['Bloco','Estágio no Grupo EMS','Molécula / Item','Forma','Está no catálogo Hikma?','Slide']
rows6=[]
for m,t in kb.EMS_PORTFOLIO_INJ.items():
    rows6.append(['Antibióticos J01 — Non Retail','PORTFÓLIO',t.replace(' Solução injetável',''),'Solução injetável','SIM','25'])
for t in kb.EMS_PORTFOLIO_INJ_OUTROS:
    rows6.append(['Antibióticos J01 — Non Retail','PORTFÓLIO',t,'Solução injetável','NÃO','25'])
for t in kb.EMS_ATB_GATE_OUTROS:
    rows6.append(['Antibióticos J01 — Non Retail','PIPELINE / GATE (0-3)',t,'Injetável','NÃO','25'])
for m,t in kb.EMS_ANEST_PORTFOLIO.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','PORTFÓLIO',t,'Injetável','SIM','34'])
for m,t in kb.EMS_ANEST_PIPELINE.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','PIPELINE',t,'Injetável','SIM','34'])
for m,t in kb.EMS_ANEST_GATE.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','EM AVALIAÇÃO (GATE 0-3)',t,'Injetável','SIM','34'])
for t in kb.EMS_ANEST_GATE_OUTROS:
    rows6.append(['Anestésicos injetáveis (ATC N)','EM AVALIAÇÃO (GATE 0-3)',t,'Injetável','NÃO','34'])
for t in ['Ciprofol','Adamgammadex','Suzetrigina']:
    rows6.append(['Anestésicos injetáveis (ATC N)','PROSPECÇÃO NOVOS NEGÓCIOS',t,'Injetável','NÃO','34'])
for m,t in kb.EMS_NOGO.items():
    rows6.append(['Antibióticos — decisões do comitê','NO GO ('+t.replace('NO GO: ','')+')',m,'Injetável/Oral','NÃO','21'])
ws=wb.add_worksheet('4. Portfólio-Pipeline EMS'); ws.freeze_panes(1,0); ws.set_row(0,34)
for i,(h,w) in enumerate(zip(C6,[34,40,44,20,22,10])): ws.write(0,i,h,F['hems']); ws.set_column(i,i,w)
for ri2,rw in enumerate(rows6,1):
    for c,v in enumerate(rw):
        f=F['t']
        if c==4: f=F['ok'] if v=='SIM' else F['tc']
        elif c==5: f=F['num']
        ws.write(ri2,c,v,f)
ws.autofilter(0,0,len(rows6),len(C6)-1)

wb.close()
print('OK ->',OUT)
print('abas: 4 | linhas na base:',total_rows,'| moléculas:',len(bymol),
      '| blocos mesclados:',nmerge,'| histórico:',nhist,'| EMS:',len(rows6))
