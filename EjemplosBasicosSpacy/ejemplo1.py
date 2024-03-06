#Elementos básicos de un programa en spacy
import spacy

# Cargar el modelo para español
nlp = spacy.load("es_core_news_sm")

# Texto de ejemplo
texto = "Open IA, the company that created ChatGPT, was recently acquired by Microsoft"

# Procesar el texto con spaCy
doc = nlp(texto)

# Imprimir el POS tagging de cada palabra
for token in doc:
    print(f"{token.text}: {token.dep_}")
