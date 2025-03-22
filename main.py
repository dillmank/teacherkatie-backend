from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
