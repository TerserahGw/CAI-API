from flask import Flask, jsonify, request, render_template
from characterai import PyCAI
from datetime import datetime, timedelta
import logging

app = Flask(__name__, template_folder='.')

client = PyCAI('29422450f9ebdf864bb798a6f9796cdab019d9f1')

logging.basicConfig(level=logging.DEBUG)

KEYS = {
    "GUESTAI": {"limit": 5, "reset_time": timedelta(seconds=15), "count": 0, "last_reset": datetime.now()},
    "OWNONLY": {"limit": float('inf'), "reset_time": timedelta(seconds=0), "count": 0, "last_reset": datetime.now()},
    "CAI2024": {"limit": 50, "reset_time": timedelta(seconds=5), "count": 0, "last_reset": datetime.now()},
    "USERCAI": {"limit": 500, "reset_time": timedelta(seconds=1), "count": 0, "last_reset": datetime.now()}
}

def check_key(key):
    if not key:
        key = "GUESTAI"
    if key in KEYS:
        now = datetime.now()
        key_info = KEYS[key]

        # Reset the count if the reset time has passed
        if now - key_info['last_reset'] >= key_info['reset_time']:
            key_info['count'] = 0
            key_info['last_reset'] = now

        if key_info['count'] < key_info['limit']:
            key_info['count'] += 1
            return True
    return False

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/api')
def home():
    return render_template('oldhome.html')

@app.route('/home')
def api():
    return render_template('home.html')

@app.route('/api/search')
def search_character():
    key = request.args.get('key')
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or rate limit exceeded'}), 403

    query = request.args.get('q', '')
    if not query:
        logging.error("Query parameter is missing")
        return jsonify({'error': 'Query is required'}), 400

    try:
        results = client.character.search(query)
        return jsonify(results), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during character search")
        return jsonify({'error': str(e)}), 500

@app.route('/api/newchat')
def new_chat():
    key = request.args.get('key')
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or rate limit exceeded'}), 403

    char_id = request.args.get('q', '')
    if not char_id:
        logging.error("Character ID parameter is missing")
        return jsonify({'error': 'Character ID is required'}), 400

    try:
        data = client.chat.new_chat(char_id)
        return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during new chat creation")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trending')
def trending_characters():
    key = request.args.get('key')
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or rate limit exceeded'}), 403

    try:
        trending = client.character.trending()
        return jsonify(trending), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during fetching trending characters")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rec')
def rec_characters():
    key = request.args.get('key')
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or rate limit exceeded'}), 403

    try:
        rec = client.character.recommended()
        return jsonify(rec), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during fetching recommended characters")
        return jsonify({'error': str(e)}), 500

@app.route('/api/info')
def info_character():
    key = request.args.get('key')
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or rate limit exceeded'}), 403

    char_id = request.args.get('id', '')
    if not char_id:
        logging.error("Character ID parameter is missing")
        return jsonify({'error': 'Character ID is required'}), 400

    try:
        info = client.character.info(char_id)
        return jsonify(info), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during fetching character info")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cai')
def cai_chat():
    key = request.args.get('key')
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or rate limit exceeded'}), 403

    char_id = request.args.get('charid', '')
    message = request.args.get('message', '')

    if not char_id:
        logging.error("Character ID parameter is missing")
        return jsonify({'error': 'Character ID is required'}), 400
    if not message:
        logging.error("Message parameter is missing")
        return jsonify({'error': 'Message is required'}), 400

    try:
        chat = client.chat.get_chat(char_id)
        participants = chat['participants']

        if not participants[0]['is_human']:
            tgt = participants[0]['user']['username']
        else:
            tgt = participants[1]['user']['username']

        data = client.chat.send_message(chat['external_id'], tgt, message)

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        return jsonify({'name': name, 'reply': text}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during chat interaction")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
