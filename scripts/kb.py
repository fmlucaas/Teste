# -*- coding: utf-8 -*-
"""Base de conhecimento: EMS (do PPT) + leitura de mercado Brasil por molécula."""

# ---- Do PPT slide 25 (posições verificadas): portfólio NON RETAIL injetável J01
EMS_PORTFOLIO_INJ = {  # molécula EN canônica -> texto do slide
 'AMPICILLIN AND SULBACTAM':'Ampicilina + Sulbactam Solução injetável',
 'CEFTRIAXONE':'Ceftriaxona Solução injetável',
 'MEROPENEM':'Meropenem Solução injetável',
 'VANCOMYCIN':'Vancomicina Solução injetável',
 'CEFAZOLIN':'Cefazolina Solução injetável',
 'AMIKACIN':'Amicacina Solução injetável',
 'CLINDAMYCIN':'Clindamicina Solução injetável',
}
# Demais itens do portfólio NR do slide sem correspondente no catálogo Hikma:
EMS_PORTFOLIO_INJ_OUTROS = ['Amoxicilina + Ácido Clavulânico','Teicoplanina','Piperacilina + Tazobactam',
 'Oxacilina','Ceftazidima','Gentamicina','Cefepima']

# ---- Anestésicos injetáveis (slide 34, posições verificadas)
EMS_ANEST_PORTFOLIO = {'MIDAZOLAM':'Midazolam','FENTANYL':'Fentanil'}
EMS_ANEST_PIPELINE  = {'KETAMINE':'Escetamina (pipeline; Cetamina é a base)'}
EMS_ANEST_GATE      = {'LIDOCAINE':'Lidocaína','DEXMEDETOMIDINE':'Dexmedetomidina','REMIFENTANIL':'Remifentanil'}
EMS_ANEST_GATE_OUTROS = ['Propofol','Remimazolam','Levobupivacaína','Suzetrigina','Epinefrina+Bupivacaína',
 'Mepivacaína','Procaína','Trimecaína','Tiopental','Epinefrina+Levobupivacaína']

# ---- Gate / pipeline antibióticos (slides 21 e 25)
EMS_ATB_GATE_OUTROS = ['Ceftazidima+Avibactam (PIPELINE, cópia Brasil)','Cefiderocol','Sulbactam+Durlobactam',
 'Aztreonam+Avibactam','Cefepima+Zidebactam','Dalbavancina']

# ---- NO GO explícitos do comitê (slide 21). Nenhum está no catálogo Hikma, mas ficam para rastreio.
EMS_NOGO = {'CEFTOBIPROL':'NO GO: inviabilidade médica','CEFTOLOZANA+TAZOBACTAM':'NO GO: desinteresse MKT',
 'ORITAVANCINA':'NO GO: mercado','TEDIZOLIDA':'NO GO: medicamento descontinuado',
 'DELAFLOXACINO':'NO GO: inviabilidade médica','MEROPENEM+VABORBACTAM':'NO GO: priorizado ceftazidima+avibactam',
 'PLAZOMICINA':'NO GO: mercado','ERAVACICLINA':'NO GO: mercado','OMADACICLINA':'NO GO: inviabilidade médica',
 'LEFAMULINA':'NO GO: mercado','IMIPENEM+CILASTATINA+RELEBACTAM':'NO GO: desinteresse médico/MKT',
 'CEFEPIME+ENMETAZOBACTAM':'NO GO: priorizado ceftazidima+avibactam'}

# ---- Área terapêutica (mapeada da coluna THERAPEUTIC CATEGORY do catálogo)
def area(cat, mol):
    c=(cat or '').lower()
    if any(k in c for k in ['antineoplastic','cytotoxic','alkylating','anthracycline','antimetabolite',
        'proteasome','microtubule','anti-tumor','nucleoside metabolic','estrogen receptor antagonist']): return 'NR - ONCOLOGIA'
    if any(k in c for k in ['cephalosporin','antibacterial','antibiotic','anti-infective','carbapenem',
        'aminoglycoside','antifungal','anti-viral']): return 'NR - ANTI-INFECCIOSOS'
    if any(k in c for k in ['anesthetic','narcotic analgesic','opioid','neuromuscular','nerve block',
        'sedative','benzodiazepine','analgesic','opiod']): return 'NR - ANESTESIA / DOR'
    if any(k in c for k in ['cardiac','antihypertensive','calcium channel','antiarrythmic','inotr',
        'adrenergic','vasoconstrictor','vasodilator','vascodilator','cardiovascular','beta1','ace inhibitor',
        'angiotensin']): return 'NR - CARDIOVASCULAR'
    if any(k in c for k in ['anticonvulsant','antipsychotic','anti-parkinsonian','neuroleptic','nervous system',
        'antimigraine','barbiturate','muscle relaxant','skelatal','skeletal','respiratory stimulant',
        'acetylcholinesterase']): return 'NR - SNC'
    if any(k in c for k in ['anticoagulant','thrombin','antianemic','blood']): return 'NR - HEMATOLOGIA'
    if any(k in c for k in ['antiemetic','nk1','proton pump','h-2 histamine','alimentary','mucolytic',
        'antispasmodic','anticholinergic','antihistamine','phenothiazine']): return 'NR - SUPORTE / TGI'
    if any(k in c for k in ['androgen','estrogen','progestine','endocrine','calcium regulator','glucocorticoid',
        'corticosteroid','myxedema','carnitine','vitamin','diluent','antihyperuricemic','carbonic',
        'diuretic','immunosuppress','sclerosing','prostaglandin','bronchodilator','complement','diagnostic',
        'cytoprotective','metabolic']): return 'NR - HOSPITALAR / OUTROS'
    return 'NR - HOSPITALAR / OUTROS'

