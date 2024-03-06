import spacy
from spacy.matcher import DependencyMatcher
import pdfplumber

def obtener_texto(ubicacionPDF):
    # Crear el PDF a leer
    pdf = pdfplumber.open(ubicacionPDF)

    # Texto
    texto = ""

    # Pagina a pagina formar el texto completo
    for page in pdf.pages:
        texto += page.extract_text()

    #closing the pdf file
    pdf.close()

    return texto

def buscar_patron(texto, patron, nombreMarcher): 
    # Cargar el modelo para español
    nlp = spacy.load("es_core_news_sm") 

    # Crear el matcher
    matcher = DependencyMatcher(nlp.vocab)

    # Agregar el patrón al matcher
    matcher.add(nombreMarcher,[patron])

    # Procesar el texto con spaCy
    doc = nlp(texto)

    # Encontrar coincidencias con el matcher
    coincidencias = matcher(doc)

    # Imprimir Vector generado por el matcher
    for match_id, token_ids in coincidencias:
        palabra = []
        for token_id in sorted(token_ids):
            token = doc[token_id]
            palabra.append(token.text)
        print(nlp.vocab.strings[match_id], ' '.join(palabra))


# Ejemplo Contencioso Administrativo Federal
"""
nombreMarcher = "JUZGADO:"

texto = obtener_texto("C:\\Users\\juani\\Desktop\\Proyecto\\Documentos\\CAF 000466_2015_1_RH001 Copy.pdf")

# Definir el patrón
patron=[{ 
    "RIGHT_ID": "Juzgado_id",
    "RIGHT_ATTRS": {"LOWER": "juzgado"}
    },
    {'LEFT_ID': 'Juzgado_id', 
    'REL_OP': '>', 
    'RIGHT_ID': 'Contensioso_id', 
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

"""

# Ejemplo Witch Doctor
"""
nombreMarcher = "Witch Doctor:"

texto = "In all of its televised BattleBots appearances, Witch Doctor featured a
potent vertical spinning disc which has been capable of causing major
damage to opponents. It often featured small front wedges which could be
replaced with a large steel plow to combat spinners. It was also
accompanied by a 30lb minibot named Shaman in early seasons of the
show. Shaman was a wedge robot designed to get behind the opponent
and distract their drivers so Witch Doctor could go in for the kill. Shaman
was not unarmed, as it was also equipped with a flamethrower to toast the
underside of opponents it can get underneath."

# Definir el patrón
patron=[{ 
    "RIGHT_ID": "Juzgado_id",
    "RIGHT_ATTRS": {"LOWER": "juzgado"}
    },
    {'LEFT_ID': 'Juzgado_id', 
    'REL_OP': '>', 
    'RIGHT_ID': 'Contensioso_id', 
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

"""

# Ejemplo JUEZ
"""
nombreMarcher = "Sr Juez:"

texto = "Que el juez a cargo del Juzgado Federal de Oberá declaró procedente la
extradición de César Elías Fucks a la República Federativa del Brasil para
someterlo a proceso por el delito de robo seguido de muerte."

# Definir el patrón
patron=[{ 
    "RIGHT_ID": "Juzgado_id",
    "RIGHT_ATTRS": {"LOWER": "juzgado"}
    },
    {'LEFT_ID': 'Juzgado_id', 
    'REL_OP': '>', 
    'RIGHT_ID': 'Contensioso_id', 
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

"""

# Ejemplo Microsoft
nombreMarcher = "ACQUIRED:"

texto = "Open IA, the company that created ChatGPT, was recently acquired by Microsoft."

# Definir el patrón
patron=[
    {"RIGHT_ID": 'Acquiered_id',
    "RIGHT_ATTRS": {'LOWER': 'acquired'}},
    {'LEFT_ID': 'Acquiered_id', 
    'REL_OP': '.', 
    'RIGHT_ID': 'By_id', 
    'RIGHT_ATTRS': {'DEP': 'nsubj'}},
    {'LEFT_ID': 'By_id', 
    'REL_OP': '>', 
    'RIGHT_ID': 'agent_id', 
    'RIGHT_ATTRS': {'DEP': 'flat'}}
    ]
    
buscar_patron(texto, patron, nombreMarcher)