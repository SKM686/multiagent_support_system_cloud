import json
import os
from agents.summarizer import summarize_conversation
from agents.action_extractor import extract_actions
from agents.resolution_recommender import recommend_resolution
from agents.router import route_ticket
from agents.time_estimator import estimate_resolution_time

def load_conversations(path='data/conversation_data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_conversation(convo):
    print("Running summarizer...")
    summary = summarize_conversation(convo)
    print("Summary:", summary)

    print("Running action extractor...")
    actions = extract_actions(convo)
    print("Actions:", actions)

    print("Running resolution recommender...")
    resolution = recommend_resolution(
        convo.get("category", ""),
        convo.get("sentiment", ""),
        convo.get("priority", "")
    )
    print("Recommendation:", resolution)

    print("Running router...")
    route = route_ticket(convo)
    print("Route:", route)

    print("Running time estimator...")
    eta = estimate_resolution_time(convo)
    print("ETA:", eta)

    return {
        "summary": summary,
        "actions": actions,
        "recommendation": resolution,
        "route_to": route,
        "estimated_resolution_time": eta
    }

def save_results(results, path='outputs/processed_results.json'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"\nResults saved to {path}")

if __name__ == "__main__":
    conversations = load_conversations()
    all_results = []

    for convo in conversations:
        print(f"\nProcessing Conversation ID: {convo['conversation_id']}")
        result = process_conversation(convo)
        all_results.append(result)

        for key, value in result.items():
            if key != "conversation_id":
                print(f"{key.title()}: {value}")

    save_results(all_results)