from app.contradiction import detect_contradiction


result = detect_contradiction(
    "llm_hallucination.pdf",
    "speculative_rag.pdf",
    "hallucination causes"
)

print("\n" + "=" * 60)
print("CONTRADICTION RESULT:\n")

print(result)