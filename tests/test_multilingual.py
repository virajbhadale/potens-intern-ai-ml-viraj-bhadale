from app.rag import generate_answer


query = "एलएलएम में hallucination क्या है?"

result = generate_answer(query)


print("\n" + "=" * 60)
print("ANSWER:\n")

print(result["answer"])


print("\n" + "=" * 60)
print("CITATIONS:\n")

for citation in result["citations"]:

    print(citation)
    print("\n")