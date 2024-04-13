# Definir VARIABLES de patrones
VerboRaiz = {'RIGHT_ID': 'Verbo_id', 
'RIGHT_ATTRS': {"POS": {"IN": ["PROPN", "NOUN", "VERB"]}, "DEP": "ROOT"}}

sujeto = {'LEFT_ID': 'Verbo_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Sujeto_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["nsubj", "det"]}}}

objeto = {'LEFT_ID': 'Verbo_id', 
'REL_OP': '.', 
'RIGHT_ID': 'Objeto1_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["obl","iobj", "obj"]}}}

#Patron "cliente extrae para/ mediante/ por su cuenta"
patronDe=[VerboRaiz, sujeto, objeto,

{'LEFT_ID': 'Objeto1_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Objeto2_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["nmod"]}}},

{'LEFT_ID': 'Objeto2_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion1_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["det"]}}},

{'LEFT_ID': 'Objeto2_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion2_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["case"]}, "POS": "ADP"}}]

#Patron "cliente extrae para/ mediante su cuenta"
patronParaSinDinero=[VerboRaiz, sujeto, objeto, 

{'LEFT_ID': 'Objeto1_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion1_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["det"]}}},

{'LEFT_ID': 'Objeto1_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion2_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["case"]}, "POS": "ADP"}}]
                    

#Patron "cliente extrae dinero para/ mediante su cuenta"
patronPara=[VerboRaiz, sujeto, objeto,

{'LEFT_ID': 'Verbo_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Modificador_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["obl"]}}},

{'LEFT_ID': 'Modificador_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion1_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["det"]}}},

{'LEFT_ID': 'Modificador_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion2_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["case"]}, "POS": "ADP"}}
]

patronATravesDe=[VerboRaiz, sujeto, objeto, 

{'LEFT_ID': 'Verbo_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Modificador_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["obl"]}}},

{'LEFT_ID': 'Modificador_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion1_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["det"]}}},

{'LEFT_ID': 'Modificador_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Preposicion2_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["case"]}, "POS": "ADP"}},
{'LEFT_ID': 'Preposicion2_id', 
'REL_OP': '>', 
'RIGHT_ID': 'atraves1_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["fixed"]}, "POS": "NOUN"}},
{'LEFT_ID': 'Preposicion2_id', 
'REL_OP': '>', 
'RIGHT_ID': 'atraves2_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["fixed"]}, "POS": "ADP"}},

]