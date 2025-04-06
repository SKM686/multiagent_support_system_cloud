from utils.ollama_client import query_ollama

def estimate_resolution_time(convo):
    text = " ".join([f"{x['sender']}: {x['message']}" for x in convo['dialogue']])
    prompt = f"Estimate the time (in hours) it will take to resolve the issue described in this conversation:\n{text}"
    return query_ollama(prompt)