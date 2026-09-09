import pdfplumber, re, json
from collections import defaultdict

PDF='/root/.claude/uploads/efecc27a-a62f-5537-a145-133cfde4c7cb/4fef8727-hikmainjectableproductcatalogjune2025.pdf'
SP='/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad/'
pdf = pdfplumber.open(PDF)

# each column = list of acceptable token-sequences
ATTR4 = [[['COMPARABLE','TO'],['BRAND','EQUIVALENT']],[['THERAPEUTIC','CATEGORY']],
         [['PRODUCT','DESCRIPTION']],[['FDA','RATING']]]
ATTR3 = [[['THERAPEUTIC','CATEGORY']],[['PRODUCT','DESCRIPTION']],[['FDA','RATING']]]
NDCH  = [[['NDC','Number']],[['Concentration']],[['Total','Drug','Content']],[['Fill','Volume']],
         [['Unit','Size']],[['Pack','Quantity'],['Pack','Quanitity'],['Case','Pack']],[['Closure']]]

def get_lines(page):
    W=float(page.width)
    ws=[w for w in page.extract_words(use_text_flow=False, keep_blank_chars=False) if w['x0']<W-2]
    b=defaultdict(list)
    for w in ws:
        ok=False
        for k in list(b):
            if abs(k-w['top'])<=3.0: b[k].append(w); ok=True; break
        if not ok: b[w['top']].append(w)
    return [{'top':k,'words':sorted(b[k],key=lambda w:w['x0']),
             'text':' '.join(w['text'] for w in sorted(b[k],key=lambda w:w['x0']))} for k in sorted(b)]

def col_starts(line, cols):
    txt=[w['text'] for w in line['words']]; starts=[]; pos=0
    for alts in cols:
        found=None
        for toks in alts:
            for i in range(pos, len(txt)-len(toks)+1):
                if txt[i:i+len(toks)]==toks:
                    found=line['words'][i]['x0']; pos=i+len(toks); break
            if found is not None: break
        if found is None: return None
        starts.append(found)
    return starts

def split_by_cols(lines, starts):
    bounds=[(starts[0]-9) if i==0 else starts[i]-0.25*(starts[i]-starts[i-1]) for i in range(len(starts))]
    cols=['']*len(starts)
    for ln in lines:
        parts=['']*len(starts)
        for w in ln['words']:
            idx=0
            for i,bd in enumerate(bounds):
                if w['x0']>=bd: idx=i
            parts[idx]=(parts[idx]+' '+w['text']).strip()
        for i in range(len(starts)):
            if parts[i]: cols[i]=(cols[i]+' '+parts[i]).strip()
    return cols

SKIP=re.compile(r'^(Injectables|BRANDED|uscustomerservice@hikma|Please see Package|Minimum order|'
                r'\*|HK-\d|Please refer to page|Wholesaler|\d{1,3}$)', re.I)
NDCRE=re.compile(r'^\*{0,2}(\d{4,5}-\d{3,4}-\d{2,3})\*{0,2}$')

products=[]; blocks=0
for pno in range(len(pdf.pages)):
    lines=get_lines(pdf.pages[pno]); attr={}; ndc={}
    for i,ln in enumerate(lines):
        s=col_starts(ln,ATTR4)
        if s: attr[i]=('C4',s); continue
        s=col_starts(ln,ATTR3)
        if s: attr[i]=('C3',s); continue
        s=col_starts(ln,NDCH)
        if s: ndc[i]=s
    if not attr: continue
    aidx=sorted(attr); nidx=sorted(ndc)
    for ai in aidx:
        blocks+=1
        kind,ast=attr[ai]
        prev=[x for x in nidx if x<ai]; floor=max(prev) if prev else -1
        title=[]; j=ai-1
        while j>floor:
            t=lines[j]['text'].strip()
            if not t or SKIP.match(t) or NDCRE.match(lines[j]['words'][0]['text']): break
            title.insert(0,t); j-=1
        nxt=[x for x in nidx if x>ai]
        if not nxt: continue
        ni=nxt[0]
        vals=split_by_cols(lines[ai+1:ni],ast)
        if kind=='C3': vals=['(Hikma is the brand)']+vals
        nxt_a=[x for x in aidx if x>ni]; end=nxt_a[0] if nxt_a else len(lines)
        for ln in lines[ni+1:end]:
            m=NDCRE.match(ln['words'][0]['text'])
            if not m: continue
            d=split_by_cols([ln],ndc[ni])
            products.append({'page':pno+1,'product_name':' '.join(title).strip(),
              'comparable_to':vals[0],'therapeutic_category':vals[1],'product_description':vals[2],
              'fda_rating':vals[3],'ndc':m.group(1),'concentration':d[1],'total_drug_content':d[2],
              'fill_volume':d[3],'unit_size':d[4],'pack_quantity':d[5],'closure':d[6]})

json.dump(products, open(SP+'products.json','w'), indent=1)
n=[p['ndc'] for p in products]
print('blocks:',blocks,'| SKUs:',len(products),'| unique NDC:',len(set(n)),'| names:',len(set(p['product_name'] for p in products)))
from collections import Counter
print('dupes:',[k for k,v in Counter(n).items() if v>1])
