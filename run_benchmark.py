"""Run 5 benchmark queries with SentenceChunker + OpenAI embeddings."""
import os
from dotenv import load_dotenv
load_dotenv()

from src.chunking import SentenceChunker
from src.embeddings import OpenAIEmbedder
from src.models import Document
from src.store import EmbeddingStore

embedder = OpenAIEmbedder()
chunker = SentenceChunker(max_sentences_per_chunk=3)

# Load all data files
data_files = {
    "1.md": {"topic": "evaluation", "lang": "vi"},
    "AI1.md": {"topic": "application", "lang": "en"},
    "hermes-agent-pricing-accuracy-architecture-design.md": {"topic": "architecture", "lang": "en"},
    "machine_learning_guide.md": {"topic": "machine_learning", "lang": "en"},
    "fast_api.md": {"topic": "rag", "lang": "vi"},
}

documents = []
for fname, meta in data_files.items():
    with open(f"data/{fname}", encoding="utf-8") as f:
        text = f.read()
    chunks = chunker.chunk(text)
    for i, chunk in enumerate(chunks):
        documents.append(Document(
            id=f"{fname}_chunk_{i}",
            content=chunk,
            metadata={**meta, "source": fname},
        ))

store = EmbeddingStore(collection_name="benchmark", embedding_fn=embedder)
store.add_documents(documents)
print(f"Store size: {store.get_collection_size()} chunks\n")

queries = [
    "What does Hermes do to handle cache billing correctly?",
    "What are the four layers in the high-level pricing architecture?",
    "When should the UI show 'included' instead of an estimated dollar amount?",
    "In the ML guide, what are the three main machine learning paradigms?",
    "In the FastHTML tutorial, what is HTMX used for?",
]

for i, q in enumerate(queries, 1):
    print(f"=== Query {i}: {q} ===")
    results = store.search(q, top_k=3)
    for rank, r in enumerate(results, 1):
        source = r.get("metadata", {}).get("source", "?")
        score = r["score"]
        preview = r["content"][:120].replace("\n", " ")
        print(f"  Top-{rank} [{source}] score={score:.4f}: {preview}...")
    print()
