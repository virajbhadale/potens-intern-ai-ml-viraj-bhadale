import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Potens RAG System",
    layout="wide"
)


# -----------------------------------
# Title
# -----------------------------------

st.title("📚 Potens AI/ML RAG System")

st.markdown("""
### Document-Grounded Multilingual RAG System

Features:
- Semantic retrieval using ChromaDB
- Grounded answer generation using Groq
- Citation-based responses
- Multilingual question answering
- Contradiction analysis
- Hallucination prevention
""")


# -----------------------------------
# Tabs
# -----------------------------------

tab1, tab2 = st.tabs([
    "Ask Questions",
    "Contradiction Checker"
])


# ===================================
# TAB 1 — ASK QUESTIONS
# ===================================

with tab1:

    st.header("Ask Questions")

    query = st.text_area(
        "Enter your question",
        height=120,
        placeholder="Ask anything from the documents..."
    )

    if st.button("Generate Answer"):

        if query.strip():

            with st.spinner("Generating answer..."):

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "query": query
                    }
                )

                result = response.json()

                # Answer
                st.subheader("Answer")

                if "do not contain enough information" in result["answer"]:     
                    st.warning(result["answer"])

                else:
                    st.success(result["answer"])

                # Citations
                st.subheader("Citations")

                for citation in result["citations"]:

                    with st.expander(
                        f'{citation["source"]} | '
                        f'Page {citation["page"]}'
                    ):

                        st.markdown(
                            f"**Chunk ID:** "
                            f'{citation["chunk_id"]}'
                        )

                        st.code(
                            citation["snippet"],
                            language="text"
                        )

        else:
            st.warning(
                "Please enter a question."
            )


# ===================================
# TAB 2 — CONTRADICTION CHECKER
# ===================================

with tab2:

    st.header("Contradiction Checker")

    doc1 = st.text_input(
        "Document 1",
        value="llm_hallucination.pdf"
    )

    doc2 = st.text_input(
        "Document 2",
        value="sufficient_context.pdf"
    )

    topic = st.text_input(
        "Topic",
        value="hallucination mitigation"
    )

    if st.button("Check Contradiction"):

        with st.spinner("Analyzing documents..."):

            response = requests.post(
                f"{API_URL}/contradict",
                json={
                    "doc1": doc1,
                    "doc2": doc2,
                    "topic": topic
                }
            )

            result = response.json()

            st.subheader(
                "Contradiction Analysis"
            )

            st.json(result["result"])

            st.markdown("---")

            st.caption(
                "Built for Potens AI/ML Internship Take-Home Assignment"
            )