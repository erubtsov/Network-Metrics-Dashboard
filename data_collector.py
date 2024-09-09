import sqlite3
from datetime import datetime, timezone
import random
import time
import os

# Define the path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'network_metrics.db')

def simulate_metrics():
    latency = random.randint(20, 100)  # Latency between 20ms and 100ms
    packet_loss = random.uniform(0.0, 5.0)  # Packet loss between 0% and 5%
    timestamp = datetime.now(timezone.utc).isoformat()  # Generate new timestamp
    print(f"Generated data: timestamp={timestamp}, latency={latency}, packet_loss={packet_loss}")
    return timestamp, latency, packet_loss

def insert_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metriscs (
                    timestamp TEXT,
                    latency INTEGER,
                    packet_loss FLOAT
                )
            ''')
            data = simulate_metrics()
            cursor.execute('INSERT INTO metrics (timestamp, latency, packet_loss) VALUES (?, ?, ?)', data)
            conn.commit()
            print(f"Data inserted successfully: {data}")
    except sqlite3.Error as e:
        print(f"Error inserting data into database: {e}")

if __name__ == "__main__":
    while True:
        print(f"Using database file: {DB_PATH}")
        insert_data()
        time.sleep(10)  # Insert new data every 10 seconds
