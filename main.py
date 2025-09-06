import psycopg2
import telebot as tb
from telebot import types

TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

bot = tb.TeleBot(TOKEN)
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host="localhost", port=5432)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Отправляем сообщение
    bot.send_message(
        message.chat.id,
        "Привет"
    )


# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
