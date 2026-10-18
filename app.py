
from flask import Flask, render_template, request
from rag import load_knowledge, build_search_index, search_knowledge
from code_runner import run_python_code
import json
import urllib.request
import urllib.error

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5-coder:3b"

# Load the knowledge base and build the search index
print("Loading CodeMate AI knowledge base...")
chunks = load_knowledge()
index = build_search_index(chunks)
print("CodeMate AI is ready!")


def generate_answer(question, context):
    """Generate an answer using the local Ollama model."""

   
    prompt = f"""
Answer the user's question using the knowledge provided below.

Knowledge:
{context}

User question:
{question}

Instructions:
- Give a short, beginner-friendly answer.
- Start with a simple explanation in 2-3 sentences.
- Include one small, complete Python example in a fenced code block.
- Show the expected output in a separate code block.
- Explain the example in no more than 2 short bullet points.
- Use simple headings such as Explanation, Example, and Output.
- Keep the answer concise and avoid repetition.
- Put headings on separate lines.
- Prefer the supplied knowledge and do not invent facts.
- If the knowledge does not contain the answer, say so honestly.
"""


    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are CodeMate AI, a helpful Python coding tutor. "
                    "Use the supplied knowledge to answer accurately."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["message"]["content"]


@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            try:
                results = search_knowledge(question, index, chunks)

                if results:
                    context = "\n\n".join(
                        result["text"] for result in results
                    )
                    answer = generate_answer(question, context)
                else:
                    answer = (
                        "I couldn't find relevant information in the "
                        "knowledge base to answer your question."
                    )

            except urllib.error.URLError:
                answer = (
                    "I couldn't connect to Ollama. Please check that "
                    "Ollama is running on your computer."
                )
            except Exception as error:
                print("Error generating answer:", error)
                answer = (
                    "Sorry, something went wrong while generating "
                    "the answer. Check the VS Code terminal for details."
                )

    return render_template(
        "index.html",
        answer=answer,
        question=question
    )



@app.route("/run-code", methods=["POST"])
def run_code():
    code = request.form.get("code", "")
    result = run_python_code(code, timeout=5)
    return result


if __name__ == "__main__":
    app.run(debug=True)
