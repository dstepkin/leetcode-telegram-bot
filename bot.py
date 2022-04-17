from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CallbackContext, CommandHandler

import config
import leetcode


def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def daily_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /daily is issued."""
    update.message.reply_text(leetcode.get_daily())


bot = Bot(config.BOT_TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

# On different commands - answer in Telegram
dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("daily", daily_command))

app = Flask(__name__)


@app.route('/')
def status():
    return config.HEALTH_CHECK_MESSAGE


@app.route(config.UPDATE_ENDPOINT, methods=['POST'])
def process_leetcode_bot_update_action():
    request_body = request.get_json()
    update = Update.de_json(request_body, bot)
    dispatcher.process_update(update)
    return '"OK"'


if __name__ == '__main__':
    app.run()
