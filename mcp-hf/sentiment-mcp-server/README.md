---
title: Sentiment Analysis MCP Server
emoji: 💬
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.34.0
app_file: app.py
pinned: false
---

# 💬 Sentiment Analysis MCP Server

A **Model Context Protocol (MCP) server** built with Gradio. It exposes a
sentiment-analysis tool that any MCP client (Claude Desktop, Cursor, an agent…)
can call — and a web UI to try it by hand.

Built as the Unit 2 project of the **[Hugging Face MCP Course](https://huggingface.co/learn/mcp-course)**.

## 🧠 What it demonstrates
- Turning a Python function into an **MCP tool** with Gradio (`launch(mcp_server=True)`).
- Exposing both a **web UI** and an **MCP endpoint** from one app.
- A deployable MCP server (Hugging Face Spaces).

## 🔌 Endpoints
- Web UI: `/`
- MCP (SSE): `/gradio_api/mcp/sse`

## 🚀 Run locally
```bash
pip install -r requirements.txt
python app.py
# UI: http://localhost:7860
```

## 🧰 Stack
`MCP` · `Gradio` · `TextBlob` · `Python`

---
**Author:** Alejandro Dueñas Real — Machine Learning Developer @ Pangeanic
🔗 [LinkedIn](https://linkedin.com/in/alejandrodr) · 💻 [GitHub](https://github.com/aduenasdev)
