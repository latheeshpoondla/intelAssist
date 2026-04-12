from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os
import hashlib

model = SentenceTransformer('all-MiniLM-L6-v2')

INDEX_PATH = "data/vector.index"
CHUNKS_PATH = "data/chunks.pkl"


def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()


def create_or_update_vector_store(new_chunks):
    new_texts = [c["text"] for c in new_chunks]
    new_embeddings = model.encode(new_texts)

    if os.path.exists(INDEX_PATH):
        print("Loading existing index...")

        index = faiss.read_index(INDEX_PATH)

        with open(CHUNKS_PATH, "rb") as f:
            existing_chunks = pickle.load(f)

        existing_hashes = set([c["hash"] for c in existing_chunks])

        filtered_chunks = []
        filtered_embeddings = []

        for chunk, emb in zip(new_chunks, new_embeddings):
            h = get_hash(chunk["text"])

            if h not in existing_hashes:
                chunk["hash"] = h
                filtered_chunks.append(chunk)
                filtered_embeddings.append(emb)

        if filtered_embeddings:
            index.add(np.array(filtered_embeddings).astype('float32'))
            all_chunks = existing_chunks + filtered_chunks
        else:
            print("No new chunks to add.")
            return

    else:
        print("Creating new index...")

        dimension = new_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)

        all_chunks = []
        for chunk, emb in zip(new_chunks, new_embeddings):
            chunk["hash"] = get_hash(chunk["text"])
            all_chunks.append(chunk)

        index.add(np.array(new_embeddings).astype('float32'))

    faiss.write_index(index, INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

    print("Total chunks:", len(all_chunks))