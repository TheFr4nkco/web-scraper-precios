# 📚 Web Scraper de Precios de Libros

Un script en Python que extrae los nombres, precios, disponibilidad y rating de libros desde [books.toscrape.com](https://books.toscrape.com). Los resultados se guardan automáticamente en un archivo CSV y se muestra un resumen en la terminal.

> **Nota:** Este proyecto usa [books.toscrape.com](https://books.toscrape.com), un sitio diseñado específicamente para practicar web scraping. Los precios y ratings son ficticios.

---

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/web-scraper-precios.git
cd web-scraper-precios
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate      # En Mac/Linux
venv\Scripts\activate         # En Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

---

## 📖 Uso

### Uso básico (scrapea solo la primera página):
```bash
python scraper.py
```

### Scrapear múltiples páginas:
```bash
python scraper.py --pages 3
```

### Filtrar por categoría:
```bash
python scraper.py --categoria travel
python scraper.py --categoria mystery --pages 2
```

### Cambiar el nombre del archivo de salida:
```bash
python scraper.py --output libros_travel.csv --categoria travel
```

---

## 🖥️ Ejemplo de ejecución

```
📚 Web Scraper de Libros - books.toscrape.com
==================================================
Páginas a scrapear: 2
Archivo de salida: resultados.csv
==================================================

Scrapeando página 1...
  -> 20 libros extraídos de página 1
Scrapeando página 2...
  -> 20 libros extraídos de página 2

==================================================
Se encontraron 40 libros en total
==================================================

Primeros libros encontrados:
──────────────────────────────────────────────────
  A Light in the Attic                   |  £51.77 | ★★★☆☆
  Tipping the Velvet                     |  £53.74 | ★☆☆☆☆
  Soumission                             |  £50.10 | ★☆☆☆☆
  Sharp Objects                          |  £47.82 | ★★★★☆
  Sapiens: A Brief History of Humankind  |  £54.23 | ★★★★★
  ... y 35 libros más
──────────────────────────────────────────────────
Datos guardados en resultados.csv
```

---

## 📄 Ejemplo del CSV generado

| titulo | precio | disponibilidad | rating |
|--------|--------|---------------|--------|
| A Light in the Attic | £51.77 | In stock | 3 |
| Tipping the Velvet | £53.74 | In stock | 1 |
| Soumission | £50.10 | In stock | 1 |
| Sharp Objects | £47.82 | In stock | 4 |
| Sapiens: A Brief History of Humankind | £54.23 | In stock | 5 |

Ver archivo completo: [resultados_ejemplo.csv](resultados_ejemplo.csv)

---

## 📁 Estructura del proyecto

```
web-scraper-precios/
├── scraper.py               # Punto de entrada, maneja argumentos y flujo principal
├── parser.py                # Funciones para extraer datos del HTML con BeautifulSoup
├── exporter.py              # Función para guardar los datos en CSV
├── requirements.txt         # requests, beautifulsoup4
├── resultados_ejemplo.csv   # Ejemplo del output generado
├── .gitignore
└── README.md
```

---

## 🛠️ Tecnologías usadas

- **Python 3.10+**
- **requests** — para hacer las peticiones HTTP
- **beautifulsoup4** — para parsear el HTML
- **csv** (librería estándar) — para guardar los datos
- **argparse** (librería estándar) — para argumentos opcionales
