import sqlite3
import csv

# Paths
db_path = 'db/support_tickets.db'
csv_path = 'data/Historical_ticket_data.csv'

# Connect to DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop the existing table (if it exists) and recreate it
cursor.execute('DROP TABLE IF EXISTS tickets')
cursor.execute('''
CREATE TABLE tickets (
    id TEXT PRIMARY KEY,
    category TEXT,
    sentiment TEXT,
    priority TEXT,
    solution TEXT,
    resolution_status TEXT,
    resolution_date TEXT
)
''')

# Load CSV with proper encoding
with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    # Normalize column names by stripping spaces
    reader.fieldnames = [field.strip() for field in reader.fieldnames]
    for row in reader:
        cursor.execute('''
        INSERT OR REPLACE INTO tickets (id, category, sentiment, priority, solution, resolution_status, resolution_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['Ticket ID'].strip(),
            row['Issue Category'].strip(),
            row['Sentiment'].strip(),
            row['Priority'].strip(),
            row['Solution'].strip(),
            row['Resolution Status'].strip(),
            row['Date of Resolution'].strip()
        ))

# Commit and close
conn.commit()
conn.close()
print("Data inserted successfully.")