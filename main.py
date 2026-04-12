import telebot
from config import TOKEN
from db.sqlite import init_db

import handlers.start
import handlers.profile
import handlers.dig
import handlers.tree
import handlers.chat
import handlers.inventory

bot = telebot.TeleBot(TOKEN)

init_db()

handlers.start.register(bot)
handlers.profile.register(bot)
handlers.dig.register(bot)
handlers.tree.register(bot)
handlers.chat.register(bot)

print("Bot started")
bot.infinity_polling()
