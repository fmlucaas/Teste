# -*- coding: utf-8 -*-
import json, re, sys, unicodedata
from collections import defaultdict
sys.path.insert(0,'/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad')
from molmap import canon, PT
import kb
SP='/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad/'

prods=json.load(open(SP+'products.json'))
hist=json.load(open(SP+'hist.json'))

def sa(s): return ''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn')
def root(pt):
    s=sa(pt).upper()
    s=re.sub(r'\(.*?\)','',s)
    s=re.sub(r'[^A-Z0-9+ ]',' ',s)
    return [w for w in s.split() if len(w)>3 and w not in ('SODIO','CALCIO','ACIDO','FERRICO','PARA','AGUA','DE')]

# ---------- agrupa SKUs por molécula ----------
bymol=defaultdict(list)
for p in prods:
    bymol[canon(p['product_name'])].append(p)

# ---------- índice do histórico ----------
def combo_key(s):
    toks=sorted(w for w in re.split(r'[^A-Z0-9]+', sa(s).upper()) if len(w)>3)
    return ' '.join(toks)

def cpx(a,b):
    n=0
    for x,y in zip(a,b):
        if x!=y: break
        n+=1
    return n

def hist_matches(mol_en, pt):
    keys=set(root(pt)) | {mol_en}
    ck=combo_key(pt)
    out=[]
    for h in hist:
        hm=h['_molecula_norm']
        if not hm: continue
        kind=None
        if combo_key(hm)==ck: kind='EXATO'
        else:
            for k in keys:
                if re.search(r'\b'+re.escape(k)+r'\b', hm): kind='PARCIAL/RELACIONADO'; break
            else:
                # variantes de grafia da base (ex.: POLIMIXIN B, REMIFENTANILA, FOSAPREPTANTO)
                htok=[w for w in re.split(r'[^A-Z0-9]+', hm) if len(w)>=7]
                for k in keys:
                    if len(k)<7: continue
                    if any(cpx(k,w)>=7 for w in htok):
                        kind='VARIANTE DE GRAFIA'; break
        if kind: out.append((kind,h))
    return out


