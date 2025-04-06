from utils.ollama_client import query_ollama

def extract_actions(convo):
    text = " ".join([f"{x['sender']}: {x['message']}" for x in convo['dialogue']])
    prompt = f"Extract key action items (e.g., escalate, restart, rollback) from this conversation:\n{text}"
    return query_ollama(prompt)