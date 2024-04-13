#!/usr/bin/python
# -*- coding: utf-8 -*-
import spacy
from spacy.matcher import Matcher
from spacy import displacy

#Cargar el modelo de spaCy para inglés
nlp = spacy.load("es_core_news_sm")


def validacionReglaUno(text):
    # Crear el matcher
    matcher = Matcher(nlp.vocab)

    # Definir los patrones
    # Usar el IN si se quiere buscar por mas de 2 valores
    patron_1 = [{"DEP":{"IN": ["nsubj", "det"]},"OP": "?"},{"POS": {"IN": ["PROPN", "NOUN", "VERB"]}, "DEP": "ROOT"}]
    patron_2 = [{"POS": {"IN": ["PROPN", "NOUN", "VERB"]}, "DEP": "ROOT"},{"DEP":{"IN": ["obl", "obj"]}, "OP": "?"}]

    # Añadir el patrón al matcher
    matcher.add("RAIZ", [patron_2])

    # Encontrar coincidencias con el matcher
    coincidencias = matcher(doc)
    
    # Imprimir los resultados
    print("Coincidencias encontradas:", len(coincidencias))
    for match_id, start, end in coincidencias:
        # Obtener el string name del ID de la coincidencia
        string_id = nlp.vocab.strings[match_id]
        # Obtener el span del texto que coincide
        span = doc[start:end]
        # Imprimir el texto de la coincidencia
        print(f"{string_id}: {start}-{end}: {span.text}")


# Texto de ejemplo
texto = """El cliente extrae dinero para su cuenta. """
#texto = """Juan después de desayunar, salió de su casa"""

# Procesar el texto con spaCy
doc = nlp(texto)


#validacionReglaUno(doc)

displacy.serve(doc)

