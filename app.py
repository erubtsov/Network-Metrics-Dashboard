from flask import Flask, jsonify, render_template
import sqlite3
import os

# Define the path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'network_metrics.db')

app = Flask(__name__)

def get_metrics():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10")
            data = cursor.fetchall()
            
            # Print database content to console for debugging
            print("Database content:")
            for row in data:
                print(row)
            
            return [{'timestamp': row[0], 'latency': row[1], 'packet_loss': row[2]} for row in data]
    except sqlite3.Error as e:
        print(f"Error fetching data from database: {e}")
        return []

@app.route('/metrics', methods=['GET'])
def metrics():
    data = get_metrics()
    print(f"Sending data to front end: {data}")  # Print data to check if it matches
    return jsonify(data)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    print(f"Using database file: {DB_PATH}")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
