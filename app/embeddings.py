from sentence_transformers import SentenceTransformer
import chromadb


# Load embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="vectorstore"
)


# Create or load collection
collection = chroma_client.get_or_create_collection(
    name="rag_collection"
)


def store_embeddings(chunks):
    """
    Generate embeddings and store them in ChromaDB.
    """

    documents = []
    metadatas = []
    ids = []

    for idx, chunk in enumerate(chunks):

        documents.append(chunk["text"])

        metadatas.append(chunk["metadata"])

        ids.append(f"chunk_{idx}")

    # Generate embeddings
    embeddings = embedding_model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    # Store in ChromaDB
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"\nStored {len(documents)} chunks in ChromaDB.")