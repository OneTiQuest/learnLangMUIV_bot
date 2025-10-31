from enum import Enum
import bot.state as state
from bot.scripts import init_settings_script, select_theme_script
import bot.menu_handlers as menu_handlers
from telebot import TeleBot


class Roles(Enum):
    STUDENT = 1
    TEACH = 2
    ADMIN = 3


def get_user(role: Roles, bot: TeleBot, user_id: int, chat_id: int):
    # Обработка ученика
    if role == 1:
        return Student(bot, user_id, chat_id)

    # Обработка преподавателя
    elif role == 2:
        return Teacher(bot, user_id, chat_id)

    # Обработка администратора
    elif role == 3:
        return Admin(bot, user_id, chat_id)

    else:
        raise ValueError(f"Не удалось обработать роль: {role}")


# Базовый класс пользователя
class Base:
    user_id: int
    bot: TeleBot

    def __init__(self, bot: TeleBot, user_id: int, chat_id: int):
        self.user_id = user_id
        self.chat_id = chat_id
        self.bot = bot

    # Обработка текстовых сообщений
    def message_handler(self, text: str):
        current_state = state.get_state(self.chat_id)

        if not current_state:
            init_settings_script(self.chat_id, self.user_id)
            current_state = state.get_state(self.chat_id)

        # self.bot.send_message(self.chat_id, f'Обрабатывается состояние: {current_state}')

        if text == "⬅️ Назад":
            self.go_back(current_state)
            current_state = state.get_state(self.chat_id)

        self.navigation_handler(current_state, text)

    # Обработка inline-кнопок
    def call_handler(self, call_data: dict):
        if (
            state.get_state(self.chat_id) == "main"
            and call_data.get("type") == "module"
        ):
            menu_handlers.module_menu_handler(
                self.bot, self.chat_id, self.user_id, call_data.get("data")
            )

    # Обработка кнопки "Назад"
    def go_back(self, current_state: str):

        # self.bot.send_message(self.chat_id, current_state)

        split_state = current_state.split("/")

        if current_state == "main":
            state.set_state(self.chat_id, "main")

        elif current_state == "lang_menu":
            state.set_state(self.chat_id, "settings")

        elif current_state == "course_menu":
            state.set_state(self.chat_id, "settings")

        elif current_state == "settings":
            state.set_state(self.chat_id, "main")

        elif current_state == "edit_module":
            state.set_state(self.chat_id, "settings")

        elif split_state[0] == "edit_module":
            state.set_state(self.chat_id, "edit_module")

        elif current_state == "edit_theme":
            state.set_state(self.chat_id, "edit_module")

        elif split_state[0] == "edit_module_child":
            state.set_state(self.chat_id, f"edit_module/{split_state[1]}")

        elif split_state[0] == "edit_theme_child":
            state.set_state(self.chat_id, f"edit_theme/{split_state[1]}")

        elif split_state[0] == "edit_theme" and len(split_state) == 3:
            state.set_state(self.chat_id, f"edit_module_child/{split_state[2]}")

        elif split_state[0] == "edit_theme_child" and len(split_state) == 3:
            state.set_state(self.chat_id, f"edit_theme_child/{split_state[1]}")

        elif current_state == "roles":
            state.set_state(self.chat_id, "settings")

        elif current_state == "2_step":
            state.set_state(self.chat_id, "1_step")

        elif current_state == "1_step":
            state.set_state(self.chat_id, "1_step")

        else:
            state.set_state(self.chat_id, "main")

    # Обработка текущего состояния и действий пользователя
    def navigation_handler(self, state, text):
        if state == "1_step":
            menu_handlers._1_step_handler(self.bot, self.chat_id, self.user_id, text)

        elif state == "2_step":
            menu_handlers._2_step_handler(self.bot, self.chat_id, self.user_id, text)

        elif state == "main":
            self.get_main_menu(text)

        elif state == "course_menu":
            self.get_courses_menu(text)

        elif state == "settings":
            self.get_settings_menu(text)

        elif state == "roles":
            self.get_roles_menu(text)

        else:
            self.bot.send_message(self.chat_id, "Я не понимаю эту команду")

    def get_main_menu(self, text):
        menu_handlers.main_menu_handler(self.bot, self.chat_id, self.user_id, text)

    def get_settings_menu(self, text):
        menu_handlers.settings_menu_handler(self.bot, self.chat_id, self.user_id, text)

    def get_courses_menu(self, text):
        menu_handlers.course_menu_handler(self.bot, self.chat_id, self.user_id, text)

    def get_roles_menu(self, text):
        menu_handlers.roles_menu_handler(self.bot, self.chat_id, self.user_id, text)


