from enum import Enum
import state
from scripts import init_settings_script, select_theme_script
import menu_handlers
from telebot import TeleBot
from menu_handlers import module_menu_handler

class Roles(Enum):
    STUDENT = 1
    TEACH = 2
    ADMIN = 3

def get_user(role: Roles, bot, user_id: int):
    # Обработка ученика
    if role == 1:
        return Student(bot, user_id)
    
    # Обработка преподавателя
    elif role == 2:
        return Teacher(bot, user_id)
    
    # Обработка администратора
    elif role == 3:
        return Admin(bot, user_id)
    
    else:
        raise ValueError(f"Не удалось обработать роль: {role}")

class Base():
    user_id: int
    bot: TeleBot
    
    
    def __init__(self, bot: TeleBot, user_id: int):
        self.user_id = user_id
        self.bot = bot


    def message_handler(self, text: str):
        current_state = state.get_state(self.user_id)

        if not current_state:
            init_settings_script(self.user_id)
            current_state = state.get_state(self.user_id)

        # self.bot.send_message(self.user_id, f'Обрабатывается состояние: {current_state}')

        if text == "⬅️ Назад":
            self.go_back(current_state)
            current_state = state.get_state(self.user_id)

        self.navigation_handler(current_state, text)


    def call_handler(self, call_data: dict):
        if call_data.get("type") == "module":
            module_menu_handler(self.bot, self.user_id, call_data.get("data"))


    # Обработка кнопки "Назад"
    def go_back(self, current_state: str):
        if current_state == "main":
            state.set_state(self.user_id, 'main')

        elif current_state == "lang_menu":
            state.set_state(self.user_id, 'settings')

        elif current_state == "course_menu":
            state.set_state(self.user_id, 'settings')

        elif current_state == "settings":
            state.set_state(self.user_id, 'main')

        elif current_state == "roles":
            state.set_state(self.user_id, 'settings')

        elif current_state == "2_step":
            state.set_state(self.user_id, '1_step')

        elif current_state == "1_step":
            state.set_state(self.user_id, '1_step')

        else:
            state.set_state(self.user_id, 'main')


    def navigation_handler(self, state, text):
        if state == '1_step':
            menu_handlers._1_step_handler(self.bot, self.user_id, text)

        elif state == '2_step':
            menu_handlers._2_step_handler(self.bot, self.user_id, text)

        elif state == 'main':
            self.get_main_menu(text)

        elif state == 'course_menu':
            self.get_courses_menu(text)

        elif state == 'settings':
            self.get_settings_menu(text)

        elif state == 'roles':
            self.get_roles_menu(text)

        else:
            self.bot.send_message(self.user_id, "Я не понимаю эту команду")

    def get_main_menu(self, text):
        menu_handlers.main_menu_handler(self.bot, self.user_id, text)


    def get_settings_menu(self, text):
        menu_handlers.settings_menu_handler(self.bot, self.user_id, text)


    def get_courses_menu(self, text):
        menu_handlers.course_menu_handler(self.bot, self.user_id, text)


    def get_roles_menu(self, text):
        menu_handlers.roles_menu_handler(self.bot, self.user_id, text)


class Student(Base):
    code = 'student'
    role = Roles.STUDENT

    def call_handler(self, call_data: dict):
        if str(state.get_state(self.user_id)).split('/')[0] == "theme":
            self.bot.send_message(self.user_id, "Сначала пройдите текущую тему : )")

        elif call_data.get("type") == "theme":
            select_theme_script(self.bot, call_data.get("data"), self.user_id)

        else:
            super().call_handler(call_data)


    def navigation_handler(self, state, text):
        if state == 'lang_menu':
            menu_handlers.lang_menu_handler(self.bot, self.user_id, text)

        elif state.split('/')[0] == 'theme':
            menu_handlers.theme_menu_handler(self.bot, self.user_id, text, int(state.split('/')[1]))

        else:
            super().navigation_handler(state, text)


class Teacher(Student):
    code = 'teacher'
    role = Roles.TEACH

    def call_handler(self, call_data: dict):
        if call_data.get("type") == "theme":
            self.bot.send_message(self.user_id, "Выбрана тема")

        else:
            super().call_handler(call_data)


    def navigation_handler(self, state, text):
        if state == '2_step':
            menu_handlers._2_step_teacher_handler(self.bot, self.user_id, text)

        else:
            super().navigation_handler(state, text)


    def get_main_menu(self, text):
        menu_handlers.teach_main_menu_handler(self.bot, self.user_id, text)


    def get_settings_menu(self, text):
        menu_handlers.teacher_settings_menu_handler(self.bot, self.user_id, text)


class Admin(Teacher):
    code = 'admin'
    role = Roles.ADMIN


    def message_handler(self, text: str):
        if not state.get_state(self.user_id):
            state.set_state(self.user_id, 'main')

        super().message_handler(text)


    def get_main_menu(self, text):
        menu_handlers.admin_main_menu_handler(self.bot, self.user_id, text)