# ---- Commodities de baixíssimo valor agregado (não faz sentido licenciar produto acabado importado)
COMMODITY = {'STERILE WATER','SODIUM ACETATE','CALCIUM GLUCONATE','THIAMINE','CYANOCOBALAMIN',
 'DEXAMETHASONE','ATROPINE','EPHEDRINE','PHENYLEPHRINE','HEPARIN','FUROSEMIDE','DOPAMINE','DOBUTAMINE',
 'DIPHENHYDRAMINE','HYDRALAZINE','METOPROLOL','DIGOXIN','ONDANSETRON','METHYLPREDNISOLONE','PROMETHAZINE',
 'CHLORPROMAZINE','GLYCOPYRROLATE','NEOSTIGMINE','SUCCINYLCHOLINE','NALOXONE','FLUMAZENIL','BUPIVACAINE',
 'LIDOCAINE','METHOTREXATE','CISPLATIN','DOXORUBICIN','ETOPOSIDE','IFOSFAMIDE','BLEOMYCIN','MITOMYCIN',
 'LEUCOVORIN','ACETYLCYSTEINE','AMIODARONE','DILTIAZEM','ENALAPRILAT','LABETALOL','FAMOTIDINE',
 'PANTOPRAZOLE','PROGESTERONE','ESTRADIOL','TESTOSTERONE','ACETAZOLAMIDE','ALLOPURINOL','AZATHIOPRINE',
 'BUMETANIDE','CLONIDINE','DICYCLOMINE','DIPYRIDAMOLE','DROPERIDOL','PHENOBARBITAL','PHENYTOIN',
 'VALPROATE','PROCHLORPERAZINE','ORPHENADRINE','METHOCARBAMOL','BENZTROPINE','TERBUTALINE','DOXAPRAM',
 'DOXYCYCLINE','CEFOXITIN','CEFUROXIME','LEVOFLOXACIN','GANCICLOVIR','DACARBAZINE','DAUNORUBICIN',
 'IDARUBICIN','IRINOTECAN','DOCETAXEL','CLADRIBINE','THIOTEPA','AZACITIDINE','DECITABINE','BORTEZOMIB',
 'GRANISETRON','LEVETIRACETAM','SUMATRIPTAN','CHLOROPROCAINE','ETOMIDATE','ROCURONIUM','VECURONIUM',
 'CISATRACURIUM','MILRINONE','NICARDIPINE','NOREPINEPHRINE','FLUPHENAZINE','LEVOTHYROXINE','CALCITONIN',
 'OCTREOTIDE','CAFFEINE CITRATE','LEVOCARNITINE','SODIUM TETRADECYL SULFATE','CARBOPROST','LINEZOLID'}

# ---- Substâncias sob controle especial (Portaria SVS/MS 344/98) — barreira alta p/ importação de acabado
CONTROLADO = {'FENTANYL','MORPHINE','HYDROMORPHONE','MEPERIDINE','REMIFENTANIL','KETAMINE','MIDAZOLAM',
 'LORAZEPAM','DIAZEPAM','PENTOBARBITAL','PHENOBARBITAL','TESTOSTERONE'}

