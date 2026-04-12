import requests


def ask_llm(context, question):
    prompt = f"""
        Use ONLY the context below to answer.

        Context:
        {context}

        Question:
        {question}
        """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]