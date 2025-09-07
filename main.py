import telebot as tb
import navigation
import json
from query import get_user_by_chat_id, save_user
from scripts import student_start_script

TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
bot = tb.TeleBot(TOKEN)

# Локальное состояние пользователей бота
users_state = {}

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    user = get_user_by_chat_id(message.chat.id)
    if not user:
        user = save_user(message.from_user)
        bot.send_message(
           message.chat.id,
           f"Привет, {message.from_user.first_name}👋."
        )
                
    role = user[5]

    # Обработка ученика
    if role == 1:
        if user_id not in users_state:
            student_start_script(users_state, user_id)

        navigation.student_nav_handler(bot, users_state, user_id, message.text)

    # Обработка преподавателя
    elif role == 2:
        # Инициализация состояния пользователя
        if user_id not in users_state:
            users_state[user_id] = 'main'

        navigation.teach_navigation_handler(bot, users_state, user_id, message.text)

    # Обработка администратора
    elif role == 3:
        # Инициализация состояния пользователя
        if user_id not in users_state:
            users_state[user_id] = 'main'

        navigation.admin_navigation_handler(bot, users_state, user_id, message.text)

# Обработчик callback-запросов от инлайн кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = json.loads(call.data)

    if data.get("type") == "module":
        print(user_id, data.get("data"))

# Обработчик текстовых сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user = get_user_by_chat_id(user_id)
    if not user:
        bot.send_message(user_id, "Пользователь не найден в системе. Для регистрации напишите комманду /start")
    
    # Обработка кнопки "Назад"
    if message.text == "⬅️ Назад":
        back_button_handler(user_id)

    role = user[5]

    # Обработка ученика
    if role == 1:
        if user_id not in users_state:
            student_start_script(users_state, user_id)
            
        navigation.student_nav_handler(bot, users_state, user_id, message.text)

    # Обработка преподавателя
    elif role == 2:
        # Инициализация состояния пользователя
        if user_id not in users_state:
            users_state[user_id] = 'main'

        navigation.teach_nav_handler(bot, users_state, user_id, message.text)

    # Обработка администратора
    elif role == 3:
        # Инициализация состояния пользователя
        if user_id not in users_state:
            users_state[user_id] = 'main'

        navigation.admin_nav_handler(bot, users_state, user_id, message.text)

    else:
        # Отправляем сообщение
        bot.send_message(
            message.chat.id,
            f"Не удалось обработать роль: {role}"
        )

def back_button_handler(user_id: int):
    current_state = users_state.get(user_id)

    # bot.send_message(user_id, f'Состояние перед НАЗАД: {current_state}')

    if current_state == "main":
        users_state[user_id] = "main"

    elif current_state == "lang_menu":
        users_state[user_id] = "settings"

    elif current_state == "course_menu":
        users_state[user_id] = "settings"

    elif current_state == "settings":
        users_state[user_id] = "main"

    elif current_state == "roles":
        users_state[user_id] = "settings"

    elif current_state == "2_step":
        users_state[user_id] = "1_step"

    elif current_state == "1_step":
        users_state[user_id] = "1_step"

    else:
        users_state[user_id] = "main"

# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
