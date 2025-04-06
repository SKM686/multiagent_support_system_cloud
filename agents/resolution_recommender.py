import sqlite3
from utils.ollama_client import query_ollama

DB_PATH = 'data/support_tickets.db'

def recommend_resolution(category, sentiment, priority):
    """
    Recommend resolution from historical data using category/sentiment/priority match
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT solution FROM tickets
        WHERE category = ? AND sentiment = ?
        ORDER BY 
            CASE priority
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END
        LIMIT 5
    ''', (category, sentiment))

    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No similar past solutions found."

    past_solutions = "\n".join(f"- {r[0]}" for r in results if r[0].strip())
    prompt = (
        f"Based on similar support tickets in category '{category}', sentiment '{sentiment}', and priority '{priority}', "
        f"recommend a suitable resolution.\n\nPast Solutions:\n{past_solutions}\n\nRecommended Resolution:"
    )

    return query_ollama(prompt)
