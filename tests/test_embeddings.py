from app.ingestion import load_pdfs
from app.chunking import chunk_documents
from app.embeddings import store_embeddings


# Step 1: Load PDFs
documents = load_pdfs()

# Step 2: Chunk documents
chunks = chunk_documents(documents)

# Step 3: Store embeddings
store_embeddings(chunks)