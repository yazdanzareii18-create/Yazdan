import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import time

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

messages_db = []
cases_db = []

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    code = str(data.get('code'))
    if code == '612':
        return jsonify({"status": "admin"})
    elif code == '512':
        return jsonify({"status": "user"})
    else:
        return jsonify({"status": "error"}), 401

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'POST':
        data = request.json
        if data and 'user' in data and 'text' in data:
            messages_db.append({"user": data['user'], "text": data['text']})
            return jsonify({"status": "success"}), 201
        return jsonify({"status": "error"}), 400
    else:
        return jsonify(messages_db)

@app.route('/api/case/create', methods=['POST'])
def create_case():
    data = request.json
    if data and 'user1' in data and 'user2' in data and 'reason' in data:
        deadline = time.time() + 3600 
        new_case = {
            "user1": data['user1'],
            "user2": data['user2'],
            "reason": data['reason'],
            "status": "open",
            "deadline": deadline
        }
        cases_db.append(new_case)
        return jsonify({"status": "success", "message": "احضاریه ارسال شد. ۱ ساعت فرصت دارند."}), 201
    return jsonify({"status": "error"}), 400

@app.route('/api/case/check', methods=['GET'])
def check_cases():
    current_time = time.time()
    for case in cases_db:
        if case['status'] == 'open' and current_time > case['deadline']:
            case['status'] = 'expired'
            messages_db.append({
                "user": "سیستم شورا", 
                "text": f"⏰ زمان احضاریه {case['user1']} و {case['user2']} به پایان رسید! لطفا به دفتر شورا مراجعه کنند."
            })
    return jsonify({"status": "checked", "cases": cases_db})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
