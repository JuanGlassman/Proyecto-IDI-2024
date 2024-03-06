import spacy
from spacy import displacy

nlp = spacy.load("es_core_news_sm")

texto = "El presidente de la compañía XYZ, Juan Pérez, anunció hoy en una conferencia de prensa que la empresa ha alcanzado un acuerdo para adquirir a su competidor principal, Google. La transacción está valuada en 1.5 mil millones de dólares y se espera que se complete a finales de este año. "

doc = nlp(texto)

for ent in doc.ents:
    print(f"Entidad encontrada:  {ent.text}, Tipo: {ent.label_}")