rows=[]
MATCHES=[]
for mol, skus in sorted(bymol.items()):
    pt = PT[mol]
    names = sorted(set(s['product_name'] for s in skus))
    cats  = sorted(set(s['therapeutic_category'] for s in skus))
    ar    = kb.area(cats[0], mol)
    comps = sorted(set(s['comparable_to'] for s in skus if s['comparable_to'] not in ('n/a','')))
    fdas  = sorted(set(s['fda_rating'] for s in skus if s['fda_rating']))
    descs = sorted(set(s['product_description'] for s in skus))
    ndcs  = [s['ndc'] for s in skus]
    conc  = sorted(set(s['concentration'] for s in skus))
    tdc   = sorted(set(s['total_drug_content'] for s in skus))
    packs = sorted(set(s['pack_quantity'] for s in skus))
    pages = sorted(set(s['page'] for s in skus))

    # forma farmacêutica / diferenciação
    is_powder = any('powder' in (s['concentration']+s['fill_volume']).lower() for s in skus)
    is_bag    = any(re.search(r'\bbags?\b', s['pack_quantity'], re.I) or 'RtU' in s['product_name'] for s in skus)
    is_syr    = any(re.search(r'\bsyringes?\b', s['pack_quantity']+' '+s['unit_size']+' '+s['product_name'], re.I) for s in skus)
    premix    = any(re.search(r'\bin\s+[\d.]+%|Dextrose|NaCl|Sodium Chloride', s['product_name'], re.I) for s in skus)
    forma=[]
    if is_powder: forma.append('Pó liofilizado/estéril')
    if any(not ('powder' in (s['concentration']+s['fill_volume']).lower()) for s in skus): forma.append('Solução')
    if is_bag or premix: forma.append('Bolsa pronta para uso (premix)')
    if is_syr: forma.append('Seringa preenchida')
    forma=' + '.join(dict.fromkeys(forma)) or 'Solução'

    # status EMS
    ems_status='LIVRE'; ems_txt=''
    if mol in kb.EMS_PORTFOLIO_INJ:
        ems_status='JÁ NO PORTFÓLIO EMS'; ems_txt=kb.EMS_PORTFOLIO_INJ[mol]
    elif mol in kb.EMS_ANEST_PORTFOLIO:
        ems_status='JÁ NO PORTFÓLIO EMS'; ems_txt=kb.EMS_ANEST_PORTFOLIO[mol]
    elif mol in kb.EMS_ANEST_PIPELINE:
        ems_status='EM PIPELINE EMS'; ems_txt=kb.EMS_ANEST_PIPELINE[mol]
    elif mol in kb.EMS_ANEST_GATE:
        ems_status='EM GATE (0-3) EMS'; ems_txt=kb.EMS_ANEST_GATE[mol]

    # histórico NN
    hmk = hist_matches(mol, pt)
    hm  = [h for _,h in hmk]
    kinds=sorted(set(k for k,_ in hmk))
    tipo_match = ('EXATO' if 'EXATO' in kinds else
                  ('VARIANTE DE GRAFIA' if 'VARIANTE DE GRAFIA' in kinds else
                   ('PARCIAL/RELACIONADO' if kinds else '—')))
    hikma_rows=[h for h in hm if 'hikma' in str(h['Fornecedor / Parceiro']).lower()]
    parceiros=sorted(set(str(h['Fornecedor / Parceiro']).strip() for h in hm if str(h['Fornecedor / Parceiro']).strip()))
    resp=sorted(set(str(h['Responsável']).strip() for h in hm if str(h['Responsável']).strip()))
    stat=sorted(set(str(h['Status']).strip() for h in hm if str(h['Status']).strip()))
    datas=[str(h['Data de Entrada'])[:10] for h in hm if h['Data de Entrada']]
    meu = 'SIM' if any('LUCAS MEDINA' in str(h['Responsável']).upper() for h in hm) else 'NÃO'
    ativos=[s for s in stat if s and s!='PASSIVO']
    situacao = 'SEM HISTÓRICO' if not hm else ('ATIVO' if ativos else 'PASSIVO (dormente)')
    STAGE={'PASSIVO':0,'PROSPECÇÃO':1,'CDA':2,'AV. TÉCNICA INICIAL':3,'AV. MARKETING':4,
           'NEGOCIAÇÃO':5,'APROVAÇÃO SUMMARY':6,'TERM SHEET':7,'CONTRATO':8}
    maxstage=max([STAGE.get(s,-1) for s in stat], default=-1)
    hist_flag = 'SIM' if hm else 'NÃO'

    for _k,_h in hmk:
        MATCHES.append({'mol_pt':pt,'kind':_k,'rec':_h})
    tese_rel, tese_txt = kb.TESE.get(mol, ('', ''))
    commodity = mol in kb.COMMODITY
    controlado = mol in kb.CONTROLADO

    # ---------------- SCORE ----------------
    # A. Atratividade/necessidade Brasil (0-30)
    A = {'ALTA':30,'MÉDIA-ALTA':24,'MÉDIA':15}.get(tese_rel, 8 if not commodity else 3)
    # B. Diferenciação da apresentação Hikma (0-25)
    B = 0
    if is_bag or premix: B += 14
    if is_syr: B += 6
    if len(ndcs) >= 5: B += 5
    if any('Reference Listed Drug' in f or 'RLD' in f for f in fdas): B += 6
    B = min(B, 25)
    # C. Espaço no portfólio EMS (0-25)
    C = {'JÁ NO PORTFÓLIO EMS': 4 if (is_bag or premix or is_syr) else 0,
         'EM PIPELINE EMS': 3, 'EM GATE (0-3) EMS': 5, 'LIVRE': 25}[ems_status]
    # D. Viabilidade de licenciamento (0-20)
    D = 20
    if controlado: D -= 12          # Portaria 344/98: importação de acabado muito restrita
    if commodity:  D -= 10          # guerra de preço com genérico local/indiano
    if maxstage >= 5: D -= 4        # já em negociação avançada com outro parceiro
    D = max(D, 0)
    score = A+B+C+D

    # ---------------- REGRAS DURAS ----------------
    bloqueio=''
    if commodity and not (is_bag or premix or is_syr) and ems_status=='LIVRE' and not tese_rel:
        bloqueio='Commodity injetável sem diferencial de apresentação — sem tese de licenciamento de acabado importado.'
    if ems_status=='JÁ NO PORTFÓLIO EMS' and not (is_bag or premix or is_syr):
        bloqueio='Molécula já no portfólio EMS Non Retail na mesma forma — duplicidade.'
    if ems_status in ('EM PIPELINE EMS','EM GATE (0-3) EMS') and not (is_bag or premix or is_syr):
        bloqueio='Já endereçada internamente (pipeline/gate EMS) — risco de duplicidade.'
    if controlado and not tese_rel:
        bloqueio=(bloqueio+' ' if bloqueio else '')+'Sujeita à Portaria 344/98: importação de produto acabado altamente restrita.'

    rec = 'SIM' if (score>=55 and not bloqueio) else 'NÃO'

    # prioridade
    if rec=='SIM':
        pri = 'A - Prioritária' if score>=75 else ('B - Avaliar' if score>=65 else 'C - Monitorar')
    else:
        pri = '—'

    just=[]
    if tese_txt: just.append(tese_txt)
    if ems_status!='LIVRE': just.append('Status EMS: %s (%s).'%(ems_status, ems_txt))
    if is_bag or premix: just.append('Apresentação em bolsa pronta para uso — atende à demanda de "solução de fácil preparo" registrada pelo board de Anestesia.')
    if is_syr: just.append('Seringa preenchida — inovação incremental de apresentação.')
    if hikma_rows: just.append('ATENÇÃO: já existe registro com a própria Hikma nesta molécula na base NN.')
    elif hm: just.append('Já prospectada pela equipe NN (match %s) com %d parceiro(s); situação: %s; status: %s.'%(tipo_match.lower(), len(parceiros), situacao.lower(), ', '.join(stat) or 'n/d'))
    else: just.append('Sem histórico de prospecção desta molécula na base NN.')
    if bloqueio: just.append('BLOQUEIO: '+bloqueio)

    rows.append({
     'Molécula (EN)':mol,'Molécula (PT/DCB)':pt,'Área terapêutica':ar,
     'Produtos no catálogo':' | '.join(names),'Categoria terapêutica (Hikma)':' | '.join(cats),
     'Referência (comparable to)':' | '.join(comps) if comps else 'n/a (Hikma é RLD ou sem referência)',
     'FDA rating':' | '.join(fdas),'Descrição do produto':' | '.join(descs),
     'Forma farmacêutica':forma,'Nº de apresentações (SKUs)':len(skus),'NDCs':', '.join(ndcs),
     'Concentrações':' | '.join(conc),'Conteúdo total':' | '.join(tdc),'Embalagem':' | '.join(packs),
     'Páginas no PDF':', '.join(str(x) for x in pages),
     'Injetável':'SIM','Controlado (Port. 344/98)':'SIM' if controlado else 'NÃO',
     'Commodity/genérico maduro':'SIM' if commodity else 'NÃO',
     'Status no Grupo EMS':ems_status,'Detalhe EMS':ems_txt,
     'Relevância Brasil (hipótese)':tese_rel or ('BAIXA' if commodity else 'A VALIDAR'),
     'Já prospectada pela equipe NN':hist_flag,'Tipo de match no histórico':tipo_match,
     'Situação do histórico':situacao,'Prospectada por VOCÊ (Lucas Medina)':meu,
     'Nº registros no histórico':len(hm),
     'Parceiros já contatados':', '.join(parceiros[:14]) + (' ...' if len(parceiros)>14 else ''),
     'Responsáveis NN':', '.join(resp),'Status no histórico':', '.join(stat),
     'Datas de entrada':', '.join(sorted(set(datas))[:6]),
     'Contato prévio com a Hikma':'SIM' if hikma_rows else 'NÃO',
     'Score A - Atratividade BR (0-30)':A,'Score B - Diferenciação (0-25)':B,
     'Score C - Espaço no portfólio (0-25)':C,'Score D - Viabilidade (0-20)':D,
     'SCORE TOTAL (0-100)':score,'RECOMENDAÇÃO':rec,'Prioridade':pri,
     'Justificativa':' '.join(just),
    })

json.dump(rows, open(SP+'evaluation.json','w'), ensure_ascii=False, indent=1)
json.dump(MATCHES, open(SP+'hist_matches.json','w'), ensure_ascii=False, indent=1, default=str)
print('moléculas avaliadas:',len(rows))
print('SIM:',sum(1 for r in rows if r['RECOMENDAÇÃO']=='SIM'),'| NÃO:',sum(1 for r in rows if r['RECOMENDAÇÃO']=='NÃO'))
print()
for r in sorted(rows,key=lambda x:-x['SCORE TOTAL (0-100)'])[:26]:
    print('%3d %-4s %-14s %-32s %s'%(r['SCORE TOTAL (0-100)'],r['RECOMENDAÇÃO'],r['Prioridade'][:14],r['Molécula (PT/DCB)'][:32],r['Status no Grupo EMS']))
