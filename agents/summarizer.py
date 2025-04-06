from utils.ollama_client import query_ollama

def summarize_conversation(convo):
    text = " ".join([f"{x['sender']}: {x['message']}" for x in convo['dialogue']])
    prompt = f"Summarize this customer support conversation:\n{text}"
    return query_ollama(prompt)