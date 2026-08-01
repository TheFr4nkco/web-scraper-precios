# parser.py - Funciones para extraer datos del HTML con BeautifulSoup

from bs4 import BeautifulSoup


# Mapeo de palabras en inglés a números para las estrellas
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def extraer_libros(html):
    """Recibe el HTML de una página y devuelve una lista de diccionarios con los datos de cada libro."""
    soup = BeautifulSoup(html, "html.parser")
    libros = []

    # Cada libro está dentro de un <article class="product_pod">
    articulos = soup.find_all("article", class_="product_pod")

    for articulo in articulos:
        # Título: está en el atributo "title" del <a> dentro del <h3>
        titulo = articulo.h3.a["title"]

        # Precio: está en <p class="price_color">
        precio = articulo.find("p", class_="price_color").text.strip()

        # Disponibilidad: está en <p class="instock availability">
        disponibilidad_tag = articulo.find("p", class_="availability")
        disponibilidad = disponibilidad_tag.text.strip() if disponibilidad_tag else "Desconocido"

        # Rating: la clase del <p class="star-rating"> tiene el nombre en inglés
        rating_tag = articulo.find("p", class_="star-rating")
        if rating_tag:
            # Las clases son algo como ["star-rating", "Three"]
            clases = rating_tag.get("class", [])
            palabra_rating = clases[1] if len(clases) > 1 else "Zero"
            estrellas = RATING_MAP.get(palabra_rating, 0)
        else:
            estrellas = 0

        libros.append({
            "titulo": titulo,
            "precio": precio,
            "disponibilidad": disponibilidad,
            "rating": estrellas,
        })

    return libros


def hay_pagina_siguiente(html):
    """Revisa si hay un botón 'next' en el paginador. Devuelve True/False."""
    soup = BeautifulSoup(html, "html.parser")
    siguiente = soup.find("li", class_="next")
    return siguiente is not None


def obtener_url_categoria(html, nombre_categoria):
    """Busca en el sidebar la URL de una categoría por nombre (case-insensitive).
    Devuelve la URL relativa o None si no se encuentra."""
    soup = BeautifulSoup(html, "html.parser")
    sidebar = soup.find("div", class_="side_categories")

    if not sidebar:
        return None

    # Buscar todos los enlaces del sidebar
    enlaces = sidebar.find_all("a")
    for enlace in enlaces:
        texto = enlace.text.strip().lower()
        if texto == nombre_categoria.strip().lower():
            return enlace["href"]

    return None
