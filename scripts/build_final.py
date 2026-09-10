# -*- coding: utf-8 -*-
"""Base factual: características do catálogo + 2 sinalizadores + colunas em branco."""
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

# fonte no deck
SLIDE={}
for m in kb.EMS_PORTFOLIO_INJ: SLIDE[m]='Slide 25 — Antibióticos J01, Non Retail'
for m in list(kb.EMS_ANEST_PORTFOLIO)+list(kb.EMS_ANEST_PIPELINE)+list(kb.EMS_ANEST_GATE):
    SLIDE[m]='Slide 34 — Anestésicos injetáveis (ATC N)'

bymol=defaultdict(list)
for p in prods: bymol[canon(p['product_name'])].append(p)

def schedule(names):
    s=set()
    for n in names:
        m=re.search(r'\bC-(I{1,3}V?|IV|V)\b', n)
        if m: s.add('C-'+m.group(1))
    return ', '.join(sorted(s)) if s else '—'

wb=xlsxwriter.Workbook(OUT,{'nan_inf_to_errors':True})
F={}
F['title']=wb.add_format({'bold':True,'font_size':17,'font_color':'#0B3D5C'})
F['sub']=wb.add_format({'font_size':10,'font_color':'#5A6B78','text_wrap':True,'valign':'top'})
F['h2']=wb.add_format({'bold':True,'font_size':12,'font_color':'#0B3D5C','bottom':2,'border_color':'#0B3D5C'})
def hdr(bg,fc='white',bc=None):
    return wb.add_format({'bold':True,'font_color':fc,'bg_color':bg,'border':1,
        'border_color':bc or bg,'text_wrap':True,'valign':'vcenter','align':'center','font_size':9})
