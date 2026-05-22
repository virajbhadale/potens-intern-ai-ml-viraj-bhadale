import os

from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from app.embeddings import collection
from app.prompts import SYSTEM_PROMPT

from app.translation import (
    detect_language,
    translate_to_english,
    translate_from_english
)
import re


# Load environment variables
load_dotenv()


# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# Load embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def retrieve_chunks(query, top_k=4, source_filter=None, distance_threshold=0.75):
    """
    Retrieve relevant chunks from ChromaDB.
    """

    # Convert query to embedding
    query_embedding = embedding_model.encode(
        query
    ).tolist()

    # Build query arguments
    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    # Optional document filtering
    if source_filter:

        query_args["where"] = {
            "source": source_filter
        }

    # Query vector DB
    results = collection.query(**query_args)

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):

        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    # Filter weak retrievals
    filtered_chunks = [
        chunk for chunk in retrieved_chunks
        if chunk["distance"] < distance_threshold
    ]

    return filtered_chunks


def generate_answer(query):
    """
    Generate grounded answer using retrieved chunks.
    """

    # Detect query language
    query_language = detect_language(query)

    # Translate query to English
    english_query = translate_to_english(
        query,
        query_language
    )

    # Retrieve relevant chunks
    retrieved_chunks = retrieve_chunks(
        english_query
    )

    # -----------------------------------
    # Hallucination Prevention
    # -----------------------------------

    # No chunks retrieved
    if not retrieved_chunks:

        return {
            "answer": (
                "The provided documents do not contain enough "
                "information to answer this confidently."
            ),
            "citations": []
        }

    # Find best semantic match
    best_distance = min(
        chunk["distance"]
        for chunk in retrieved_chunks
    )

    # Reject weak retrievals
    if best_distance > 0.7:

        return {
            "answer": (
                "The provided documents do not contain enough "
                "information to answer this confidently."
            ),
            "citations": []
        }

    # -----------------------------------
    # Build Context
    # -----------------------------------

    context = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    )

    # -----------------------------------
    # Generate Answer
    # -----------------------------------

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{english_query}
"""
            }
        ],

        temperature=0.2
    )

    answer = response.choices[0].message.content

    # Remove inline citation markers like [21]
    import re

    answer = re.sub(
        r"\[\d+\]",
        "",
        answer
    )

    # Translate answer back
    final_answer = translate_from_english(
        answer,
        query_language
    )

    # -----------------------------------
    # Build Citations
    # -----------------------------------

    citations = []

    for chunk in retrieved_chunks:

        citations.append({
            "source": chunk["metadata"]["source"],
            "page": chunk["metadata"]["page"],
            "chunk_id": chunk["metadata"]["chunk_id"],
            "snippet": chunk["text"][:300]
        })

    return {
        "answer": final_answer,
        "citations": citations
    }