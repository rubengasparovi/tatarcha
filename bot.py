import logging
import requests
import os
from telegram.ext import Updater, MessageHandler, Filters

# Load from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_joke_from_gemini():
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {"parts": [{"text": "Tell me a short, clever, original joke."}]}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Oops! Gemini forgot the punchline."

def handle_message(update, context):
    message = update.message
    bot_username = context.bot.username

    if f"@{bot_username}" in message.text:
        joke = get_joke_from_gemini()
        context.bot.send_message(chat_id=message.chat.id, text=joke)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
