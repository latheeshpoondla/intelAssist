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

# # Code for Meta llama3.1 8B Intruct hugging-face
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# MODEL_PATH = r"D:\Latheesh\Projects\dsmlai_projects\intelAssist\models\Meta-Llama3.1-8B-Instruct"

# # Load once (IMPORTANT)
# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_PATH,
#     device_map="auto",   # CPU/GPU auto
#     dtype=torch.float32
# )

# device = torch.device("cpu")
# model.to(device)

# def ask_llm(context, question):
    
#     prompt = f"""
# You are an intelligent assistant.
# Answer ONLY from the given context.

# Context:
# {context}

# Question:
# {question}
# """

#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=200,
#             temperature=0.7,
#             do_sample=True

#         )

#     return tokenizer.decode(outputs[0], skip_special_tokens=True)