# Класс пользователя - студента
class Student(Base):
    code = "student"
    role = Roles.STUDENT

    def call_handler(self, call_data: dict):
        if str(state.get_state(self.chat_id)).split("/")[0] == "theme":
            self.bot.send_message(self.chat_id, "Сначала пройдите текущую тему : )")

        elif call_data.get("type") == "theme":
            select_theme_script(
                self.bot, call_data.get("data"), self.user_id, self.chat_id
            )

        else:
            super().call_handler(call_data)

    def navigation_handler(self, state, text):
        if state == "lang_menu":
            menu_handlers.lang_menu_handler(self.bot, self.chat_id, self.user_id, text)

        elif state.split("/")[0] == "theme":
            menu_handlers.theme_menu_handler(
                self.bot,
                self.chat_id,
                self.user_id,
                text,
                int(state.split("/")[1]),
            )

        else:
            super().navigation_handler(state, text)


# Класс пользователя - учителя
class Teacher(Student):
    code = "teacher"
    role = Roles.TEACH

    def call_handler(self, call_data: dict):
        current_state = str(state.get_state(self.chat_id))
        split_state = current_state.split("/")

        if split_state[0] == "edit_theme" and len(split_state) > 1:
            self.bot.send_message(self.chat_id, "Закончите процесс изменения темы")
            return

        if split_state[0] == "edit_theme_child" and len(split_state) > 2:
            self.bot.send_message(
                self.chat_id, "Закончите процесс изменения упражнения"
            )
            return

        elif split_state[0] == "edit_module" and len(split_state) > 1:
            self.bot.send_message(self.chat_id, "Закончите процесс изменения модуля")
            return

        elif split_state[0] == "edit_module_child":
            menu_handlers.edit_theme_handler(
                self.bot, self.chat_id, self.user_id, None, call_data.get("data")
            )

        elif split_state[0] == "edit_theme_child":
            menu_handlers.edit_exersise_handler(
                self.bot, self.chat_id, self.user_id, None, call_data.get("data")
            )

        elif current_state == "edit_module":
            menu_handlers.edit_module_handler(
                self.bot, self.chat_id, self.user_id, None, call_data.get("data")
            )

        elif current_state == "edit_theme":
            menu_handlers.edit_theme_handler(
                self.bot, self.chat_id, self.user_id, None, call_data.get("data")
            )

        else:
            super().call_handler(call_data)

    def navigation_handler(self, state: str, text: str):
        split_state = state.split("/")

        if state == "2_step":
            menu_handlers._2_step_teacher_handler(
                self.bot, self.chat_id, self.user_id, text
            )

        elif state == "edit":
            menu_handlers.edit_module_menu_handler(
                self.bot, self.chat_id, self.user_id, text
            )

        elif state == "create_module":
            menu_handlers.create_handler(
                self.bot, self.chat_id, self.user_id, text, "module"
            )

        elif split_state[0] == "create_theme":
            menu_handlers.create_handler(
                self.bot, self.chat_id, self.user_id, text, "theme", int(split_state[1])
            )

        elif state == "edit_module":
            menu_handlers.edit_module_menu_handler(
                self.bot, self.chat_id, self.user_id, text
            )

        elif split_state[0] == "edit_module":
            menu_handlers.edit_module_handler(
                self.bot, self.chat_id, self.user_id, text, int(split_state[1])
            )

        elif split_state[0] == "edit_module_child":
            menu_handlers.edit_theme_menu_handler(
                self.bot, self.chat_id, self.user_id, text, int(split_state[1])
            )

        elif split_state[0] == "edit_theme":
            menu_handlers.edit_theme_handler(
                self.bot, self.chat_id, self.user_id, text, int(split_state[1])
            )

        elif split_state[0] == "create_exersise":
            menu_handlers.create_exersise_handler(
                self.bot, self.chat_id, self.user_id, text
            )

        elif split_state[0] == "edit_theme_child" and len(split_state) == 3:
            menu_handlers.edit_exersise_handler(
                self.bot, self.chat_id, self.user_id, text, int(split_state[2])
            )

        elif split_state[0] == "edit_theme_child":
            menu_handlers.edit_exersises_menu_handler(
                self.bot, self.chat_id, self.user_id, text, int(split_state[1])
            )

        else:
            super().navigation_handler(state, text)

    def get_main_menu(self, text):
        menu_handlers.teach_main_menu_handler(
            self.bot, self.chat_id, self.user_id, text
        )

    def get_settings_menu(self, text):
        menu_handlers.teacher_settings_menu_handler(
            self.bot, self.chat_id, self.user_id, text
        )


# Класс пользователя - администратора
class Admin(Teacher):
    code = "admin"
    role = Roles.ADMIN

    def message_handler(self, text: str):
        if not state.get_state(self.chat_id):
            state.set_state(self.chat_id, "main")

        super().message_handler(text)

    def get_main_menu(self, text):
        menu_handlers.admin_main_menu_handler(
            self.bot, self.chat_id, self.user_id, text
        )
