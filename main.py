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
                'unit_amount': 2500,  # $25 example session
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

