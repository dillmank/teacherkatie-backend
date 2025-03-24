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
    from datetime import datetime, timedelta

    # Define your real class schedule clearly
    session_times = ['09:00', '10:00', '13:00', '14:00']  # sessions clearly defined
    session_length = timedelta(minutes=45)

    start_date = datetime(2025, 5, 5)
    end_date = datetime(2025, 7, 31)

    # Dates for no classes
    vacation_start = datetime(2025, 6, 30)
    vacation_end = datetime(2025, 7, 3)

    events = []
    current_date = start_date

    while current_date <= end_date:
        # Check if it's Mon-Thu and NOT during vacation
        if current_date.weekday() in [0,1,2,3] and not (vacation_start <= current_date <= vacation_end):
            for session_time in session_times:
                start_dt = datetime.strptime(f"{current_date.date()}T{session_time}", '%Y-%m-%dT%H:%M')
                end_dt = start_dt + session_length

                event = {
                    "title": "Available",
                    "start": start_dt.strftimestart_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
,
                    "end": end_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
                events.append(event)

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

