from flask import Flask, jsonify, request, render_template_string
from characterai import PyCAI
from datetime import datetime, timedelta
import logging

app = Flask(__name__, template_folder='.')

client = PyCAI('29422450f9ebdf864bb798a6f9796cdab019d9f1')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define keys and their cooldown periods (in seconds)
KEYS = {
    "GakModalYa": {"cooldown": 60, "last_used": datetime.min},  # 1 minute cooldown
    "PunyaOwnNihBos": {"cooldown": 0, "last_used": datetime.min},  # No cooldown
    "CAI2024": {"cooldown": 10, "last_used": datetime.min},
    "UPPremiumCAI": {"cooldown": 2, "last_used": datetime.min}
}

# Check if the key is valid and not in cooldown period
def check_key(key):
    if key in KEYS:
        now = datetime.now()
        last_used = KEYS[key]['last_used']
        cooldown = timedelta(seconds=KEYS[key]['cooldown'])
        
        if key == "PunyaOwnNihBos" or now - last_used >= cooldown:
            KEYS[key]['last_used'] = now
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

@app.route('/key')
def list_keys():
    now = datetime.now()
    keys_status = {
        key: {
            "cooldown": KEYS[key]['cooldown'],
            "last_used": KEYS[key]['last_used'],
            "next_available": KEYS[key]['last_used'] + timedelta(seconds=KEYS[key]['cooldown'])
        }
        for key in KEYS
    }
    
    table_html = """
    <html>
    <head>
        <title>API Keys</title>
        <style>
            table {
                width: 50%;
                border-collapse: collapse;
                margin: 50px auto;
                font-family: Arial, sans-serif;
                font-size: 18px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h2 style="text-align: center;">API Keys and Cooldown Periods</h2>
        <table>
            <tr>
                <th>Key</th>
                <th>Cooldown (seconds)</th>
                <th>Last Used</th>
                <th>Next Available</th>
            </tr>
    """
    for key, status in keys_status.items():
        table_html += f"""
            <tr>
                <td>{key}</td>
                <td>{status['cooldown']}</td>
                <td>{status['last_used']}</td>
                <td>{status['next_available']}</td>
            </tr>
        """
    table_html += """
        </table>
    </body>
    </html>
    """
    return render_template_string(table_html)

@app.route('/api/search')
def search_character():
    key = request.args.get('key', 'GakModalYa')  # Default to GakModalYa if no key provided
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or cooldown period has not passed'}), 403

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
    key = request.args.get('key', 'GakModalYa')  # Default to GakModalYa if no key provided
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or cooldown period has not passed'}), 403

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
    key = request.args.get('key', 'GakModalYa')  # Default to GakModalYa if no key provided
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or cooldown period has not passed'}), 403

    try:
        trending = client.character.trending()
        return jsonify(trending), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during fetching trending characters")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rec')
def rec_characters():
    key = request.args.get('key', 'GakModalYa')  # Default to GakModalYa if no key provided
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or cooldown period has not passed'}), 403

    try:
        rec = client.character.recommended()
        return jsonify(rec), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logging.exception("Error during fetching recommended characters")
        return jsonify({'error': str(e)}), 500

@app.route('/api/info')
def info_character():
    key = request.args.get('key', 'GakModalYa')  # Default to GakModalYa if no key provided
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or cooldown period has not passed'}), 403

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
    key = request.args.get('key', 'GakModalYa')  # Default to GakModalYa if no key provided
    if not check_key(key):
        logging.warning(f"Invalid or missing key: {key}")
        return jsonify({'error': 'Valid key is required or cooldown period has not passed'}), 403

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
