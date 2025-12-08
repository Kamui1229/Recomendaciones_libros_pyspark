import pandas as pd
import sys

# Cargar datos
matriz = pd.read_csv('matriz_similitud_libros.csv', index_col=0)
libros = list(matriz.index)
tfidf = pd.read_csv('datos_tfidf_libros.csv')

# Función para buscar libro
def buscar_libro(nombre):
    nombre = nombre.lower()
    for libro in libros:
        if nombre in libro.lower():
            return libro
    return None

# Obtener argumentos
if len(sys.argv) < 4:
    print("Uso: python3 script.py [recomendar|palabras] 'nombre libro' N")
    print("Ejemplo 1: python3 script.py recomendar 'The Great Gatsby' 3")
    print("Ejemplo 2: python3 script.py palabras 'The Great Gatsby' 5")
    sys.exit(1)

accion = sys.argv[1]
nombre_libro = sys.argv[2]
n = int(sys.argv[3])

# Buscar libro
libro_exacto = buscar_libro(nombre_libro)
if not libro_exacto:
    print(f"Libro no encontrado. Libros disponibles:")
    for libro in libros[:10]:
        print(f"  - {libro}")
    sys.exit(1)

# Ejecutar acción
if accion == "recomendar":
    idx = libros.index(libro_exacto)
    similitudes = matriz.iloc[idx]
    resultados = similitudes.drop(libro_exacto).sort_values(ascending=False)
    
    print(f"Recomendaciones para '{libro_exacto}':")
    for i, (libro, sim) in enumerate(resultados.head(n).items(), 1):
        print(f"{i}. {libro}")

elif accion == "palabras":
    palabras = tfidf[tfidf['doc'] == libro_exacto]
    palabras_ord = palabras.sort_values('pesos', ascending=False)
    
    print(f"Palabras importantes de '{libro_exacto}':")
    for i, palabra in enumerate(palabras_ord.head(n)['texto'].tolist(), 1):
        print(f"{i}. {palabra}")

else:
    print("Acción debe ser 'recomendar' o 'palabras'")