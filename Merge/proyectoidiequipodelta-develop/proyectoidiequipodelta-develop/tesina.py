import spacy
from spacy.matcher import Matcher

nlp = spacy.load("es_core_news_sm")  

text1 = "El veloz zorro marrón salta sobre el perro perezoso."
# text2 = "Un veloz zorro de color oscuro salta sobre el canino inactivo."
text2 = "Mi casa es azul por fuera y blanca por dentro"
# Process the texts
doc1 = nlp(text1)
doc2 = nlp(text2)

# Define a Matcher to identify negations and antonyms
matcher = Matcher(nlp.vocab)
pattern = [{"LEMMA": "not"}, {"POS": "VERB"}]  # Example pattern for negation
matcher.add("NEGATION", [pattern])

# Find matches in both documents
matches1 = matcher(doc1)
matches2 = matcher(doc2)

# Function to remove stopwords and punctuation and perform lemmatization
def preprocess(doc):
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

# Preprocess documents
processed_doc1 = preprocess(doc1)
processed_doc2 = preprocess(doc2)

# Calculate similarity
similarity = doc1.similarity(doc2)

# Compare sets of lemmas for additional detail
detail_diff = set(processed_doc1).symmetric_difference(set(processed_doc2))

# Output the results
print(f"Text 1: {text1}")
print(f"Text 2: {text2}")
print(f"Similarity: {similarity}")
print(f"Negations in Text 1: {matches1}")
print(f"Negations in Text 2: {matches2}")
print(f"Difference in detail: {detail_diff}")

# You would expand on the matching patterns to better find contradictions and detail differences.
