# -*- coding: utf-8 -*-
import json, sys, re, unicodedata
import xlsxwriter
from collections import defaultdict, Counter
sys.path.insert(0,'/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad')
from molmap import canon, PT
import kb
SP='/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad/'
OUT='/home/user/Teste/Hikma_Injetaveis_Avaliacao_NN.xlsx'

prods=json.load(open(SP+'products.json'))
ev=json.load(open(SP+'evaluation.json'))
hist=json.load(open(SP+'hist.json'))

wb=xlsxwriter.Workbook(OUT, {'nan_inf_to_errors':True})
# ---------- formatos ----------
F={}
F['title']  = wb.add_format({'bold':True,'font_size':17,'font_color':'#0B3D5C'})
F['sub']    = wb.add_format({'font_size':10,'font_color':'#5A6B78','text_wrap':True,'valign':'top'})
F['h']      = wb.add_format({'bold':True,'font_color':'white','bg_color':'#0B3D5C','border':1,
                             'border_color':'#0B3D5C','text_wrap':True,'valign':'vcenter','align':'center'})
F['h2']     = wb.add_format({'bold':True,'font_size':12,'font_color':'#0B3D5C','bottom':2,'border_color':'#0B3D5C'})
F['t']      = wb.add_format({'text_wrap':True,'valign':'top','border':1,'border_color':'#D8DEE4','font_size':9})
F['tc']     = wb.add_format({'text_wrap':True,'valign':'top','align':'center','border':1,'border_color':'#D8DEE4','font_size':9})
F['num']    = wb.add_format({'valign':'top','align':'center','border':1,'border_color':'#D8DEE4','font_size':9})
F['sim']    = wb.add_format({'bold':True,'font_color':'#0E6B3D','bg_color':'#DFF3E6','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['nao']    = wb.add_format({'bold':True,'font_color':'#8A1C1C','bg_color':'#FBE4E4','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['pa']     = wb.add_format({'bold':True,'font_color':'#7A4B00','bg_color':'#FFF0CC','align':'center','valign':'vcenter','border':1,'border_color':'#D8DEE4','font_size':9})
F['bold']   = wb.add_format({'bold':True,'valign':'top','text_wrap':True})
F['wrap']   = wb.add_format({'text_wrap':True,'valign':'top'})
F['kpi']    = wb.add_format({'bold':True,'font_size':22,'font_color':'#0B3D5C','align':'center','valign':'vcenter','bg_color':'#EEF4F8','border':1,'border_color':'#C9D6E0'})
F['kpil']   = wb.add_format({'font_size':9,'font_color':'#5A6B78','align':'center','valign':'vcenter','bg_color':'#EEF4F8','border':1,'border_color':'#C9D6E0','text_wrap':True})
F['note']   = wb.add_format({'italic':True,'font_size':9,'font_color':'#8A1C1C','text_wrap':True,'valign':'top'})

def sheet(name, headers, rows, widths, freeze=(1,0), fmts=None):
    ws=wb.add_worksheet(name)
    ws.freeze_panes(*freeze)
    ws.set_row(0, 34)
    for i,hd in enumerate(headers):
        ws.write(0,i,hd,F['h']); ws.set_column(i,i,widths[i])
    for r,row in enumerate(rows,1):
        for c,v in enumerate(row):
            f=(fmts or {}).get(c)
            if callable(f): f=f(v)
            ws.write(r,c,v,f or F['t'])
    ws.autofilter(0,0,len(rows),len(headers)-1)
    return ws

# ================= 1. LEIA-ME =================
ws=wb.add_worksheet('1. Leia-me e Metodologia')
ws.set_column('A:A',3); ws.set_column('B:B',120)
ws.write('B2','Catálogo Hikma de Injetáveis 2025 — Avaliação para Novos Negócios / Licenciamento (EMS Non Retail)',F['title'])
r=3
blocos=[
 ('O que é este arquivo',
  'Conversão integral do PDF "Hikma 2025 Injectable Product Catalog" (84 páginas) para planilha, com as '
  'características de cada produto separadas em colunas, cruzada com (a) o portfólio/pipeline do Grupo EMS '
  'extraído da apresentação da Comissão de Estratégia de set/26 e (b) a base histórica de carregamento de '
  'Novos Negócios (1.038 linhas). Fecha com uma recomendação binária SIM/NÃO por molécula.'),
 ('Resposta à dúvida sobre injetáveis',
  'CONFIRMADO: as 164 fichas de produto do corpo do catálogo (321 apresentações/NDCs) são 100% injetáveis — '
  'nenhuma tem forma oral. Portanto a lista inteira está dentro do foco pedido pela sua gestão. '
  'Única exceção fora do corpo do catálogo: o índice de distribuidores (pág. 81) lista "Mefloquine '
  'Hydrochloride Tablets" (comprimido) e mais 2 NDCs sem ficha no catálogo — irrelevantes para a avaliação.'),
 ('Como o catálogo foi lido',
  'Extração posicional (coordenadas x/y de cada palavra) e não leitura de texto corrido, porque o PDF tem '
  'páginas com conteúdo "fantasma" fora da área visível que duplicava a página seguinte. Cada NDC extraído foi '
  'reconciliado contra o índice independente de distribuidores (Wholesaler OENs, págs. 68-83): 321/321 NDCs '
  'conferem, sem duplicidade e com contagem de fichas idêntica (164).'),
 ('Modelo de avaliação (score 0-100)',
  'A — Atratividade/necessidade no Brasil (0-30): tese clínica e de mercado da molécula no ambiente hospitalar.\n'
  'B — Diferenciação da apresentação Hikma (0-25): bolsa pronta para uso/premix, seringa preenchida, amplitude '
  'de apresentações e condição de RLD (medicamento de referência no FDA).\n'
  'C — Espaço no portfólio EMS (0-25): 25 se a molécula está livre; penalizada se já está no portfólio, '
  'pipeline ou em gate do Grupo.\n'
  'D — Viabilidade de licenciamento (0-20): desconta substância sob Portaria 344/98, commodity em guerra de '
  'preço e molécula já em negociação avançada com outro parceiro.'),
 ('Regra da recomendação binária',
  'SIM apenas quando score ≥ 55 E nenhuma regra de bloqueio é acionada. Bloqueios: (1) molécula já no portfólio '
  'EMS Non Retail na mesma forma; (2) já endereçada em pipeline/gate do Grupo; (3) commodity injetável sem '
  'diferencial de apresentação; (4) controlado da Portaria 344/98 sem tese específica. '
  'A exceção desenhada de propósito: quando a Hikma traz apresentação diferenciada (bolsa RTU, seringa) de uma '
  'molécula que o EMS já tem, o bloqueio não se aplica — é justamente o caso Vancomicina.'),
 ('Alinhamento com o método do próprio time',
  'Os critérios espelham a lâmina "WarMap | Premissas" do deck: corte de moléculas com mercado > R$ 10 MM e '
  'USD 10 MM; oportunidades inovadoras com valoração > R$ 10 MM; preferência por empresas não multinacionais '
  '(a Hikma É multinacional — pela regra do time isso é "caso a discutir", não impedimento).'),
 ('ATENÇÃO — o que este arquivo NÃO tem',
  'Não há dados de mercado brasileiro (Close-Up/NRC/MIDAS), preço, volume, status de registro na Anvisa nem '
  'condição patentária, porque nada disso está nos três arquivos enviados. A coluna "Relevância Brasil" é '
  'HIPÓTESE FUNDAMENTADA, não medição. Antes de levar ao gate, preencha as colunas da aba 7.'),
]
for t,d in blocos:
    ws.write(r,1,t,F['h2']); r+=1
    ws.write(r,1,d,F['note'] if t.startswith('ATENÇÃO') else F['sub'])
    ws.set_row(r, 14*(1+d.count('\n')+len(d)//115))
    r+=2
ws.write(r,1,'Fontes: hikmainjectableproductcatalogjune2025.pdf · Apresentação Reunião Portfólio Setembro.pptx · data_7.xlsx (aba "data (8)", 1.038 linhas → 1.029 registros lógicos após reparo de 9 registros quebrados por quebra de linha).',F['sub'])

# ================= 2. RESUMO EXECUTIVO =================
ws=wb.add_worksheet('2. Resumo Executivo')
ws.set_column('A:A',3); ws.set_column('B:B',26); ws.set_column('C:H',15); ws.set_column('I:I',60)
ws.write('B2','Resumo Executivo',F['title'])
sim=[e for e in ev if e['RECOMENDAÇÃO']=='SIM']
kpis=[('164','fichas de produto no catálogo'),('321','apresentações (NDCs)'),('136','moléculas distintas'),
      ('100%','injetáveis'),(str(len(sim)),'moléculas recomendadas (SIM)'),
      (str(sum(1 for e in ev if e['Prioridade'].startswith('A'))),'prioridade A'),
      (str(sum(1 for e in ev if e['Já prospectada pela equipe NN']=='SIM')),'com histórico na base NN'),
      ('1','já em CDA com a Hikma')]
c=1
for v,l in kpis:
    ws.merge_range(3,c,4,c,v,F['kpi']); ws.merge_range(5,c,6,c,l,F['kpil']); c+=1
ws.set_row(3,20); ws.set_row(4,16)

r=8
ws.write(r,1,'Leitura de 30 segundos',F['h2']); r+=1
resumo=[
 'A lista é 100% injetável hospitalar — está dentro do foco que sua gestão pediu.',
 'Das 136 moléculas, 24 passam no filtro (SIM). As outras 112 caem por três motivos previsíveis: o EMS já tem '
 'a molécula, o Grupo já a endereça em pipeline/gate, ou é commodity injetável sem diferencial de apresentação.',
 'A relação com a Hikma JÁ ESTÁ ABERTA: a base mostra "Vancomicina Injetável / Hikma Pharmaceuticals / CDA / '
 'Livia Silva / 15-06-2026". Não é uma prospecção fria — é ampliação de escopo de um CDA vigente.',
 'O ativo mais valioso do catálogo não é uma molécula nova, é a PLATAFORMA DE APRESENTAÇÃO: bolsas prontas para '
 'uso (premix) e seringas preenchidas. O board de Anestesia do próprio deck pede literalmente '
 '"soluções de fácil preparo", "apresentações intravenosas" e "seringas pré-preenchidas".',
 'Combogesic® IV (paracetamol+ibuprofeno) é citado NOMINALMENTE no deck como oportunidade opioid-sparing '
 '("Comborex IV") — e a Hikma é a detentora do RLD. A base mostra que o time já olhou isso em 2018 via AFT '
 'Pharma e deixou PASSIVO. É a oportunidade mais bem endossada do arquivo.',
 'Dantroleno, Icatibanto, Regadenoson e Colistimetato não têm NENHUM registro na base histórica: são espaço '
 'branco real, não retrabalho. Polimixina B tem um único registro, dormente desde 2020 (Xellia, PASSIVO).',
 'O cruzamento pegou 4 moléculas que estavam escritas errado na base e passariam batido numa busca simples: '
 'POLIMIXIN B, REMIFENTANILA, FOSAPREPTANTO e NOREPINEFRINA. Elas estão marcadas como "variante de grafia" '
 'na aba 3 — vale corrigir na base de origem.',
 'Ressalva metodológica: a Hikma é multinacional. Pela lâmina "WarMap | Premissas", Novos Negócios prioriza '
 'empresas não multinacionais e trata multinacional como "caso a discutir" — alinhe isso antes do gate.',
]
for t in resumo:
    ws.write(r,1,'•',F['bold']); ws.merge_range(r,2,r,8,t,F['wrap']); ws.set_row(r,13*(1+len(t)//95)); r+=1

r+=1
ws.write(r,1,'Recomendadas (SIM) por prioridade',F['h2']); r+=1
hdr=['Prioridade','Molécula (PT)','Área','Score','Status EMS','Histórico NN','Por que']
for i,h in enumerate(hdr): ws.write(r,1+i,h,F['h'])
ws.set_column('B:B',26); ws.set_column('C:C',30); ws.set_column('D:D',26); ws.set_column('E:E',8)
ws.set_column('F:F',22); ws.set_column('G:G',20); ws.set_column('H:H',80)
r+=1
for e in sorted(sim,key=lambda x:(-x['SCORE TOTAL (0-100)'])):
    pf = F['sim'] if e['Prioridade'].startswith('A') else (F['pa'] if e['Prioridade'].startswith('B') else F['tc'])
    ws.write(r,1,e['Prioridade'],pf)
    ws.write(r,2,e['Molécula (PT/DCB)'],F['t'])
    ws.write(r,3,e['Área terapêutica'],F['t'])
    ws.write(r,4,e['SCORE TOTAL (0-100)'],F['num'])
    ws.write(r,5,e['Status no Grupo EMS'],F['t'])
    ws.write(r,6,('SIM ('+e['Situação do histórico']+')') if e['Já prospectada pela equipe NN']=='SIM' else 'NÃO',F['t'])
    ws.write(r,7,e['Justificativa'],F['t'])
    ws.set_row(r,13*(1+len(e['Justificativa'])//105)); r+=1

# ================= 3. AVALIAÇÃO POR MOLÉCULA =================
cols=['Molécula (PT/DCB)','Molécula (EN)','Área terapêutica','RECOMENDAÇÃO','Prioridade','SCORE TOTAL (0-100)',
 'Score A - Atratividade BR (0-30)','Score B - Diferenciação (0-25)','Score C - Espaço no portfólio (0-25)',
 'Score D - Viabilidade (0-20)','Relevância Brasil (hipótese)','Status no Grupo EMS','Detalhe EMS',
 'Já prospectada pela equipe NN','Tipo de match no histórico','Situação do histórico',
 'Prospectada por VOCÊ (Lucas Medina)','Contato prévio com a Hikma','Nº registros no histórico',
 'Parceiros já contatados','Responsáveis NN','Status no histórico','Datas de entrada',
 'Forma farmacêutica','Nº de apresentações (SKUs)','Injetável','Controlado (Port. 344/98)',
 'Commodity/genérico maduro','Referência (comparable to)','FDA rating','Categoria terapêutica (Hikma)',
 'Descrição do produto','Concentrações','Conteúdo total','Embalagem','Produtos no catálogo','NDCs',
 'Páginas no PDF','Justificativa']
W=[26,24,26,14,15,9, 10,10,10,10, 16,22,34, 14,16,18, 14,14,10, 46,24,26,22, 26,10,9,12,12, 30,26,30,34,30,30,26,44,40,12,95]
rows=[[e.get(c,'') for c in cols] for e in sorted(ev,key=lambda x:(x['RECOMENDAÇÃO']!='SIM',-x['SCORE TOTAL (0-100)'],x['Molécula (PT/DCB)']))]
fmts={3:lambda v: F['sim'] if v=='SIM' else F['nao'],
      4:lambda v: F['sim'] if str(v).startswith('A') else (F['pa'] if str(v).startswith('B') else F['tc']),
      5:F['num'],6:F['num'],7:F['num'],8:F['num'],9:F['num'],18:F['num'],24:F['num'],
      13:lambda v: F['pa'] if v=='SIM' else F['tc'], 17:lambda v: F['sim'] if v=='SIM' else F['tc'],
      25:F['tc'],26:F['tc'],27:F['tc']}
sheet('3. Avaliação por Molécula',cols,rows,W,freeze=(1,1),fmts=fmts)

# ================= 4. CATÁLOGO COMPLETO (SKU) =================
cols4=['Página PDF','Produto (catálogo Hikma)','Molécula (EN)','Molécula (PT/DCB)','Área terapêutica',
 'Categoria terapêutica (Hikma)','Referência (Comparable To)','Descrição do produto','FDA Rating','NDC',
 'Concentração','Conteúdo total de fármaco','Volume de enchimento','Tamanho da unidade','Embalagem',
 'Fechamento (closure)','Forma','Bolsa pronta p/ uso','Controlado 344/98','Recomendação da molécula']
recmap={e['Molécula (EN)']:e for e in ev}
rows4=[]
for p in sorted(prods,key=lambda x:(x['page'],x['product_name'],x['ndc'])):
    m=canon(p['product_name']); e=recmap[m]
    powder='Pó' if 'powder' in (p['concentration']+p['fill_volume']).lower() else 'Solução'
    bag='SIM' if re.search(r'bag',p['pack_quantity'],re.I) or re.search(r'\bin\s+[\d.]+%|Dextrose|NaCl|Sodium Chloride',p['product_name'],re.I) else 'NÃO'
    rows4.append([p['page'],p['product_name'],m,PT[m],e['Área terapêutica'],p['therapeutic_category'],
      p['comparable_to'],p['product_description'],p['fda_rating'],p['ndc'],p['concentration'],
      p['total_drug_content'],p['fill_volume'],p['unit_size'],p['pack_quantity'],p['closure'],powder,bag,
      e['Controlado (Port. 344/98)'],e['RECOMENDAÇÃO']])
W4=[9,46,22,24,26,30,24,34,26,15,20,22,16,16,14,14,10,11,11,14]
sheet('4. Catálogo Completo (SKU)',cols4,rows4,W4,freeze=(1,2),
      fmts={0:F['num'],16:F['tc'],17:lambda v:F['sim'] if v=='SIM' else F['tc'],
            18:lambda v:F['pa'] if v=='SIM' else F['tc'],
            19:lambda v:F['sim'] if v=='SIM' else F['nao']})

# ================= 5. CRUZAMENTO COM HISTÓRICO =================
cols5=['Molécula Hikma (PT)','Tipo de match','Molécula no histórico','Fornecedor / Parceiro','Status',
 'Situação','Responsável','Categoria','Área Terapêutica','Coligada','Data de Entrada','Data Início Prospecção',
 'Data Conclusão Prospecção','Data Início CDA','Data Concl. CDA','Início Negociações','Concl. Negociações']
matches=json.load(open(SP+'hist_matches.json'))
rows5=[]
for m in sorted(matches, key=lambda x:(x['mol_pt'], x['kind']!='EXATO')):
    h=m['rec']; st=str(h['Status']).strip()
    rows5.append([m['mol_pt'],m['kind'],str(h['Molécula']),str(h['Fornecedor / Parceiro']),st,
      'PASSIVO (dormente)' if st=='PASSIVO' else 'ATIVO',str(h['Responsável']),str(h['Categoria']),
      str(h['Área Terapêutica']),str(h['Coligada']),str(h['Data de Entrada'])[:10],
      str(h['Data Início Prospecção'])[:10],str(h['Data Conclusão Prospecção'])[:10],
      str(h['Data Inicio Processo de CDA'])[:10],str(h['Data de Concl. CDA'])[:10],
      str(h['DATA - Inicio Negociações com parceiro'])[:10],str(h['DATA - Conclusão Negociações com parceiro'])[:10]])
W5=[26,20,34,32,20,18,20,22,24,14,14,14,14,14,14,14,14]
sheet('5. Cruzamento Histórico NN',cols5,rows5,W5,freeze=(1,1),
      fmts={1:lambda v:F['sim'] if v=='EXATO' else F['tc'],5:lambda v:F['tc'] if v=='ATIVO' else F['pa']})

# ================= 6. PORTFÓLIO / PIPELINE EMS =================
cols6=['Bloco','Situação no Grupo EMS','Molécula / Item','Forma','Presente no catálogo Hikma?','Observação']
rows6=[]
for m,t in kb.EMS_PORTFOLIO_INJ.items():
    rows6.append(['Antibióticos J01 — Non Retail','PORTFÓLIO',t.replace(' Solução injetável',''),'Solução injetável','SIM','Duplicidade, salvo apresentação diferenciada (bolsa/seringa).'])
for t in kb.EMS_PORTFOLIO_INJ_OUTROS:
    rows6.append(['Antibióticos J01 — Non Retail','PORTFÓLIO',t,'Solução injetável','NÃO','Do portfólio EMS, sem correspondente no catálogo Hikma.'])
for t in kb.EMS_ATB_GATE_OUTROS:
    rows6.append(['Antibióticos J01 — Non Retail','PIPELINE / GATE (0-3)',t,'Injetável','NÃO','Endereçado internamente; catálogo Hikma não cobre.'])
for m,t in kb.EMS_ANEST_PORTFOLIO.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','PORTFÓLIO',t,'Injetável','SIM','Duplicidade.'])
for m,t in kb.EMS_ANEST_PIPELINE.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','PIPELINE',t,'Injetável','SIM','Endereçado internamente.'])
for m,t in kb.EMS_ANEST_GATE.items():
    rows6.append(['Anestésicos injetáveis (ATC N)','EM AVALIAÇÃO (GATE 0-3)',t,'Injetável','SIM','Em gate; evitar duplicidade.'])
for t in kb.EMS_ANEST_GATE_OUTROS:
    rows6.append(['Anestésicos injetáveis (ATC N)','EM AVALIAÇÃO (GATE 0-3)',t,'Injetável','NÃO',''])
for t in ['Ciprofol','Adamgammadex','Suzetrigina']:
    rows6.append(['Anestésicos injetáveis (ATC N)','PROSPECÇÃO NOVOS NEGÓCIOS',t,'Injetável','NÃO','Já em prospecção pelo NN (deck set/26).'])
for m,t in kb.EMS_NOGO.items():
    rows6.append(['Antibióticos — decisões do comitê','NO GO',m,'Injetável/Oral','NÃO',t])
sheet('6. Portfólio-Pipeline EMS',cols6,rows6,[34,28,44,20,24,64],
      fmts={4:lambda v:F['pa'] if v=='SIM' else F['tc']})

# ================= 7. LACUNAS E PERGUNTAS =================
ws=wb.add_worksheet('7. Lacunas e Perguntas')
ws.set_column('A:A',3); ws.set_column('B:B',34); ws.set_column('C:C',95); ws.set_column('D:D',22)
ws.write('B2','O que falta para fechar a decisão',F['title'])
ws.write('B3','Nenhum dos três arquivos enviados traz estas informações. Sem elas, a coluna RECOMENDAÇÃO é uma triagem — boa para priorizar, insuficiente para o gate.',F['sub'])
hd=['Lacuna','Por que trava a decisão / o que pedir','Onde buscar']
for i,h in enumerate(hd): ws.write(4,1+i,h,F['h'])
gaps=[
 ('Mercado brasileiro por molécula','O corte do próprio time é "mercado > R$ 10 MM e USD 10 MM". Sem valor de mercado por molécula não dá para aplicar o corte — hoje as 24 recomendadas estão ordenadas por tese, não por faturamento.','Close-Up/NRC e MIDAS (o deck já usa)'),
 ('Status de registro na Anvisa','Define se é cópia (via abreviada), registro novo ou molécula sem registro no país — muda prazo e custo do projeto.','Consulta Anvisa / time de Portfólio'),
 ('Situação patentária','Define ano possível de lançamento. O deck faz isso para os antibióticos novos; o catálogo Hikma não traz nada.','Cortellis (CPI/DDI) / Marcas e Patentes'),
 ('Preço de transferência da Hikma','Sem CIF/FOB não há margem nem comparação com o genérico local ou indiano. É o dado que mais mexe no ranking.','Pedir price list à Hikma sob o CDA vigente'),
 ('Escopo territorial e exclusividade','A Hikma é multinacional e pode ter compromissos na LatAm. Precisa saber se o Brasil está livre e se há exclusividade.','Hikma — mesma conversa do CDA'),
 ('Capacidade e site de fabricação','Injetável estéril exige inspeção; certificado de BPF do site é pré-requisito de registro.','Hikma / Assuntos Regulatórios'),
 ('Interesse médico e da BU','A lâmina WarMap exige avaliação médica e interesse comercial antes do gate. Vários "NO GO" do comitê foram por desinteresse médico, não por mercado.','Board Médico-Científico e BU Non Retail'),
 ('Posição sobre parceiro multinacional','"Empresas não multinacionais / *Discutir casos de multinacionais". A Hikma é multinacional — precisa de aval antes de investir tempo.','Diretoria de Novos Negócios'),
 ('Estabilidade e cadeia fria','Bolsas RTU e premix têm exigência de transporte/armazenagem que pode inviabilizar o custo logístico no Brasil.','Hikma (dossiê) / Logística'),
 ('Base histórica só com datas','A base tem status e datas, mas não tem motivo de perda nem preço proposto. Sem isso não dá para saber por que Daptomicina/Micafungina ficaram PASSIVO.','Enriquecer o próprio controle de NN'),
]
r=5
for a,b,c in gaps:
    ws.write(r,1,a,F['t']); ws.write(r,2,b,F['t']); ws.write(r,3,c,F['t'])
    ws.set_row(r,13*(1+len(b)//95)); r+=1
r+=1
ws.write(r,1,'Perguntas que eu preciso que você responda',F['h2']); r+=1
qs=[
 'Seu escopo é só Non Retail hospitalar? Liraglutida e Testosterona, por exemplo, são Retail — devo descartá-las de saída?',
 'Oncologia entra? Você tem 55 registros de oncologia na base, mas o deck de set/26 não trouxe oncologia — quero saber se mantenho ou tiro do escopo.',
 'O CDA com a Hikma (Vancomicina, Livia Silva) é seu para ampliar ou é dela? Isso muda quem conduz e a velocidade.',
 'Existe teto de preço ou margem mínima para produto acabado importado? Sem isso não consigo separar "bom produto" de "bom negócio".',
 'Controlados da Portaria 344/98 (fentanil, morfina, midazolam, cetamina) estão fora por política, ou avaliamos caso a caso?',
 'A gestão quer volume (muitos SKUs para encorpar a linha hospitalar) ou valor (poucos produtos diferenciados)? A resposta reordena a lista.',
]
for q in qs:
    ws.write(r,1,'?',F['bold']); ws.merge_range(r,2,r,3,q,F['wrap']); ws.set_row(r,13*(1+len(q)//110)); r+=1

# ================= 8. MELHORIAS =================
ws=wb.add_worksheet('8. Melhorias sugeridas')
ws.set_column('A:A',3); ws.set_column('B:B',34); ws.set_column('C:C',100)
ws.write('B2','Melhorias para a próxima versão desta planilha',F['title'])
for i,h in enumerate(['Melhoria','Como fazer e o que muda']): ws.write(4,1+i,h,F['h'])
mel=[
 ('Coluna de faturamento potencial','Plugar Close-Up/NRC por molécula e trocar o Score A (hoje qualitativo) por faixa de mercado real. Só assim o corte de R$ 10 MM do time roda automático.'),
 ('Semáforo de registro Anvisa','Três estados (registrado / cópia possível / sem registro) por molécula. Transforma a aba 3 em plano de projeto, não só triagem.'),
 ('Motivo de perda na base NN','Incluir campo obrigatório de motivo ao mover para PASSIVO. Hoje 290 das 1.029 linhas estão PASSIVO sem explicação — é o maior desperdício de inteligência da base.'),
 ('Deduplicar a base histórica','A base tem "Vancomicina Injetável" e "VANCOMICINA", "RUXOLITINIB" e "RUXOLITINIBE" como registros distintos. Um campo DCB padronizado eliminaria o retrabalho de cruzamento.'),
 ('Cadastro de parceiro','500 parceiros sem país, porte nem se é multinacional. Com isso a regra "empresas não multinacionais" do WarMap viraria filtro automático.'),
 ('Aba de apresentação, não de molécula','O diferencial da Hikma é a apresentação (bolsa RTU). Uma visão por forma farmacêutica revelaria oportunidades que a visão por molécula esconde.'),
 ('Reavaliação periódica dos PASSIVOS','Combogesic ficou parado desde 2018 e voltou a ser prioridade pelo board de 2026. Uma rotina de re-acesso anual dos PASSIVO recuperaria oportunidades como essa.'),
 ('Integrar as decisões do comitê','Trazer a coluna "STATUS GRUPO EMS" do deck (NO GO / GATE / PIPELINE) para dentro da base de NN, evitando prospectar o que o comitê já vetou.'),
]
r=5
for a,b in mel:
    ws.write(r,1,a,F['t']); ws.write(r,2,b,F['t']); ws.set_row(r,13*(1+len(b)//100)); r+=1

wb.close()
print('OK ->',OUT)
print('abas: 8 | moléculas:',len(ev),'| SKUs:',len(prods),'| linhas cruzamento:',len(rows5))
