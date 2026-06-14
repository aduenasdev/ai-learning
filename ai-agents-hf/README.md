# 🤖 AI Agents — Hugging Face

Building AI agents with LLMs: tool use, the **Thought → Action → Observation** loop and the
**ReAct** approach, applied with **smolagents**.

🎓 **Certificate — Fundamentals (Unit 1):**
[view certificate](https://huggingface.co/datasets/agents-course/certificates/resolve/main/certificates/aduenasdev/2026-06-14.png) · issued by Hugging Face (2026-06-14)

## 🛠️ What I can do (demonstrated here)
- Build a **CodeAgent** with smolagents.
- Define **custom tools** with the `@tool` decorator (type hints + docstrings).
- Use models via the **Hugging Face Inference API** and built-in tools (web search).
- Apply the **Thought–Action–Observation** loop and **ReAct** reasoning.

## 📁 Contents
- [`code/`](code/) — runnable examples (smolagents).
- [`APUNTES.md`](APUNTES.md) — personal study notes (ES), chapter by chapter.

## 🚀 Run
```bash
# from the repo root (ai-learning/)
pip install smolagents pytz python-dotenv
cp .env.example .env        # add your HF_TOKEN
python ai-agents-hf/code/first_agent_smolagents.py
```

## 🧰 Stack
`smolagents` · `Hugging Face` · `Python` · `LLMs` · `AI Agents` · `Prompt Engineering`

---
**Author:** Alejandro Dueñas Real — Machine Learning Developer @ Pangeanic
🔗 [LinkedIn](https://linkedin.com/in/alejandrodr) · 💻 [GitHub](https://github.com/aduenasdev)
