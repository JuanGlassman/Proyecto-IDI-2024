from flask import Flask, request, jsonify, send_from_directory
from sentence_transformers import SentenceTransformer, util
from spacy.matcher import DependencyMatcher
import spacy

app = Flask(__name__, static_folder='static')


# Cargar el modelo de lenguaje es_core_news_lg de spaCy
nlp = spacy.load("es_core_news_lg")

# Cargar un modelo de Sentence Transformers
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/compare', methods=['POST'])
def compare_texts():
    text1 = request.form['text1'].lower()
    text2 = request.form['text2'].lower()

    # Procesamiento de texto con spaCy para análisis léxico
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    
    def normalize_text(doc):
        reconstructed_text = []
        previous_subject = None

        for sent in doc.sents:
            tokens = [token for token in sent]
            new_sentence = []
            subject_found = False

            for token in tokens:
                if token.dep_ == 'nsubj':
                    subject_found = True
                    if token.pos_ == 'PRON' and previous_subject and token.text in ['él', 'ella', 'ellos', 'ellas']:
                        new_sentence.append(previous_subject)  # Reemplazar pronombre con sujeto anterior
                    else:
                        new_sentence.append(token.text)
                        previous_subject = token.text  # Actualizar el último subject conocido solo si no es un pronombre

                else:
                    new_sentence.append(token.text)

            # Anteponer el sujeto anterior si no se encontró ningún sujeto en esta oración.
            if not subject_found and previous_subject:
                reconstructed_text.append(previous_subject + " " + " ".join(new_sentence))
            else:
                reconstructed_text.append(" ".join(new_sentence))

        return " ".join(reconstructed_text)

    reconstructed_text1 = normalize_text(doc1)
    reconstructed_text2 = normalize_text(doc2)

    print("---------Textos reconstruidos---------")
    print(reconstructed_text1)
    print(reconstructed_text2)
    
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
        
        # Verificar si un verbo es negativo si arranca en algun prefijo negativo
    def is_negative_verb(verb):
        negative_pref = ["in", "im", "des", "anti", "dis"]
        return any(verb.startswith(pref) for pref in negative_pref)

    # Verificar si un verbo es negativo si arranca en algun prefijo negativo
    def has_negative_adv(sentence):    
        negative_adv = ["no", "nunca", "jamás", "nada", "ni", "tampoco"]
        words = sentence.lower().split()
        return any(adv in words for adv in negative_adv)


    # buscar patrón pasado por parametro en el documento "doc" y agregar correspondiente si es negativa o positiva al vector
    def find_pattern (pattern, doc):
        # Crear el matcher
        matcher = DependencyMatcher(nlp.vocab)

        # Agregar el patrón al matcher
        matcher.add("PATRON: ",[pattern])

        # Encontrar coincidencias con el matcher
        matches = matcher(doc)

        is_1 = False

        for match_id, token_ids in matches:
            word = []
            is_negative = False

            for token_id in sorted(token_ids):
                token = doc[token_id]
                if ((token.dep_ == "ROOT") and (token.pos_ in {"VERB", "PROPN", "NOUN"})):
                    if is_negative_verb(token.lemma_):
                        is_negative = True
                word.append(token.text)
            
            # Convertir lista de palabras en oración y añadir a la lista de oraciones
            sentence = ' '.join(word)
        
            is_negative2 = has_negative_adv(sentence)

            is_1= (is_negative or is_negative2) and not(is_negative and is_negative2)

        return is_1

    

    sentences1 = split_sentences(reconstructed_text1)
    sentences2 = split_sentences(reconstructed_text2)
    
    pattern = define_pattern()
    positive_sentence = []
    negative_sentence = []


    for sentence1 in sentences1:
    # Procesar el texto con spaCy
        doc1 = nlp(sentence1)
        character1 = find_pattern(pattern, doc1)
        if (character1):
            positive_sentence.append(sentence1)
        else:
            negative_sentence.append(sentence1)
        
    for sentence2 in sentences2:
    # Procesar el texto con spaCy
        doc2 = nlp(sentence2)
        character2 = find_pattern(pattern, doc2)
        if (character2):
            positive_sentence.append(sentence2)
        else:
            negative_sentence.append(sentence2)
    
    print("Positivas: ", positive_sentence, ", Negativas: ", negative_sentence)
    
    # Calcular similaridad con  Sentence Transformers (vectores)
    embeddings = model.encode([reconstructed_text1, reconstructed_text2])
    structural_similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

    # Comparar pañabras e intersecciones
    important_words1 = {token.lemma_ for token in doc1 if not token.is_stop and not token.is_punct}
    important_words2 = {token.lemma_ for token in doc2 if not token.is_stop and not token.is_punct}
    word_similarity = len(important_words1.intersection(important_words2)) / max(len(important_words1), len(important_words2))

    # Negaciones 
    negation_words = {"no", "nunca", "tampoco", "ninguna", "jamás"}
    negations_text1 = [token for token in doc1 if token.lemma_ in negation_words]
    negations_text2 = [token for token in doc2 if token.lemma_ in negation_words]
    negation_impact = 0.5 if negations_text1 or negations_text2 else 1.0

    adjusted_similarity = ((structural_similarity * negation_impact) + word_similarity) / 2

    # Detalles de diferencias
    details_difference = important_words1.symmetric_difference(important_words2)
    
    result = {
        "similarity": adjusted_similarity,
        "structural_similarity": structural_similarity,
        "word_similarity": word_similarity,
        "details_difference": list(details_difference),
        "negations_text1": [neg.text for neg in negations_text1],
        "negations_text2": [neg.text for neg in negations_text2]
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
