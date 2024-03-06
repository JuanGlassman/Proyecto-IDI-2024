import spacy

nlp = spacy.load("es_core_news_sm")

# Texto de ejemplo
texto1 = "En el estudio de las ciencias sociales, los investigadores examinan cómo los patrones de migración afectan las dinámicas familiares. El análisis detallado de estos patrones revela tendencias que sugieren cambios en la estructura social."
texto2 = "La investigación médica sobre el impacto de la dieta en la salud cardiovascular demuestra que ciertos alimentos promueven un corazón más saludable. Los datos recopilados indican que las personas que siguen una dieta rica en antioxidantes tienen menos probabilidades de desarrollar enfermedades cardíacas." 
texto3 = "En el campo de la inteligencia artificial, los expertos están explorando cómo los algoritmos pueden mejorar la eficiencia en la toma de decisiones. Los resultados preliminares sugieren que la implementación de estas tecnologías puede tener un impacto significativo en diversos sectores." 

# Procesar el texto con spaCy
doc = nlp(texto1)

# Lugar donde guardamos los objetos directos
objetos_directos = []

# Imprimir el POS tagging de cada palabra
for token in doc:
    if "obj" in token.dep_:
        objetos_directos.append(token.text)

# Imprimir los objetos directos
print("Objetos Directos encontrados:")
for token in objetos_directos:
    print("- ",token)