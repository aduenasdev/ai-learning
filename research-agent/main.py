"""
Punto de entrada por consola (CLI) del Asistente de Investigación.

Uso:
    python main.py                 -> modo interactivo (pregunta tras pregunta)
    python main.py "tu pregunta"   -> responde una sola pregunta y termina

Requisitos: definir GROQ_API_KEY en un archivo .env (ver .env.example).
"""

import sys
from agent import crear_agente, preguntar


def main() -> None:
    # Creamos el agente una sola vez (reutilizable para varias preguntas).
    agente = crear_agente()

    # Si pasamos la pregunta como argumento, respondemos y salimos.
    if len(sys.argv) > 1:
        pregunta = " ".join(sys.argv[1:])
        print(preguntar(agente, pregunta))
        return

    # Modo interactivo: bucle de preguntas hasta que el usuario escriba "salir".
    print("🔎 Asistente de Investigación con IA")
    print("   Escribe tu pregunta (o 'salir' para terminar).")
    while True:
        try:
            pregunta = input("\n❓ > ").strip()
        except (EOFError, KeyboardInterrupt):
            break  # Ctrl+C / Ctrl+D para salir
        if pregunta.lower() in ("salir", "exit", "quit", ""):
            break
        respuesta = preguntar(agente, pregunta)
        print(f"\n💡 {respuesta}")

    print("\n¡Hasta luego!")


if __name__ == "__main__":
    main()
