"""
Herramientas personalizadas del Asistente de Investigación.

Una "tool" en smolagents es una función decorada con @tool: el decorador lee el
nombre, el docstring y los type hints para describírsela al modelo.

`buscar_wikipedia` usa la API oficial de Wikipedia (MediaWiki) vía requests:
es fiable y no depende de paquetes frágiles. Wikipedia exige un User-Agent propio.
"""

import requests
from smolagents import tool

# Wikipedia pide identificar la aplicación con un User-Agent (si no, puede rechazar).
CABECERAS = {"User-Agent": "ai-learning-research-agent/1.0 (https://github.com/aduenasdev)"}


@tool
def buscar_wikipedia(consulta: str, idioma: str = "es") -> str:
    """Busca un tema en Wikipedia y devuelve el título y un resumen de la página.

    Args:
        consulta: tema, persona o título que se quiere buscar en Wikipedia.
        idioma: código de idioma de Wikipedia (p. ej. 'es', 'en'). Por defecto 'es'.
    """
    api = f"https://{idioma}.wikipedia.org/w/api.php"
    try:
        # 1) Buscamos la página más relevante para la consulta.
        busqueda = requests.get(
            api,
            params={
                "action": "query",
                "list": "search",
                "srsearch": consulta,
                "srlimit": 1,
                "format": "json",
            },
            headers=CABECERAS,
            timeout=15,
        ).json()

        resultados = busqueda.get("query", {}).get("search", [])
        if not resultados:
            return f"Sin resultados en Wikipedia ({idioma}) para: {consulta}"
        titulo = resultados[0]["title"]

        # 2) Pedimos el extracto (resumen en texto plano) de esa página.
        resumen = requests.get(
            api,
            params={
                "action": "query",
                "prop": "extracts",
                "exintro": True,        # solo la introducción
                "explaintext": True,    # texto plano (sin HTML)
                "titles": titulo,
                "format": "json",
            },
            headers=CABECERAS,
            timeout=15,
        ).json()

        paginas = resumen.get("query", {}).get("pages", {})
        extracto = next(iter(paginas.values()), {}).get("extract", "")
        # Limitamos el tamaño para no saturar el contexto del modelo.
        return f"{titulo}\n{extracto[:4000]}".strip()

    except Exception as error:
        return f"Error consultando Wikipedia: {error}"
