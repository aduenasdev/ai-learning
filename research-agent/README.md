# 🔎 AI Research Agent

A small but real **AI agent** that answers questions by combining multiple tools —
web search, Wikipedia, webpage reading and a Python interpreter — following the
**ReAct loop** (Thought → Action → Observation). Built with **smolagents**.

> Model-agnostic: runs on **Groq (free)** by default; switch to OpenAI / Anthropic /
> Hugging Face by changing one line.

## ✨ What it demonstrates
- Designing a **multi-tool agent** with smolagents (`CodeAgent`).
- Writing a **custom tool** (`buscar_wikipedia`) with the `@tool` decorator.
- **Tool orchestration** + the Thought–Action–Observation loop (ReAct).
- Clean config with `.env` (secrets never committed) and a simple CLI.

## 🧰 Stack
`smolagents` · `LiteLLM` · `Groq (Llama 3.3 70B)` · `Python` · `DuckDuckGo` · `Wikipedia`

## 🚀 Run it
```bash
pip install -r requirements.txt
cp .env.example .env          # add your GROQ_API_KEY (free: https://console.groq.com/keys)

python main.py                # interactive mode
python main.py "Who painted Guernica and in what year?"   # single question
```

## 📁 Structure
```
research-agent/
├── agent.py   # agent definition (the brain + tools + ReAct config)
├── tools.py   # custom Wikipedia tool
├── main.py    # CLI entry point
├── requirements.txt
└── .env.example
```

> 📝 Note: code comments are in Spanish. README is in English for wider reach —
> ask if you want a Spanish README too.

---
**Author:** Alejandro Dueñas Real — Machine Learning Developer @ Pangeanic
🔗 [LinkedIn](https://linkedin.com/in/alejandrodr) · 💻 [GitHub](https://github.com/aduenasdev)
