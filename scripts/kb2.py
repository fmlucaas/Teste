# -*- coding: utf-8 -*-
"""v2 — camada econômica e crítica. Faixas de preço são HIPÓTESE de especialista,
a serem substituídas pelo IQVIA Non-Retail (NRC/HPP)."""

# Faixa de preço fábrica hospitalar por unidade (frasco/ampola/bolsa/seringa), Brasil
# A: > R$ 1.000 | B: R$ 200-1.000 | C: R$ 50-200 | D: R$ 10-50 | E: < R$ 10
BAND = {
'ICATIBANT':'A','ERIBULIN':'A','LIRAGLUTIDE':'A','VALRUBICIN':'A',
'ARGATROBAN':'B','AZACITIDINE':'B','BORTEZOMIB':'B','CLADRIBINE':'B','DANTROLENE':'B',
'DAPTOMYCIN':'B','DECITABINE':'B','DEXRAZOXANE':'B','FOSCARNET':'B','FULVESTRANT':'B',
'LEVOTHYROXINE':'B','MICAFUNGIN':'B','OCTREOTIDE':'B','REGADENOSON':'B','THIOTEPA':'B',
'ACETAZOLAMIDE':'C','ACETYLCYSTEINE':'C','ALLOPURINOL':'C','AZATHIOPRINE':'C','BLEOMYCIN':'C',
'CAFFEINE CITRATE':'C','CALCITONIN':'C','CARBOPROST':'C','CISATRACURIUM':'C','COLISTIMETHATE':'C',
'DAUNORUBICIN':'C','DEXMEDETOMIDINE':'C','DOCETAXEL':'C','DOXYCYCLINE':'C','ERTAPENEM':'C',
'FOSAPREPITANT':'C','GANCICLOVIR':'C','IDARUBICIN':'C','IFOSFAMIDE':'C','IRINOTECAN':'C',
'LEVETIRACETAM':'C','LEVOCARNITINE':'C','LINEZOLID':'C','MEROPENEM':'C','MILRINONE':'C',
'MITOMYCIN':'C','NICARDIPINE':'C','PHENTOLAMINE':'C','POLYMYXIN B':'C','REMIFENTANIL':'C',
'SODIUM FERRIC GLUCONATE COMPLEX':'C','SODIUM TETRADECYL SULFATE':'C','ACETAMINOPHEN + IBUPROFEN':'C',
'AMIKACIN':'D','AMIODARONE':'D','AMPICILLIN AND SULBACTAM':'D','BENZTROPINE':'D','BUMETANIDE':'D',
'CEFAZOLIN':'D','CEFOXITIN':'D','CEFTRIAXONE':'D','CEFUROXIME':'D','CHLOROPROCAINE':'D',
'CISPLATIN':'D','CLINDAMYCIN':'D','CLONIDINE':'D','DACARBAZINE':'D','DILTIAZEM':'D',
'DIPYRIDAMOLE':'D','DOXAPRAM':'D','DOXORUBICIN':'D','DROPERIDOL':'D','ENALAPRILAT':'D',
'ESTRADIOL':'D','ETOMIDATE':'D','ETOPOSIDE':'D','FLUMAZENIL':'D','FLUPHENAZINE':'D',
'GLYCOPYRROLATE':'D','GRANISETRON':'D','HYDROMORPHONE':'D','KETAMINE':'D','LABETALOL':'D',
'LEUCOVORIN':'D','LEVOFLOXACIN':'D','LORAZEPAM':'D','METHOCARBAMOL':'D','METHOTREXATE':'D',
'METHYLPREDNISOLONE':'D','METOPROLOL':'D','NALOXONE':'D','NOREPINEPHRINE':'D','ORPHENADRINE':'D',
'PANTOPRAZOLE':'D','PENTOBARBITAL':'D','PHENYTOIN':'D','PROCHLORPERAZINE':'D','PROGESTERONE':'D',
'ROCURONIUM':'D','SUCCINYLCHOLINE':'D','SUMATRIPTAN':'D','TERBUTALINE':'D','TESTOSTERONE':'D',
'VALPROATE':'D','VANCOMYCIN':'D','VECURONIUM':'D','DICYCLOMINE':'D',
'ACETAMINOPHEN':'E','ATROPINE':'E','BUPIVACAINE':'E','CALCIUM GLUCONATE':'E','CHLORPROMAZINE':'E',
'CYANOCOBALAMIN':'E','DEXAMETHASONE':'E','DIAZEPAM':'E','DIGOXIN':'E','DIPHENHYDRAMINE':'E',
'DOBUTAMINE':'E','DOPAMINE':'E','EPHEDRINE':'E','FAMOTIDINE':'E','FENTANYL':'E','FUROSEMIDE':'E',
'HEPARIN':'E','HYDRALAZINE':'E','LIDOCAINE':'E','MEPERIDINE':'E','MIDAZOLAM':'E','MORPHINE':'E',
'NEOSTIGMINE':'E','ONDANSETRON':'E','PHENOBARBITAL':'E','PHENYLEPHRINE':'E','PROMETHAZINE':'E',
'SODIUM ACETATE':'E','STERILE WATER':'E','THIAMINE':'E',
}
BAND_LABEL={'A':'A · > R$ 1.000/un','B':'B · R$ 200-1.000/un','C':'C · R$ 50-200/un',
            'D':'D · R$ 10-50/un','E':'E · < R$ 10/un'}
