from ingest import load_documents, chunk_text
from embed_store import create_or_update_vector_store
from retrieve import retrieve
from llm import ask_llm

docs = load_documents("data/docs")

chunks = []

for filename, doc in docs:
    chunks.extend(chunk_text(doc, filename))

create_or_update_vector_store(chunks)

query = input("Ask your question: ")

results = retrieve(query)

context = "\n".join([r["text"] for r in results])

answer = ask_llm(context, query)

print("\nANSWER:\n")
print(answer)

print("\nSOURCE:\n")
print(results)