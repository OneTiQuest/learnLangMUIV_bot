import telebot as tb
import json
from query import get_user_by_chat_id, save_user
from roles import Base as BaseRole, get_user

TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
bot = tb.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    user = get_user_by_chat_id(user_id)
    if not user:
        user = save_user(message.from_user)
        bot.send_message(
           user_id,
           f"Привет, {message.from_user.first_name}👋."
        )
                
    role = user[4]

    auth_user: BaseRole = get_user(role, bot, user_id)
    auth_user.message_handler(message.text)


# Обработчик callback-запросов от инлайн кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = json.loads(call.data)
    user = get_user_by_chat_id(user_id)

    role = user[4]

    auth_user: BaseRole = get_user(role, bot, user_id)
    auth_user.call_handler(data)

# Обработчик текстовых сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user = get_user_by_chat_id(user_id)
    if not user:
        bot.send_message(user_id, "Пользователь не найден в системе. Для регистрации напишите комманду /start")

    role = user[4]

    auth_user: BaseRole = get_user(role, bot, user_id)
    auth_user.message_handler(message.text)

# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
