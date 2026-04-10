from src.embeddings import OpenAIEmbedder
from src.chunking import compute_similarity
from dotenv import load_dotenv

load_dotenv()

e = OpenAIEmbedder(model_name="text-embedding-3-small")

pairs = [
    ("Python là ngôn ngữ lập trình bậc cao dễ học.",
     "Python là một ngôn ngữ lập trình phổ biến, thân thiện với người mới."),

    ("Machine learning uses algorithms to learn from data.",
     "Deep learning is a subset of machine learning."),

    ("Python là ngôn ngữ lập trình bậc cao dễ học.",
     "Hôm nay trời rất đẹp, trời nắng ấm."),

    ("Vector databases store embeddings for similarity search.",
     "The cat sat on the mat."),

    ("RAG retrieves relevant documents before generating answers.",
     "Retrieval-augmented generation improves LLM accuracy."),
]

print("Pair | Sentence A | Sentence B | Score")
print("-----|-----------|-----------|------")
for i, (a, b) in enumerate(pairs, 1):
    score = compute_similarity(e(a), e(b))
    print(f"  {i}  | {a[:50]}... | {b[:50]}... | {score:.4f}")
