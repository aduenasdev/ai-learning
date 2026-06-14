# 📚 Apuntes — Hugging Face AI Agents Course

> Resúmenes capítulo a capítulo del curso de Agentes de Hugging Face.
> Curso: https://huggingface.co/learn/agents-course
> Objetivo: certificado de Fundamentos (Unit 1) → para CV/LinkedIn de Alejandro Dueñas Real.

## Índice
- [Unidad 1 — Introducción a los agentes](#unidad-1)
  - [1. ¿Qué es un agente?](#c1-que-es-un-agente)
  - [Cuestionario rápido 1 (respuestas)](#quiz1)
  - [2. ¿Qué son los LLM?](#c2-llms)
  - [3. Mensajes y Tokens Especiales](#c3-mensajes)
  - [4. ¿Qué son las herramientas?](#c4-tools)
  - [5. Ciclo Pensamiento–Acción–Observación](#c5-ciclo)
  - [6. Pensamiento (ReAct)](#c6-pensamiento)
  - [7. Acciones](#c7-acciones)
  - [8. Observación](#c8-observacion)
  - [9. Primer agente con smolagents (práctica)](#c9-smolagents)

---
<a id="unidad-1"></a>
# Unidad 1 — Introducción a los agentes

<a id="c1-que-es-un-agente"></a>
## 1. ¿Qué es un agente?

Un **agente de IA** = un sistema que **razona, planifica y usa herramientas** para interactuar con su entorno y lograr un objetivo.

Fórmula mental: **LLM (cerebro que razona/planifica) + Herramientas (para actuar) + ciclo Pensamiento→Acción→Observación.**

- El **LLM** es el cerebro: entiende instrucciones y decide.
- Las **herramientas** le dan capacidades que el texto solo no tiene (buscar, calcular, llamar APIs…).
- Ejemplo de agente real: un asistente como Siri/Alexa (entiende + razona + ejecuta acciones).

<a id="quiz1"></a>
## Cuestionario rápido 1 — Respuestas
- **P1** ¿Qué es un agente? → *Modelo de IA que razona, planifica y usa herramientas para interactuar con su entorno y lograr un objetivo.*
- **P2** Papel de la planificación → *Decidir la secuencia de acciones y seleccionar las herramientas adecuadas.*
- **P3** Cómo mejoran las tools → *Permiten ejecutar acciones que un modelo de solo texto no puede (hacer café, generar imágenes…).*
- **P4** Acciones vs herramientas → *Acción = el paso que da el agente; Herramienta = el recurso que usa para ese paso.*
- **P5** Papel de los LLM → *Son el "cerebro" que razona, entiende instrucciones y planifica acciones.*
- **P6** Mejor ejemplo de agente → *Un asistente virtual (Siri/Alexa) que entiende, razona y ejecuta tareas.*

> Patrón: la opción correcta menciona **razonar/planificar + actuar/usar herramientas**; las incorrectas dicen "estático", "solo texto" o "sin interactuar".

---
<a id="c2-llms"></a>
## 2. ¿Qué son los LLM?

**Qué es:** modelo de IA que **entiende y genera lenguaje humano**, entrenado con muchísimo texto, millones/miles de millones de parámetros. Es el **"cerebro" del agente**.

**Arquitectura: Transformer** (mecanismo de **atención**, desde BERT 2018). 3 tipos:

| Tipo | Qué hace | Ejemplo | Usos |
|---|---|---|---|
| **Encoder** | Texto → embedding | BERT | Clasificación, búsqueda semántica, NER |
| **Decoder** | Genera tokens uno a uno | Llama | Generación de texto, chatbots, código |
| **Seq2Seq** | Encoder + Decoder | T5, BART | Traducción, resumen, paráfrasis |

Los LLM más conocidos (GPT-4, Llama 3, DeepSeek-R1, Gemma, Mistral) son **decoders** con miles de millones de parámetros.

**Principio clave:** predecir el **siguiente token** dada la secuencia previa.
- **Token** ≈ subpalabra (no palabra completa). Llama 2 ≈ 32.000 tokens de vocabulario.
- **Tokens especiales**: marcan estructura; el más importante es **EOS** (fin de secuencia), distinto en cada modelo.

**Autorregresivo:** la salida de un paso es la entrada del siguiente, en bucle **hasta el token EOS**.
- Decodificación: *greedy* (token de mayor probabilidad) o *beam search* (explora varias secuencias).

**Atención** ("Attention is all you need"): identifica las palabras **más relevantes** para predecir el siguiente token. **Context length** = máximo de tokens procesables.

**Prompt:** la secuencia de entrada; diseñarlo bien **guía** la salida.

**Entrenamiento:** 1) **Pre-training** autosupervisado (predecir siguiente token) → 2) **Fine-tuning** supervisado (chat, tools, código…).

**Uso:** en local o vía **API en la nube** (HF Inference API).

**En agentes:** el LLM interpreta instrucciones, mantiene contexto, planifica y decide qué tools usar = **el cerebro**.

---
<a id="c3-mensajes"></a>
## 3. Mensajes y Tokens Especiales

**Idea central:** el chat (mensajes separados) por dentro se **concatena en un único prompt**.
> ⚠️ El modelo **no recuerda** la conversación: la **relee entera cada vez**. El historial es el contexto.

**Tipos de mensajes:**
- **System:** instrucciones persistentes que definen comportamiento/personalidad.
- **User:** lo que escribe la persona.
- **Assistant:** la respuesta del modelo.
→ User/Assistant se **alternan** y construyen el contexto.

**Chat Templates:** puente entre tus mensajes (rol/contenido) y el **formato exacto** de cada LLM; insertan los **tokens especiales** de cada turno. Cada modelo formatea distinto (SmolLM2 simple; Llama 3.2 añade metadatos).

**Base vs Instruct:**
- **Base:** solo predice el siguiente token (texto crudo).
- **Instruct:** afinado para **seguir instrucciones y conversar**.

**En código:** `tokenizer.apply_chat_template()` convierte la lista de mensajes en el prompt formateado automáticamente.

---
<a id="c4-tools"></a>
## 4. ¿Qué son las herramientas (Tools)?

**Qué es:** una **función dada al LLM** para un objetivo concreto. Amplía al agente más allá del texto.

**Por qué se necesitan:** conocimiento estático (fecha de corte), cálculo poco fiable, e interacción con el mundo real.

**Ejemplos:** búsqueda web, generación de imágenes, recuperación de datos, integración con APIs (GitHub, YouTube, Spotify…).

**Composición de una tool:** nombre · descripción · argumentos (con tipos) · tipo de salida · función.

**Cómo la "usa" el LLM** (clave):
1. Se le enseñan las tools en el **system prompt**.
2. El LLM **genera un texto** que representa la llamada.
3. **El código del agente** la detecta, **ejecuta la función** y devuelve el resultado.
4. El LLM redacta la respuesta final.
→ El LLM **no ejecuta** la tool; la ejecuta la aplicación.

**Cómo se describen:** formato preciso en el system prompt. Ej.: *Nombre: calculadora · Descripción: Multiplica dos enteros · Argumentos: a: int, b: int · Salida: int*.

**En código — decorador `@tool`:**
```python
@tool
def calculadora(a: int, b: int) -> int:
    """Multiplica dos enteros."""
    return a * b
```
Genera la descripción automáticamente (nombre, docstring, type hints). La clase `Tool` + `to_string()` produce la descripción lista para el LLM.

---
<a id="c5-ciclo"></a>
## 5. Ciclo Pensamiento–Acción–Observación

Bucle continuo que **se repite hasta lograr el objetivo**:
```
Pensamiento (Thought) → Acción (Action) → Observación (Observation) → ↺
```
1. 🧠 **Pensamiento:** el LLM razona y decide el siguiente paso.
2. ⚙️ **Acción:** ejecuta una tool, normalmente con una llamada en **JSON** (tool + parámetros).
3. 👀 **Observación:** recibe el resultado y lo realimenta al razonamiento.

**System prompt:** incrusta comportamiento + tools + instrucciones del ciclo.

**Ejemplo (Alfred, agente del tiempo):** Piensa (necesito API) → Actúa (`get_weather("New York")`) → Observa ("15°C, nublado") → Responde.

**ReAct** = **Re**asoning + **Act**ing: razonar y actuar de forma iterativa.

---
<a id="c6-pensamiento"></a>
## 6. Pensamiento (Thought) y ReAct

**Qué es:** el **razonamiento interno** del agente — su "diálogo interno" para analizar la tarea y formular la estrategia.

**Permite:** descomponer problemas, reflexionar sobre lo ocurrido, ajustar el plan con nueva info.

**Tipos de razonamiento (8):** planificación, análisis, decisión, resolución, memoria, autorreflexión, objetivos, priorización.

**ReAct:** pedir "pensar paso a paso" (*"Let's think step by step"*) → el modelo genera un **plan** antes de la respuesta. Descomponer en sub-tareas = más detalle, menos errores (**chain-of-thought**).

**Reasoning models:** DeepSeek-R1, OpenAI o1 → están **entrenados** para incluir secciones de pensamiento (con tokens especiales), no es solo un truco de prompt.

---

<a id="c7-acciones"></a>
## 7. Acciones (cómo el agente interactúa con su entorno)

**Qué son:** los **pasos concretos** que da el agente para interactuar con su entorno (buscar datos, llamar a una API, manipular interfaces, controlar dispositivos). Pensar no basta; hay que **ejecutar**.

**Tipos de agente (según cómo estructuran la salida):**
1. **JSON Agents** → la acción en **JSON** estructurado.
2. **Code Agents** → **código ejecutable** (normalmente Python); más flexibles.
3. **Function-Calling Agents** → subtipo de JSON, un mensaje nuevo por acción.

**Categorías de acciones:** recopilar info (búsquedas, BD) · usar tools (APIs, cálculos) · interactuar con el entorno · comunicarse (usuario u otros agentes).

**Enfoque "Stop and Parse" 🔑:**
1. El agente **genera la acción** en un formato predeterminado.
2. La generación **se detiene** al completar la acción (*stop*).
3. Un **parser externo** extrae función + parámetros y los **ejecuta** (*parse*).
→ Salidas estructuradas y predecibles.

**Code Agents vs JSON Agents:**
- **Code:** más expresivos (bucles, condicionales), modulares, fáciles de depurar, integran librerías.
- **JSON:** salida más simple y acotada.
- Ambos siguen **stop-and-parse**.

---

<a id="c8-observacion"></a>
## 8. Observación (integrar resultados para reflexionar y adaptarse)

**Qué es:** cómo el agente **percibe las consecuencias de sus acciones** (respuestas de API, errores, logs). Señales del entorno que alimentan el siguiente razonamiento.

**En esta fase el agente:**
- Recibe **feedback** (éxito o fallo).
- Actualiza la **memoria** (integra la info al contexto).
- Refina la **estrategia**.

**Tipos de observaciones (5):**
1. Feedback del sistema (errores, éxito, status codes)
2. Cambios de datos (BD, archivos, estado)
3. Lecturas del entorno (sensores, métricas, recursos)
4. Análisis de respuestas (salidas de API, consultas, cálculos)
5. Eventos temporales (deadlines, tareas programadas)

**Integración:** el resultado se **añade como observación al prompt** → el agente se mantiene alineado con su objetivo.

**En el bucle:** **cierra** el ciclo Pensar→Actuar→Observar y decide si necesita otra vuelta o ya da la **respuesta final**.

---

<a id="c9-smolagents"></a>
## 9. Tu primer agente con smolagents (práctica)

**smolagents:** framework **ligero** de HF; su estrella es el **CodeAgent** (actúa ejecutando **código** y observa el resultado).

**Setup:**
1. Cuenta HF + **token** de acceso.
2. **Duplicar** la plantilla `agents-course/First_agent_template` (copia en tu perfil).
3. Editar **`app.py`**.

**Tools — decorador `@tool`** (3 requisitos): type hints (entrada/salida) + docstring con descripción + implementación.
Ejemplo de la plantilla: `get_current_time_in_timezone()` (hora local con `pytz`).

**Modelo:** `InferenceClientModel` con **Qwen/Qwen2.5-Coder-32B-Instruct** vía API serverless (`max_tokens=2096`, `temperature=0.5`).

**CodeAgent:**
```python
agent = CodeAgent(
    model=model,
    tools=[final_answer],   # añade aquí tus tools
    max_steps=6,
    verbosity_level=1
)
```
Tools extra disponibles: `DuckDuckGoSearchTool` (búsqueda web), generación de imágenes, etc.

> 💡 Se aprende **probando**: duplica el template, añade tools y ejecuta.

---

---
## ✅ Unit 1 COMPLETADA — Cuestionario final APROBADO 🎓
**Certificado obtenido:** *AI Agents — Fundamentals* (Hugging Face), junio 2026.

Respuestas del cuestionario final (referencia):
| Q | Resp | Q | Resp |
|---|---|---|---|
| 1 | special token = estructura la conversación | 6 | feedback del entorno |
| 2 | refina iterativamente con feedback | 7 | Transformer |
| 3 | captura feedback/resultados | 8 | actualiza memoria/contexto |
| 4 | (NO uso) jugar ajedrez/Go | 9 | Thought |
| 5 | respuesta de API del tiempo | 10 | señales del entorno |

> ⏭️ Siguiente: **Unidad 2 — Marcos para agentes** (smolagents, LlamaIndex, LangGraph). Escribe `continue` para empezar.
