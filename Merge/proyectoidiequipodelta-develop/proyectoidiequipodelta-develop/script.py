import os
import uuid
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from sentence_transformers import SentenceTransformer, util
import spacy
from fpdf import FPDF
import json

app = Flask(__name__, static_folder='static')

# Cargar el modelo de lenguaje es_core_news_lg de spaCy
nlp = spacy.load("es_core_news_lg")

# Carga del JSON con sinónimos
with open('adjetivos.json', 'r', encoding='utf-8') as f:
    grupos_adjetivos = json.load(f)

# Cargar un modelo de Sentence Transformers
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/compare', methods=['POST'])
def compare_texts():
    text1 = request.form['text1'].lower()
    text2 = request.form['text2'].lower()

    doc1 = nlp(text1)
    doc2 = nlp(text2)

    reconstructed_text1 = normalize_text(doc1)
    reconstructed_text2 = normalize_text(doc2)

    embeddings = model.encode([reconstructed_text1, reconstructed_text2])
    structural_similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

    important_words1 = {token.lemma_ for token in doc1 if not token.is_stop and not token.is_punct}
    important_words2 = {token.lemma_ for token in doc2 if not token.is_stop and not token.is_punct}
    word_similarity = len(important_words1.intersection(important_words2)) / max(len(important_words1), len(important_words2))

    negation_words = {"no", "nunca", "tampoco", "ninguna", "jamás"}
    negations_text1 = [token for token in doc1 if token.lemma_ in negation_words]
    negations_text2 = [token for token in doc2 if token.lemma_ in negation_words]
    negation_impact = 0.5 if negations_text1 or negations_text2 else 1.0

    adjusted_similarity = ((structural_similarity * negation_impact) + word_similarity) / 2

    details_difference = important_words1.symmetric_difference(important_words2)
    
    common_verbs = calculate_common_verbs(doc1, doc2)
    
    adjective_synonyms = find_adjective_synonyms(doc1, doc2)
    verb_synonyms = find_verb_synonyms(doc1, doc2)

    semantic_description = get_semantic_description(structural_similarity)
    
    # Contar adjetivos y verbos
    adjectives1, verbs1 = count_adjectives_and_verbs(doc1)
    adjectives2, verbs2 = count_adjectives_and_verbs(doc2)
    
    detail_richness_result = evaluate_detail_richness(
    adjective_synonyms, verb_synonyms,
    len(adjectives1), len(adjectives2),
    len(verbs1), len(verbs2)
    )

    pdf_path = create_pdf(text1, text2, details_difference, common_verbs, semantic_description, 
                          adjective_synonyms, verb_synonyms, len(adjectives1), len(adjectives2), len(verbs1), len(verbs2),detail_richness_result)

    if pdf_path is not None:
        pdf_url = request.host_url.rstrip('/') + '/download/' + os.path.basename(pdf_path)
    else:
        pdf_url = None
    
    
    result = {
        "similarity": adjusted_similarity,
        "structural_similarity": structural_similarity,
        "word_similarity": word_similarity,
        "negations_text1": [neg.text for neg in negations_text1],
        "negations_text2": [neg.text for neg in negations_text2],
        "pdf_url": pdf_url
    }

    return jsonify(result)

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    directory = tempfile.gettempdir()
    return send_from_directory(directory=directory, path=filename, as_attachment=True)

# Configuración del PDF
def create_pdf(text1, text2, details_difference, common_verbs, semantic_description, 
               adjective_synonyms, verb_synonyms, count_adj1, count_adj2, 
               count_verb1, count_verb2, detail_richness_result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 10, 15)  # Establece los márgenes (izquierda, arriba, derecha)

    logo_path = 'images/delta.png'
    pdf.image(logo_path, x=170, y=10, w=25)  # Ajusta la posición (x, y) y el tamaño (w - ancho)
    
    pdf.ln(10)  # Añade un espacio vertical

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, 'Resultados de Comparación de Textos', 0, 1, 'C')

    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 10, 'Descripción semántica: ' + semantic_description, 0, 'C')

    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, 'Texto 1: ', 0, 1)
    pdf.multi_cell(0, 10, text1)
    pdf.ln(5)  # Añade un espacio vertical

    pdf.cell(0, 10, 'Texto 2: ', 0, 1)
    pdf.multi_cell(0, 10, text2)
    pdf.ln(5)  # Añade un espacio vertical

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, 'Diferencias de Detalles', 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, ', '.join(details_difference))
    pdf.ln(5)  # Añade un espacio vertical

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, 'Sinónimos de Adjetivos:', 0, 1)
    pdf.set_font("Arial", size=10)
    for adj, syns in adjective_synonyms.items():
        pdf.multi_cell(0, 10, f"{adj}: {', '.join(syns)}")
    pdf.ln(5)  # Añade un espacio vertical

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, 'Sinónimos de Verbos:', 0, 1)
    pdf.set_font("Arial", size=10)
    for verb, syns in verb_synonyms.items():
        pdf.multi_cell(0, 10, f"{verb}: {', '.join(syns)}")
    pdf.ln(5)  # Añade un espacio vertical

    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 10, f"Total de adjetivos en Texto 1: {count_adj1}, Total de adjetivos en Texto 2: {count_adj2}")
    pdf.multi_cell(0, 10, f"Total de verbos en Texto 1: {count_verb1}, Total de verbos en Texto 2: {count_verb2}")
    pdf.ln(5)  # Añade un espacio vertical

    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 10, 'Análisis de Riqueza en Detalles:', 0, 1, 'C')
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, detail_richness_result, 0, 'C')
    pdf.ln(5)  # Añade un espacio vertical más grande al final

    pdf_filename = f'compare_result_{uuid.uuid4()}.pdf'
    pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)
    pdf.output(pdf_path)
    return pdf_path


