from telebot import types
import json
from bot.api import HttpClient


# Предложение выбора кнопок флагов
def get_lang_markup(chat_id, user_id: int = None, draw_back: bool = True):
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    http_client = HttpClient(chat_id)

    if user_id:
        langs = http_client.get(f"/users/{user_id}/langs")
    else:
        langs = http_client.get(f"/langs")

    for lang in langs:
        markup.add(types.KeyboardButton(f"{lang[2]} {lang[1]}"))

    if draw_back:
        markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


# Предложение выбора кнопок курса
def get_course_markup(chat_id: int, draw_back: bool = True):
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    http_client = HttpClient(chat_id)
    courses = http_client.get(f"/courses")
    for course in courses:
        markup.add(types.KeyboardButton(f"{course[1]} {course[2]}"))

    if draw_back:
        markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


# Предложение выбора кнопок редактирования
def get_edit_module_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton(f"➕ Создать модуль"),
        types.KeyboardButton(f"✏️ Выбрать модуль"),
    )

    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


# Предложение выбора кнопок редактирования
def get_edit_theme_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton(f"➕ Создать тему"),
        types.KeyboardButton(f"✏️ Выбрать тему"),
        types.KeyboardButton("⬅️ Назад"),
    )

    return markup


# Предложение выбора кнопок редактирования
def get_edit_exersises_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(
        types.KeyboardButton(f"➕ Создать упражнение"),
        types.KeyboardButton(f"✏️ Выбрать упражнение"),
        types.KeyboardButton("⬅️ Назад"),
    )

    return markup


def get_edit_exersise_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(
        types.KeyboardButton(f"✏️ Изменить заголовок"),
        types.KeyboardButton(f"✏️ Изменить контент"),
        types.KeyboardButton("⬅️ Назад"),
    )

    return markup


# Предложение выбора кнопок редактирования
def get_exersises_markup(theme_id: int, chat_id: int):
    markup = types.InlineKeyboardMarkup(row_width=2)
    http_client = HttpClient(chat_id)
    exs = http_client.get(f"/themes/{theme_id}/exercises")
    for exersise in exs:
        markup.add(
            types.InlineKeyboardButton(
                exersise[1],
                callback_data=json.dumps({"type": "exersise", "data": exersise[0]}),
            )
        )

    return markup


# Предложение выбора типа упражнения
def get_exersises_types_markup(chat_id: int):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    http_client = HttpClient(chat_id)

    exs_t = http_client.get(f"/exercises/types")

    for exersise in exs_t:
        markup.add(types.KeyboardButton(exersise[1]))

    return markup


# Предложение выбора кнопок редактирования модуля
def get_edit_object_markup(add_back: bool = True):
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.row(
        types.KeyboardButton(f"✏️ Изменить название"),
        types.KeyboardButton(f"❌ Удалить"),
    )

    if add_back:
        markup.row(
            types.KeyboardButton(f"Редактировать содержимое"),
            types.KeyboardButton("⬅️ Назад"),
        )
    else:
        markup.row(types.KeyboardButton(f"Редактировать содержимое"))

    return markup


# Предложение выбора кнопок для ученика
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("ℹ️ Модули"),
        types.KeyboardButton("⚙️ Настройки"),
        types.KeyboardButton("⭐️ Мои оценки"),
    )

    return markup


# Предложение выбора кнопок для ученика
def get_teacher_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📊 Статистика оценок"),
        types.KeyboardButton("⚙️ Настройки"),
    )

    return markup


# Предложение выбора кнопок для ученика
def get_admin_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📊 Сводка о пользователях"),
        types.KeyboardButton("⚙️ Настройки"),
    )

    return markup


# Предложение выбора кнопок для ученика
def get_teacher_settings_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Изменить роль (тестовая функция)"),
        types.KeyboardButton("⚙️ Редактировать"),
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
def get_roles_markup(chat_id: int):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    http_client = HttpClient(chat_id)
    roles = http_client.get(f"/roles")

    for role in roles:
        markup.add(types.KeyboardButton(role[1]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


def remove_markup():
    return types.ReplyKeyboardRemove()


# Предложение выбора модулей
def get_modules_markup(chat_id: int, user_id: int):
    markup = types.InlineKeyboardMarkup(row_width=2)
    http_client = HttpClient(chat_id)
    u_modules = http_client.get(f"/users/{user_id}/modules")

    for module in u_modules:
        markup.add(
            types.InlineKeyboardButton(
                module[1],
                callback_data=json.dumps({"type": "module", "data": module[0]}),
            )
        )

    return markup


# Предложение выбора модулей
def get_themes_markup(chat_id: int, module_id: int):
    markup = types.InlineKeyboardMarkup(row_width=2)
    http_client = HttpClient(chat_id)
    u_themes = http_client.get(f"/modules/{module_id}/themes")

    for theme in u_themes:
        markup.add(
            types.InlineKeyboardButton(
                theme[1], callback_data=json.dumps({"type": "theme", "data": theme[0]})
            )
        )

    return markup


def get_next_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(types.KeyboardButton("Продолжить ➡️"))

    return markup


def get_back_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup


def auth_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(types.KeyboardButton("Вход"))
    markup.add(types.KeyboardButton("Регистрация"))

    return markup
