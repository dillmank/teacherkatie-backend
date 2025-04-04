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
                    "end": end_dt.strftime('%Y-%m-%dT%H:%M:%S')
                })

        current_date += timedelta(days=1)

    return jsonify(events)


@app.route('/api/create-checkout-session', methods=['POST'])
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json
    sessions = data.get('sessions', [])
    quantity = len(sessions)

    if quantity == 0:
        return jsonify({'error': 'No sessions selected'}), 400

    customer_email = data['email']
    student_name = data['name']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Tutoring Session'},
                'unit_amount': 3000,
            },
            'quantity': quantity,
        }],
        mode='payment',
        customer_email=customer_email,
        allow_promotion_codes=True,
        success_url='https://www.teacherkatie.org/success.html',
        cancel_url='https://www.teacherkatie.org/cancel.html',
        metadata={
            'student_name': student_name,
            'session_datetimes': ','.join(sessions)
        }
    )

    # Brevo SMTP email sending clearly
    smtp_server = os.getenv('BREVO_SMTP_SERVER')
    smtp_port = int(os.getenv('BREVO_SMTP_PORT'))
    smtp_user = os.getenv('BREVO_SMTP_USERNAME')
    smtp_pass = os.getenv('BREVO_SMTP_PASSWORD')

    subject = "Your Tutoring Sessions Confirmation"
    sender_email = smtp_user
    receiver_email = customer_email

    # Email content clearly formatted
    session_list = "\n".join([
        f"- {datetime.fromisoformat(dt).strftime('%A, %B %d, %Y %I:%M %p')}" for dt in sessions
    ])

    email_body = f"""
    Hello {student_name},

    Your tutoring sessions have been successfully booked!

    Sessions booked:
    {session_list}

    Thank you!
    Teacher Katie
    """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(email_body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")  # logs clearly in Render

    return jsonify({'id': session.id})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


