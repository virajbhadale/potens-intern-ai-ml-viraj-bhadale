from app.ingestion import load_pdfs
from app.chunking import chunk_documents

documents = load_pdfs()

chunks = chunk_documents(documents)

print(f"\nTotal chunks created: {len(chunks)}")

print("\nSample Chunk:\n")
print(chunks[0]["text"])

print("\nMetadata:")
print(chunks[0]["metadata"])