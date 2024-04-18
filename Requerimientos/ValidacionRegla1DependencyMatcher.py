#!/usr/bin/python
# -*- coding: utf-8 -*-
import spacy
from spacy.matcher import DependencyMatcher
from spacy import displacy

# Cargar el modelo para español
nlp = spacy.load("es_core_news_sm")

# Verificar si un verbo es negativo si arranca en algun prefijo negativo
def verificarNegativismo1(verbo):
    prefijos_negativos = ["in", "im", "des", "a", "anti", "dis"]
    for prefijo in prefijos_negativos:
        if verbo.startswith(prefijo):
            return True
    return False

# Verificar si un verbo es negativo si arranca en algun prefijo negativo
def verificarNegativismo2(oracion):    
    adverbio_negativo = ["no", "nunca", "jamas", "nada", "ni", "tampoco"]
    oracion = oracion.lower()
    for prefijo in adverbio_negativo:
        if prefijo in oracion.split():
            return True
    return False


# buscar patrón pasado por parametro en el documento "doc" y agregar correspondiente si es negativa o positiva al vector
def buscarPatron (patron, doc, oracion_positiva, oracion_negativa, negativa2):
    # Crear el matcher
    matcher = DependencyMatcher(nlp.vocab)

    # Agregar el patrón al matcher
    matcher.add("PATRON:",[patron])

    # Encontrar coincidencias con el matcher
    coincidencias = matcher(doc)

    # Imprimir Vector creado por el matcher
    for match_id, token_ids in coincidencias:
        palabra = []
        negativa1 = False

        for token_id in sorted(token_ids):
            token = doc[token_id]

            if ((token.dep_ == "ROOT") and (token.pos_ in {"VERB", "PROPN", "NOUN"})):
                if verificarNegativismo1(token.text):
                    negativa1 = True
            palabra.append(token.text)
        
        # Convertir lista de palabras en oración y añadir a la lista de oraciones
        oracion = ' '.join(palabra)
       
       # XOR
        if (negativa1 or negativa2) and not(negativa1 and negativa2):
            oracion_negativa.append(oracion)
        else:
            oracion_positiva.append(oracion)

    return oracion_positiva, oracion_negativa


# Definir patrones     
def definirPatron():

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

    return [verboRaiz, sujeto, objeto]


def separarOraciones(texto):
    # Reemplazar todos los puntos, las comas y las "y" por puntos y comas para tener un único delimitador
    texto_unificado = texto.replace('.', ';').replace(',', ';').replace(' y ', ' ; ')

    # Dividir el texto en oraciones usando punto y coma como delimitador
    oraciones_brutas = texto_unificado.split(';')

    # Limpiar espacios en blanco alrededor de las oraciones y eliminar cualquier oración vacía
    oraciones = [oracion.strip() for oracion in oraciones_brutas if oracion.strip()]

    return oraciones


          
# Texto de ejemplo
texto = """Las cobardes rompen el silencio, Los amigos nunca incumplen las promesas y la familia nunca te deja morir"""

doc = nlp(texto)

oraciones = separarOraciones(texto)

# Lista para guardar oraciones que cumplen el patrón
oraciones_positivas = []
oraciones_negativas = []

for oracion in oraciones:
    # Procesar el texto con spaCy
    doc = nlp(oracion)

    oraciones_positivas, oraciones_negativas = buscarPatron(definirPatron(), doc, oraciones_positivas, oraciones_negativas, verificarNegativismo2(oracion))

print("Positivas: ", oraciones_positivas, ", Negativas: ", oraciones_negativas)