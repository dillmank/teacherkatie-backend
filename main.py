from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import stripe

app = Flask(__name__)
CORS(app)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  # Set via Render environment variable

@app.route('/')
def home():
    return jsonify({"message": "Teacher Katie's Flask backend is live!"})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/info')
def info():
    return jsonify({"app": "Teacher Katie API", "version": "1.0"})

@app.route('/api/slots')
def slots():
    session_times = ['09:00', '10:00', '13:00', '14:00']  # 24-hour format
    session_length = timedelta(minutes=45)

    # Set the real schedule window
    start_date = datetime(2025, 5, 5)
    end_date = datetime(2025, 7, 31)

    # Vacation window
    vacation_start = datetime(2025, 6, 30)
    vacation_end = datetime(2025, 7, 3)

    events = []
    current_date = start_date

    while current_date <= end_date:
        weekday = current_date.weekday()
        is_vacation = vacation_start.date() <= current_date.date() <= vacation_end.date()
        is_teaching_day = weekday in [0, 1, 2, 3]  # Monday–Thursday

        if is_teaching_day and not is_vacation:
            for time_str in session_times:
                time_parts = [int(t) for t in time_str.split(':')]
                start_dt = current_date.replace(hour=time_parts[0], minute=time_parts[1], second=0)
                end_dt = start_dt + session_length

                events.append({
                    "title": "Available",
                    "start": start_dt.strftime('%Y-%m-%dT%H:%M:%S'),
                    "end": end_dt.strftime('%Y-%m-%dT%H:%M:%S_


