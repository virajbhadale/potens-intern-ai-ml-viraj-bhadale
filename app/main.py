from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import generate_answer
from app.contradiction import detect_contradiction


app = FastAPI(
    title="Potens RAG System"
)


# -----------------------------
# Request Models
# -----------------------------

class AskRequest(BaseModel):
    query: str


class ContradictRequest(BaseModel):
    doc1: str
    doc2: str
    topic: str


# -----------------------------
# Ask Endpoint
# -----------------------------

@app.post("/ask")
def ask_question(request: AskRequest):

    result = generate_answer(
        request.query
    )

    return result


# -----------------------------
# Contradict Endpoint
# -----------------------------

@app.post("/contradict")
def contradict_documents(
    request: ContradictRequest
):

    result = detect_contradiction(
        request.doc1,
        request.doc2,
        request.topic
    )

    return {
        "result": result
    }


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def root():

    return {
        "message": "Potens AI/ML RAG System Running"
    }