#Subir el resultado a la web y hacer esquema.
import spacy
from spacy import displacy

# Cargar el modelo de spaCy para español
nlp_es = spacy.load("es_core_news_sm")

# Texto traducido al español
texto_espanol = "Open IA, the company that created ChatGPT, was recently acquired by Microsoft."

# Procesar el texto en español con spaCy
doc_espanol = nlp_es(texto_espanol)

displacy.serve(doc_espanol)
