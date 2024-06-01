from flask import Flask, jsonify, request, render_template
from characterai import PyCAI
import json
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

app = Flask(__name__, template_folder='.')

client = PyCAI('29422450f9ebdf864bb798a6f9796cdab019d9f1')

# Load API keys from JSON file
def load_api_keys():
    if not os.path.exists('api_keys.json'):
        return {}
    with open('api_keys.json', 'r') as f:
        return json.load(f)

# Save API keys to JSON file
def save_api_keys(api_keys):
    with open('api_keys.json', 'w') as f:
        json.dump(api_keys, f, indent=4)

# Check if the API key is valid and update usage
def check_api_key(api_key):
    api_keys = load_api_keys()
    if api_key in api_keys:
        if api_keys[api_key]['limit'] == -1 or api_keys[api_key]['usage'] < api_keys[api_key]['limit']:
            if api_keys[api_key]['limit'] != -1:
                api_keys[api_key]['usage'] += 1
            save_api_keys(api_keys)
            return True
    return False

# Reset usage count for all API keys at 12 PM WIB
def reset_api_keys():
    api_keys = load_api_keys()
    for key in api_keys:
        api_keys[key]['usage'] = 0
    save_api_keys(api_keys)
    print("API keys reset at 12 PM WIB")

# Schedule the reset task
def schedule_reset_task():
    scheduler = BackgroundScheduler()
    wib = pytz.timezone('Asia/Jakarta')
    reset_time = datetime.now(wib).replace(hour=12, minute=0, second=0, microsecond=0)
    if reset_time < datetime.now(wib):
        reset_time += timedelta(days=1)
    scheduler.add_job(reset_api_keys, 'interval', days=1, start_date=reset_time)
    scheduler.start()

schedule_reset_task()

@app.before_request
def before_request():
    api_key = request.args.get('apikey')
    if not api_key or not check_api_key(api_key):
        return jsonify({'error': 'Valid API key is required or usage limit exceeded'}), 403

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
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    results = client.character.search(query)

    return jsonify(results), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/newchat')
def new_chat():
    char_id = request.args.get('q', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    data = client.chat.new_chat(char_id)

    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/trending')
def trending_characters():
    trending = client.character.trending()

    return jsonify(trending), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/rec')
def rec_characters():
    rec = client.character.recommended()

    return jsonify(rec), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/info')
def info_character():
    char_id = request.args.get('id', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    info = client.character.info(char_id)

    return jsonify(info), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/cai')
def cai_chat():
    char_id = request.args.get('charid', '')
    message = request.args.get('message', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400
    if not message:
        return jsonify({'error': 'Message is required'}), 400

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
