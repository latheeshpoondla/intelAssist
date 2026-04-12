import streamlit as st
from ingest import load_documents, chunk_text
from embed_store import create_or_update_vector_store
from retrieve import retrieve
from llm import ask_llm
import os

st.title("🧠 Intel Assist - AI Knowledge Assistant")

if not (os.path.exists("data/vector.index") and os.path.exists("data/chunks.pkl")):
    docs = load_documents("data/docs")

    chunks = []

    for filename, doc in docs:
        chunks.extend(chunk_text(doc, filename))

    create_or_update_vector_store(chunks)

# Upload files
uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        content = file.read().decode("utf-8")

        chunks = chunk_text(content, file.name)
        create_or_update_vector_store(chunks)

    st.success("Documents added successfully!")

# Query
query = st.text_input("Ask a question")

if query:
    results = retrieve(query)

    context = "\n".join([r["text"] for r in results])

    answer = ask_llm(context, query)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")
    for r in results:
        st.write(f"📄 {r['source']}: {r['text']}")