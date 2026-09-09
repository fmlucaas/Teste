# -*- coding: utf-8 -*-
"""Canonical molecule extraction + EN->PT(DCB) mapping for the Hikma injectable catalog."""
import re

SALTS = (r'HYDROCHLORIDE|HCL|SULFATE|SODIUM PHOSPHATE|SODIUM SUCCINATE|SODIUM|CITRATE|MESYLATE|'
         r'BESYLATE|EDISYLATE|TARTRATE|BITARTRATE|LACTATE|MALEATE|ACETATE|GLUCONATE|BROMIDE|'
         r'CHLORIDE|CALCIUM|DECANOATE|VALERATE|CYPIONATE|ENANTHATE|TROMETHAMINE|METHYLSULFATE|'
         r'POTASSIUM|MAGNESIUM|DISODIUM|SALMON|SYNTHETIC')

SPECIAL = {
 '(acetaminophen and ibuprofen) injection': 'ACETAMINOPHEN + IBUPROFEN',
 'INFUMORPH® 200 & 500 (Preservative-Free Morphine Sulfate Sterile Solution), C-II': 'MORPHINE',
 'IMMPHENTIV (Phenylephrine HCl Injection, USP) ®': 'PHENYLEPHRINE',
 'SODIUM ACETATE Injection, USP': 'SODIUM ACETATE',
 'CALCIUM GLUCONATE Injection, USP': 'CALCIUM GLUCONATE',
 'SODIUM FERRIC GLUCONATE COMPLEX in Sucrose Injection': 'SODIUM FERRIC GLUCONATE COMPLEX',
 'SODIUM TETRADECYL Sulfate Injection, 3%': 'SODIUM TETRADECYL SULFATE',
 'CAFFEINE CITRATE Injection, USP': 'CAFFEINE CITRATE',
 'STERILE WATER for Injection, USP': 'STERILE WATER',
}

