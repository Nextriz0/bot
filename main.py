import os
import telebot

from db.sqlite import init_db

import handlers.start
import handlers.profile
import handlers.dig
import handlers.tree
import handlers.chat
import handlers.inventory

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN is missing")

print("TOKEN OK")

bot = telebot.TeleBot(TOKEN)

init_db()

handlers.start.register(bot)
handlers.profile.register(bot)
handlers.dig.register(bot)
handlers.tree.register(bot)
handlers.chat.register(bot)
handlers.inventory.register(bot)
handlers.inventory.register_actions(bot)

print("Bot started")
bot.infinity_polling()
