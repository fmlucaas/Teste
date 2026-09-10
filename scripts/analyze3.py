# -*- coding: utf-8 -*-
"""Recomendação binária por regras de negócio, sem score. Texto em linguagem de negócio."""
import json, re, sys, unicodedata
from collections import defaultdict
sys.path.insert(0,'/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad')
from molmap import canon, PT
import kb, kb2
SP='/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad/'
prods=json.load(open(SP+'products.json')); hist=json.load(open(SP+'hist.json'))

def sa(s): return ''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn')
def root(pt):
    s=re.sub(r'[^A-Z0-9+ ]',' ',re.sub(r'\(.*?\)','',sa(pt).upper()))
    return [w for w in s.split() if len(w)>3 and w not in ('SODIO','CALCIO','ACIDO','FERRICO','PARA','AGUA')]
def ckey(s): return ' '.join(sorted(w for w in re.split(r'[^A-Z0-9]+', sa(s).upper()) if len(w)>3))
def cpx(a,b):
    n=0
    for x,y in zip(a,b):
        if x!=y: break
        n+=1
    return n
def hist_matches(mol_en, pt):
    keys=set(root(pt))|{mol_en}; ck=ckey(pt); out=[]
    for h in hist:
        hm=h['_molecula_norm']
        if not hm: continue
        kind=None
        if ckey(hm)==ck: kind='EXATO'
        else:
            for k in keys:
                if re.search(r'\b'+re.escape(k)+r'\b',hm): kind='PARCIAL/RELACIONADO'; break
            else:
                htok=[w for w in re.split(r'[^A-Z0-9]+',hm) if len(w)>=7]
                for k in keys:
                    if len(k)>=7 and any(cpx(k,w)>=7 for w in htok): kind='VARIANTE DE GRAFIA'; break
        if kind: out.append((kind,h))
    return out

bymol=defaultdict(list)
for p in prods: bymol[canon(p['product_name'])].append(p)

