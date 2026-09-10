# -*- coding: utf-8 -*-
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
for mol, skus in sorted(bymol.items()):
    pt=PT[mol]; band=kb2.BAND[mol]; viab=kb2.VIAB[band]
    names=sorted(set(s['product_name'] for s in skus))
    cats=sorted(set(s['therapeutic_category'] for s in skus)); ar=kb.area(cats[0],mol)
    comps=sorted(set(s['comparable_to'] for s in skus if s['comparable_to'] not in ('n/a','')))
    fdas=sorted(set(s['fda_rating'] for s in skus if s['fda_rating']))
    ndcs=[s['ndc'] for s in skus]

    is_powder=any('powder' in (s['concentration']+s['fill_volume']).lower() for s in skus)
    is_bag=any(re.search(r'\bbags?\b',s['pack_quantity'],re.I) or 'RtU' in s['product_name'] for s in skus)
    is_syr=any(re.search(r'\bsyringes?\b',s['pack_quantity']+' '+s['unit_size']+' '+s['product_name'],re.I) for s in skus)
    premix=any(re.search(r'\bin\s+[\d.]+%|Dextrose|NaCl|Sodium Chloride',s['product_name'],re.I) for s in skus)
    rtu = is_bag or premix
    is_rld=any('Reference Listed Drug' in f or 'RLD' in f for f in fdas)
    forma=[]
    if is_powder: forma.append('Pó liofilizado/estéril')
    if any('powder' not in (s['concentration']+s['fill_volume']).lower() for s in skus): forma.append('Solução')
    if rtu: forma.append('Bolsa pronta para uso (premix)')
    if is_syr: forma.append('Seringa preenchida')
    forma=' + '.join(dict.fromkeys(forma)) or 'Solução'

    ems='LIVRE'; emstxt=''
    if mol in kb.EMS_PORTFOLIO_INJ: ems,emstxt='JÁ NO PORTFÓLIO EMS',kb.EMS_PORTFOLIO_INJ[mol]
    elif mol in kb.EMS_ANEST_PORTFOLIO: ems,emstxt='JÁ NO PORTFÓLIO EMS',kb.EMS_ANEST_PORTFOLIO[mol]
    elif mol in kb.EMS_ANEST_PIPELINE: ems,emstxt='EM PIPELINE EMS',kb.EMS_ANEST_PIPELINE[mol]
    elif mol in kb.EMS_ANEST_GATE: ems,emstxt='EM GATE (0-3) EMS',kb.EMS_ANEST_GATE[mol]

    hmk=hist_matches(mol,pt); hm=[h for _,h in hmk]
    for k,h in hmk: MATCHES.append({'mol_pt':pt,'kind':k,'rec':h})
    kinds=sorted(set(k for k,_ in hmk))
    tipo=('EXATO' if 'EXATO' in kinds else ('VARIANTE DE GRAFIA' if 'VARIANTE DE GRAFIA' in kinds
          else ('PARCIAL/RELACIONADO' if kinds else '—')))
    hikma=[h for h in hm if 'hikma' in str(h['Fornecedor / Parceiro']).lower()]
    parc=sorted(set(str(h['Fornecedor / Parceiro']).strip() for h in hm if str(h['Fornecedor / Parceiro']).strip()))
    resp=sorted(set(str(h['Responsável']).strip() for h in hm if str(h['Responsável']).strip()))
    stat=sorted(set(str(h['Status']).strip() for h in hm if str(h['Status']).strip()))
    datas=sorted(set(str(h['Data de Entrada'])[:10] for h in hm if h['Data de Entrada']))
    meu='SIM' if any('LUCAS MEDINA' in str(h['Responsável']).upper() for h in hm) else 'NÃO'
    npass=sum(1 for h in hm if str(h['Status']).strip()=='PASSIVO')
    frac=(npass/len(hm)) if hm else 0
    cemiterio = len(parc)>=4 and frac>=0.70
    ativos=[s for s in stat if s and s!='PASSIVO']
    situ='SEM HISTÓRICO' if not hm else ('ATIVO' if ativos else 'PASSIVO (dormente)')
    if cemiterio: sinal='CEMITÉRIO — %d parceiros, %d%% dormentes'%(len(parc),round(frac*100))
    elif hikma: sinal='RELAÇÃO ABERTA COM A HIKMA'
    elif not hm: sinal='ESPAÇO BRANCO'
    elif ativos: sinal='EM ANDAMENTO com outro parceiro'
    else: sinal='DORMENTE — candidato a re-acesso'

    rel, tese = kb2.TESE.get(mol,('',''))

    # ---------------- SCORE v2 ----------------
    E1={'A':30,'B':26,'C':15,'D':5,'E':0}[band]
    E2=0
    if mol in kb2.ESCASSO: E2+=10
    if mol in kb2.COMPLEX_ALTA: E2+=10
    elif is_powder: E2+=4
    E2=min(E2,20)
    if ems=='EM GATE (0-3) EMS': E3,anos=20,'3 a 5 anos'
    elif ems=='EM PIPELINE EMS': E3,anos=17,'2 a 3 anos'
    elif ems=='JÁ NO PORTFÓLIO EMS': E3,anos=(12,'Extensão de linha') if (rtu or is_syr) else (0,'Nenhuma')
    else: E3,anos=14,'Entrada nova'
    if isinstance(E3,tuple): E3,anos=E3
    E4=0
    if rtu: E4+=9
    if is_syr: E4+=6
    if is_rld: E4+=4
    if len(ndcs)>=5: E4+=2
    E4=min(E4,15)
    if hikma: E5=15
    elif cemiterio: E5=-10
    elif not hm: E5=8
    elif ativos: E5=3
    else: E5=0
    score=E1+E2+E3+E4+E5

    # ---------------- EXCLUSÕES E ROTA ----------------
    excl=''
    if mol in kb2.SEM_MERCADO_BR: excl='Sem mercado relevante no Brasil.'
    elif mol in kb2.FORA_NR: excl='Fora do escopo Non Retail (canal Retail/especialidade).'
    elif viab=='Inviável' and not hikma: excl=('Preço unitário na faixa %s não absorve frete, imposto, estoque '
        'e margem de importação de acabado.'%band)

    if mol in kb2.SEM_MERCADO_BR: rota='Descartar — sem mercado no Brasil'
    elif mol in kb2.FORA_NR: rota='Encaminhar à BU Retail — fora do seu escopo'
    elif band in 'AB': rota='Licenciar produto acabado (importar e distribuir)'
    elif band=='C' and ems in ('EM GATE (0-3) EMS','EM PIPELINE EMS'):
        rota='BRIDGE — importar para antecipar lançamento e migrar para produção própria'
    elif band=='C': rota='Licenciar acabado — condicionado a teste de preço'
    elif (rtu or is_syr) and hikma: rota='BRIDGE condicional — testar prêmio de preço da apresentação antes de investir'
    elif rtu or is_syr: rota='Licenciar dossiê / transferência de tecnologia (fora do escopo de acabado)'
    else: rota='Descartar — desenvolvimento interno é mais barato que importar'

    # decisão por REGRAS (não só por nota), auditável linha a linha
    diferencial = rtu or is_syr
    gates=[]
    if mol in kb2.SEM_MERCADO_BR: gates.append('sem mercado no Brasil')
    if mol in kb2.FORA_NR:        gates.append('fora do escopo Non Retail')
    if cemiterio and not diferencial: gates.append('cemitério de prospecção sem diferencial novo')
    if viab=='Inviável' and not hikma: gates.append('economia do acabado importado não fecha')
    if score<50: gates.append('qualidade geral abaixo do piso (score < 50)')
    if rel=='BAIXA' and not hikma: gates.append('veto de especialista: tese comercial fraca apesar da nota')
    rec='NÃO' if gates else 'SIM'
    override = ('VETO — tese fraca' if (rel=='BAIXA' and not hikma) else
                ('TETO C — tese apenas parcial' if rel=='BAIXA-MÉDIA' else '—'))
    if gates and not excl: excl='; '.join(gates).capitalize()+'.'
    pri = ('—' if rec=='NÃO' else
           'A - Atacar agora' if score>=68 else ('B - Qualificar' if score>=57 else 'C - Fila'))
    if rec=='SIM' and rel=='BAIXA-MÉDIA': pri='C - Fila'

    riscos=[]
    if band=='C': riscos.append('Preço na fronteira: só fecha com volume ou custo logístico baixo.')
    if viab=='Inviável': riscos.append('Economia de acabado importado não fecha na faixa de preço estimada.')
    if rtu: riscos.append('Bolsa premix exige estabilidade/cadeia fria — encarece frete e reduz shelf life útil.')
    if mol in kb.CONTROLADO: riscos.append('Portaria 344/98: cota e autorização de importação restringem o acabado.')
    if cemiterio: riscos.append('%d parceiros já abordados e dormentes — a barreira provável é preço, não sourcing.'%len(parc))
    if ems=='JÁ NO PORTFÓLIO EMS' and not (rtu or is_syr): riscos.append('EMS já produz — importar destrói margem.')
    riscos.append('Hikma é multinacional: pela lâmina WarMap, "caso a discutir" antes do gate.')

    just=[]
    if tese: just.append(tese)
    if ems!='LIVRE': just.append('Status EMS: %s (%s) — aceleração estimada: %s.'%(ems,emstxt,anos))
    if hikma: just.append('CDA vigente com a Hikma nesta molécula (Livia Silva, 15-06-2026).')
    elif cemiterio: just.append('Base NN: %d parceiros abordados, %d%% dormentes.'%(len(parc),round(frac*100)))
    elif hm: just.append('Base NN: %d parceiro(s), situação %s.'%(len(parc),situ.lower()))
    else: just.append('Sem histórico na base NN.')
    if excl: just.append('EXCLUSÃO: '+excl)

    rows.append({'Molécula (PT/DCB)':pt,'Molécula (EN)':mol,'Área terapêutica':ar,
     'RECOMENDAÇÃO':rec,'Prioridade':pri,'Rota recomendada':rota,'SCORE TOTAL (0-100)':score,
     'E1 Economia do acabado (0-30)':E1,'E2 Escassez/barreira (0-20)':E2,'E3 Aceleração (0-20)':E3,
     'E4 Diferenciação (0-15)':E4,'E5 Sinal do histórico (-10 a 15)':E5,
     'Faixa de preço (hipótese)':kb2.BAND_LABEL[band],'Viabilidade acabado importado':viab,
     'Aceleração vs desenv. interno':anos,'Relevância (hipótese)':rel or ('BAIXA' if band in 'DE' else 'A VALIDAR'),
     'Override de especialista':override,
     'Status no Grupo EMS':ems,'Detalhe EMS':emstxt,
     'Sinal do histórico':sinal,'Já prospectada pela equipe NN':'SIM' if hm else 'NÃO',
     'Tipo de match no histórico':tipo,'Situação do histórico':situ,
     'Prospectada por VOCÊ (Lucas Medina)':meu,'Contato prévio com a Hikma':'SIM' if hikma else 'NÃO',
     'Nº parceiros já abordados':len(parc),'Nº registros no histórico':len(hm),
     'Parceiros já contatados':', '.join(parc[:14])+(' ...' if len(parc)>14 else ''),
     'Responsáveis NN':', '.join(resp),'Status no histórico':', '.join(stat),
     'Datas de entrada':', '.join(datas[:6]),
     'Forma farmacêutica':forma,'Nº de apresentações (SKUs)':len(skus),
     'Controlado (Port. 344/98)':'SIM' if mol in kb.CONTROLADO else 'NÃO',
     'Referência (comparable to)':' | '.join(comps) if comps else 'n/a (Hikma é RLD)',
     'FDA rating':' | '.join(fdas),'Categoria terapêutica (Hikma)':' | '.join(cats),
     'Produtos no catálogo':' | '.join(names),'NDCs':', '.join(ndcs),
     'Páginas no PDF':', '.join(str(x) for x in sorted(set(s['page'] for s in skus))),
     'Justificativa':' '.join(just),'Riscos e condicionantes':' '.join(riscos)})

json.dump(rows,open(SP+'evaluation2.json','w'),ensure_ascii=False,indent=1)
json.dump(MATCHES,open(SP+'hist_matches.json','w'),ensure_ascii=False,indent=1,default=str)
print('moléculas:',len(rows),'| SIM:',sum(1 for r in rows if r['RECOMENDAÇÃO']=='SIM'))
from collections import Counter
print('rotas:',Counter(r['Rota recomendada'].split(' —')[0].split(' (')[0] for r in rows).most_common())
print()
for r in sorted(rows,key=lambda x:-x['SCORE TOTAL (0-100)'])[:30]:
    print('%3d %-3s %-16s %-26s %-22s %s'%(r['SCORE TOTAL (0-100)'],r['RECOMENDAÇÃO'],r['Prioridade'][:16],
      r['Molécula (PT/DCB)'][:26],r['Faixa de preço (hipótese)'][:22],r['Sinal do histórico'][:34]))
