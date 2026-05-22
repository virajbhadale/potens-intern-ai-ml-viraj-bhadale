from app.rag import retrieve_chunks


query = "What causes hallucinations in large language models?"

results = retrieve_chunks(query)


print("\n" + "=" * 60)
print(f"Retrieved {len(results)} chunks\n")


for idx, result in enumerate(results):

    print("=" * 60)
    print(f"RESULT {idx + 1}\n")

    print(result["text"][:800])

    print("\nMETADATA:")
    print(result["metadata"])

    print("\nDISTANCE:")
    print(result["distance"])