import os

TOKEN = os.environ.get("BOT_TOKEN")

print("DEBUG TOKEN:", repr(TOKEN))

if TOKEN is None:
    raise Exception("BOT_TOKEN NOT FOUND")

import telebot
bot = telebot.TeleBot(TOKEN)

print("Bot started")

bot.infinity_polling()
