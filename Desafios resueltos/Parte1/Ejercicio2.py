import spacy
from spacy.matcher import Matcher

# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")

# Crear el matcher
matcher = Matcher(nlp.vocab)

# Definir el patrón
patron_fecha = [{"shape": "dd/dd/dddd"}] 

# Añadir el patrón al matcher
matcher.add("Fecha_Pattern", [patron_fecha])

# Texto de ejemplo
texto = "El presidente de la compañía XYZ, Juan Pérez, anunció hoy en una conferencia de prensa el día 22/05/2034 que la empresa ha alcanzado un acuerdo para adquirir a su competidor principal, Google. La transacción está valuada en 1.5 mil millones de dólares y se espera que se complete a finales de este año. "

# Procesar el texto con spaCy
doc = nlp(texto)

# Encontrar coincidencias con el matcher
coincidencias = matcher(doc)

# Imprimir los resultados
for match_id, start, end in coincidencias:
    print(f"Caso encontrado: {doc[start:end].text}")