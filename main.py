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
from datetime import datetime, timedelta

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
                    "end": end_dt.strftime('%Y-%m-%dT%H:%M:%S')
                })

        current_date += timedelta(days=1)

    return jsonify(events)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import stripe
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  # Set via Render environment variable

@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Tutoring Session'},
                'unit_amount': 3500,  # $35 example session
            },
            'quantity': 1,
        }],
        mode='payment',
        customer_email=data['email'],
        success_url='https://www.teacherkatie.org/success.html',
        cancel_url='https://www.teacherkatie.org/cancel.html',
        metadata={
            'student_name': data['name'],
            'session_datetime': data['session_datetime']
        }
    )
    return jsonify({'id': session.id})

# Existing routes remain the same...

@app.route('/api/slots')
def slots():
    today = datetime.today()
    events = []
    for i in range(1, 10):
        slot_date = today + timedelta(days=i)
        event = {
            "title": "Available",
            "start": slot_date.strftime("%Y-%m-%dT16:00:00"),
            "end": slot_date.strftime("%Y-%m-%dT17:00:00")
        }
        events.append(event)
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

