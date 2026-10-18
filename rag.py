
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Paths
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"

# Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_knowledge():
    """Read Markdown files and split them into searchable chunks."""
    chunks = []

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        # Split by sections, keeping useful context
        sections = text.split("\n## ")

        for section in sections:
            section = section.strip()

            if section:
                if not section.startswith("#"):
                    section = "## " + section

                chunks.append(section)

    return chunks


def build_search_index(chunks):
    """Convert knowledge chunks into vectors and index them."""
    if not chunks:
        raise ValueError(
            "No knowledge found. Add Markdown files to the knowledge folder."
        )

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


def search_knowledge(question, index, chunks, top_k=3):
    """Find the most relevant knowledge sections for a question."""
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    question_embedding = np.asarray(
        question_embedding, dtype="float32"
    )

    k = min(top_k, len(chunks))
    scores, indices = index.search(question_embedding, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx >= 0:
            results.append({
                "text": chunks[idx],
                "score": float(score)
            })

    return results


if __name__ == "__main__":
    chunks = load_knowledge()
    index = build_search_index(chunks)

    print(f"\nLoaded {len(chunks)} knowledge sections.")
    print("CodeMate AI semantic search is ready!")

    while True:
        question = input(
            "\nAsk a Python question (or type 'exit' to quit): "
        ).strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        results = search_knowledge(question, index, chunks)

        print("\nRelevant knowledge:")
        for number, result in enumerate(results, start=1):
            print(
                f"\n{number}. Similarity: {result['score']:.3f}"
            )
            print(result["text"])
