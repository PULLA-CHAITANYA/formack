from flask import Flask, render_template, request, session
from telethon import TelegramClient
import asyncio
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Required for session storage
SESSION_DIR = "./sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        api_id = request.form['api_id']
        api_hash = request.form['api_hash']
        phone = request.form['phone']
        session_name = phone.replace('+', '')

        session['api_id'] = api_id
        session['api_hash'] = api_hash
        session['phone'] = phone
        session['session_name'] = session_name

        try:
            asyncio.run(handle_send_code(session_name, api_id, api_hash, phone))
            return render_template('code.html', api_id=api_id, api_hash=api_hash, phone=phone)
        except Exception as e:
            message = f"Error: {e}"
    return render_template('index.html', message=message)

@app.route('/verify', methods=['POST'])
def verify():
    code = request.form['code']
    api_id = session.get('api_id')
    api_hash = session.get('api_hash')
    phone = session.get('phone')
    session_name = session.get('session_name')
    phone_code_hash = session.get('phone_code_hash')

    if not phone_code_hash:
        return "❌ Missing phone_code_hash. Please restart login."

    try:
        asyncio.run(handle_sign_in(session_name, api_id, api_hash, phone, code, phone_code_hash))
        return render_template('success.html', session_name=session_name)
    except Exception as e:
        return f"❌ Verification failed: {e}"

async def handle_send_code(session_name, api_id, api_hash, phone):
    client = TelegramClient(os.path.join(SESSION_DIR, session_name), int(api_id), api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        result = await client.send_code_request(phone)
        session['phone_code_hash'] = result.phone_code_hash

    await client.disconnect()

async def handle_sign_in(session_name, api_id, api_hash, phone, code, phone_code_hash):
    client = TelegramClient(os.path.join(SESSION_DIR, session_name), int(api_id), api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)

    await client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
