
# Script para análisis de similitudes

![Portada](/images/image.png)

Ejecutar el script.py y acceder al html que se levanta para poder probar con una 
interfaz más agradable.

Se cargan dos modelos: es_core_news_lgde spaCy para análisis léxico detallado en español y 
paraphrase-multilingual-MiniLM-L12-v2de Sentence Transformers para comparar semánticamente 
los textos.

## Análisis de Texto y Cálculo de Similitud

Se procesan los textos con spaCy, extrayendo características léxicas y verificando la presencia 
de modificadores de frecuencia.
Se utilizan los Sentence Transformerspara obtener incrustaciones de los textos y calcular su 
similitud estructural usando la similitud coseno.


La similitud coseno es una métrica que se utiliza ampliamente en el procesamiento de lenguaje natural y en la recuperación de información para medir cuán similares son dos documentos (o textos) en términos de su contenido. Esta métrica evalúa la similitud como el Coseno del ángulo entre dos vectores en un espacio vectorial. La clave de su eficacia y ventaja sobre otras métricas se puede entender mejor con un ejemplo práctico. 

Ejemplo ilustrativo Supongamos que tenemos dos documentos y queremos comparar su similitud: 

**Texto 1: "El perro persigue al gato".** 

**Texto 2: "El can corre tras el felino".** 

Primero, convertimos estos textos en vectores. 

Cada dimensión en el vector representa una palabra distinta en el corpus total (conjunto de todos los textos considerados), y el valor en cada dimensión representa la importancia de esa palabra en el texto (por ejemplo, frecuencia de la palabra). 
Para simplificar, supongamos que nuestro análisis y vocabulario sólo considera las palabras clave y sinónimos, ignorando conectores y preposiciones comunes.

Podríamos tener algo como esto: 

**Vector para Texto 1 = [1 (perro), 0 (can), 1 (persigue), 0 (corre), 1 (gato), 0 (felino)]**

**Vector para Texto 2 = [0 ( perro), 1 (can), 0 (persigue), 1 (corre), 0 (gato), 1 (felino)]**

Cálculo de la Similitud Coseno La similitud coseno se calcula utilizando la fórmula:

![Función](/images/function.png)

A y B son los vectores que representan los textos.

**Vector para Texto 1 = [1, 0, 1, 0, 1, 0]**
**Vector para Texto 2 = [0, 1, 0, 1, 0, 1]**

**A⋅B=( 1×0 )+( 0×1 )+( 1×0 )+( 0×1 )+( 1×0 )+( 0×1 )=0**

![Magnitudes](/images/magnitud.png)

![Cálculo](/images/magnitud.png)

El resultado de similitud coseno de 0 indica que los textos son ortogonales entre sí en el espacio vectorial, implicando que no comparten palabras clave en común (según el análisis simplificado de sinónimos). Sin embargo, intuitivamente sabemos que los textos son similares porque "perro" y "can", así como "persigue" y "corre", "gato" y "felino" son pares de sinónimos.


En resumen, este script es un ejemplo cómodo de cómo combinar múltiples herramientas y 
técnicas de PNL para crear un sistema integral de análisis de texto que va más allá de 
simples comparaciones léxicas, incorporando semántica, contexto léxico y ajustes basados 
en el uso lingüístico específico.


**Informe**

Una vez hecha las comparaciones entre texto, se puede proceder a generar un informe
en pdf.

![Infrorme](/images/informe.png)


