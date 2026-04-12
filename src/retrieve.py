from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

def retrieve(query, top_k=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    index = faiss.read_index("data/vector.index")

    with open("data/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    
    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype('float32'),
        top_k
    )

    return [chunks[i] for i in indices[0]]