import sys
import os
import json
import streamlit as st

# Add parent directory to the system path so modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.summarizer import summarize_conversation
from agents.action_extractor import extract_actions
from agents.resolution_recommender import recommend_resolution
from agents.router import route_ticket
from agents.time_estimator import estimate_resolution_time


# Load conversations
@st.cache_data
def load_conversations(path='data/conversation_data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Process single conversation
def process_conversation(convo):
    summary = summarize_conversation(convo)
    actions = extract_actions(convo)
    recommendation = recommend_resolution(
        convo.get("category", ""),
        convo.get("sentiment", ""),
        convo.get("priority", "")
    )
    route = route_ticket(convo)
    eta = estimate_resolution_time(convo)

    return {
        "Summary": summary,
        "Actions": actions,
        "Recommendation": recommendation,
        "Route To": route,
        "Estimated Resolution Time": eta
    }

# Streamlit UI
st.set_page_config(page_title="AI Support Assistant", layout="wide")
st.title("Multi-Agent AI Customer Support Assistant")

conversations = load_conversations()

convo_ids = [convo["conversation_id"] for convo in conversations]
selected_id = st.selectbox("Select a Conversation ID", convo_ids)

selected_convo = next(c for c in conversations if c["conversation_id"] == selected_id)

if st.button("Process Conversation"):
    with st.spinner("Processing with all agents..."):
        result = process_conversation(selected_convo)

    st.subheader("Conversation Summary")
    st.write(result["Summary"])

    st.subheader("Action Items")
    st.write(result["Actions"])

    st.subheader("Recommended Resolution")
    st.write(result["Recommendation"])

    st.subheader("Route Ticket To")
    st.write(result["Route To"])

    st.subheader("Estimated Resolution Time")
    st.write(result["Estimated Resolution Time"])