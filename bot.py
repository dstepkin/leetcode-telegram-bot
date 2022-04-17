import requests
from flask import Flask, request

import config
import leetcode

base_url = f'https://api.telegram.org/bot{config.BOT_TOKEN}'


def _send_telegram_request(method, payload=None):
    url = f'{base_url}/{method}'
    requests.post(url=url, json=payload)


def reply_to_message(update, text):
    message = update.get('message', {})
    chat_id = message.get('chat', {}).get('id', None)
    message_id = message.get('message_id', None)
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': message_id,
    }
    _send_telegram_request(method='sendMessage', payload=payload)


def start_command(update) -> None:
    """Send a message when the command /start is issued."""
    reply_to_message(update, 'Hello!')


def help_command(update) -> None:
    """Send a message when the command /help is issued."""
    reply_to_message(update, 'Help!')


def daily_command(update) -> None:
    """Send a message when the command /daily is issued."""
    reply_to_message(update, leetcode.get_daily())


handlers = {
    '/daily': daily_command,
    '/help': help_command,
    '/start': start_command,
}

app = Flask(__name__)


@app.route('/')
def status():
    return config.HEALTH_CHECK_MESSAGE


@app.route(config.UPDATE_ENDPOINT, methods=['POST'])
def process_leetcode_bot_update_action():
    update = request.get_json()
    text = update.get('message', {}).get('text', None)
    if text in handlers:
        handlers[text](update)
    return '"OK"'


if __name__ == '__main__':
    app.run()
