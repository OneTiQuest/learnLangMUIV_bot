import telebot as tb
import json
from query import save_user, get_user_by_chat_id
from roles import Base as BaseRole, get_user

TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
bot = tb.TeleBot(TOKEN)

# Авторизация пользователя в системе
def auth_user(user_id: int, bot) -> BaseRole:
    user = get_user_by_chat_id(user_id)

    if not user:
        return None

    role = user[4]

    return get_user(role, bot, user_id)

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    user = auth_user(user_id, bot)

    if not user:
        new_user = save_user(message.from_user)
        user = auth_user(new_user[3], bot)
        bot.send_message(
           user_id,
           f"Привет, {message.from_user.first_name}👋."
        )


    user.message_handler(message.text)


# Обработчик команды /help
@bot.message_handler(commands=["help"])
def help(message):
    user_id = message.chat.id
    bot.send_message(
        user_id,
        f"""
Бот-система для изучения иностранных языков.
Разработал: <i>Артюшихин Максим Юрьевич</i>
1. Для начала работы с ботом напишите команду /start
2. Навигация осуществляется по кнопкам выпадающего меню
3. Для изменения роли пользователя перейдите в меню \"Настройки\"
        """,
        parse_mode="HTML"
    )


# Обработчик callback-запросов от инлайн кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = json.loads(call.data)

    user = auth_user(user_id, bot)
    user.call_handler(data)


# Обработчик текстовых сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user = auth_user(user_id, bot)
    

    if not user:
        bot.send_message(user_id, "Пользователь не найден в системе. Для регистрации напишите комманду /start")

    user.message_handler(message.text)


# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