# ---- Moléculas com tese própria (conhecimento de mercado; validar com Close-Up/NRC)
TESE = {
 'ACETAMINOPHEN + IBUPROFEN':('ALTA','Combinação IV fixa (COMBOGESIC® IV). O deck de Anestesia cita '
   'nominalmente "Comborex IV (paracetamol+ibuprofeno)" como oportunidade de analgesia opioid-sparing. '
   'Hikma é RLD. Sem similar no Brasil.'),
 'ACETAMINOPHEN':('MÉDIA-ALTA','Paracetamol IV: mercado hospitalar consolidado no Brasil e alinhado à '
   'tese opioid-sparing. Hikma tem frasco 100 mL e BOLSA (RLD) — a bolsa é o diferencial de "solução de '
   'fácil preparo" citada pelo board de anestesia.'),
 'DANTROLENE':('ALTA','Antídoto de hipertermia maligna: item de arsenal obrigatório em centro cirúrgico, '
   'poucos fornecedores no mundo e histórico de desabastecimento no Brasil. Baixo volume/alto valor '
   'estratégico e forte porta de entrada institucional.'),
 'ICATIBANT':('ALTA','Angioedema hereditário (doença rara). Alto valor, canal especialidade/judicialização, '
   'baixa competição. Requer avaliação de acesso e preço CMED.'),
 'REGADENOSON':('MÉDIA-ALTA','Agente de estresse farmacológico para cintilografia miocárdica. Nicho '
   'diagnóstico com poucos players; substitui dipiridamol com melhor perfil.'),
 'MICAFUNGIN':('MÉDIA-ALTA','Equinocandina para candidemia. Mercado hospitalar relevante e crescente; '
   'concorrência menor que anfotericina/fluconazol.'),
 'DAPTOMYCIN':('MÉDIA-ALTA','Gram-positivos resistentes (MRSA/VRE) — aderente à tese de resistência '
   'antimicrobiana do deck. Molécula em domínio público, vários players; disputa por preço.'),
 'ERTAPENEM':('MÉDIA','Carbapenêmico. EMS já tem meropenem no portfólio; ertapenem cobre nicho '
   'ambulatorial/OPAT distinto, mas alta competição de genéricos.'),
 'COLISTIMETHATE':('MÉDIA-ALTA','Resgate para Gram-negativos MDR. Aderente à tese de resistência; '
   'mercado pequeno mas estratégico e com histórico de falta.'),
 'POLYMYXIN B':('MÉDIA-ALTA','Mesma tese de colistimetato; uso relevante no Brasil frente a KPC/NDM.'),
 'ARGATROBAN':('MÉDIA','Anticoagulante para trombocitopenia induzida por heparina (HIT). Nicho, mas '
   'sem alternativa direta; Hikma tem apresentação RtU (pronta para uso).'),
 'FOSAPREPITANT':('MÉDIA','Antiemético NK1 IV para CINV. Suporte oncológico com boa margem, porém '
   'genéricos já presentes.'),
 'FOSCARNET':('MÉDIA','Antiviral de resgate (CMV resistente). Nicho pequeno, poucos fornecedores.'),
 'VALRUBICIN':('MÉDIA','Quimioterápico intravesical para câncer de bexiga BCG-refratário. Conecta com o '
   'WarMap de Urologia; mercado pequeno e de nicho.'),
 'LIRAGLUTIDE':('MÉDIA','GLP-1. Alto valor, mas é arena Retail altamente disputada e fora do escopo '
   'Non Retail; avaliar com a BU correta.'),
 'SODIUM FERRIC GLUCONATE COMPLEX':('MÉDIA','Ferro EV. A base histórica mostra prospecção intensa de '
   'carboximaltose férrica (superior); tende a "já temos molécula melhor no pipeline".'),
 'FULVESTRANT':('MÉDIA','Oncologia hormonal em seringa preenchida. Genéricos já disponíveis no Brasil.'),
 'ERIBULIN':('MÉDIA','Oncológico de nicho (mama metastática). Patente/competição a validar.'),
 'DEXRAZOXANE':('MÉDIA','Cardioprotetor em antraciclinas. Nicho de suporte oncológico, poucos players.'),
 'VANCOMYCIN':('ALTA','EMS já tem vancomicina pó no portfólio, MAS a Hikma oferece bolsa PRONTA PARA USO '
   '(premix). É exatamente a "solução de fácil preparo" pedida pelo board. JÁ EXISTE CDA ATIVO COM A HIKMA '
   'nesta molécula (Livia Silva).'),
 'CLINDAMYCIN':('MÉDIA-ALTA','EMS tem clindamicina injetável; a Hikma oferece premix em dextrose 5% '
   '(pronta para uso) — potencial inovação incremental de apresentação.'),
 'LINEZOLID':('MÉDIA','EMS tem linezolida sólido oral; a bolsa IV completa a linha hospitalar. '
   'Competição de genéricos IV já relevante.'),
}
