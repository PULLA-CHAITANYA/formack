from flask import Flask, render_template, request, redirect, url_for
from telethon import TelegramClient
import asyncio
import os

app = Flask(__name__)
SESSION_DIR = "./"  # You can change this to a subfolder if needed

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        api_id = request.form['api_id']
        api_hash = request.form['api_hash']
        phone = request.form['phone']
        session_name = phone.replace('+', '')

        try:
            asyncio.run(handle_send_code(session_name, api_id, api_hash, phone))
            return render_template('code.html', api_id=api_id, api_hash=api_hash, phone=phone)
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
        asyncio.run(handle_sign_in(session_name, api_id, api_hash, phone, code))
        return render_template('success.html', session_name=session_name)
    except Exception as e:
        return f"❌ Verification failed: {e}"

async def handle_send_code(session_name, api_id, api_hash, phone):
    async with TelegramClient(session_name, int(api_id), api_hash) as client:
        await client.send_code_request(phone)

async def handle_sign_in(session_name, api_id, api_hash, phone, code):
    async with TelegramClient(session_name, int(api_id), api_hash) as client:
        await client.sign_in(phone=phone, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
