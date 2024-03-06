import PyPDF2
import spacy
from spacy.matcher import DependencyMatcher

def extraerPalabritas(coincidencias,doc):
    palabra= ""
    for _ , token_ids in coincidencias:
        for token_id in token_ids:
            token = doc[token_id]
            palabra = palabra + token.text + " "
    return palabra

# Crear el PDF a leer
pdf = open("C:\\Users\\juani\\Desktop\\Proyecto\\Documentos\\CAF 000466_2015_1_RH001 Copy.pdf","rb")

# Crear el lector de PDF
pdf_reader = PyPDF2.PdfReader(pdf)

# Texto
texto = ""

# Pagina a pagina formar el texto completo
for page in pdf_reader.pages:
    texto += page.extract_text()

#con encode y decode solucionan el problema de las palabras divididas por espacios
texto.encode('utf-8').decode('utf-8')

#closing the pdf file
pdf.close()

print(texto)

nlp = spacy.load("es_core_news_sm")
matcher = DependencyMatcher(nlp.vocab)
# Define los nodos de anclaje
matcher.add("Materia", [
        [
            {'RIGHT_ID': 'Juzgado ', 'RIGHT_ATTRS':  {"lower": "juzgado"}},
            {'LEFT_ID': 'Juzgado ', 'REL_OP': '>', 'RIGHT_ID': 'contensioso', 'RIGHT_ATTRS':  {"DEP": "nmod"}},
            {'LEFT_ID': 'contensioso', 'REL_OP': '.', 'RIGHT_ID': 'resto', 'RIGHT_ATTRS':  {"DEP": "flat"}},     
        ]
])

# Procesar el texto con spaCy
doc = nlp(texto)

# Encontrar coincidencias con el matcher
coincidencias = matcher(doc)

matcheado = extraerPalabritas(coincidencias,doc)
print(matcheado)
#displacy.serve(doc)