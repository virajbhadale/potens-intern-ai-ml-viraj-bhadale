from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    """
    Split documents into smaller overlapping chunks
    while preserving metadata.

    Also filters:
    - extremely small chunks
    - bibliography/reference-heavy chunks
    """

    # Chunking configuration
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunked_documents = []

    # Process each document
    for doc in documents:

        # Split text into chunks
        chunks = text_splitter.split_text(doc["text"])

        # Store chunks with metadata
        for idx, chunk in enumerate(chunks):

            # Remove empty/tiny chunks
            if len(chunk.strip()) < 100:
                continue

            # Skip bibliography/reference-heavy chunks
            reference_indicators = [
                "references",
                "bibliography",
                "arxiv",
                "et al.",
                "proceedings of",
                "conference on",
                "journal of"
            ]

            citation_density = chunk.count("[") + chunk.count("]")

            if citation_density > 6:
                continue

            if any(indicator in chunk.lower() for indicator in reference_indicators):
                continue

            chunked_documents.append({
                "text": chunk.strip(),
                "metadata": {
                    "source": doc["metadata"]["source"],
                    "page": doc["metadata"]["page"],
                    "chunk_id": idx
                }
            })

    return chunked_documents