def canon(name):
    if name in SPECIAL: return SPECIAL[name]
    s = name
    m = re.match(r'^[A-Z][A-Za-z]*®?\s*(?:INJECTION|Injection)?\s*\((.+?)\)', s)
    if m: s = m.group(1)                       # brand wrapper -> inner generic
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r',?\s*C-(II|III|IV|V)\b', ' ', s)
    s = re.sub(r'\bin\s+[\d.]+%.*$', ' ', s, flags=re.I)     # diluent
    s = re.sub(r'\bin\s+(Sucrose|5% Dextrose|0\.9%).*$', ' ', s, flags=re.I)
    s = re.sub(r'\b(for|Intravesical|Injection|Solution|USP|USP\.|Sterile)\b.*$', ' ', s, flags=re.I)
    s = re.sub(r'[®*,]', ' ', s)
    s = s.upper()
    s = re.sub(r'\b(' + SALTS + r')\b', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# EN -> PT-BR (DCB / Anvisa) name
PT = {
 'ACETAMINOPHEN':'Paracetamol','ACETAMINOPHEN + IBUPROFEN':'Paracetamol + Ibuprofeno',
 'ACETYLCYSTEINE':'Acetilcisteína','ACETAZOLAMIDE':'Acetazolamida','ALLOPURINOL':'Alopurinol',
 'AMIKACIN':'Amicacina','AMIODARONE':'Amiodarona','AMPICILLIN AND SULBACTAM':'Ampicilina + Sulbactam',
 'ARGATROBAN':'Argatrobana','ATROPINE':'Atropina','AZACITIDINE':'Azacitidina',
 'AZATHIOPRINE':'Azatioprina','BENZTROPINE':'Benzatropina','BLEOMYCIN':'Bleomicina',
 'BORTEZOMIB':'Bortezomibe','BUMETANIDE':'Bumetanida','BUPIVACAINE':'Bupivacaína',
 'CALCITONIN':'Calcitonina','CALCIUM GLUCONATE':'Gluconato de cálcio','SODIUM ACETATE':'Acetato de sódio',
 'SODIUM TETRADECYL SULFATE':'Tetradecilsulfato de sódio','CAFFEINE CITRATE':'Citrato de cafeína',
 'CARBOPROST':'Carboprosta','CEFAZOLIN':'Cefazolina','CEFOXITIN':'Cefoxitina',
 'CEFTRIAXONE':'Ceftriaxona','CEFUROXIME':'Cefuroxima','CHLOROPROCAINE':'Cloroprocaína',
 'CISATRACURIUM':'Cisatracúrio','CISPLATIN':'Cisplatina','CLADRIBINE':'Cladribina',
 'CLINDAMYCIN':'Clindamicina','CLONIDINE':'Clonidina','COLISTIMETHATE':'Colistimetato',
 'CYANOCOBALAMIN':'Cianocobalamina','DACARBAZINE':'Dacarbazina','DANTROLENE':'Dantroleno',
 'DAPTOMYCIN':'Daptomicina','DAUNORUBICIN':'Daunorrubicina','DECITABINE':'Decitabina',
 'DEXAMETHASONE':'Dexametasona','DEXMEDETOMIDINE':'Dexmedetomidina','DEXRAZOXANE':'Dexrazoxano',
 'DIAZEPAM':'Diazepam','DICYCLOMINE':'Diciclomina','DIGOXIN':'Digoxina','DILTIAZEM':'Diltiazem',
 'DIPYRIDAMOLE':'Dipiridamol','DOBUTAMINE':'Dobutamina','DOCETAXEL':'Docetaxel',
 'DOXAPRAM':'Doxapram','DOPAMINE':'Dopamina','DOXORUBICIN':'Doxorrubicina',
 'DOXYCYCLINE':'Doxiciclina','DROPERIDOL':'Droperidol','MORPHINE':'Morfina',
 'DIPHENHYDRAMINE':'Difenidramina','ENALAPRILAT':'Enalaprilato','EPHEDRINE':'Efedrina',
 'ERIBULIN':'Eribulina','ERTAPENEM':'Ertapenem','ESTRADIOL':'Estradiol (valerato)',
 'ETOMIDATE':'Etomidato','ETOPOSIDE':'Etoposídeo','FAMOTIDINE':'Famotidina','FENTANYL':'Fentanil',
 'FLUMAZENIL':'Flumazenil','FLUPHENAZINE':'Flufenazina','FOSAPREPITANT':'Fosaprepitanto',
 'FOSCARNET':'Foscarnete','FULVESTRANT':'Fulvestranto','FUROSEMIDE':'Furosemida',
 'GANCICLOVIR':'Ganciclovir','GLYCOPYRROLATE':'Glicopirrolato','GRANISETRON':'Granisetrona',
 'HEPARIN':'Heparina','HYDROMORPHONE':'Hidromorfona','ICATIBANT':'Icatibanto',
 'IDARUBICIN':'Idarrubicina','IFOSFAMIDE':'Ifosfamida','IRINOTECAN':'Irinotecano',
 'KETAMINE':'Cetamina','LABETALOL':'Labetalol','LEUCOVORIN':'Leucovorina (ác. folínico)',
 'LEVETIRACETAM':'Levetiracetam','LEVOCARNITINE':'Levocarnitina','LEVOFLOXACIN':'Levofloxacino',
 'LEVOTHYROXINE':'Levotiroxina','LIDOCAINE':'Lidocaína','LINEZOLID':'Linezolida',
 'LIRAGLUTIDE':'Liraglutida','LORAZEPAM':'Lorazepam','MEPERIDINE':'Meperidina (petidina)',
 'MEROPENEM':'Meropenem','METHOTREXATE':'Metotrexato','METOPROLOL':'Metoprolol',
 'MICAFUNGIN':'Micafungina','MIDAZOLAM':'Midazolam','MILRINONE':'Milrinona',
 'MITOMYCIN':'Mitomicina','NALOXONE':'Naloxona','NEOSTIGMINE':'Neostigmina',
 'NICARDIPINE':'Nicardipino','NOREPINEPHRINE':'Noradrenalina','OCTREOTIDE':'Octreotida',
 'ONDANSETRON':'Ondansetrona','ORPHENADRINE':'Orfenadrina','PANTOPRAZOLE':'Pantoprazol',
 'PENTOBARBITAL':'Pentobarbital','PROMETHAZINE':'Prometazina','PHENOBARBITAL':'Fenobarbital',
 'PHENTOLAMINE':'Fentolamina','PHENYLEPHRINE':'Fenilefrina','PHENYTOIN':'Fenitoína',
 'POLYMYXIN B':'Polimixina B','PROCHLORPERAZINE':'Proclorperazina','PROGESTERONE':'Progesterona',
 'REGADENOSON':'Regadenoson','REMIFENTANIL':'Remifentanil','METHOCARBAMOL':'Metocarbamol',
 'ROCURONIUM':'Rocurônio','SODIUM FERRIC GLUCONATE COMPLEX':'Gluconato férrico de sódio','STERILE WATER':'Água para injeção',
 'SUCCINYLCHOLINE':'Succinilcolina','SUMATRIPTAN':'Sumatriptana','TERBUTALINE':'Terbutalina',
 'TESTOSTERONE':'Testosterona','THIAMINE':'Tiamina','THIOTEPA':'Tiotepa',
 'VALPROATE':'Valproato de sódio','VALRUBICIN':'Valrubicina','VANCOMYCIN':'Vancomicina',
 'VECURONIUM':'Vecurônio','CHLORPROMAZINE':'Clorpromazina','HYDRALAZINE':'Hidralazina',
 'METHYLPREDNISOLONE':'Metilprednisolona',
}