# Normalizar consiste en dejar los textos lo más redundantes posibles cuando se 
# encuentran pronombres o tácitos. Da más claridad al comparar luego.

def normalize_text(doc):
    reconstructed_text = []
    previous_subject = None
    for sent in doc.sents:
        new_sentence = []
        subject_found = False
        for token in sent:
            if token.dep_ == 'nsubj':
                subject_found = True
                if token.pos_ == 'PRON' and previous_subject:
                    new_sentence.append(previous_subject)
                else:
                    new_sentence.append(token.text)
                    previous_subject = token.text
            else:
                new_sentence.append(token.text)
        reconstructed_text.append(" ".join(new_sentence))
    return " ".join(reconstructed_text)


# Interpretación de resultados.

def get_semantic_description(similarity):
    if similarity > 0.90:
        return "Los textos significan lo mismo"
    elif similarity > 0.85:
        return "Textos muy similares"
    elif similarity > 0.75:
        return "Textos similares"
    elif similarity > 0.60:
        return "Textos medianamente similares"
    elif similarity > 0.45:
        return "Textos semanticamente con algunas diferencias"
    elif similarity > 0.20:
        return "Textos semanticamente distintos"
    else:
        return "Textos semanticamente muy distintos"
    
    
def calculate_common_verbs(doc1, doc2):
    verbs1 = {token.lemma_ for token in doc1 if token.pos_ == "VERB" and not token.is_stop and token.dep_ != "aux"}
    verbs2 = {token.lemma_ for token in doc2 if token.pos_ == "VERB" and not token.is_stop and token.dep_ != "aux"}
    return list(verbs1.intersection(verbs2))


# Búsqueda de adjetivos sinónimos
def find_adjective_synonyms(doc1, doc2):
    adjectives1 = {token.lemma_ for token in doc1 if token.pos_ == 'ADJ'}
    adjectives2 = {token.lemma_ for token in doc2 if token.pos_ == 'ADJ'}

    synonyms_found = {}
    for adj1 in adjectives1:
        for adj2 in adjectives2:
            if adj1 == adj2:  # Caso trivial, el mismo adjetivo en ambos textos
                synonyms_found.setdefault(adj1, set()).add(adj2)
            else:
                for category, synonyms in grupos_adjetivos.items():
                    if (adj1 in synonyms and adj2 in synonyms) and adj1 != adj2:
                        synonyms_found.setdefault(adj1, set()).add(adj2)
                        break 

    return synonyms_found

# Búsqueda de verbos sinónimos
def find_verb_synonyms(doc1, doc2):
    verbs1 = {token.lemma_ for token in doc1 if token.pos_ == 'VERB'}
    verbs2 = {token.lemma_ for token in doc2 if token.pos_ == 'VERB'}
    synonyms_found = {}

    verb_synonyms = {key: set(value) for key, value in grupos_adjetivos['verbs'].items()}

    for verb1 in verbs1:
        if verb1 in verbs2:
            continue  # No añadir si el verbo es igual en ambos textos

        found_synonyms = set()
        for synonyms in verb_synonyms.values():
            if verb1 in synonyms:
                common_synonyms = synonyms.intersection(verbs2)
                if common_synonyms:
                    found_synonyms.update(common_synonyms)

        if found_synonyms:
            synonyms_found[verb1] = found_synonyms

    return synonyms_found

# Evaluación de riqueza, considera la cantidad de verbos y adjetivos
def evaluate_detail_richness(adjective_synonyms, verb_synonyms, adj_count1, adj_count2, verb_count1, verb_count2):

    synonyms_count1 = sum(len(syns) for syns in adjective_synonyms.values()) + sum(len(syns) for syns in verb_synonyms.values())
    synonyms_count2 = sum(len(syns) for syns in verb_synonyms.values()) + sum(len(syns) for syns in verb_synonyms.values())
    
    richness1 = synonyms_count1 / (adj_count1 + verb_count1)
    richness2 = synonyms_count2 / (adj_count2 + verb_count2)
    
    if richness1 > richness2:
        return "Texto 1 es más rico en detalles."
    elif richness2 > richness1:
        return "Texto 2 es más rico en detalles."
    else:
        return "Ambos textos tienen una riqueza en detalles similar."

# Contador de adjetivos y verbos
def count_adjectives_and_verbs(doc):
    
    for token in doc:
        print(f"Token: {token.text}, POS: {token.pos_}")
        
    adjectives = {token.lemma_ for token in doc if token.pos_ == 'ADJ'}
    verbs = {token.lemma_ for token in doc if token.pos_ == 'VERB'}
    return adjectives, verbs



if __name__ == '__main__':
    app.run(debug=True)
