#!/usr/bin/python
# -*- coding: utf-8 -*-
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("es_core_news_sm")


#@hug.startup()
def init_settings(api):
    api.http.falcon.req_options.auto_parse_qs_csv = False

def validacionReglaUno(text):
    sujeto = False
    verbo = False
    objeto = False
    doc = nlp(text)
    for token in doc:
        if token.dep_ == "nsubj":
            sujeto = True
        if token.pos_ == "NOUN" and token.dep_ == "ROOT" and verbo == False:
            sujeto = True
        if token.pos_ == "AUX" and token.dep_ == "cop" and sujeto:
            verbo = True
        if token.pos_ == "VERB" and token.dep_ == "ROOT" and sujeto:
            verbo = True
        if verbo and (token.pos_ == "NOUN"
                      or token.pos_ == "ADJ") and (token.dep_ == "obj"
                                                   or token.dep_ == "ROOT"):
            objeto = True
        print(token.text, token.pos_, token.dep_)
    return (sujeto & verbo & objeto)

def validacionReglaUnoBeta(text, nlp):
    matcher = Matcher(nlp.vocab)
    
    pattern_sujeto = [{'DEP': 'nsubj', 'IS_STOP': False}]
    
    pattern_verbo = [{'POS': 'VERB', 'DEP': {'IN': ['ROOT', 'aux', 'cop']}, 'IS_STOP': False}]
    
    pattern_objeto = [{'POS': {'IN': ['NOUN', 'ADJ']}, 'DEP': {'IN': ['dobj', 'attr', 'oprd']}, 'IS_STOP': False}]
    
    # Agrego los patrones al Matcher
    matcher.add('SUJETO', [pattern_sujeto])
    matcher.add('VERBO', [pattern_verbo])
    matcher.add('OBJETO', [pattern_objeto])

    doc = nlp(text)

    matches = matcher(doc)
    # Diccionario para almacenar si cada componente ha sido encontrado
    componentes = {'SUJETO': False, 'VERBO': False, 'OBJETO': False}
    
    for match_id, start, end in matches:
        # Obtén el string name del patrón que coincidió
        string_id = nlp.vocab.strings[match_id]
        componentes[string_id] = True

    for token in doc:
        print(token.text, token.pos_, token.dep_)

    # Retorna True solo si todos los componentes han sido encontrados
    return all(componentes.values())

def deteccionPalabrasDuplicadas(text, nlp):
    doc = nlp(text)

    sujeto = False
    verbo = False
    objeto = False
    palabras_repetidas = False
    repeticiones = []

    for i, token in enumerate(doc[:-1]): 
        if token.lower_ == doc[i + 1].lower_:
            palabras_repetidas = True
            repeticiones.append(token.text)
            
        if token.dep_ == "nsubj":
            sujeto = True
        if (token.pos_ == "VERB" and token.dep_ == "ROOT") and not verbo:
            verbo = True
        if verbo and (token.pos_ == "NOUN" or token.pos_ == "ADJ") and (token.dep_ == "obj" or token.dep_ == "ROOT"):
            objeto = True

    print(f"Palabras repetidas: {repeticiones}") if palabras_repetidas else print("No se encontraron palabras repetidas.")
    
    for token in doc:
        print(token.text, token.pos_, token.dep_)

    # Retorna True si se encuentran sujeto, verbo, objeto y no hay repeticiones
    return sujeto and verbo and objeto and not palabras_repetidas

def deteccionyEliminacionPalabrasDuplicadas(text, nlp):
    doc = nlp(text)
    sujeto = False
    verbo = False
    objeto = False
    
    repeticiones = []
    texto_limpio = []
    ultima_palabra = ''

    for token in doc:
        if token.lower_ == ultima_palabra:
            repeticiones.append(token.text)
            continue 
        
        # Agregar la palabra actual al texto limpio y actualizar ultima_palabra
        texto_limpio.append(token.text_with_ws)
        ultima_palabra = token.lower_
        
        if token.dep_ == "nsubj":
            sujeto = True
        if (token.pos_ == "VERB" and token.dep_ == "ROOT") and not verbo:
            verbo = True
        if verbo and (token.pos_ == "NOUN" or token.pos_ == "ADJ") and (token.dep_ == "obj" or token.dep_ == "ROOT"):
            objeto = True

    texto_limpio_final = ''.join(texto_limpio)
    
    for token in nlp(texto_limpio_final):
        print(token.text, token.pos_, token.dep_)

    if repeticiones:
        print(f"Se encontraron y eliminaron repeticiones: {' '.join(repeticiones)}")
    else:
        print("No se encontraron repeticiones.")
    
    print(f"Texto limpio: {texto_limpio_final}")
    
    return sujeto and verbo and objeto, texto_limpio_final

# def validacionReglaDos(text):
#     pronombre = True
#     sujeto = False
#     palabrasReservadas = ["que", "quien", "cuyo", "quienes", "cuyos"]
#     nlp = spacy.load("es_core_news_sm")
#     doc = nlp(text)
#     for token in doc:
#         if token.pos_ == "PRON" and token.text not in palabrasReservadas:
#             pronombre = False
#         if token.dep_ == "nsubj":
#             sujeto = True
#         print(token.text, token.pos_, token.dep_)
#     return (pronombre & sujeto)
#     # for ent in doc.ents:    
#     #     print(ent.text, ent.label_)

# def validacionReglaTres(text):
#     tamaño = True
#     conjuncciones = True
#     palabrasReservadas = {"que":0, "quien":0,"cuyo":0,"cuya":0,"cuyas":0,"quienes":0,"cuyos":0,",":0,".":0,"y":0,"o":0,"cual":0,
#     "cuales":0}
#     nlp = spacy.load("es_core_news_sm")
#     doc = nlp(text)
#     for token in doc:
#         if token.text in palabrasReservadas:
#              palabrasReservadas[token.text]=palabrasReservadas[token.text] +1
#         print(token.text, token.pos_, token.dep_)
#     if len(text) > 200:
#         tamaño = False
#     total = sum(palabrasReservadas.values())
#     if total > 10:
#        conjuncciones = False
#     return (tamaño & conjuncciones)



texto = """El cliente extrae dinero de su su su de cuenta"""
doc = nlp(texto)

print("---------------Validación regla uno beta----------------")
validacionReglaUnoBeta(doc, nlp)
print("---------------Validación duplicidad----------------")
print(deteccionPalabrasDuplicadas(texto, nlp))
print("---------------Validación duplicidad y eliminación----------------")

validacion, texto_procesado = deteccionyEliminacionPalabrasDuplicadas(texto, nlp)
print(f"Validación de la oración: {validacion}")
print(f"Texto procesado: {texto_procesado}")