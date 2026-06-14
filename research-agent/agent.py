"""
Asistente de Investigación con IA — definición del agente.

Construye un agente (smolagents) capaz de responder preguntas combinando varias
herramientas: búsqueda web, Wikipedia, lectura de páginas y un intérprete de
Python para cálculos. Sigue el ciclo ReAct (Pensamiento -> Acción -> Observación).

El modelo (el "cerebro") se sirve por Groq vía LiteLLM: gratis, rápido y potente.
Es model-agnostic: cambiando `model_id`/`api_key` puedes usar OpenAI, Anthropic, HF, etc.
"""

import os
from dotenv import load_dotenv
from smolagents import (
    CodeAgent,
    LiteLLMModel,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    PythonInterpreterTool,
)
from tools import buscar_wikipedia

# Carga las variables del archivo .env (entre ellas, GROQ_API_KEY).
# El .env NO se sube al repositorio (está en .gitignore).
load_dotenv()

# Instrucción de comportamiento: define el "estilo" de respuesta del asistente.
INSTRUCCION = (
    "Eres un asistente de investigación riguroso. Responde en español, de forma "
    "concisa y verificada. Usa tus herramientas (búsqueda web, Wikipedia, lectura "
    "de páginas, Python) para fundamentar la respuesta. Cuando uses información de "
    "internet, cita la fuente (URL o página de Wikipedia) al final."
)


def crear_agente() -> CodeAgent:
    """Crea y devuelve el agente de investigación ya configurado."""
    # El "cerebro": LLM servido por Groq. temperature baja => respuestas estables.
    modelo = LiteLLMModel(
        model_id="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
    )

    # El agente: recibe la pregunta, razona qué herramienta usar, la ejecuta,
    # observa el resultado y repite hasta tener la respuesta final.
    agente = CodeAgent(
        tools=[
            buscar_wikipedia,          # herramienta propia (Wikipedia ES/EN)
            DuckDuckGoSearchTool(),    # búsqueda web general
            VisitWebpageTool(),        # leer el contenido de una URL
            PythonInterpreterTool(),   # cálculos / procesamiento de datos
        ],
        model=modelo,
        max_steps=8,  # límite de iteraciones del ciclo ReAct (evita bucles infinitos)
        additional_authorized_imports=["math", "statistics", "datetime"],
    )
    return agente


def preguntar(agente: CodeAgent, pregunta: str) -> str:
    """Lanza una pregunta al agente aplicando la instrucción de estilo."""
    # Anteponemos la instrucción para que el agente responda con el formato deseado.
    return str(agente.run(f"{INSTRUCCION}\n\nPregunta: {pregunta}"))
