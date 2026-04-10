from src.chunking import ChunkingStrategyComparator

files = ["data/1.md", "data/RAG.md"]
comparator = ChunkingStrategyComparator()

for fname in files:
    with open(fname, encoding="utf-8") as f:
        text = f.read()

    print(f"=== {fname} ({len(text)} chars) ===")
    result = comparator.compare(text, chunk_size=200)

    for strategy, stats in result.items():
        print(f"  {strategy}: count={stats['count']}, avg_length={stats['avg_length']}")
    print()
