# 📚 Apuntes — Hugging Face MCP Course (Model Context Protocol)

> Resúmenes capítulo a capítulo del curso de MCP de Hugging Face (en colaboración con Anthropic).
> Objetivo: Certificado de Fundamentos (Unit 1) → para CV/LinkedIn de Alejandro Dueñas Real.

## 🔗 URLs del curso
- **Curso (Unit 1):** https://huggingface.co/learn/mcp-course/unit1/introduction
- Capítulos Unit 1: `/what-is-mcp`, `/key-concepts`, `/architectural-components`, `/communication-protocol`, `/sdk`, `/mcp-clients`, `/quiz1`, `/quiz2`, `/unit1-recap`, `/certificate`
- **Quizzes de repaso (sin certificado):** `/unit1/quiz1` y `/unit1/quiz2`

## 🎓 EXAMEN / CERTIFICADO (Unit 1 — Fundamentos)
El examen que **emite el certificado** es un **Space**, NO la página del curso
(la versión embebida da 404 → entra directo al Space):
👉 **https://huggingface.co/spaces/mcp-course/unit_1_quiz**
- Logéate con tu cuenta de HF (aduenasdev) → Start → responde → necesitas **≥ 80%**.
- Certificado de **Completion** (curso entero) = además Units 2 y 3 (casos de uso).

## Índice
- [Unidad 1 — Fundamentos, Arquitectura y Conceptos](#unidad-1)
  - [1. Introducción y problema M×N](#u1-intro)
  - [2. Conceptos clave (Host/Client/Server + capacidades)](#u1-conceptos)
  - [3. Protocolo de comunicación (JSON-RPC, transports)](#u1-protocolo)
  - [4. SDK: crear tu primer servidor (FastMCP)](#u1-sdk)

---
<a id="unidad-1"></a>
# Unidad 1 — Fundamentos, Arquitectura y Conceptos Clave

<a id="u1-intro"></a>
## 1. Introducción y el problema M×N

**¿Qué es MCP?** El **Model Context Protocol** es un estándar abierto que conecta modelos de IA con **datos, herramientas y entornos externos**. Resuelve que los LLM **no tienen acceso nativo a info en tiempo real ni a herramientas especializadas**.

**Problema M×N → M+N:**
- Sin estándar: conectar **M** apps de IA con **N** herramientas = **M×N** integraciones a medida.
- Con MCP: cada app implementa el protocolo una vez (**M** clientes) y cada herramienta una vez (**N** servidores) → **M+N**.

**Analogía:** MCP es **"el USB-C de la IA"** — un conector estándar para todo el ecosistema.

<a id="u1-conceptos"></a>
## 2. Conceptos clave y terminología

**Arquitectura (3 piezas):**
| Componente | Qué es |
|---|---|
| **Host** | La app de IA con la que interactúa el usuario (Claude Desktop, Cursor, app propia). |
| **Client** | Componente dentro del host que gestiona la comunicación con **un** servidor MCP (detalles del protocolo). |
| **Server** | Programa externo que **expone capacidades** vía MCP. |

**Las 4 capacidades del servidor:**
1. **Tools** — funciones ejecutables que el modelo invoca (acciones o datos calculados).
2. **Resources** — fuentes de datos de **solo lectura** (contexto sin computación).
3. **Prompts** — plantillas predefinidas que guían la interacción usuario-IA-capacidad.
4. **Sampling** — el **servidor** solicita una generación al LLM (decisiones recursivas/agénticas).

**Principio:** estándar único → más interoperabilidad y menos fragmentación (beneficia a usuarios, desarrolladores y proveedores de herramientas).

---

<a id="u1-protocolo"></a>
## 3. Protocolo de comunicación

**Base: JSON-RPC 2.0** — formato de mensajes ligero, legible y agnóstico al lenguaje.

**Tipos de mensaje:**
| Tipo | Dirección | Qué es |
|---|---|---|
| **Request** | Cliente → Servidor | `id`, `method`, `params` |
| **Response** | Servidor → Cliente | `result` o `error` (emparejado por `id`) |
| **Notification** | Servidor → Cliente | Unidireccional, **sin respuesta** |

**Transports:**
- **stdio** — local: el cliente lanza el servidor como subproceso (E/S estándar).
- **HTTP + SSE / Streamable HTTP** — remoto por red; SSE permite **streaming**.

**Ciclo de vida:**
1. **Initialization** — intercambio de versión de protocolo + capacidades.
2. **Discovery** — el cliente pide las tools/resources disponibles.
3. **Execution** — el cliente invoca tools (notificaciones de progreso opcionales).
4. **Termination** — cierre ordenado.

**Diseño:** extensible vía negociación de versión y descubrimiento de capacidades (compatibilidad hacia atrás).

---

<a id="u1-sdk"></a>
## 4. SDK: crear tu primer servidor MCP (FastMCP)

**SDKs oficiales:** Python, JS/TS, Java, Kotlin, C#, Swift, Rust, Dart.

**Python = `FastMCP`** (decoradores):
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Nombre")

@mcp.tool()
def get_data(param: str) -> str:
    return f"Result for {param}"

@mcp.resource("resource://{id}")
def resource_handler(id: str) -> str:
    return f"Resource data for {id}"

@mcp.prompt()
def prompt_handler(input: str) -> str:
    return f"Prompt content for {input}"

if __name__ == "__main__":
    mcp.run()
```

- **Tools** `@mcp.tool()` · **Resources** `@mcp.resource("uri://{x}")` · **Prompts** `@mcp.prompt()`.
- Arrancar en dev: `mcp dev server.py`.
- Probar sin LLM: **MCP Inspector** (`@modelcontextprotocol/inspector`), en el navegador.

> 💻 Ejemplo propio en `code/server.py`: servidor MCP de utilidades de texto (tool + resource + prompt).

---

> ⏭️ Siguiente: **MCP Clients (conectar el servidor a un host/cliente)**. Escribe `continue`.
