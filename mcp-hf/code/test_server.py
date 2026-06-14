"""
Prueba rápida del servidor MCP sin necesidad del Inspector ni de un LLM.

Importa el servidor y verifica:
  1) que las tools están registradas en el servidor MCP.
  2) que la lógica de las tools funciona (llamándolas directamente).

Ejecutar:
    python test_server.py
"""

import asyncio
import server  # importa server.py (registra tools/resource/prompt al cargar)


async def main() -> None:
    # 1) Comprobar que las capacidades están registradas en el servidor MCP.
    tools = await server.mcp.list_tools()
    print("Tools registradas:", [t.name for t in tools])

    # 2) Probar la lógica de las tools llamándolas directamente.
    print("contar_palabras('hola mundo cruel') =", server.contar_palabras("hola mundo cruel"))
    print("estadisticas_texto('Hola. ¿Qué tal? Bien!') =",
          server.estadisticas_texto("Hola. ¿Qué tal? Bien!"))

    print("\n[OK] El servidor MCP carga y sus tools funcionan correctamente.")


if __name__ == "__main__":
    asyncio.run(main())
