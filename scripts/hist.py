import openpyxl, json, unicodedata, re
SP='/tmp/claude-0/-home-user-Teste/efecc27a-a62f-5537-a145-133cfde4c7cb/scratchpad/'
wb=openpyxl.load_workbook('/root/.claude/uploads/efecc27a-a62f-5537-a145-133cfde4c7cb/c30d6c07-data_7.xlsx',data_only=True)
ws=wb['data (8)']
rows=list(ws.iter_rows(values_only=True))
hdr=[str(h) for h in rows[0]]
raw=[list(r) for r in rows[1:] if any(x not in (None,'') for x in r)]

# merge records split by embedded newline in the molecule cell
recs=[]; i=0; merged=0
while i < len(raw):
    r=raw[i]
    tail_empty = all((x in (None,'')) for x in r[2:])
    if tail_empty and i+1 < len(raw) and str(raw[i+1][0]).strip().endswith('"'):
        cont=raw[i+1]
        mol = (str(r[1]).strip().lstrip('"') + ' ' + str(cont[0]).strip().rstrip('"')).strip()
        new = [r[0], mol] + cont[1:]           # shift continuation right by one
        new = new[:len(hdr)] + ['']*(len(hdr)-len(new))
        recs.append(new); merged+=1; i+=2
    else:
        recs.append(r + ['']*(len(hdr)-len(r))); i+=1
print('physical rows:',len(raw),'| logical records:',len(recs),'| merged:',merged)

def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn')
def norm_mol(s):
    s=strip_acc(s).upper().strip().strip('"')
    s=re.sub(r'\b(CLORIDRATO|SULFATO|SODICO|SODICA|DE|DO|DA|ACETATO|MESILATO|BESILATO|CITRATO|'
             r'FOSFATO|SUCCINATO|LACTATO|MALEATO|TARTARATO|BITARTARATO|GLUCONATO|BROMETO|'
             r'CLORETO|DISSODICO|POTASSICO|CALCICO|MONOIDRATADO|ANIDRO|HCL)\b',' ',s)
    s=re.sub(r'[^A-Z0-9+ ]+',' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

out=[]
for r in recs:
    d=dict(zip(hdr,r))
    d['_molecula_norm']=norm_mol(d.get('Molécula',''))
    out.append(d)
json.dump(out, open(SP+'hist.json','w'), ensure_ascii=False, indent=1, default=str)

from collections import Counter
mols=Counter(d['_molecula_norm'] for d in out if d['_molecula_norm'])
print('unique normalized molecules:',len(mols))
print('top:',mols.most_common(12))
