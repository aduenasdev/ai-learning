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
- [Unidad 2 — Marcos para agentes](#unidad-2)
  - [Introducción a los frameworks](#u2-intro)
  - [2.1 smolagents](#u21)
  - [2.2 LlamaIndex](#u22)
  - [2.3 LangGraph](#u23)
- [Unidad 3 — RAG Agéntico (caso de uso)](#unidad-3)
- [Unidad 4 — Proyecto Final (GAIA)](#unidad-4)

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

<a id="unidad-2"></a>
# Unidad 2 — Marcos para agentes de IA

<a id="u2-intro"></a>
## Introducción a los frameworks

**¿Hace falta un framework?** No siempre. Para casos simples, **flujos predefinidos bastan**. El framework aporta valor con la **complejidad**: cuando el LLM llama funciones o **coordina varios agentes**.

**Qué resuelve un buen framework (componentes esenciales):**
- Motor **LLM** que mueve el sistema
- **Lista de tools** accesible
- **Parser de salida** que extrae las llamadas a tools
- **System prompts** sincronizados
- **Gestión de memoria**
- **Manejo de errores y reintentos**

**Los 3 frameworks del curso:**
| Framework | De | Fuerte en |
|---|---|---|
| **smolagents** | Hugging Face | Agentes que actúan con **código** (CodeAgent), ligero |
| **LlamaIndex** | LlamaIndex | **Indexación y recuperación** (RAG) |
| **LangGraph** | LangChain | Flujos **agénticos** con grafos de estados |

**Idea clave:** elegir entre **cadenas de prompts simples** (control total) y **frameworks** (abstracción para flujos complejos).

---

<a id="u21"></a>
## 2.1 smolagents

### ¿Por qué smolagents?
Framework **ligero** (~1.000 líneas) para que los LLM actúen con tools.
- **Mínima complejidad** y abstracciones.
- **Code-first**: el agente escribe **Python** en vez de JSON → sin overhead de parseo.
- **Model-agnostic**: Transformers, OpenAI, Azure, LiteLLM, Inference API.
- Integración con el **HF Hub**. Ideal para **prototipado rápido**.
- Diseño **MultiStepAgent** (ciclos pensamiento-acción iterativos).

### Code Agents (`CodeAgent`) — tipo por defecto
- Genera **código Python** para actuar (no JSON). Los LLM **rinden mejor con código** (componibilidad, objetos complejos, expresividad; alineado con su entrenamiento).
- Sigue el bucle **ReAct**: memoria → mensajes → LLM → parsear código → ejecutar → log → repetir.
- 🔒 **Seguridad**: ejecución en **sandbox** con imports restringidos; añadir con `additional_authorized_imports`.
```python
from smolagents import CodeAgent, DuckDuckGoSearchTool
agent = CodeAgent(tools=[DuckDuckGoSearchTool()])
agent.run("Search for party music recommendations")
```

### Tool Calling Agents (`ToolCallingAgent`)
- Usa el **tool-calling nativo** del LLM → genera **JSON** (`{"name":..., "arguments":...}`) en vez de código.
- Mejor para **sistemas simples**; el CodeAgent rinde más en lógica compleja. Mismo flujo multi-step, distinta representación de la acción.

### Tools
- Definir con **`@tool`** (simple) o **clase `Tool`** (`name`, `description`, `inputs`, `output_type`, `forward()`).
- **Toolbox por defecto**: `PythonInterpreterTool`, `FinalAnswerTool`, `UserInputTool`, `DuckDuckGoSearchTool`, `GoogleSearchTool`, `VisitWebpageTool`.
- **Compartir/cargar**: `push_to_hub()`, `load_tool()`, `Tool.from_space()`, `Tool.from_langchain()`.

### Retrieval Agents (RAG agéntico)
- El agente **controla** la recuperación: formula sus queries, **multi-step retrieval**, reformula y **valida** resultados (supera el RAG de un solo paso por similitud).
- Tools: `DuckDuckGoSearchTool` (web) y **`BM25Retriever`** + `RecursiveCharacterTextSplitter` (base de conocimiento propia).

### Multi-Agent Systems
- Un **agente manager** orquesta y **delega** en agentes especializados (búsqueda, código…).
- **Memoria separada** por agente → **menos tokens, menos latencia y coste**.
- Úsalo cuando la tarea es compleja, requiere especialización o el contexto se llena.

### Vision & Browser Agents
- Integra **VLMs** (ej. GPT-4o) para razonar sobre **imágenes**: estáticas (`task_images`) o **screenshots** durante navegación (`observation_images`).
- Automatización web con **Selenium / Helium** (buscar texto, navegar atrás, cerrar popups). Ej.: verificación de identidad por captura + análisis visual.

---

> Cuestionario final 2.1: retos de código (no calificado). Soluciones en el repo / chat.

<a id="u22"></a>
## 2.2 LlamaIndex

**¿Qué es?** Toolkit completo para crear **agentes sobre tus datos** con **índices y workflows**. Fuerte en **RAG** y ecosistema maduro. Extras: **LlamaHub** (integraciones), **LlamaParse** (parseo de documentos), **LlamaTrace/LlamaCloud** (observabilidad).

### LlamaHub
Registro de cientos de integraciones/tools/agentes. Instalación con patrón fijo:
`pip install llama-index-{tipo}-{framework}` (ej. `llama-index-llms-huggingface-api`). → llamahub.ai

### Components (RAG) — pipeline en 5 etapas
1. **Loading** — `SimpleDirectoryReader`, LlamaParse, LlamaHub
2. **Indexing** — embeddings vía `IngestionPipeline`
3. **Storage** — vector stores (p. ej. **ChromaDB**)
4. **Querying** — `as_query_engine`, `as_retriever`, `as_chat_engine`
5. **Evaluation** — `FaithfulnessEvaluator`, `AnswerRelevancyEvaluator`, `CorrectnessEvaluator`

Piezas: **Nodes** (chunks con referencia al doc), **VectorStoreIndex**, **ResponseSynthesizer** (refine/compact/tree_summarize), **QueryEngine** (clave para RAG agéntico).

### Tools — 4 tipos
- **FunctionTool**: envuelve una función Python.
- **QueryEngineTool**: un query engine como tool (agentes anidados).
- **ToolSpecs**: colecciones de la comunidad (ej. Gmail).
- **Utility Tools**: `OnDemandToolLoader`, `LoadAndSearchToolSpec` (grandes volúmenes).

### Agents — 3 tipos
**Function-Calling**, **ReAct** (cualquier LLM de chat) y **custom**. Se crean dándoles tools; LlamaIndex usa function-calling si está disponible, si no ReAct.
- **Stateless** por defecto → usa **`Context`** para mantener memoria entre runs.
- **Agentic RAG**: el agente decide autónomamente si usar las tools.
- Multi-agente con **`AgentWorkflow`** (un hablante activo; el control pasa entre agentes).

### Workflows
Organizan el código en **pasos** event-driven:
- **Steps** (`@step`) que reaccionan/emiten **Events** (`StartEvent`, `StopEvent`, custom).
- **Type hints** para ramas/bucles.
- Estado compartido con **`Context`** (`ctx.store.set()` / `ctx.store.get()`).
- Single-step manual vs **`AgentWorkflow`** multi-agente.
Beneficios: organización clara, control flexible por eventos, comunicación tipada, estado integrado.

---

<a id="u23"></a>
## 2.3 LangGraph

**¿Qué es?** Framework de **LangChain** para apps **production-ready** con LLMs, con **control granular** del flujo. (Ejemplos con GPT-4o.)

### ¿Cuándo usarlo? (control vs libertad)
LangGraph = extremo **CONTROL** (smolagents = libertad/creatividad). Úsalo cuando necesitas **predictibilidad y orquestación**:
- Razonamiento **multi-paso** con flujo explícito
- **Persistencia de estado** entre pasos
- Sistemas **híbridos** (determinista + IA)
- **Human-in-the-loop**
- Arquitecturas complejas interdependientes
> Vs Python a pelo: aporta **estado, visualización, tracing y human-in-the-loop** integrados.

### Building blocks
- **State**: `TypedDict` con toda la info que fluye (base de las decisiones).
- **Nodes**: funciones Python que reciben el state, actúan (LLM/tool/lógica/humano) y devuelven updates.
- **Edges**: conexiones entre nodos → **normales** (secuenciales) y **condicionales** (enrutan según el state).
- Ejecución: `START → … → END`, con **`graph.invoke(estado_inicial)`**.

### Tu primer grafo (ejemplo: email de Alfred)
Clasifica spam/legítimo y redacta respuesta:
1. **State** (`EmailState`) 2. **Nodos** (`read_email`, `classify_email`, `handle_spam`, `draft_response`, `notify_mr_hugg`) 3. **Routing condicional** (`route_email` + **`add_conditional_edges`**) 4. Ensamblar con **`StateGraph`** + edges 5. **Compilar y ejecutar**. Observabilidad con **Langfuse**.

### Ejemplo avanzado: análisis de documentos
Agente **GPT-4o** multimodal: tool `extract_text()` (imagen→texto, base64) + `divide()`. Patrón **ReAct** con **`tools_condition`** (decide cuándo usar tools) y **`add_messages`** (acumula historial en vez de reemplazarlo).

### 🆚 Comparativa de los 3 frameworks (Unit 2)
| | smolagents | LlamaIndex | LangGraph |
|---|---|---|---|
| **Fuerte en** | code-first, ligero | RAG sobre datos | control del flujo |
| **Estilo** | libertad/creatividad | índices + workflows | grafos de estados (control) |
| **Úsalo si** | prototipado rápido | apps con datos/RAG | flujos deterministas, producción |

---

> ✅ **Unidad 2 COMPLETA** (frameworks).

<a id="unidad-3"></a>
# Unidad 3 — RAG Agéntico (caso de uso: Alfred, el anfitrión)

**Escenario:** construir a **Alfred**, agente que organiza una gala y responde sobre invitados, menú, agenda y clima, con **acceso a información + RAG** para imprevistos.

### ¿Qué es el RAG Agéntico?
RAG + **decisión del agente**: en vez de recuperar documentos automáticamente, el agente **decide qué tool/estrategia usar** (recuperar, web, clima…). Frente al RAG clásico aporta **flexibilidad**: razona qué fuente conviene, se adapta y **combina varias fuentes**.

### 1. Tool de recuperación de invitados (RAG)
- Dataset `agents-course/unit3-invitees` (lib `datasets`) → cada invitado = `Document` (nombre, relación, descripción, email).
- **`BM25Retriever`**: búsqueda por palabras clave **sin embeddings**; devuelve top-3.
- Se expone como **tool** en los 3 frameworks. Ej.: *"Háblame de Lady Ada Lovelace"*.

### 2. Más tools para Alfred
- 🔎 **Web search** (`DuckDuckGoSearchTool`).
- 🌦️ **Weather info** (custom: condición + temperatura).
- 📊 **Hub stats** (modelo más descargado de un autor en el HF Hub).

### 3. El agente Alfred completo
- Integra **tools + retriever** en smolagents (`CodeAgent`), LlamaIndex (`AgentWorkflow`) o LangGraph (`StateGraph`).
- **Orquesta varias tools** en secuencia (datos del invitado → investigar intereses → temas de conversación).
- 🧠 **Memoria** multi-turno: smolagents `memory=True`; LangGraph acumula mensajes en el `AgentState`.

**Idea clave:** un mismo caso de uso se resuelve con **cualquiera de los 3 frameworks** → eliges según necesites code-first (smolagents), datos/RAG (LlamaIndex) o control (LangGraph).

---

<a id="unidad-4"></a>
# Unidad 4 — Proyecto Final (GAIA)

**Qué construyes:** tu **propio agente** y lo evalúas contra el benchmark **GAIA**. Objetivo **≥ 30%** → **Certificado de Completion**. Es la unidad más avanzada (más código, menos guía).

### ¿Qué es GAIA?
Benchmark de asistentes de IA en **tareas reales**: razonamiento + multimodal + navegación web + tools. **466 preguntas** fáciles para humanos, difíciles para la IA.
- **Niveles:** L1 (<5 pasos) · L2 (5-10 pasos, varias tools) · L3 (planificación a largo plazo).
- **Rendimiento:** Humanos ~92% · GPT-4+plugins ~15% · Deep Research (OpenAI) ~67%.
- **Leaderboard** público en HF.

### Trabajo práctico (final assignment)
- Evalúa tu agente contra **20 preguntas filtradas de GAIA Nivel 1**.
- Envío vía **API** → puntuación por **coincidencia exacta** (prompt engineering crítico).
- Requisitos: **≥30%** · duplicar el **template Space** · **repo público** · enviar **usuario HF + link repo + respuestas**.
- Resultados en el **Students Leaderboard**.

---

# ✅ CURSO COMPLETADO (resumen)
- **Unit 1** — Fundamentos de agentes → 🎓 **Certificado de Fundamentos obtenido** (2026-06-14).
- **Unit 2** — Frameworks: smolagents · LlamaIndex · LangGraph.
- **Unit 3** — RAG Agéntico (caso Alfred).
- **Unit 4** — Proyecto final con GAIA (≥30% → Certificado de Completion).

**Idea de proyecto propio (para GitHub/portfolio):** un agente tipo "Alfred" con **RAG + multi-tool + memoria**, montado en el framework que prefieras → material perfecto para vender el perfil.
