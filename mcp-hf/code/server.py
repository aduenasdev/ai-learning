"""
Servidor MCP de utilidades de texto (ejemplo del MCP Course de Hugging Face).

Expone capacidades vía Model Context Protocol usando FastMCP (el SDK de Python):
  - Tools: funciones que el modelo puede invocar (contar palabras, estadísticas).
  - Resource: dato de solo lectura accesible por URI (info del servidor).
  - Prompt: plantilla reutilizable (pedir un resumen).

Probar en local:
    pip install "mcp[cli]"
    mcp dev server.py          # abre el MCP Inspector en el navegador

Autor: Alejandro Dueñas Real (github.com/aduenasdev)
"""

from mcp.server.fastmcp import FastMCP

# Creamos el servidor MCP con un nombre identificativo.
mcp = FastMCP("text-utils")


# ---------------------------------------------------------------------------
# TOOLS — funciones ejecutables que el modelo puede invocar.
# El docstring y los type hints se exponen al modelo como descripción/esquema.
# ---------------------------------------------------------------------------
@mcp.tool()
def contar_palabras(texto: str) -> int:
    """Cuenta el número de palabras de un texto.

    Args:
        texto: el texto que se quiere analizar.
    """
    return len(texto.split())


@mcp.tool()
def estadisticas_texto(texto: str) -> dict:
    """Devuelve estadísticas básicas de un texto: palabras, caracteres y frases.

    Args:
        texto: el texto que se quiere analizar.
    """
    # Contamos frases de forma sencilla por los signos de puntuación finales.
    frases = [f for f in texto.replace("!", ".").replace("?", ".").split(".") if f.strip()]
    return {
        "palabras": len(texto.split()),
        "caracteres": len(texto),
        "frases": len(frases),
    }


# ---------------------------------------------------------------------------
# RESOURCE — dato de solo lectura, accesible por URI (sin computación pesada).
# ---------------------------------------------------------------------------
@mcp.resource("info://servidor")
def info_servidor() -> str:
    """Información estática del servidor."""
    return "Servidor MCP 'text-utils' v1.0 — utilidades de análisis de texto."


# ---------------------------------------------------------------------------
# PROMPT — plantilla reutilizable que guía la interacción con el modelo.
# ---------------------------------------------------------------------------
@mcp.prompt()
def resumir(texto: str) -> str:
    """Genera un prompt para resumir un texto en 3 frases."""
    return f"Resume el siguiente texto en 3 frases claras y concisas:\n\n{texto}"


if __name__ == "__main__":
    # Arranca el servidor (por defecto usa el transport stdio).
    mcp.run()
