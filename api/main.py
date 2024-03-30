from flask import Flask, jsonify, request, render_template
from characterai import PyCAI

app = Flask(__name__, template_folder='.')

client = PyCAI('29422450f9ebdf864bb798a6f9796cdab019d9f1')

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/api')
def home():
    return render_template('home.html')

@app.route('/home')
def api():
    return render_template('web/home.html')
    
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
