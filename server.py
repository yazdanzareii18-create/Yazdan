import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

messages_db = []

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
