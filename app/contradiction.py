from groq import Groq
from dotenv import load_dotenv
import os

from app.rag import retrieve_chunks


# Load environment variables
load_dotenv()


# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def detect_contradiction(doc1, doc2, topic):
    """
    Compare two documents on a topic and
    determine whether they conflict.
    """

    # Retrieve chunks ONLY from document 1
    chunks_doc1 = retrieve_chunks(
        topic,
        top_k=6,
        source_filter=doc1,
        distance_threshold=0.9
    )

    # Retrieve chunks ONLY from document 2
    chunks_doc2 = retrieve_chunks(
        topic,
        top_k=6,
        source_filter=doc2,
        distance_threshold=0.9
    )

    # Hallucination prevention
    if not chunks_doc1 or not chunks_doc2:

        return {
            "conflict": None,
            "reasoning": (
                "The provided documents do not contain enough "
                "relevant information for grounded comparison."
            )
        }

    # Build contexts
    context1 = "\n\n".join(
        [chunk["text"] for chunk in chunks_doc1]
    )

    context2 = "\n\n".join(
        [chunk["text"] for chunk in chunks_doc2]
    )

    prompt = f"""
You are a document comparison assistant.

Compare the following two document contexts.

TOPIC:
{topic}

DOCUMENT 1:
{doc1}

CONTEXT 1:
{context1}

DOCUMENT 2:
{doc2}

CONTEXT 2:
{context2}

Rules:
1. Use ONLY the provided contexts.
2. Do not assume missing information.
3. If comparison is not possible, say so explicitly.
4. Be concise and factual.

Return valid JSON only.

Format:
{{
  "conflict": true/false,
  "reasoning": "..."
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content