rows=[]; MATCHES=[]
for mol, skus in sorted(bymol.items(), key=lambda kv: PT[kv[0]]):
    pt=PT[mol]; band=kb2.BAND[mol]
    names=sorted(set(s['product_name'] for s in skus))
    cats=sorted(set(s['therapeutic_category'] for s in skus)); ar=kb.area(cats[0],mol)
    comps=sorted(set(s['comparable_to'] for s in skus if s['comparable_to'] not in ('n/a','')))
    fdas=sorted(set(s['fda_rating'] for s in skus if s['fda_rating']))

    is_powder=any('powder' in (s['concentration']+s['fill_volume']).lower() for s in skus)
    is_bag=any(re.search(r'\bbags?\b',s['pack_quantity'],re.I) or 'RtU' in s['product_name'] for s in skus)
    is_syr=any(re.search(r'\bsyringes?\b',s['pack_quantity']+' '+s['unit_size']+' '+s['product_name'],re.I) for s in skus)
    premix=any(re.search(r'\bin\s+[\d.]+%|Dextrose|NaCl|Sodium Chloride',s['product_name'],re.I) for s in skus)
    rtu=is_bag or premix; diferencial=rtu or is_syr
    forma=[]
    if is_powder: forma.append('Pó liofilizado/estéril')
    if any('powder' not in (s['concentration']+s['fill_volume']).lower() for s in skus): forma.append('Solução')
    if rtu: forma.append('Bolsa pronta para uso (premix)')
    if is_syr: forma.append('Seringa preenchida')
    forma=' + '.join(dict.fromkeys(forma)) or 'Solução'
    difs=[]
    if rtu: difs.append('Bolsa pronta para uso')
    if is_syr: difs.append('Seringa preenchida')

    ems='LIVRE'; emstxt=''
    if mol in kb.EMS_PORTFOLIO_INJ: ems,emstxt='JÁ NO PORTFÓLIO EMS',kb.EMS_PORTFOLIO_INJ[mol]
    elif mol in kb.EMS_ANEST_PORTFOLIO: ems,emstxt='JÁ NO PORTFÓLIO EMS',kb.EMS_ANEST_PORTFOLIO[mol]
    elif mol in kb.EMS_ANEST_PIPELINE: ems,emstxt='EM PIPELINE EMS',kb.EMS_ANEST_PIPELINE[mol]
    elif mol in kb.EMS_ANEST_GATE: ems,emstxt='EM GATE (0-3) EMS',kb.EMS_ANEST_GATE[mol]
    em_desenv = ems in ('EM PIPELINE EMS','EM GATE (0-3) EMS')

    hmk=hist_matches(mol,pt); hm=[h for _,h in hmk]
    for k,h in hmk: MATCHES.append({'mol_pt':pt,'kind':k,'rec':h})
    hikma=[h for h in hm if 'hikma' in str(h['Fornecedor / Parceiro']).lower()]
    parc=sorted(set(str(h['Fornecedor / Parceiro']).strip() for h in hm if str(h['Fornecedor / Parceiro']).strip()))
    datas=sorted(set(str(h['Data de Entrada'])[:10] for h in hm if h['Data de Entrada']))
    quando = '—' if not datas else (datas[0] if len(datas)==1 else '%s a %s'%(datas[0],datas[-1]))
    npass=sum(1 for h in hm if str(h['Status']).strip()=='PASSIVO')
    frac=(npass/len(hm)) if hm else 0
    cemiterio = len(parc)>=4 and frac>=0.70
    controlado = mol in kb.CONTROLADO
    rel, tese = kb2.TESE.get(mol,('',''))
    economia_fecha = band in ('A','B')

    # ---------------- REGRAS DE NEGÓCIO ----------------
    motivo=None
    if mol in kb2.SEM_MERCADO_BR:
        motivo='Sem uso relevante no Brasil — não há mercado a atender.'
    elif mol in kb2.FORA_NR:
        motivo='Canal Retail/especialidade, fora do seu escopo Non Retail.'
    elif cemiterio and not diferencial:
        motivo=('A casa já abordou %d parceiros nesta molécula e %d%% estão dormentes. O gargalo é preço de '
                'origem, e a Hikma não é fornecedor de baixo custo.'%(len(parc),round(frac*100)))
    elif controlado and not economia_fecha:
        motivo=('Substância sob Portaria 344/98: cota e autorização de importação pesam demais para o preço '
                'unitário desta molécula.')
    elif rel=='BAIXA' and not hikma:
        motivo='__TESE__'
    elif economia_fecha:
        motivo=None
    elif band=='C' and (mol in kb2.ESCASSO or diferencial or em_desenv):
        motivo=None
    elif hikma:
        motivo=None
    else:
        motivo=('Preço unitário baixo no hospital brasileiro: a margem não cobre frete, imposto, estoque e '
                'registro de um produto acabado importado.')
    rec = 'NÃO' if motivo else 'SIM'

    # ---------------- JUSTIFICATIVA EM LINGUAGEM DE NEGÓCIO ----------------
    j=[]
    if tese: j.append(tese)
    fala_ems = bool(re.search(r'EMS|Grupo|portf[óo]lio|pipeline|[Gg]ate', tese))
    if ems=='JÁ NO PORTFÓLIO EMS' and not fala_ems:
        j.append('O Grupo já tem esta molécula no portfólio Non Retail (%s).'%emstxt)
    elif em_desenv and not fala_ems:
        j.append('O Grupo já a endereça internamente (%s) — licenciar o acabado antecipa a entrada enquanto o '
                 'projeto interno amadurece.'%ems.replace(' EMS',''))
    if difs and not tese:
        j.append('A Hikma traz %s, apresentação que o portfólio atual não cobre.'%(' e '.join(d.lower() for d in difs)))
    fala_nn = bool(re.search(r'base NN|Novos Neg|parceiro|CDA|hist[óo]rico', tese))
    if hikma and not fala_nn: j.append('Já existe CDA vigente com a Hikma nesta molécula.')
    elif hm and not fala_nn: j.append('Já passou por Novos Negócios (%d parceiro(s), %s).'%(len(parc),quando))
    elif not hm and not fala_nn: j.append('Sem registro na base de Novos Negócios.')
    if motivo=='__TESE__': j.append('Não recomendo — a leitura acima não sustenta um licenciamento de acabado.')
    elif motivo: j.append('Não recomendo: '+motivo)
    elif not tese: j.append('Recomendo avaliar: o preço unitário comporta a importação de acabado e não há duplicidade evidente.')

    rows.append({'Molécula (PT/DCB)':pt,'Molécula (EN)':mol,'Agrupamento terapêutico':ar,
     'RECOMENDAÇÃO':rec,'Justificativa':' '.join(j),
     'Categoria terapêutica (Hikma)':' | '.join(cats),'Produtos no catálogo':' | '.join(names),
     'Referência (Comparable To)':' | '.join(comps) if comps else 'n/a (Hikma é RLD)',
     'FDA Rating':' | '.join(fdas),'Forma farmacêutica':forma,
     'Apresentação diferenciada':' + '.join(difs) if difs else '—',
     'Nº de apresentações (SKUs)':len(skus),
     'Concentrações':' | '.join(sorted(set(s['concentration'] for s in skus))),
     'Conteúdo total':' | '.join(sorted(set(s['total_drug_content'] for s in skus))),
     'Embalagens':' | '.join(sorted(set(s['pack_quantity'] for s in skus))),
     'NDCs':', '.join(s['ndc'] for s in skus),
     'Páginas no PDF':', '.join(str(x) for x in sorted(set(s['page'] for s in skus))),
     'Está em portfólio/pipeline EMS?':'SIM' if ems!='LIVRE' else 'NÃO',
     'Estágio no Grupo EMS':ems if ems!='LIVRE' else '—','Texto do deck':emstxt or '—',
     'Já avaliada por NN?':'SIM' if hm else 'NÃO','Quando':quando,
     'Contato prévio com a Hikma':'SIM' if hikma else 'NÃO',
     '_controlado':'SIM' if controlado else 'NÃO'})

json.dump(rows,open(SP+'final.json','w'),ensure_ascii=False,indent=1)
json.dump(MATCHES,open(SP+'hist_matches.json','w'),ensure_ascii=False,indent=1,default=str)
print('moléculas:',len(rows),'| SIM:',sum(1 for r in rows if r['RECOMENDAÇÃO']=='SIM'),
      '| NÃO:',sum(1 for r in rows if r['RECOMENDAÇÃO']=='NÃO'))
print()
for r in rows:
    if r['RECOMENDAÇÃO']=='SIM':
        print('  %-28s EMS=%-3s NN=%-3s %s'%(r['Molécula (PT/DCB)'][:28],r['Está em portfólio/pipeline EMS?'],r['Já avaliada por NN?'],r['Quando']))
