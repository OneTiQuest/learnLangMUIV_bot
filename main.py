import telebot as tb
from telebot import types

TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
bot = tb.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Отправляем сообщение
    bot.send_message(
        message.chat.id,
        "Привет"
    )

bot.infinity_polling()