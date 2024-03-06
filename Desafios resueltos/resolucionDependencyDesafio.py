import spacy
from spacy.matcher import DependencyMatcher

def buscarPatron (texto, patron):
    # Cargar el modelo para español
    nlp = spacy.load("es_core_news_sm")

    # Crear el matcher
    matcher = DependencyMatcher(nlp.vocab)

    # Agregar el patrón al matcher
    matcher.add("JUZGADO:",[patron])

    # Procesar el texto con spaCy
    doc = nlp(texto)

    # Encontrar coincidencias con el matcher
    coincidencias = matcher(doc)

    # Imprimir Vector creado por el matcher
    for match_id, token_ids in coincidencias:
        palabra = []
        for token_id in sorted(token_ids):
            token = doc[token_id]
            palabra.append(token.text)
        print(nlp.vocab.strings[match_id], ' '.join(palabra))


# Definir el patrón
patron=[{'RIGHT_ID': 'Contensioso_id', 
'RIGHT_ATTRS': {'DEP': 'nmod'}},
{'LEFT_ID': 'Contensioso_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Adiministrativo_id', 
'RIGHT_ATTRS': {'DEP': 'flat'}},
{'LEFT_ID': 'Adiministrativo_id', 
'REL_OP': '.', 
'RIGHT_ID': 'Federal_id', 
'RIGHT_ATTRS': {'DEP': 'flat'}}
]

# Texto de ejemplo
texto = """Tribunal que intervino con anterioridad: Juzgado Nacional de Primera Instancia
en lo Contencioso Administrativo Federal n° 4. """

buscarPatron(texto, patron)