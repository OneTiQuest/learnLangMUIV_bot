from telebot import TeleBot, types
import json
import os
from bot.markups import auth_markup
from bot.roles import Base as BaseRole, get_user
from bot.api import HttpClient
from bot.scripts import register_form, login_form

TOKEN = os.environ.get("BOT_TOKEN")
bot = TeleBot(TOKEN)


# Авторизация пользователя в системе
def auth_user(bot: TeleBot, message: types.Message) -> BaseRole:
    chat_id = message.chat.id if message.chat else message.from_user.id
    http_client = HttpClient(chat_id, bot)

    if http_client.is_login():
        user = http_client.get(f"/users/profile")

        role = user[4]
        
        user = get_user(role, bot, chat_id)

        if message.chat:
            user.message_handler(message)

        else:
            user.call_handler(message.data)

    else:
        bot.send_message(
            chat_id, f"Необходима авторизация ⚠️", reply_markup=auth_markup()
        )

        def auth_form(msg: types.Message):
            if msg.text == "Вход":

                def success_handler(payload):
                    login, password = payload

                    if http_client.login(login, password):
                        bot.send_message(chat_id, f"Авторизация завершена ✅")
                        auth_user(bot, msg)

                    else:
                        bot.send_message(
                            chat_id,
                            f"Пользователь не найден ❌",
                            reply_markup=auth_markup(),
                        )

                login_form(bot, msg, success_handler)

            elif msg.text == "Регистрация":

                def success_handler(payload):
                    login, password = payload
                    register_data = {
                        "login": login,
                        "password": password,
                        "chat_id": chat_id,
                        "first_name": message.from_user.first_name,
                        "last_name": message.from_user.last_name,
                    }

                    if http_client.register(register_data):
                        bot.send_message(chat_id, f"Авторизация завершена ✅")
                        auth_user(bot, msg)

                    else:
                        bot.send_message(
                            chat_id,
                            f"Ошибка регистрации. Пользователь уже существует ❌",
                            reply_markup=auth_markup(),
                        )

                register_form(bot, msg, success_handler)
            else:
                bot.send_message(
                    chat_id, f"Необходима авторизация ⚠️", reply_markup=auth_markup()
                )
                bot.register_next_step_handler(message, lambda msg: auth_form(msg))

        bot.register_next_step_handler(message, lambda msg: auth_form(msg))


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message: types.Message):
    user = auth_user(bot, message)
    if user:
        user.message_handler(message.text)


# Обработчик команды /help
@bot.message_handler(commands=["help"])
def help(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        f"""
Бот-система для изучения иностранных языков.
Разработал: <i>Артюшихин Максим Юрьевич</i>
1. Для начала работы с ботом напишите команду /start
2. Навигация осуществляется по кнопкам выпадающего меню
3. Для изменения роли пользователя перейдите в меню \"Настройки\"
        """,
        parse_mode="HTML",
    )


# Обработчик callback-запросов от инлайн кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = json.loads(call.data)

    user = auth_user(bot, call)
    if user:
        user.call_handler(data)


# Обработчик текстовых сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message: types.Message):
    user = auth_user(bot, message)
    if user:
        user.message_handler(message.text)


# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
