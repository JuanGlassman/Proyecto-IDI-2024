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
    patron_1 = [{"DEP": "nsubj"}]
    # Usar el IN si se quiere buscar por mas de 2 valores
    patron_2 = [{"POS": {"IN": ["PROPN", "NOUN", "VERB"]}, "DEP": "ROOT"}]
    patron_3 = [{"POS": "AUX", "DEP": "cop"}]
    patron_4 = [{"POS": "VERB", "DEP": "ROOT"}]
    patron_5 = [{"POS": "NOUN"},{"POS": "ADJ"}, {"DEP": "obj"}, {"DEP": "ROOT"}]


    # Añadir el patrón al matcher
    #matcher.add("Subjeto", [patron_1])
    matcher.add("Sustantivo", [patron_2])
    #matcher.add("Auxiliar", [patron_3])
    #matcher.add("Verbo", [patron_4])
    #matcher.add("Mix", [patron_5])

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
texto = """El cliente extraer dinero de su cuenta. """

# Procesar el texto con spaCy
doc = nlp(texto)

displacy.serve(doc, style="dep")

validacionReglaUno(doc)