F['hcat']=hdr('#0B3D5C')                       # fatos do catálogo
F['hems']=hdr('#1F6F54')                       # sinal pipeline
F['hnn'] =hdr('#5B3A8C')                       # sinal histórico
F['hin'] =hdr('#FFD24D','#3D2B00','#B98F00')   # em branco p/ preencher
F['hrec']=hdr('#8A1C1C')                       # minha recomendação
F['grp'] =wb.add_format({'bold':True,'font_color':'white','align':'center','valign':'vcenter','font_size':10,'border':1})
F['t']=wb.add_format({'text_wrap':True,'valign':'top','border':1,'border_color':'#D8DEE4','font_size':9})
F['tc']=wb.add_format({'text_wrap':True,'valign':'top','align':'center','border':1,'border_color':'#D8DEE4','font_size':9})
F['num']=wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#D8DEE4','font_size':9})
F['sim']=wb.add_format({'bold':True,'font_color':'#0E6B3D','bg_color':'#DFF3E6','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['nao']=wb.add_format({'align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9,'font_color':'#8A93A0'})
F['inp']=wb.add_format({'border':1,'border_color':'#B98F00','bg_color':'#FFF7DB','font_size':9})
F['nao2']=wb.add_format({'bold':True,'font_color':'#8A1C1C','bg_color':'#FBE4E4','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['bold']=wb.add_format({'bold':True,'valign':'top','text_wrap':True})
F['wrap']=wb.add_format({'text_wrap':True,'valign':'top'})

GRP_CAT=wb.add_format({'bold':True,'font_color':'white','bg_color':'#0B3D5C','align':'center','valign':'vcenter','border':1,'font_size':10})
GRP_EMS=wb.add_format({'bold':True,'font_color':'white','bg_color':'#1F6F54','align':'center','valign':'vcenter','border':1,'font_size':10})
GRP_NN =wb.add_format({'bold':True,'font_color':'white','bg_color':'#5B3A8C','align':'center','valign':'vcenter','border':1,'font_size':10})
GRP_REC=wb.add_format({'bold':True,'font_color':'white','bg_color':'#8A1C1C','align':'center','valign':'vcenter','border':1,'font_size':10})
GRP_IN =wb.add_format({'bold':True,'font_color':'#3D2B00','bg_color':'#FFD24D','align':'center','valign':'vcenter','border':1,'font_size':10})

# ================= 1. LEIA-ME =================
ws=wb.add_worksheet('1. Leia-me')
ws.set_column('A:A',3); ws.set_column('B:B',120)
ws.write('B2','Catálogo Hikma de Injetáveis 2025 — base de produtos com sinalizadores',F['title'])
r=3
for t,d in [
 ('O que este arquivo é',
  'O catálogo Hikma 2025 convertido em planilha, com as características de cada produto separadas em colunas, '
  'mais minha recomendação binária por molécula e dois sinalizadores factuais: se a molécula aparece no '
  'portfólio/pipeline do Grupo EMS e se já passou por Novos Negócios. As colunas de análise de mercado estão '
  'em branco para você preencher.'),
 ('As cinco faixas de coluna',
  'VERMELHA — minha recomendação e a justificativa dela.\n'
  'AZUL — fato do catálogo Hikma, extraído do PDF.\n'
  'VERDE — sinalizador de portfólio/pipeline, extraído da apresentação da Comissão de set/26.\n'
  'ROXA — sinalizador de histórico de Novos Negócios: sim/não e quando.\n'
  'AMARELA — em branco, para você preencher (faturamento, unidades, preço por unidade e o que mais precisar).'),
 ('Como cheguei ao SIM/NÃO',
  'Regra de negócio, não nota. Recomendo NÃO quando: a molécula não tem uso relevante no Brasil; é de canal '
  'Retail, fora do seu escopo; a casa já abordou quatro ou mais parceiros e quase todos estão dormentes; é '
  'substância da Portaria 344/98 sem preço que justifique a cota de importação; ou o preço unitário no '
  'hospital brasileiro é baixo demais para cobrir frete, imposto, estoque e registro de um acabado importado. '
  'Recomendo SIM quando o preço unitário comporta a importação, ou quando é faixa intermediária com escassez '
  'no mercado, apresentação diferenciada ou projeto interno em andamento que o licenciamento pode antecipar. '
  'A justificativa de cada linha diz qual desses caminhos foi acionado. Resultado: 30 SIM e 106 NÃO.'),
 ('O que a recomendação NÃO é',
  'É triagem para você não gastar tempo com as 106, não veredito. A premissa mais frágil é o preço unitário, '
  'que estimei por conhecimento de mercado porque a base IQVIA não coube no anexo. Se o preço real de uma '
  'molécula for muito diferente do que presumi, a recomendação dela vira. Por isso a justificativa sempre diz '
  'o motivo — para você discordar item a item com dado na mão.'),
 ('Sobre o sinalizador de pipeline',
  'Indica presença e estágio (PORTFÓLIO, PIPELINE ou EM AVALIAÇÃO/GATE 0-3), com o texto exato do deck e o '
  'slide de origem. Tratei estar em pipeline como direcional positivo — o Grupo já quis a molécula, e '
  'licenciar o acabado pode antecipar a entrada — mas nunca como fator isolado de decisão.'),
 ('Sobre o sinalizador de histórico',
  'Só sim/não e quando (primeiro e último registro de entrada), para servir de balizador das suas buscas. '
  'O detalhe por parceiro, status e responsável está na aba 4, se precisar. Guardei uma coluna à parte para '
  'contato prévio com a própria Hikma — é o caso da vancomicina, que tem CDA vigente.'),
 ('Injetáveis',
  'As 164 fichas do corpo do catálogo (321 apresentações) são todas injetáveis. O índice de distribuidores '
  '(pág. 81) traz 3 NDCs sem ficha, um deles comprimido (mefloquina) — ficaram de fora da base.'),
 ('Como o PDF foi lido',
  'Extração por coordenada de cada palavra, e não leitura de texto corrido, porque o arquivo tem conteúdo fora '
  'da área visível que duplicava a página seguinte. Os 321 NDCs foram reconciliados contra o índice '
  'independente de distribuidores (págs. 68-83), sem divergência.'),
 ('Fontes',
  'hikmainjectableproductcatalogjune2025.pdf · Apresentação Reunião Portfólio Setembro.pptx (slides 25 e 34) · '
  'data_7.xlsx, aba "data (8)" — 1.038 linhas, 1.029 registros após reparo de 9 quebrados por quebra de linha.'),
]:
    ws.write(r,1,t,F['h2']); r+=1
    ws.write(r,1,d,F['sub']); ws.set_row(r,13.5*(1+d.count('\n')+len(d)//116)); r+=2

# ================= 2. CONSOLIDADO POR MOLÉCULA =================
AVAL=['Molécula (PT/DCB)','Molécula (EN)','Agrupamento terapêutico','RECOMENDAÇÃO','Justificativa']
CAT=['Categoria terapêutica (Hikma)','Produtos no catálogo','Referência (Comparable To)','FDA Rating',
 'Forma farmacêutica','Apresentação diferenciada','Controle DEA no catálogo','Nº de apresentações (SKUs)',
 'Concentrações','Conteúdo total','Embalagens','NDCs','Páginas no PDF']
EMSC=['Está em portfólio/pipeline EMS?','Estágio no Grupo EMS','Texto do deck','Slide de origem']
NNC=['Já avaliada por NN?','Quando','Contato prévio com a Hikma']
INC=['Faturamento NR (R$ MM)','Unidades/ano','Preço por unidade (R$)','Nº de competidores',
 'Registro Anvisa','Situação patentária','Preço de transferência','Sua avaliação','Observações']
cols=AVAL+CAT+EMSC+NNC+INC
W=[26,22,26,14,96,
   30,46,26,26,30,24,14,11,30,30,26,44,12,
   16,20,40,26,
   14,22,15,
   16,14,16,14,18,18,18,18,34]
ws=wb.add_worksheet('2. Moléculas'); ws.freeze_panes(2,1)
a0=0; a1=len(AVAL); b=a1+len(CAT); c=b+len(EMSC); d=c+len(NNC); e_=d+len(INC)
ws.merge_range(0,a0,0,a1-1,'MOLÉCULA E MINHA RECOMENDAÇÃO',GRP_REC)
ws.merge_range(0,a1,0,b-1,'FATOS DO CATÁLOGO HIKMA',GRP_CAT)
ws.merge_range(0,b,0,c-1,'SINAL · PORTFÓLIO / PIPELINE EMS',GRP_EMS)
ws.merge_range(0,c,0,d-1,'SINAL · HISTÓRICO NOVOS NEGÓCIOS',GRP_NN)
ws.merge_range(0,d,0,e_-1,'PARA VOCÊ PREENCHER',GRP_IN)
ws.set_row(0,20); ws.set_row(1,42)
for i,h in enumerate(cols):
    f=F['hrec'] if i<a1 else (F['hcat'] if i<b else (F['hems'] if i<c else (F['hnn'] if i<d else F['hin'])))
    ws.write(1,i,h,f); ws.set_column(i,i,W[i])

rows=[]
for mol, skus in sorted(bymol.items(), key=lambda kv: PT[kv[0]]):
    e=EV[mol]; names=sorted(set(s['product_name'] for s in skus))
    rows.append([
     e['Molécula (PT/DCB)'], e['Molécula (EN)'], e['Agrupamento terapêutico'],
     e['RECOMENDAÇÃO'], e['Justificativa'],
     e['Categoria terapêutica (Hikma)'], e['Produtos no catálogo'], e['Referência (Comparable To)'],
     e['FDA Rating'], e['Forma farmacêutica'], e['Apresentação diferenciada'],
     schedule(names), e['Nº de apresentações (SKUs)'], e['Concentrações'], e['Conteúdo total'],
     e['Embalagens'], e['NDCs'], e['Páginas no PDF'],
     e['Está em portfólio/pipeline EMS?'], e['Estágio no Grupo EMS'], e['Texto do deck'], SLIDE.get(mol,'—'),
     e['Já avaliada por NN?'], e['Quando'], e['Contato prévio com a Hikma'],
    ])
for ri,row in enumerate(rows,2):
    for ci,v in enumerate(row):
        f=F['t']
        if cols[ci]=='RECOMENDAÇÃO': f=F['sim'] if v=='SIM' else F['nao2']
        elif cols[ci] in ('Nº de apresentações (SKUs)',): f=F['num']
        elif cols[ci] in ('Está em portfólio/pipeline EMS?','Já avaliada por NN?','Contato prévio com a Hikma'):
            f=F['sim'] if v=='SIM' else F['nao']
        elif cols[ci] in ('Controle DEA no catálogo','Apresentação diferenciada','Quando'): f=F['tc']
        ws.write(ri,ci,v,f)
    for ci in range(d,e_): ws.write_blank(ri,ci,None,F['inp'])
ws.autofilter(1,0,len(rows)+1,len(cols)-1)

# ================= 3. CATÁLOGO SKU =================
C4=['RECOMENDAÇÃO','Página PDF','Produto (catálogo Hikma)','Molécula (PT/DCB)','Molécula (EN)','Agrupamento terapêutico',
 'Categoria terapêutica (Hikma)','Referência (Comparable To)','Descrição do produto','FDA Rating','NDC',
 'Concentração','Conteúdo total de fármaco','Volume de enchimento','Tamanho da unidade','Embalagem',
 'Fechamento (closure)','Forma','Bolsa pronta p/ uso','Seringa preenchida','Controle DEA']
E4=['Está em portfólio/pipeline EMS?','Estágio no Grupo EMS']
N4=['Já avaliada por NN?','Quando']
I4=['Faturamento NR (R$ MM)','Unidades/ano','Preço por unidade (R$)','Observações']
c4=C4+E4+N4+I4
W4=[14,9,46,24,22,25,30,24,34,26,15,20,22,16,16,14,14,10,11,11,12, 16,20, 14,22, 16,14,16,30]
ws=wb.add_worksheet('3. Catálogo (SKU)'); ws.freeze_panes(2,2)
a=0;b=len(C4);c=b+len(E4);d=c+len(N4);e_=d+len(I4)
ws.write(0,0,'AVALIAÇÃO',GRP_REC)
ws.merge_range(0,1,0,b-1,'FATOS DO CATÁLOGO HIKMA',GRP_CAT)
ws.merge_range(0,b,0,c-1,'SINAL · EMS',GRP_EMS)
ws.merge_range(0,c,0,d-1,'SINAL · NN',GRP_NN)
ws.merge_range(0,d,0,e_-1,'PARA VOCÊ PREENCHER',GRP_IN)
ws.set_row(0,20); ws.set_row(1,42)
for i,h in enumerate(c4):
    f=F['hrec'] if i==0 else (F['hcat'] if i<b else (F['hems'] if i<c else (F['hnn'] if i<d else F['hin'])))
    ws.write(1,i,h,f); ws.set_column(i,i,W4[i])
ri=1
for p in sorted(prods,key=lambda x:(x['page'],x['product_name'],x['ndc'])):
    ri+=1; m=canon(p['product_name']); e=EV[m]
    powder='Pó' if 'powder' in (p['concentration']+p['fill_volume']).lower() else 'Solução'
    bag='SIM' if re.search(r'\bbags?\b',p['pack_quantity'],re.I) or re.search(r'\bin\s+[\d.]+%|Dextrose|NaCl|Sodium Chloride',p['product_name'],re.I) else 'NÃO'
    syr='SIM' if re.search(r'\bsyringes?\b',p['pack_quantity']+' '+p['unit_size']+' '+p['product_name'],re.I) else 'NÃO'
    vals=[e['RECOMENDAÇÃO'],p['page'],p['product_name'],PT[m],m,e['Agrupamento terapêutico'],p['therapeutic_category'],
     p['comparable_to'],p['product_description'],p['fda_rating'],p['ndc'],p['concentration'],
     p['total_drug_content'],p['fill_volume'],p['unit_size'],p['pack_quantity'],p['closure'],
     powder,bag,syr,schedule([p['product_name']]),
     e['Está em portfólio/pipeline EMS?'], e['Estágio no Grupo EMS'],
     e['Já avaliada por NN?'], e['Quando']]
    for ci,v in enumerate(vals):
        f=F['t']
        if ci==0: f=F['sim'] if v=='SIM' else F['nao2']
        elif ci==1: f=F['num']
        elif ci in (17,20,24): f=F['tc']
        elif ci in (18,19,21,23): f=F['sim'] if v=='SIM' else F['nao']
        ws.write(ri,ci,v,f)
    for ci in range(d,e_): ws.write_blank(ri,ci,None,F['inp'])
ws.autofilter(1,0,ri,len(c4)-1)

# ================= 4. HISTÓRICO NN =================
C5=['Molécula Hikma (PT)','Tipo de match','Molécula no histórico','Fornecedor / Parceiro','Status','Situação',
 'Responsável','Categoria','Área Terapêutica','Data de Entrada','Início Prospecção','Concl. Prospecção',
 'Início CDA','Concl. CDA','Início Negociações','Concl. Negociações']
ws=wb.add_worksheet('4. Histórico NN (detalhe)'); ws.freeze_panes(1,1); ws.set_row(0,34)
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
    for ci,v in enumerate(vals): ws.write(ri,ci,v,F['tc'] if ci in (1,5) else F['t'])
ws.autofilter(0,0,ri,len(C5)-1)

# ================= 5. PORTFÓLIO / PIPELINE EMS =================
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
ws=wb.add_worksheet('5. Portfólio-Pipeline EMS'); ws.freeze_panes(1,0); ws.set_row(0,34)
for i,(h,w) in enumerate(zip(C6,[34,40,44,20,22,10])): ws.write(0,i,h,F['hems']); ws.set_column(i,i,w)
for ri,row in enumerate(rows6,1):
    for ci,v in enumerate(row):
        f=F['t']
        if ci==4: f=F['sim'] if v=='SIM' else F['nao']
        elif ci==5: f=F['num']
        ws.write(ri,ci,v,f)
ws.autofilter(0,0,len(rows6),len(C6)-1)

wb.close()
print('OK ->',OUT)
print('abas: 5 | moléculas:',len(rows),'| SKUs:',len(prods),'| histórico:',len(matches),'| EMS:',len(rows6))
