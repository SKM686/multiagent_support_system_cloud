from utils.ollama_client import query_ollama

def route_ticket(convo):
    text = " ".join([f"{x['sender']}: {x['message']}" for x in convo['dialogue']])
    prompt = f"Which internal team should handle this issue? Choose from: Support, Technical, Billing, Escalation.\nConversation:\n{text}"
    return query_ollama(prompt)