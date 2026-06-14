"""
GAIA Final Assignment — Agent (Hugging Face AI Agents Course, Unit 4)

Drop-in replacement for the `BasicAgent` class in the course's
`Final_Assignment_Template` Space (app.py). Builds a real smolagents
CodeAgent with web search + webpage reading + a Python sandbox, and
forces a GAIA-style exact-match answer format.

Target: >= 30% on the 20 filtered GAIA Level-1 questions -> Completion certificate.

requirements.txt (Space):
    gradio
    requests
    smolagents
    duckduckgo-search
    markdownify
    wikipedia-api

Author: Alejandro Dueñas Real (github.com/aduenasdev)
"""

import re
from smolagents import (
    CodeAgent,
    InferenceClientModel,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    PythonInterpreterTool,
)

# System prompt: GAIA is scored by EXACT MATCH, so the answer format is critical.
SYSTEM_PROMPT = """You are a precise general AI assistant solving GAIA benchmark questions.
Use your tools (web search, visit webpage, python) to find the verified answer.
Think step by step, but your LAST line MUST be exactly:

FINAL ANSWER: <answer>

Formatting rules for <answer>:
- A number: digits only, no thousands separators, no units (unless the question asks for the unit).
- A string: as few words as possible, no articles, no abbreviations, no trailing period.
- A comma-separated list: apply the rules above to each element, in the requested order.
- Do NOT add any text after the FINAL ANSWER line.
"""


class BasicAgent:
    def __init__(self):
        # Swap model_id for a stronger model if you have access (better GAIA score).
        model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
        self.agent = CodeAgent(
            tools=[
                DuckDuckGoSearchTool(),
                VisitWebpageTool(),
                PythonInterpreterTool(),
            ],
            model=model,
            max_steps=8,
            additional_authorized_imports=[
                "pandas", "numpy", "datetime", "json", "re", "math", "statistics",
            ],
        )
        print("BasicAgent (smolagents CodeAgent) initialized.")

    def __call__(self, question: str) -> str:
        try:
            raw = self.agent.run(f"{SYSTEM_PROMPT}\n\nQuestion: {question}")
            return self._extract_final_answer(str(raw))
        except Exception as e:  # never crash the whole run for one bad question
            print(f"[agent error] {e}")
            return "unknown"

    @staticmethod
    def _extract_final_answer(text: str) -> str:
        """Pull out the text after 'FINAL ANSWER:' (case-insensitive)."""
        match = re.search(r"final answer\s*:\s*(.*)", text, flags=re.IGNORECASE | re.DOTALL)
        answer = match.group(1) if match else text
        return answer.strip().strip(".").strip()
