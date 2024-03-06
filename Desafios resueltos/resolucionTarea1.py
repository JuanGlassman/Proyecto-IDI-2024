"""
Extraer la información mas importante, como hablamos hoy de un escrito judicial. El escrito judicial que les voy a pasar es de la materia contencioso administrativo/ tributario. 
Lo mas importante que tienen que hacer es, extraer justamente la materia (Pista: mirar a lo ultimo de todo).
y ademas si pueden y quieren pueden extraer cosas interesantes como: Quien esta involucrado / personas (pueden usar entidades), 
extraer fechas (pista tienen que retocar el shape o buscar el patron directamente de fechas), y el resultado (que es lo que hace la corte, por ejemplo si acepta o "declara admisible")
"""
import spacy
from spacy.matcher import Matcher
import PyPDF2


def obtener_info(ubicacionPDF):
    # Cargar el modelo de spaCy para inglés
    nlp = spacy.load("es_core_news_sm")

    # Crear el matcher
    matcher = Matcher(nlp.vocab)

    # Definir los patrones
    patron_admisible = [{"LOWER": "declara admisible"}]
    patron_fecha = [{"POS": "NUM"}, {"POS": "ADP"}, {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "NUM"}]

    # Añadir el patrón al matcher
    matcher.add("Declara_admisible", [patron_admisible])
    matcher.add("Fecha", [patron_fecha])

    #---------------------- Cargar PDF ---------------------------
    # Crear el PDF a leer
    pdf = open(ubicacionPDF,"rb")

    # Crear el lector de PDF
    pdf_reader = PyPDF2.PdfReader(pdf)

    # Texto
    texto = ""

    # Pagina a pagina formar el texto completo
    for page in pdf_reader.pages:
        texto += page.extract_text()

    # Eliminar los saltos de linea
    texto = texto.replace('\n', ' ')
    texto = texto.replace('-', '')

    #con encode y decode solucionan el problema de las palabras divididas por espacios
    texto.encode('utf-8').decode('utf-8')

    #closing the pdf file
    pdf.close()
    #-------------------------- Fin de Carga ------------------------------------------
    

    # Procesar el texto con spaCy
    doc = nlp(texto)

    # Encontrar coincidencias con el matcher
    coincidencias = matcher(doc)

    # Utilizar un conjunto para almacenar resultados únicos
    resultados_unicos = []

    
    # Almacenar solo resultados únicos en el conjunto
    for match_id, start, end in coincidencias:
        resultados_unicos.append(doc[start:end].text)
    
    # Almacenar entidades
    for token in doc.ents:
        resultados_unicos.append(token.text)

    # Imprimir los resultados únicos
    for resultado in resultados_unicos:
        print(f"Resultado: {resultado}") 
   
ubicacionPDF = "C:\\Users\\juani\\Desktop\\Proyecto\\Documentos\\CAF 000466_2015_1_RH001 Copy.pdf"

obtener_info(ubicacionPDF)