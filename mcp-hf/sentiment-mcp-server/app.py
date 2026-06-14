"""
Servidor MCP de Análisis de Sentimiento (MCP Course - Unit 2).

Usa Gradio con soporte MCP integrado: al lanzar con `mcp_server=True`, las
funciones de la app se exponen AUTOMÁTICAMENTE como herramientas (tools) MCP.
Así, cualquier cliente MCP (Claude Desktop, Cursor, un agente...) puede invocar
el análisis de sentimiento.

- UI web: para usarlo a mano.
- Endpoint MCP: para que lo consuman modelos/agentes.

Ejecutar en local:
    pip install -r requirements.txt
    python app.py
    # UI en http://localhost:7860 ; endpoint MCP en /gradio_api/mcp/sse

Autor: Alejandro Dueñas Real (github.com/aduenasdev)
"""

import gradio as gr
from textblob import TextBlob


def analizar_sentimiento(texto: str) -> dict:
    """Analiza el sentimiento de un texto y devuelve polaridad, subjetividad y etiqueta.

    Args:
        texto (str): el texto a analizar.

    Returns:
        dict: polarity (-1 a 1), subjectivity (0 a 1) y la etiqueta de sentimiento.
    """
    # TextBlob calcula la polaridad (negativo↔positivo) y la subjetividad.
    blob = TextBlob(texto)
    polaridad = round(blob.sentiment.polarity, 3)
    subjetividad = round(blob.sentiment.subjectivity, 3)

    # Traducimos la polaridad numérica a una etiqueta legible.
    if polaridad > 0.1:
        etiqueta = "positivo"
    elif polaridad < -0.1:
        etiqueta = "negativo"
    else:
        etiqueta = "neutral"

    return {
        "polarity": polaridad,
        "subjectivity": subjetividad,
        "sentimiento": etiqueta,
    }


# Interfaz Gradio: define la UI web Y, con mcp_server=True, la tool MCP.
# El docstring de la función se usa como descripción de la tool para el modelo.
demo = gr.Interface(
    fn=analizar_sentimiento,
    inputs=gr.Textbox(placeholder="Escribe un texto para analizar su sentimiento..."),
    outputs=gr.JSON(),
    title="Análisis de Sentimiento (Servidor MCP)",
    description="Servidor MCP que expone una herramienta de análisis de sentimiento (TextBlob).",
)


if __name__ == "__main__":
    # mcp_server=True publica las funciones como herramientas MCP además de la UI.
    demo.launch(mcp_server=True)
