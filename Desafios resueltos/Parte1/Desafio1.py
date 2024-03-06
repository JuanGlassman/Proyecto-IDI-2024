import spacy

nlp = spacy.load("es_core_news_sm")

# Texto de ejemplo
texto1 = "En el ámbito de la electrónica, los circuitos integrados desempeñan un papel fundamental. Estos dispositivos compactos contienen componentes electrónicos interconectados, permitiendo la implementación de funciones complejas en dispositivos electrónicos modernos. La miniaturización y la eficiencia son objetivos clave en el diseño de circuitos integrados para impulsar el avance tecnológico."
texto2 = "La inteligencia artificial (IA) revoluciona la forma en que las máquinas aprenden y realizan tareas. Los algoritmos de aprendizaje profundo, un subcampo de la IA, permiten a las máquinas procesar datos de manera autónoma y mejorar su rendimiento con el tiempo. La IA encuentra aplicaciones en la visión por computadora, el procesamiento del lenguaje natural y la toma de decisiones automatizada." 
texto3 = "Los fractales, una rama fascinante de las matemáticas, exhiben patrones complejos y auto semejantes a diferentes escalas. Un ejemplo icónico es el conjunto de Mandelbrot, cuya estructura revela detalles infinitos. La teoría de fractales se aplica en diversas disciplinas, desde la representación visual hasta la modelización de fenómenos naturales, proporcionando una visión única de la geometría y la complejidad matemática." 

# Procesar el texto con spaCy
doc = nlp(texto2)

# Lugar donde guardamos la información 
important = []

# Recorrer el texto guardando los Sustantivos y verbos.
for token in doc:
    if "NOUN" in token.pos_:
        important.append(token.text)
    if "VERB" in token.pos_:
        important.append(token.text)

# Recorrer el texto guardando las entidades.
for ent in doc.ents:
    important.append(ent.text)

# Imprimir los propn
print("INFORMACION RELEVANTE:")
for token in important:
    print("- ",token)