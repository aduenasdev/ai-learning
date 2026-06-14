"""
Primer agente con smolagents — ejemplo del Hugging Face AI Agents Course.

Un CodeAgent que combina una herramienta propia (@tool) con una tool
integrada (búsqueda web), siguiendo el ciclo Pensamiento → Acción → Observación.

Requisitos:
    pip install smolagents pytz python-dotenv
    # Crea un archivo .env (raíz de ai-learning) con:  HF_TOKEN=hf_xxx
    # Token en: https://hf.co/settings/tokens  (tipo "Read")

Autor: Alejandro Dueñas Real (github.com/aduenasdev)
"""

import datetime
import pytz
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool, tool

# Carga HF_TOKEN desde el archivo .env (no se sube al repo).
load_dotenv()


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Devuelve la hora local actual en una zona horaria dada.

    Args:
        timezone: nombre de zona horaria IANA, p. ej. 'Europe/Madrid'.
    """
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    return f"La hora actual en {timezone} es {now.strftime('%Y-%m-%d %H:%M:%S')}"


# El "cerebro" del agente: un LLM servido vía Inference API de Hugging Face.
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    max_tokens=2096,
    temperature=0.5,
)

# El agente: razona, decide qué tool usar, la ejecuta y observa el resultado.
agent = CodeAgent(
    model=model,
    tools=[get_current_time_in_timezone, DuckDuckGoSearchTool()],
    max_steps=6,
    verbosity_level=1,
)


if __name__ == "__main__":
    # El agente decidirá usar la tool de hora y/o la búsqueda web según haga falta.
    respuesta = agent.run("¿Qué hora es ahora mismo en Madrid?")
    print("\n=== Respuesta del agente ===")
    print(respuesta)
