# exporter.py - Función para guardar los datos en CSV

import csv


def guardar_csv(libros, archivo="resultados.csv"):
    """Guarda una lista de diccionarios de libros en un archivo CSV."""
    if not libros:
        print("No hay datos para guardar.")
        return

    # Definir los encabezados del CSV
    campos = ["titulo", "precio", "disponibilidad", "rating"]

    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(libros)

    print(f"Datos guardados en {archivo}")
