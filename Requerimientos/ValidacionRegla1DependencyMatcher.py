#!/usr/bin/python
# -*- coding: utf-8 -*-
import spacy
from spacy.matcher import DependencyMatcher
from spacy import displacy


def buscarPatron (patron, doc):
    # Crear el matcher
    matcher = DependencyMatcher(nlp.vocab)

    # Agregar el patrón al matcher
    matcher.add("CLIENTE:",[patron])

    # Encontrar coincidencias con el matcher
    coincidencias = matcher(doc)

    # Lista para guardar oraciones que cumplen el patrón
    oraciones_cumplen_patron = []

    # Imprimir Vector creado por el matcher
    for match_id, token_ids in coincidencias:
        palabra = []
        for token_id in sorted(token_ids):
            token = doc[token_id]
            palabra.append(token.text)
        
        # Convertir lista de palabras en oración y añadir a la lista de oraciones
        oracion = ' '.join(palabra)
        oraciones_cumplen_patron.append(oracion)
        print(nlp.vocab.strings[match_id], oracion)

    return oraciones_cumplen_patron
        


# Definir patrones
verboRaiz = {'RIGHT_ID': 'Verbo_id', 
'RIGHT_ATTRS': {"POS": {"IN": ["PROPN", "NOUN", "VERB"]}, "DEP": "ROOT"}}

sujeto = {'LEFT_ID': 'Verbo_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Sujeto_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["nsubj", "det"]}}}

objeto = {'LEFT_ID': 'Verbo_id', 
'REL_OP': '>', 
'RIGHT_ID': 'Objeto1_id', 
'RIGHT_ATTRS': {"DEP":{"IN": ["obl","iobj", "obj"]}}}

patron=[verboRaiz, sujeto, objeto]

# Texto de ejemplo
texto = """Los clientes cumplen con el pago. Las personas Caminan en el centro"""
#texto = """Juan después de desayunar, salió de su casa"""

# Cargar el modelo para español
nlp = spacy.load("es_core_news_sm")

# Procesar el texto con spaCy
doc = nlp(texto)

oraciones_encontradas = buscarPatron(patron, doc)
print(oraciones_encontradas)

# Visualizar arbol gramatical con displaCy (descomentar si se desea usar)
#displacy.serve(doc)