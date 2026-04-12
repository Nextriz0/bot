import os

TOKEN = os.getenv("8640949306:AAF7e5zIOxmQOZ4y-Ox2FE-O4gmQ5EWjI-A")

print("TOKEN =", TOKEN)  # временно для проверки

import telebot
bot = telebot.TeleBot(TOKEN)
