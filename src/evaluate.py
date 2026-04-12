from retrieve import retrieve
from llm import ask_llm

# Helper function
def check_answer(answer, keywords):
    answer = answer.lower()
    return all(k.lower() in answer for k in keywords)

# Test Cases (20 total)
test_cases = [

    # HR POLICY
    {"q": "How many paid leave days?", "kw": ["20"], "src": "hr_policy.txt"},
    {"q": "What is sick leave limit?", "kw": ["10"], "src": "hr_policy.txt"},
    {"q": "When is medical certificate required?", "kw": ["3"], "src": "hr_policy.txt"},
    {"q": "Can casual leave be carried forward?", "kw": ["cannot"], "src": "hr_policy.txt"},
    {"q": "How many WFH days allowed?", "kw": ["2"], "src": "hr_policy.txt"},
    {"q": "What are office hours?", "kw": ["9", "6"], "src": "hr_policy.txt"},

    # SECURITY POLICY
    {"q": "Password requirement?", "kw": ["12"], "src": "security_policy.txt"},
    {"q": "Is 2FA required?", "kw": ["mandatory"], "src": "security_policy.txt"},
    {"q": "Can we share passwords?", "kw": ["prohibited"], "src": "security_policy.txt"},
    {"q": "What to do for suspicious email?", "kw": ["report"], "src": "security_policy.txt"},
    {"q": "Is VPN required?", "kw": ["vpn"], "src": "security_policy.txt"},

    # BENEFITS
    {"q": "When does health insurance start?", "kw": ["first day"], "src": "benifits.txt"},
    {"q": "What is travel allowance?", "kw": ["5000"], "src": "benifits.txt"},
    {"q": "Gym reimbursement amount?", "kw": ["2000"], "src": "benifits.txt"},
    {"q": "How many public holidays?", "kw": ["12"], "src": "benifits.txt"},

    # PROJECT DOC
    {"q": "What does the system use?", "kw": ["natural language"], "src": "project_doc.txt"},
    {"q": "Main components?", "kw": ["query", "retrieval", "response"], "src": "project_doc.txt"},
    {"q": "Future improvements?", "kw": ["multilingual"], "src": "project_doc.txt"},

    # ML SYSTEM
    {"q": "What are ML pipeline steps?", "kw": ["preprocessing", "training"], "src": "ml_system.txt"},
    {"q": "Which model is used?", "kw": ["gradient boosting"], "src": "ml_system.txt"},
]


# Evaluation
retrieval_correct = 0
answer_correct = 0

for i, t in enumerate(test_cases, 1):
    results = retrieve(t["q"], top_k=3)
    sources = [r["source"] for r in results]

    # Retrieval check
    if t["src"] in sources:
        retrieval_correct += 1

    context = "\n".join([r["text"] for r in results])
    answer = ask_llm(context, t["q"])

    # Answer check
    if check_answer(answer, t["kw"]):
        answer_correct += 1

# Final Scores
total = len(test_cases)

print("\n==============================")
print("FINAL RESULTS")
print("==============================")

print(f"Retrieval Accuracy: {retrieval_correct}/{total} = {retrieval_correct/total:.2f}")
print(f"Answer Accuracy: {answer_correct}/{total} = {answer_correct/total:.2f}")