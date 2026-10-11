"""Day 8: inspect relevant and irrelevant retrieval scores before setting MAX_DISTANCE."""
from lc_config import EMBED_PROVIDER, get_vectorstore

store = get_vectorstore()
questions = [
    "What CGPA do I need to be eligible for placements?",
    "What is the capital of France?",
    "How much is the late fee for paying fees after the due date?",
    "Can I write the exam with 70% attendance?",
]

print(f"Embedding provider: {EMBED_PROVIDER}")
for query in questions:
    print(f"\nQ: {query}")
    for doc, score in store.similarity_search_with_score(query, k=3):
        print(f"  {score:.3f}  [{doc.metadata.get('source', 'unknown')}]  {doc.page_content[:120]!r}")

print("\nFiltered to library.md:")
for doc in store.similarity_search("fine for late return", k=2, filter={"source": "library.md"}):
    print("  ", doc.metadata["source"], "->", doc.page_content[:80].replace("\n", " "))
