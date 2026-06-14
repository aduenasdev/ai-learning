"""
GAIA Final Assignment — improved agent (Hugging Face AI Agents Course, Unit 4).
Full app.py for the duplicated Final_Assignment_Template Space.

Improvements over the template:
- Real smolagents CodeAgent (web search + webpage reading + python).
- Downloads & reads ATTACHED FILES (.py/.txt/.csv/.json/.xlsx) and injects them
  into the prompt -> unlocks file-based questions (e.g. "run this python", "sum the Excel").
- GAIA exact-match answer formatting (FINAL ANSWER: ...).
- max_steps raised for harder multi-step questions.

Author: Alejandro Dueñas Real (github.com/aduenasdev)
"""
import os
import re
import gradio as gr
import requests
import inspect
import pandas as pd
import wikipedia
from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool, VisitWebpageTool, PythonInterpreterTool, tool


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return the title and summary of the best-matching page.

    Args:
        query: the topic, person, or page title to look up on Wikipedia.
    """
    try:
        page = wikipedia.page(query, auto_suggest=True)
        return f"{page.title}\n{page.content[:4000]}"
    except Exception:
        try:
            options = wikipedia.search(query)
            return "No exact page. Closest matches: " + ", ".join(options[:5])
        except Exception as e:
            return f"No Wikipedia result: {e}"

# --- Constants ---
DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"
FILES_URL = f"{DEFAULT_API_URL}/files"

SYSTEM_PROMPT = (
    "You are a precise general AI assistant solving GAIA benchmark questions. "
    "Use your tools (web search, visit webpage, python) to find the verified answer. "
    "If python code is given, run it. If tabular data is given, compute on it. "
    "Think step by step, but your LAST line MUST be exactly:\n"
    "FINAL ANSWER: <answer>\n"
    "Rules: a number = digits only (no thousands separators, no units unless asked); "
    "a string = as few words as possible, no articles, no trailing period; "
    "a list = comma-separated in the requested order. No text after the FINAL ANSWER line."
)


# --- Agent ---
class BasicAgent:
    def __init__(self):
        model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", temperature=0.1)
        self.agent = CodeAgent(
            tools=[wikipedia_search, DuckDuckGoSearchTool(), VisitWebpageTool(), PythonInterpreterTool()],
            model=model,
            max_steps=12,
            additional_authorized_imports=[
                "pandas", "numpy", "datetime", "json", "re", "math", "statistics", "csv", "io",
            ],
        )
        print("BasicAgent (smolagents CodeAgent) initialized.")

    def __call__(self, item) -> str:
        # Accept either the full question dict (preferred) or a plain string.
        if isinstance(item, dict):
            question = item.get("question", "")
            task_id = item.get("task_id")
            file_name = item.get("file_name")
        else:
            question, task_id, file_name = item, None, None

        print(f"Agent received question (first 60 chars): {str(question)[:60]}...")

        extra = ""
        if file_name and task_id:
            content = self._read_attached_file(task_id, file_name)
            if content:
                extra = f"\n\nATTACHED FILE ({file_name}) content:\n```\n{content}\n```"
            else:
                extra = f"\n\n(There is an attached file '{file_name}' that could not be read as text.)"

        try:
            raw = str(self.agent.run(f"{SYSTEM_PROMPT}\n\nQuestion: {question}{extra}"))
            m = re.search(r"final answer\s*:\s*(.*)", raw, flags=re.IGNORECASE | re.DOTALL)
            answer = (m.group(1) if m else raw).strip().strip(".").strip()
            print(f"Agent answer: {answer}")
            return answer
        except Exception as e:
            print(f"[agent error] {e}")
            return "unknown"

    @staticmethod
    def _read_attached_file(task_id, file_name):
        """Download the task file and return a TEXT representation (or None)."""
        try:
            r = requests.get(f"{FILES_URL}/{task_id}", timeout=30)
            r.raise_for_status()
            path = f"/tmp/{file_name}"
            with open(path, "wb") as f:
                f.write(r.content)
            ext = file_name.lower().rsplit(".", 1)[-1] if "." in file_name else ""
            if ext in ("txt", "py", "csv", "json", "md", "tsv"):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()[:8000]
            if ext in ("xlsx", "xls"):
                return pd.read_excel(path).to_csv(index=False)[:8000]
            return None  # images / audio / video: not handled here
        except Exception as e:
            print(f"[file read error] {e}")
            return None


def run_and_submit_all(profile: gr.OAuthProfile | None):
    space_id = os.getenv("SPACE_ID")

    if profile:
        username = f"{profile.username}"
        print(f"User logged in: {username}")
    else:
        print("User not logged in.")
        return "Please Login to Hugging Face with the button.", None

    api_url = DEFAULT_API_URL
    questions_url = f"{api_url}/questions"
    submit_url = f"{api_url}/submit"

    try:
        agent = BasicAgent()
    except Exception as e:
        print(f"Error instantiating agent: {e}")
        return f"Error initializing agent: {e}", None
    agent_code = f"https://huggingface.co/spaces/{space_id}/tree/main"
    print(agent_code)

    print(f"Fetching questions from: {questions_url}")
    try:
        response = requests.get(questions_url, timeout=15)
        response.raise_for_status()
        questions_data = response.json()
        if not questions_data:
            return "Fetched questions list is empty or invalid format.", None
        print(f"Fetched {len(questions_data)} questions.")
    except Exception as e:
        print(f"Error fetching questions: {e}")
        return f"Error fetching questions: {e}", None

    results_log = []
    answers_payload = []
    print(f"Running agent on {len(questions_data)} questions...")
    for item in questions_data:
        task_id = item.get("task_id")
        question_text = item.get("question")
        if not task_id or question_text is None:
            print(f"Skipping item with missing task_id or question: {item}")
            continue
        try:
            submitted_answer = agent(item)  # pass the FULL item (so the agent can read files)
            answers_payload.append({"task_id": task_id, "submitted_answer": submitted_answer})
            results_log.append({"Task ID": task_id, "Question": question_text, "Submitted Answer": submitted_answer})
        except Exception as e:
            print(f"Error running agent on task {task_id}: {e}")
            results_log.append({"Task ID": task_id, "Question": question_text, "Submitted Answer": f"AGENT ERROR: {e}"})

    if not answers_payload:
        return "Agent did not produce any answers to submit.", pd.DataFrame(results_log)

    submission_data = {"username": username.strip(), "agent_code": agent_code, "answers": answers_payload}
    status_update = f"Agent finished. Submitting {len(answers_payload)} answers for user '{username}'..."
    print(status_update)

    print(f"Submitting {len(answers_payload)} answers to: {submit_url}")
    try:
        response = requests.post(submit_url, json=submission_data, timeout=60)
        response.raise_for_status()
        result_data = response.json()
        final_status = (
            f"Submission Successful!\n"
            f"User: {result_data.get('username')}\n"
            f"Overall Score: {result_data.get('score', 'N/A')}% "
            f"({result_data.get('correct_count', '?')}/{result_data.get('total_attempted', '?')} correct)\n"
            f"Message: {result_data.get('message', 'No message received.')}"
        )
        print("Submission successful.")
        return final_status, pd.DataFrame(results_log)
    except Exception as e:
        status_message = f"Submission Failed: {e}"
        print(status_message)
        return status_message, pd.DataFrame(results_log)


# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("# Basic Agent Evaluation Runner")
    gr.Markdown(
        """
        **Instructions:**
        1. Duplicate this space and modify the agent logic / tools / packages.
        2. Log in to your Hugging Face account using the button below.
        3. Click 'Run Evaluation & Submit All Answers' to fetch questions, run your agent, and see the score.
        """
    )
    gr.LoginButton()
    run_button = gr.Button("Run Evaluation & Submit All Answers")
    status_output = gr.Textbox(label="Run Status / Submission Result", lines=5, interactive=False)
    results_table = gr.DataFrame(label="Questions and Agent Answers", wrap=True)
    run_button.click(fn=run_and_submit_all, outputs=[status_output, results_table])


if __name__ == "__main__":
    print("\n" + "-" * 30 + " App Starting " + "-" * 30)
    space_host_startup = os.getenv("SPACE_HOST")
    space_id_startup = os.getenv("SPACE_ID")
    if space_host_startup:
        print(f"✅ SPACE_HOST found: {space_host_startup}")
    if space_id_startup:
        print(f"✅ SPACE_ID found: {space_id_startup}")
    print("-" * 74 + "\n")
    print("Launching Gradio Interface for Basic Agent Evaluation...")
    demo.launch(debug=True, share=False)
