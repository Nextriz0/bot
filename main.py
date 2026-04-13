import os
import telebot
from db.sqlite import init_db

import handlers.start as start
import handlers.profile as profile
import handlers.dig as dig
import handlers.inventory as inventory
import handlers.tree as tree
import handlers.daily as daily
import handlers.chat as chat
import handlers.top as top

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN NOT FOUND")

bot = telebot.TeleBot(TOKEN)

init_db()

start.register(bot)
profile.register(bot)
dig.register(bot)
inventory.register(bot)
tree.register(bot)
daily.register(bot)
chat.register(bot)
top.register(bot)

print("Bot started")
bot.infinity_polling()
