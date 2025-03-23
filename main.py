from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Teacher Katie's Flask backend is live!"})

@app.route('/api/health')
def health():
    return jsonify({"status":"healthy"})

@app.route('/api/info')
def info():
    return jsonify({"app":"Teacher Katie API","version":"1.0"})

@app.route('/api/slots')
def slots():
    today = datetime.today()
    events = []
    for i in range(1, 10):  # Generate slots for next 10 days
        slot_date = today + timedelta(days=i)
        event = {
            "title": "Available",
            "start": slot_date.strftime("%Y-%m-%dT16:00:00"), # 4pm slot example
            "end": slot_date.strftime("%Y-%m-%dT17:00:00")    # 1-hour session
        }
        events.append(event)
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

