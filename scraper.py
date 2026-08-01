# scraper.py - Punto de entrada del web scraper de libros
# Scrapea books.toscrape.com para extraer títulos, precios, disponibilidad y rating

import argparse
import requests
from parser import extraer_libros, hay_pagina_siguiente, obtener_url_categoria
from exporter import guardar_csv


BASE_URL = "https://books.toscrape.com/"


def obtener_pagina(url):
    """Hace una petición GET a la URL y devuelve el HTML. Si falla, devuelve None."""
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.text
    except requests.ConnectionError:
        print(f"Error: No se pudo conectar a {url}")
        print("Verifica tu conexión a internet e intenta de nuevo.")
        return None
    except requests.Timeout:
        print(f"Error: La conexión a {url} tardó demasiado.")
        return None
    except requests.HTTPError as e:
        print(f"Error HTTP: {e}")
        return None
    except requests.RequestException as e:
        print(f"Error inesperado al conectar: {e}")
        return None


def construir_url_pagina(pagina, url_base_categoria=None):
    """Construye la URL para una página específica.
    Si hay categoría, usa la URL base de esa categoría."""
    if url_base_categoria:
        # Para categorías, la paginación es page-N.html dentro de la carpeta de la categoría
        if pagina == 1:
            return url_base_categoria
        else:
            # Reemplazar index.html por page-N.html
            return url_base_categoria.rsplit("/", 1)[0] + f"/page-{pagina}.html"
    else:
        # Para el catálogo general
        if pagina == 1:
            return BASE_URL
        else:
            return BASE_URL + f"catalogue/page-{pagina}.html"


def buscar_categoria(nombre):
    """Busca la URL de una categoría en la página principal.
    Devuelve la URL completa o None si no se encuentra."""
    print(f"Buscando categoría '{nombre}'...")
    html = obtener_pagina(BASE_URL)
    if not html:
        return None

    url_relativa = obtener_url_categoria(html, nombre)
    if url_relativa:
        url_completa = BASE_URL + url_relativa
        print(f"Categoría encontrada: {nombre}")
        return url_completa
    else:
        print(f"Error: No se encontró la categoría '{nombre}'.")
        print("Revisa que el nombre esté en inglés (ejemplo: travel, mystery, fiction).")
        return None


def scrapear(paginas_max=1, categoria=None):
    """Función principal que coordina el scraping de las páginas solicitadas."""
    todos_los_libros = []
    url_base_categoria = None

    # Si el usuario pidió una categoría, buscar su URL
    if categoria:
        url_base_categoria = buscar_categoria(categoria)
        if not url_base_categoria:
            return []

    pagina_actual = 1

    while pagina_actual <= paginas_max:
        # Construir la URL de esta página
        url = construir_url_pagina(pagina_actual, url_base_categoria)

        print(f"Scrapeando página {pagina_actual}...")
        html = obtener_pagina(url)

        # Si no pudimos obtener la página, parar
        if not html:
            print(f"No se pudo obtener la página {pagina_actual}. Deteniendo.")
            break

        # Extraer los libros de esta página
        libros = extraer_libros(html)

        if not libros:
            print(f"No se encontraron libros en la página {pagina_actual}.")
            break

        todos_los_libros.extend(libros)
        print(f"  -> {len(libros)} libros extraídos de página {pagina_actual}")

        # Verificar si hay más páginas
        if not hay_pagina_siguiente(html):
            print("No hay más páginas disponibles.")
            break

        pagina_actual += 1

    return todos_los_libros


def mostrar_resumen(libros):
    """Muestra un resumen de los libros encontrados en la terminal."""
    print(f"\n{'='*50}")
    print(f"Se encontraron {len(libros)} libros en total")
    print(f"{'='*50}")

    if libros:
        # Mostrar los primeros 5 como preview
        print("\nPrimeros libros encontrados:")
        print(f"{'-'*50}")
        for libro in libros[:5]:
            estrellas = "*" * libro["rating"] + "-" * (5 - libro["rating"])
            # Algunos títulos tienen caracteres especiales, los reemplazamos para no crashear
            titulo_safe = libro["titulo"][:40].encode("ascii", "replace").decode("ascii")
            print(f"  {titulo_safe:<40} | {libro['precio']:>7} | {estrellas}")
        if len(libros) > 5:
            print(f"  ... y {len(libros) - 5} libros mas")
        print(f"{'-'*50}")


def main():
    # Configurar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Web scraper de libros - Extrae datos de books.toscrape.com"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Número de páginas a scrapear (por defecto: 1)"
    )
    parser.add_argument(
        "--categoria",
        type=str,
        default=None,
        help="Filtrar por categoría (ejemplo: travel, mystery, fiction)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="resultados.csv",
        help="Nombre del archivo CSV de salida (por defecto: resultados.csv)"
    )

    args = parser.parse_args()

    # Mostrar qué vamos a hacer
    print("\n[*] Web Scraper de Libros - books.toscrape.com")
    print(f"{'='*50}")
    if args.categoria:
        print(f"Categoría: {args.categoria}")
    print(f"Páginas a scrapear: {args.pages}")
    print(f"Archivo de salida: {args.output}")
    print(f"{'='*50}\n")

    # Ejecutar el scraping
    libros = scrapear(paginas_max=args.pages, categoria=args.categoria)

    if libros:
        # Mostrar resumen en la terminal
        mostrar_resumen(libros)

        # Guardar en CSV
        guardar_csv(libros, args.output)
    else:
        print("\nNo se encontraron libros. Nada que guardar.")


if __name__ == "__main__":
    main()
