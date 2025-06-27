
from flask import Flask, render_template, request
from telethon.sync import TelegramClient
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        api_id = request.form['api_id']
        api_hash = request.form['api_hash']
        phone = request.form['phone']
        session_name = phone.replace('+', '')

        try:
            client = TelegramClient(session_name, int(api_id), api_hash)
            client.connect()

            if not client.is_user_authorized():
                client.send_code_request(phone)
                return render_template('code.html', api_id=api_id, api_hash=api_hash, phone=phone)

            message = "Already logged in!"
        except Exception as e:
            message = f"Error: {e}"
    return render_template('index.html', message=message)


@app.route('/verify', methods=['POST'])
def verify():
    code = request.form['code']
    api_id = request.form['api_id']
    api_hash = request.form['api_hash']
    phone = request.form['phone']
    session_name = phone.replace('+', '')

    try:
        client = TelegramClient(session_name, int(api_id), api_hash)
        client.connect()

        if not client.is_user_authorized():
            client.sign_in(phone, code)

        return "✅ Logged in successfully! Session saved."
    except Exception as e:
        return f"❌ Verification failed: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