# Viabilidade do produto ACABADO IMPORTADO (escopo do usuário)
VIAB={'A':'Viável','B':'Viável','C':'Marginal','D':'Inviável','E':'Inviável'}

# Escassez estrutural no Brasil / poucos fornecedores / histórico de desabastecimento
ESCASSO={'DANTROLENE','ICATIBANT','REGADENOSON','FOSCARNET','VALRUBICIN','DEXRAZOXANE','ERIBULIN',
 'CLADRIBINE','THIOTEPA','LEVOTHYROXINE','CALCITONIN','CARBOPROST','SODIUM TETRADECYL SULFATE',
 'PHENTOLAMINE','ACETAZOLAMIDE','ALLOPURINOL','DOXYCYCLINE','CAFFEINE CITRATE','LEVOCARNITINE',
 'COLISTIMETHATE','POLYMYXIN B','ARGATROBAN','DOXAPRAM','ACETYLCYSTEINE','MITOMYCIN'}

# Complexidade tecnológica (defende margem e justifica licenciar em vez de fazer)
COMPLEX_ALTA={'ICATIBANT','OCTREOTIDE','LIRAGLUTIDE','CALCITONIN','ERIBULIN','THIOTEPA','DANTROLENE',
 'REGADENOSON','MICAFUNGIN','DAPTOMYCIN','FULVESTRANT','VALRUBICIN','CAFFEINE CITRATE'}

# Moléculas fora do escopo Non Retail (canal Retail/especialidade)
FORA_NR={'LIRAGLUTIDE','TESTOSTERONE','ESTRADIOL','SUMATRIPTAN','PROGESTERONE'}

# Não comercializadas / sem uso relevante no Brasil (mercado inexistente)
SEM_MERCADO_BR={'BENZTROPINE','DICYCLOMINE','ENALAPRILAT','CHLOROPROCAINE','METHOCARBAMOL',
 'ORPHENADRINE','PENTOBARBITAL','LORAZEPAM','DOXAPRAM','PROCHLORPERAZINE','DROPERIDOL'}

