import telebot as tb
from telebot import types
from query import get_user_by_chat_id, save_user

TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
bot = tb.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user = get_user_by_chat_id(message.chat.id)
    if not user:
        save_user(message.from_user)

    # Отправляем сообщение
    bot.send_message(
        message.chat.id,
        "Привет"
    )


# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
