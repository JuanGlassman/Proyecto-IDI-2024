#!/usr/bin/python
# -*- coding: utf-8 -*-
import spacy
from spacy.matcher import DependencyMatcher
from spacy import displacy

# Cargar el modelo para español
nlp = spacy.load("es_core_news_lg")

# Verificar si un verbo es negativo si arranca en algun prefijo negativo
def is_negative_verb(verb):
    negative_pref = ["in", "im", "des", "anti", "dis"]
    return any(verb.startswith(pref) for pref in negative_pref)

# Verificar si un verbo es negativo si arranca en algun prefijo negativo
def has_negative_adv(sentence):    
    negative_adv = ["no", "nunca", "jamás", "nada", "ni", "tampoco"]
    sentences = split_sentences(sentence)
    # Verificar negación en la primer oración: Ej: El gato no ama la comida, debe ser porque no es de pescado. 
    words = sentences[0].lower().split()
    return any(adv in words for adv in negative_adv)


# Definir patrones     
def define_pattern():
    root_verb = {'RIGHT_ID': 'Verbo_id', 
    'RIGHT_ATTRS': {"POS": {"IN": ["PROPN", "NOUN", "VERB"]}, "DEP": "ROOT"}}

    subject = {'LEFT_ID': 'Verbo_id', 
    'REL_OP': '>', 
    'RIGHT_ID': 'Sujeto_id', 
    'RIGHT_ATTRS': {"DEP":{"IN": ["nsubj", "det"]}}}

    object = {'LEFT_ID': 'Verbo_id', 
    'REL_OP': '>', 
    'RIGHT_ID': 'Objeto1_id', 
    'RIGHT_ATTRS': {"DEP":{"IN": ["obl","iobj", "obj"]}}}

    return [root_verb, subject, object]


# Separar oraciones
def split_sentences(text):
    # Lista de delimitadores para reemplazar por punto y coma
    delimiters = ['.', ',', ' y ', ' e ', ' o ']

    # Reemplazar todos los delimitadores por punto y coma usando un bucle for
    for delimiter in delimiters:
        text = text.replace(delimiter, ';')

    # Limpiar espacios en blanco alrededor de las oraciones y eliminar cualquier oración vacía
    sentences = [sentence.strip() for sentence in text.split(';') if sentence.strip()]

    return sentences

# Buscar patrón en text con el matcher que se pasa por parametro con el patron cargado 
def find_pattern (matcher, text):
    doc = nlp(text)
    matches = matcher(doc)
    results = []

    for match_id, token_ids in matches:
        # Formar nuevamente la oración para retornarla y para verificar "has negative adverb"
        sentence_text = doc[token_ids[0]].sent.text
        
        is_negative_adv = has_negative_adv(sentence_text)
        is_negative = False

        for token_id in token_ids:
                token = doc[token_id]
                if ((token.dep_ == "ROOT") and (token.pos_ in {"VERB", "PROPN", "NOUN"})):
                    is_negative = is_negative_verb(token.lemma_)

        #XOR
        is_negative = ((is_negative or is_negative_adv) and not(is_negative and is_negative_adv))
            
        results.append((sentence_text, is_negative))

    return results



matcher = DependencyMatcher(nlp.vocab)
matcher.add("PATRON: ",[define_pattern()])

text = """La gazela vuela por la laguna como nunca""" #PROBLEMA con el "como nunca"

#sentences = split_sentences(text)

positive_sentence = []
negative_sentence = []

indices = find_pattern(matcher, text)

for text, is_negative in indices:   
    if (is_negative):
        negative_sentence.append(text)
    else:
        positive_sentence.append(text)

print("Positivas: ", positive_sentence, ", Negativas: ", negative_sentence)
