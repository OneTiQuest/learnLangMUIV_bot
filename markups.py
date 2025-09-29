from telebot import types
from query import get_langs, get_courses, get_roles, get_modules, get_themes_by_module_id, get_exersises, get_exersises_types
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

# Предложение выбора кнопок редактирования
def get_edit_module_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton(f"➕ Создать модуль"),
        types.KeyboardButton(f"✏️ Изменить модуль")
    )
    
    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup

# Предложение выбора кнопок редактирования
def get_edit_theme_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton(f"➕ Создать тему"),
        types.KeyboardButton(f"✏️ Изменить тему"),
        types.KeyboardButton("⬅️ Назад")
    )

    return markup

# Предложение выбора кнопок редактирования
def get_edit_exersises_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    markup.add(
        types.KeyboardButton(f"➕ Создать упражнение"),
        types.KeyboardButton(f"✏️ Изменить упражнение"),
        types.KeyboardButton("⬅️ Назад")
    )

    return markup

def get_edit_exersise_markup():
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    markup.add(
        types.KeyboardButton(f"✏️ Изменить заголовок"),
        types.KeyboardButton(f"✏️ Изменить контент"),
        types.KeyboardButton("⬅️ Назад")
    )

    return markup

# Предложение выбора кнопок редактирования
def get_exersises_markup(theme_id: int):
    markup = types.InlineKeyboardMarkup(row_width=2)

    for exersise in get_exersises(theme_id):
        markup.add(types.InlineKeyboardButton(exersise[1], callback_data=json.dumps({"type": "exersise", "data": exersise[0]})))

    return markup

# Предложение выбора типа упражнения
def get_exersises_types_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2)

    for exersise in get_exersises_types():
        markup.add(types.KeyboardButton(exersise[1]))

    return markup

# Предложение выбора кнопок редактирования модуля
def get_edit_object_markup(add_back: bool=True):
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.row(
        types.KeyboardButton(f"✏️ Изменить название"),
        types.KeyboardButton(f"❌ Удалить")
    )

    if add_back:
        markup.row(
            types.KeyboardButton(f"Редактировать содержимое"),
            types.KeyboardButton("⬅️ Назад")
        )
    else:
        markup.row(
            types.KeyboardButton(f"Редактировать содержимое")
        )

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
        types.KeyboardButton("📊 Статистика оценок"),
        types.KeyboardButton("⚙️ Настройки"),
    )
        
    return markup

# Предложение выбора кнопок для ученика
def get_admin_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📊 Сводка о пользователях"),
        types.KeyboardButton("⚙️ Настройки")
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
def get_roles_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    for role in get_roles():
        markup.add(types.KeyboardButton(role[1]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup

def remove_markup():
    return types.ReplyKeyboardRemove()

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

def get_back_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(types.KeyboardButton("⬅️ Назад"))

    return markup
