from telebot import types
from query import get_langs, get_courses


# Предложение выбора кнопок флагов
def get_lang_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for lang in get_langs():
        markup.add(types.KeyboardButton(f"{lang[2]} {lang[1]}"))
        
    return markup


# Предложение выбора кнопок курса
def get_course_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for course in get_courses():
        markup.add(types.KeyboardButton(f"{course[1]} {course[2]}"))
        
    return markup


# Предложение выбора кнопок для ученика
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Модули"),
        types.KeyboardButton("Настройки"),
    )
        
    return markup


# Предложение выбора кнопок для ученика
def get_settings_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Изменить изучаемый язык"),
        types.KeyboardButton("Изменить курс обучения"),
        types.KeyboardButton("Изменить роль (тестовая функция)"),
        types.KeyboardButton("⬅️ Назад"),
    )
        
    return markup