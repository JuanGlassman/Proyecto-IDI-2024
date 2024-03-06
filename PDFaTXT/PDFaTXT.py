import PyPDF2

def Cargar_TXT(ubicacionPDF, ubicacionTXT):
    # Crear el PDF a leer
    pdf = open(ubicacionPDF,"rb")

    # Crear el lector de PDF
    pdf_reader = PyPDF2.PdfReader(pdf)

    # Texto Vacío
    texto = ""

    # Cargar pagina a pagina para formar el texto
    for page in pdf_reader.pages:
        texto += page.extract_text()

    # Cerrar archivo PDF
    pdf.close()

    print(texto)

    # Crear el TXT a esctribir
    txt = open (ubicacionTXT, 'w')

    # Escribir el texto en el archivo TXT
   # txt.write(texto)

    # Cerrar archivo TXT
    txt.close

    print(texto)

ubicacionPDF = "C:\\Users\\juani\\Desktop\\CAF 000466_2015_1_RH001 Copy.pdf" 
ubicacionTXT = "C:\\Users\\juani\\Desktop\\TEXTO.txt"

Cargar_TXT(ubicacionPDF, ubicacionTXT)