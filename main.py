import telebot as tb
from telebot import types
from query import get_user_by_chat_id, save_user

TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
bot = tb.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user = get_user_by_chat_id(message.chat.id)
    if not user:
        user = save_user(message.from_user)

    role = user[5]

    # Обработка ученика
    if role == 1:
        # Создаем клавиатуру
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        # Добавляем кнопки в клавиатуру
        markup.add(
            types.KeyboardButton("🇷🇺 Русский"),
            types.KeyboardButton("🇬🇧 Английский"),
            types.KeyboardButton("🇨🇵 Французский"),
        )
        
        bot.send_message(
            message.chat.id,
            f"Привет, {user[1]}👋.\n\nВыбери пожалуйста язык для обучения:",
            reply_markup=markup
        )


    # Обработка преподавателя
    elif role == 2:
        pass

    # Обработка администратора
    elif role == 3:
        pass
    else:
        # Отправляем сообщение
        bot.send_message(
            message.chat.id,
            f"Не удалось обработать роль: {role}"
        )

# Обработчик текстовых сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🇷🇺 Русский":
        pass
    
    elif message.text == "🇬🇧 Английский":
        pass
    
    elif message.text == "🇨🇵 Французский":
        pass
    
    else:
        bot.send_message(message.chat.id, "Я не понимаю эту команду")

# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
