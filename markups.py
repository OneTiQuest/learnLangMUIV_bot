from telebot import types
from query import get_langs, get_courses, get_roles, get_modules, get_themes_by_module_id
import json

# Предложение выбора кнопок флагов
def get_lang_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for lang in get_langs():
        markup.add(types.KeyboardButton(f"{lang[2]} {lang[1]}"))
    
    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


# Предложение выбора кнопок курса
def get_course_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for course in get_courses():
        markup.add(types.KeyboardButton(f"{course[1]} {course[2]}"))
    
    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


# Предложение выбора кнопок для ученика
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("ℹ️ Модули"),
        types.KeyboardButton("⚙️ Настройки"),
    )
        
    return markup


# Предложение выбора кнопок для ученика
def get_teacher_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("ℹ️ Модули"),
        types.KeyboardButton("📊 Общая статистика"),
        types.KeyboardButton("⚙️ Настройки"),
    )
        
    return markup

# Предложение выбора кнопок для ученика
def get_admin_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("⚙️ Настройки"),
    )
        
    return markup


# Предложение выбора кнопок для ученика
def get_teacher_settings_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Изменить роль (тестовая функция)"),
        types.KeyboardButton("⬅️ Назад"),
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


# Предложение выбора кнопок для ученика
def get_roles_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    for role in get_roles():
        markup.add(types.KeyboardButton(role[1]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


# Предложение выбора модулей
def get_modules_markup(user_id: int):
    markup = types.InlineKeyboardMarkup(row_width=2)

    for module in get_modules(user_id):
        markup.add(types.InlineKeyboardButton(module[1], callback_data=json.dumps({"type": "module", "data": module[0]})))

    return markup

# Предложение выбора модулей
def get_themes_markup(module_id: int):
    markup = types.InlineKeyboardMarkup(row_width=2)

    for theme in get_themes_by_module_id(module_id):
        markup.add(types.InlineKeyboardButton(theme[1], callback_data=json.dumps({"type": "theme", "data": theme[0]})))

    return markup

def get_next_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(types.KeyboardButton("Продолжить ➡️"))

    return markup