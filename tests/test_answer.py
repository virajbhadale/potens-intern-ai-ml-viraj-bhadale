from app.rag import generate_answer


query = "What are hallucinations in large language models?"

result = generate_answer(query)


print("\n" + "=" * 60)
print("ANSWER:\n")

print(result["answer"])


print("\n" + "=" * 60)
print("CITATIONS:\n")

for citation in result["citations"]:

    print(citation)
    print("\n")