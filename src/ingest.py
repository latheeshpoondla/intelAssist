import os
import re

def load_documents(folder_path):
    docs = []

    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                docs.append((file, f.read()))

    return docs


def chunk_text(text, source, chunk_size=300):
    # Split text into sentence-like parts (., !, ?, ;, :)
    sentences = re.split(r'(?<=[.!?;:])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Further split using commas
        parts = re.split(r',\s*', sentence)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # If adding this part exceeds chunk size → finalize current chunk
            if len(current_chunk) + len(part) + 1 > chunk_size:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "source": source
                    })
                current_chunk = part
            else:
                if current_chunk:
                    current_chunk += " " + part
                else:
                    current_chunk = part

    # Add last chunk
    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "source": source
        })

    return chunks

if __name__ == "__main__":
    docs = load_documents("data/docs")

    all_chunks = []

    for doc in docs:
        all_chunks.extend(chunk_text(doc))

    print(all_chunks)