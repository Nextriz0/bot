import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

print("TOKEN =", TOKEN)

bot = telebot.TeleBot(TOKEN)