# Tese comercial por molécula (v2 — com leitura econômica)
TESE={
'ICATIBANT':('ALTA','Angioedema hereditário. Preço por seringa na casa dos milhares de reais e canal de '
  'especialidade/judicialização: é o perfil que melhor absorve custo de importação de acabado. Peptídeo '
  'sintético, com barreira técnica real.'),
'DANTROLENE':('ALTA','Antídoto de hipertermia maligna. Item de arsenal obrigatório em centro cirúrgico, '
  'oligopólio mundial e histórico de desabastecimento. Volume baixo com preço alto — economia que funciona '
  'para importado. Porta de entrada institucional em centro cirúrgico, onde o EMS quer crescer.'),
'REGADENOSON':('ALTA','Estresse farmacológico em cintilografia miocárdica, em seringa preenchida. Nicho '
  'diagnóstico de poucos players, preço alto e uso concentrado em serviços de medicina nuclear — canal '
  'estreito e defensável, oposto da lógica de licitação por menor preço.'),
'DEXRAZOXANE':('MÉDIA-ALTA','Cardioproteção em antraciclinas. Nicho de suporte oncológico, poucos '
  'fornecedores, preço sustenta importação. Sem histórico na base.'),
'FOSCARNET':('MÉDIA-ALTA','Antiviral de resgate para CMV resistente. Mercado pequeno, mas preço alto e '
  'quase sem concorrência. Único registro na base está dormente desde 2019 (Clinigen).'),
'VALRUBICIN':('MÉDIA-ALTA','Quimioterápico intravesical para câncer de bexiga BCG-refratário. Conecta '
  'diretamente com o WarMap de Urologia de set/26. Nicho, preço alto, sem concorrência local.'),
'ERIBULIN':('MÉDIA-ALTA','Oncológico de nicho (mama metastática, lipossarcoma). Preço alto e síntese '
  'complexa. Validar situação patentária antes de qualquer contato.'),
'MICAFUNGIN':('MÉDIA','Equinocandina para candidemia. O preço unitário sustenta importação de acabado.'),
'DAPTOMYCIN':('MÉDIA','Gram-positivos resistentes, aderente à tese de resistência antimicrobiana do deck. '
  'Domínio público com muitos players asiáticos — a Hikma dificilmente ganha de um indiano no preço.'),
'COLISTIMETHATE':('MÉDIA','Resgate para Gram-negativos MDR, aderente à tese de resistência. Preço na '
  'fronteira do viável para importado; decide no volume e no custo logístico.'),
'POLYMYXIN B':('MÉDIA','Mesma tese de colistimetato, com uso brasileiro relevante frente a KPC/NDM. '
  'Uso brasileiro consolidado em terapia intensiva.'),
'ARGATROBAN':('MÉDIA','Anticoagulante para trombocitopenia induzida por heparina. Nicho sem alternativa '
  'direta e apresentação pronta para uso. Preço sustenta importação.'),
'THIOTEPA':('MÉDIA','Condicionamento pré-transplante de medula. Nicho hospitalar de alto valor, '
  'poucos fornecedores.'),
'CLADRIBINE':('MÉDIA','Tricoleucemia. Nicho pequeno mas de preço alto e concorrência mínima.'),
'LEVOTHYROXINE':('MÉDIA','Levotiroxina IV para coma mixedematoso. Escasso no Brasil, preço alto, '
  'volume muito baixo — avaliar se o volume paga o registro.'),
'FULVESTRANT':('BAIXA-MÉDIA','Seringa preenchida e preço bom, mas já genericizado no Brasil. Chegou tarde.'),
'FOSAPREPITANT':('BAIXA-MÉDIA','Antiemético NK1 já genericizado, com preço em queda.'),
'ACETAMINOPHEN + IBUPROFEN':('MÉDIA','COMBOGESIC® IV. O deck cita nominalmente a combinação como '
  'oportunidade opioid-sparing e a Hikma é a detentora do RLD — endosso estratégico raro. PORÉM o preço '
  'de referência é puxado para baixo pelo paracetamol IV: como acabado importado a conta é apertada. '
  'O caminho realista é licenciar o dossiê e fabricar localmente, já que o EMS domina as duas moléculas.'),
'ACETAMINOPHEN':('BAIXA','Paracetamol IV é commodity de preço baixo em licitação hospitalar. Mesmo com '
  'a bolsa RLD como diferencial, a margem por unidade não absorve frete, imposto e estoque de importado. '
  'Fora do escopo de licenciamento de acabado.'),
'VANCOMYCIN':('BAIXA-MÉDIA','A bolsa pronta para uso é um diferencial real de segurança e tempo de '
  'enfermagem, e existe CDA vigente com a Hikma. Mas vancomicina é commodity: o prêmio de RTU precisa ser '
  'aceito pelo comprador hospitalar, e bolsa premix tem exigência de estabilidade/cadeia fria que encarece '
  'a importação. Vale seguir pelo CDA já aberto, com teste de preço antes de qualquer investimento.'),
'CLINDAMYCIN':('BAIXA','Premix em dextrose é bom conceito, mas clindamicina é commodity de licitação. '
  'Como acabado importado não fecha; faria sentido apenas como transferência de tecnologia.'),
'DEXMEDETOMIDINE':('MÉDIA','Bolsa pronta para uso em NaCl. O EMS já tem projeto interno em Gate, então '
  'aqui o licenciamento compra TEMPO: entra com importado agora e migra para produção própria depois. '
  'Preço na faixa que aguenta importação no curto prazo.'),
'LINEZOLID':('BAIXA-MÉDIA','Bolsa IV completa a linha (o EMS tem o sólido oral), mas a IV já é '
  'genericizada e disputada por preço.'),
'ERTAPENEM':('BAIXA-MÉDIA','Nicho de OPAT distinto do meropenem, mas os genéricos já pressionam o preço.'),
'MILRINONE':('BAIXA','Premix em dextrose; preço não sustenta importado.'),
'NICARDIPINE':('BAIXA','Premix em NaCl; mercado brasileiro pequeno e preço baixo.'),
'SODIUM FERRIC GLUCONATE COMPLEX':('BAIXA','A carboximaltose férrica é superior e já está no radar do Grupo — cai na regra "já temos molécula melhor".'),
'LIRAGLUTIDE':('BAIXA','Alto valor, mas é arena Retail e altamente disputada — fora do escopo Non Retail.'),
'CAFFEINE CITRATE':('BAIXA-MÉDIA','Apneia da prematuridade. Nicho neonatal defensável, mas volume pequeno.'),
'LEVOCARNITINE':('BAIXA','Nicho metabólico pequeno; preço não justifica importação.'),
'OCTREOTIDE':('BAIXA','Preço bom, mas o mercado é dominado pela formulação LAR, que a Hikma não oferece.'),
}
