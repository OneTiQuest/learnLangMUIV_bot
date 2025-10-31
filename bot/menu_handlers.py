import json
import bot.markups as markups
from bot.exersise_handlers import ExersiseFactory
from bot.scripts import calc_result
import bot.state as state
from bot.check_answers import (
    lang_answer,
    course_answer,
    role_answer,
    exersise_types_answer,
)
from bot.api import HttpClient


def _1_step_handler(bot, chat_id: int, user_id: int, text: str):
    answer = lang_answer(text, chat_id)
    if answer:
        http_client = HttpClient(chat_id)
        http_client.post(f"/users/{user_id}/langs", {"lang_id": answer[0]})

        bot.send_message(chat_id, f"Текущий язык для обучения: {text}")

        state.set_state(chat_id, "2_step")
        bot.send_message(
            chat_id,
            "Смена курса обучения:",
            reply_markup=markups.get_course_markup(chat_id),
        )

    else:
        bot.send_message(
            chat_id,
            "Смена языка обучения:",
            reply_markup=markups.get_lang_markup(chat_id, None, False),
        )


def _2_step_handler(bot, chat_id: int, user_id: int, text: str):
    answer = course_answer(text, chat_id)
    if answer:
        http_client = HttpClient(chat_id)
        http_client.post(f"/users/{user_id}/courses", {"course_id": answer[0]})

        bot.send_message(chat_id, f"Текущий выбранный курс: {text}")

        state.set_state(chat_id, "main")
        bot.send_message(
            chat_id, "Выбери пункт меню:", reply_markup=markups.get_main_markup()
        )

    else:
        bot.send_message(
            chat_id,
            "Смена курса обучения:",
            reply_markup=markups.get_course_markup(chat_id, False),
        )


def _2_step_teacher_handler(bot, chat_id: int, user_id: int, text: str):
    answer = course_answer(text, chat_id)
    if answer:
        http_client = HttpClient(chat_id)
        http_client.post(f"/users/{user_id}/courses", {"course_id": answer[0]})
        bot.send_message(chat_id, f"Текущий выбранный курс: {text}")

        state.set_state(chat_id, "main")
        bot.send_message(
            chat_id,
            "Выбери пункт меню:",
            reply_markup=markups.get_teacher_main_markup(),
        )

    else:
        bot.send_message(
            chat_id,
            "Смена курса обучения:",
            reply_markup=markups.get_course_markup(chat_id),
        )


def main_menu_handler(bot, chat_id: int, user_id: int, text: str):
    if text == "ℹ️ Модули":
        mrkp = markups.get_modules_markup(chat_id, user_id)

        isEmpty = not mrkp.to_dict().get("inline_keyboard")

        text = "Выберите нужный модуль:"

        if isEmpty:
            text = (
                "К сожалению доступных модулей для вашего языка и курса не найдено :("
            )

        bot.send_message(chat_id, text, reply_markup=mrkp)

    elif text == "⚙️ Настройки":
        state.set_state(chat_id, "settings")
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_settings_markup(),
        )

    elif text == "⭐️ Мои оценки":
        my_grades(bot, chat_id, user_id)

    else:
        bot.send_message(
            chat_id, "Выберите вариант из меню:", reply_markup=markups.get_main_markup()
        )


def lang_menu_handler(bot, chat_id: int, user_id: int, text: str):
    answer = lang_answer(text, chat_id)
    if answer:
        http_client = HttpClient(chat_id)
        res = http_client.put(f"/users/{user_id}/langs", {"lang_id": answer[0]})
        import json

        bot.send_message(chat_id, json.dumps(res))
        bot.send_message(chat_id, f"Текущий язык для обучения: {text}")

        state.set_state(chat_id, "settings")
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_settings_markup(),
        )

    else:
        bot.send_message(
            chat_id,
            "Смена языка обучения:",
            reply_markup=markups.get_lang_markup(chat_id),
        )


def course_menu_handler(bot, chat_id: int, user_id: int, text: str):
    answer = course_answer(text, chat_id)
    if answer:
        http_client = HttpClient(chat_id)
        http_client.put(f"/users/{user_id}/courses", {"course_id": answer[0]})

        bot.send_message(chat_id, f"Текущий выбранный курс: {text}")

        state.set_state(chat_id, "settings")
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_settings_markup(),
        )

    else:
        bot.send_message(
            chat_id,
            "Смена курса обучения:",
            reply_markup=markups.get_course_markup(chat_id),
        )


def settings_menu_handler(bot, chat_id: int, user_id: int, text: str):
    if text == "Изменить изучаемый язык":
        state.set_state(chat_id, "lang_menu")
        bot.send_message(
            chat_id,
            "Смена языка обучения:",
            reply_markup=markups.get_lang_markup(chat_id),
        )

    elif text == "Изменить курс обучения":
        state.set_state(chat_id, "course_menu")
        bot.send_message(
            chat_id,
            "Смена курса обучения:",
            reply_markup=markups.get_course_markup(chat_id),
        )

    elif text == "Изменить роль (тестовая функция)":
        state.set_state(chat_id, "roles")
        bot.send_message(
            chat_id,
            "Выберите желаемую роль:",
            reply_markup=markups.get_roles_markup(chat_id),
        )

    else:
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_settings_markup(),
        )


def roles_menu_handler(bot, chat_id: int, user_id: int, text: str):
    answer = role_answer(text, chat_id)
    if answer:
        http_client = HttpClient(chat_id)
        http_client.post(f"/users/{user_id}/roles", {"role_id": answer[0]})
        http_client.refresh_token()

        state.set_state(chat_id, None)
        bot.send_message(
            chat_id,
            "Ваша роль успешно изменилась",
            reply_markup=markups.get_next_markup(),
        )

    else:
        bot.send_message(
            chat_id,
            "Выберите желаемую роль:",
            reply_markup=markups.get_roles_markup(chat_id),
        )


def module_menu_handler(bot, chat_id: int, user_id: int, module_id: int):
    mrkp = markups.get_themes_markup(chat_id, module_id)

    isEmpty = not mrkp.to_dict().get("inline_keyboard")

    text = "Выберите необходимую тему:"
    if isEmpty:
        text = "К сожалению доступных тем для данного модуля еще не добавили 😞"

    bot.send_message(chat_id, text, reply_markup=mrkp)


def theme_menu_handler(bot, chat_id: int, user_id: int, text: str, theme_id: int):
    user_state = str(state.get_state(chat_id)).split("/")
    current_theme_id = user_state[1]
    current_exersise_id = user_state[2]
    http_client = HttpClient(chat_id)

    if text != "Продолжить ➡️":
        http_client.post(
            f"/users/{user_id}/exercises/{current_exersise_id}/answers",
            {"answer": text},
        )

    ex = http_client.get(
        f"/themes/{current_theme_id}/exercises/{current_exersise_id}/next"
    )

    if not ex:
        calc_result(bot, user_id, chat_id, theme_id)
        state.set_state(chat_id, "main")
        return

    ExersiseFactory.create_exersise(ex, bot, chat_id).send()

    next_exersise_id = ex[0]
    state.set_state(chat_id, f"theme/{current_theme_id}/{next_exersise_id}")


def teach_main_menu_handler(bot, chat_id: int, user_id: int, text: str):
    if text == "ℹ️ Модули":
        mrkp = markups.get_modules_markup(chat_id, user_id)

        isEmpty = not mrkp.to_dict().get("inline_keyboard")

        text = "Выберите нужный модуль:"

        if isEmpty:
            text = (
                "К сожалению доступных модулей для вашего языка и курса не найдено 😞"
            )

        bot.send_message(chat_id, text, reply_markup=mrkp)

    elif text == "📊 Статистика оценок":
        text_stat = "<b>Статистика оценок по вашим модулям 📊:</b>\n\n"

        http_client = HttpClient(chat_id)
        stat = http_client.get(f"/users/{user_id}/grades")

        if not stat:
            bot.send_message(
                chat_id, "Тестов по темам ваших модулей еще не решалось 😞"
            )
            return

        for module_id, module_name, themes in stat:
            module_stat_text = f"<b>{module_name}</b>\n"

            for theme_data in themes:
                theme_stat_text = f"ㅤ<i>{theme_data.get('theme_name')}</i>\n"

                for grade in theme_data.get("grades_data"):
                    user = grade.get("user")
                    grade = grade.get("grade")
                    last_name = user.get("last_name")
                    name = user.get("name")
                    login = user.get("login")

                    user_alias = ""
                    if last_name:
                        user_alias += f"{last_name} "
                    if name:
                        user_alias += f"{name} "
                    if login:
                        user_alias += f"({login})"

                    grade_stat_text = f"ㅤㅤ{user_alias} - {grade}\n"

                    theme_stat_text += grade_stat_text

                theme_stat_text += "\n"
                module_stat_text += theme_stat_text

            module_stat_text += "\n"
            text_stat += module_stat_text

        bot.send_message(chat_id, text_stat, parse_mode="HTML")

    elif text == "⚙️ Настройки":
        state.set_state(chat_id, "settings")
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_teacher_settings_markup(),
        )

    else:
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_teacher_main_markup(),
        )


def my_grades(bot, chat_id: int, user_id: int):
    http_client = HttpClient(chat_id)
    grades = http_client.get(f"/users/{user_id}/grades")

    if not grades:
        bot.send_message(chat_id, f"Оценок нет")

    grades_text = ""

    for module_name, module_data in grades:
        grades_text += f"<b>{module_name}</b>\n"

        for data in module_data:
            theme_name = data.get("name")
            theme_grade = data.get("grade")
            grades_text += f"ㅤ{theme_name} - {theme_grade}\n"

        grades_text += "\n"

    bot.send_message(chat_id, grades_text, parse_mode="HTML")


def admin_main_menu_handler(bot, chat_id: int, user_id: int, text: str):
    if text == "⚙️ Настройки":
        state.set_state(chat_id, "settings")
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_teacher_settings_markup(),
        )

    elif text == "📊 Сводка о пользователях":
        u_text = "<b>Список пользователей</b>\n"
        http_client = HttpClient(chat_id)
        users = http_client.get(f"/users")
        for user in users:
            name = user[1]
            last_name = user[2]
            login = user[3]
            created_at = user[7]
            role = user[8]

            user_alias = ""
            if last_name:
                user_alias += f"{last_name} "
            if name:
                user_alias += f"{name} "
            if login:
                user_alias += f"({login})"
            u_text += f"{user_alias} {role}. Создан: {created_at}\n"

        bot.send_message(chat_id, u_text, parse_mode="HTML")

    else:
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_admin_main_markup(),
        )


def teacher_settings_menu_handler(bot, chat_id: int, user_id: int, text: str):
    if text == "Изменить роль (тестовая функция)":
        state.set_state(chat_id, "roles")
        bot.send_message(
            chat_id,
            "Выберите желаемую роль:",
            reply_markup=markups.get_roles_markup(chat_id),
        )

    elif text == "⚙️ Редактировать":
        state.set_state(chat_id, "edit_module")
        bot.send_message(
            chat_id,
            "Выберите действие с модулем:",
            reply_markup=markups.get_edit_module_markup(),
        )

    else:
        bot.send_message(
            chat_id,
            "Выберите вариант из меню:",
            reply_markup=markups.get_teacher_settings_markup(),
        )


def edit_module_menu_handler(bot, chat_id: int, user_id: int, text: str):
    if text == "➕ Создать модуль":
        state.set_state(chat_id, "create_module")
        bot.send_message(
            chat_id,
            "Введите название нового модуля:",
            reply_markup=markups.remove_markup(),
        )

    elif text == "✏️ Выбрать модуль":
        bot.send_message(
            chat_id,
            "Выберите модуль для изменения:",
            reply_markup=markups.get_modules_markup(chat_id, user_id),
        )

    else:
        bot.send_message(
            chat_id,
            "Выберите действие с модулем:",
            reply_markup=markups.get_edit_module_markup(),
        )


def edit_theme_menu_handler(
    bot, chat_id: int, user_id: int, text: str, module_id: int = None
):
    if text == "➕ Создать тему":
        module_id = str(state.get_state(chat_id)).split("/")[1]
        state.set_state(chat_id, f"create_theme/{module_id}")
        bot.send_message(
            chat_id,
            "Введите название новой темы:",
            reply_markup=markups.remove_markup(),
        )

    elif text == "✏️ Выбрать тему":
        module_id = str(state.get_state(chat_id)).split("/")[1]
        mrkp = markups.get_themes_markup(chat_id, module_id)

        isEmpty = not mrkp.to_dict().get("inline_keyboard")
        if not isEmpty:
            bot.send_message(chat_id, "Выберите тему для изменения:", reply_markup=mrkp)
        else:
            bot.send_message(chat_id, "К сожалению, тем у данного модуля нет.")

    else:
        if module_id:
            state.set_state(chat_id, f"edit_module_child/{module_id}")
        bot.send_message(
            chat_id,
            f"Выберите действие внутри модуля:",
            reply_markup=markups.get_edit_theme_markup(),
        )


def edit_exersises_menu_handler(
    bot, chat_id: int, user_id: int, text: str, theme_id: int = None
):
    if text == "➕ Создать упражнение":
        theme_id = str(state.get_state(chat_id)).split("/")[1]
        state.set_state(chat_id, f"create_exersise/{theme_id}")
        create_exersise_handler(bot, chat_id, user_id, text)

    elif text == "✏️ Выбрать упражнение":
        theme_id = str(state.get_state(chat_id)).split("/")[1]
        mrkp = markups.get_exersises_markup(theme_id, chat_id)

        isEmpty = not mrkp.to_dict().get("inline_keyboard")
        if not isEmpty:
            bot.send_message(
                chat_id, "Выберите упражнение для изменения:", reply_markup=mrkp
            )
        else:
            bot.send_message(chat_id, "К сожалению, упражнений по данной теме нет.")

    else:
        if theme_id:
            state.set_state(chat_id, f"edit_theme_child/{theme_id}")
        bot.send_message(
            chat_id,
            f"Выберите действие внутри темы:",
            reply_markup=markups.get_edit_exersises_markup(),
        )


def edit_module_handler(bot, chat_id: int, user_id: int, text, module_id: int = None):
    if text == "✏️ Изменить название":
        module_id = str(state.get_state(chat_id)).split("/")[1]
        mess = bot.send_message(
            chat_id,
            "Введите новое название модуля:",
            reply_markup=markups.remove_markup(),
        )
        bot.register_next_step_handler(
            mess,
            lambda message: change_name(
                bot, chat_id, user_id, message.text, "module", module_id
            ),
        )

    elif text == "❌ Удалить":
        module_id = str(state.get_state(chat_id)).split("/")[1]

        http_client = HttpClient(chat_id)
        http_client.delete(f"/modules/{module_id}")

        bot.send_message(
            chat_id, f"Модуль удален ✅", reply_markup=markups.get_back_markup()
        )

    elif text == "Редактировать содержимое":
        state.set_state(chat_id, f"edit_module_child/{module_id}")
        edit_theme_menu_handler(bot, chat_id, user_id, None)

    else:
        if module_id:
            state.set_state(chat_id, f"edit_module/{module_id}")

        bot.send_message(
            chat_id,
            f"Выберите действие с модулем:",
            reply_markup=markups.get_edit_object_markup(),
        )


def edit_theme_handler(bot, chat_id: int, user_id: int, text, theme_id: int):
    if text == "✏️ Изменить название":
        theme_id = str(state.get_state(chat_id)).split("/")[1]
        mess = bot.send_message(
            chat_id,
            "Введите новое название темы:",
            reply_markup=markups.remove_markup(),
        )
        bot.register_next_step_handler(
            mess,
            lambda message: change_name(
                bot, chat_id, user_id, message.text, "theme", theme_id
            ),
        )

    elif text == "❌ Удалить":
        theme_id = str(state.get_state(chat_id)).split("/")[1]

        http_client = HttpClient(chat_id)
        http_client.delete(f"/themes/{theme_id}")

        bot.send_message(
            chat_id, f"Тема удалена ✅", reply_markup=markups.get_back_markup()
        )

    elif text == "Редактировать содержимое":
        state.set_state(chat_id, f"edit_theme_child/{theme_id}")
        edit_exersises_menu_handler(bot, chat_id, user_id, text, theme_id)

    else:
        if theme_id:
            module_id = str(state.get_state(chat_id)).split("/")[1]
            state.set_state(chat_id, f"edit_theme/{theme_id}/{module_id}")

        bot.send_message(
            chat_id,
            f"Выберите действие с темой:",
            reply_markup=markups.get_edit_object_markup(),
        )


def create_handler(
    bot, chat_id: int, user_id: int, text: str, create_type: str, parent_id: int = None
):
    http_client = HttpClient(chat_id)

    if create_type == "module":
        state.set_state(chat_id, "edit_module")
        langs = markups.get_lang_markup(chat_id, user_id, False)
        if len(langs.keyboard) > 1:

            def save_m(module_name: str, lang_name: str):
                lang_id = lang_answer(lang_name, chat_id)
                module_id = http_client.post(
                    f"/modules", {"name": module_name, "lang_id": lang_id[0]}
                )
                http_client.post(f"/users/{user_id}/modules", {"module_id": module_id})
                bot.send_message(
                    chat_id,
                    f'Модуль "{text}" создан ✅',
                    reply_markup=markups.get_next_markup(),
                )

            msg = bot.send_message(
                chat_id, f"Выберите язык нового модуля", reply_markup=langs
            )
            bot.register_next_step_handler(msg, lambda msg: save_m(text, msg.text))

        else:
            lang_id = lang_answer(langs.keyboard[0][0].get("text"), chat_id)
            module_id = http_client.post(
                f"/modules", {"name": text, "lang_id": lang_id[0]}
            )
            http_client.post(f"/users/{user_id}/modules", {"module_id": module_id})
            bot.send_message(
                chat_id,
                f'Модуль "{text}" создан ✅',
                reply_markup=markups.get_next_markup(),
            )

    elif create_type == "theme":
        state.set_state(chat_id, f"edit_module/{parent_id}")
        http_client.post(f"/modules/{parent_id}/themes", {"name": text})

        bot.send_message(
            chat_id, f'Тема "{text}" создана ✅', reply_markup=markups.get_next_markup()
        )


def change_name(bot, chat_id: int, user_id: int, text: str, type: str, id: int):
    http_client = HttpClient(chat_id)

    if type == "module":
        http_client.patch(f"/modules/{id}", {"name": text})
        state.set_state(chat_id, f"edit_module/{id}")
        bot.send_message(
            chat_id,
            f"Название модуля изменено ✅",
            reply_markup=markups.get_next_markup(),
        )

    elif type == "theme":
        http_client.patch(f"/themes/{id}", {"name": text})
        state.set_state(chat_id, f"edit_theme/{id}")
        bot.send_message(
            chat_id,
            f"Название темы изменено ✅",
            reply_markup=markups.get_next_markup(),
        )

    elif type == "exersise":
        http_client.patch(f"/exercises/{id}", {"title": text})
        bot.send_message(
            chat_id,
            f"Название упражнения изменено ✅",
            reply_markup=markups.get_next_markup(),
        )


def create_exersise_handler(bot, chat_id, user_id: int, text):
    answer = exersise_types_answer(text, chat_id)
    if answer:

        def save_exersise(theme_id: int, title: str):
            http_client = HttpClient(chat_id)
            exersise = http_client.post(
                f"/themes/{theme_id}/exercises", {"title": title, "type_id": answer[0]}
            )
            state.set_state(chat_id, f"edit_theme_child/{theme_id}")
            bot.send_message(chat_id, f"Упражнение создано ✅")
            edit_exersise_handler(bot, chat_id, user_id, None, exersise[0])

        theme_id = str(state.get_state(chat_id)).split("/")[1]
        mess = bot.send_message(
            chat_id,
            "Введите название упражнения:",
            reply_markup=markups.remove_markup(),
        )
        bot.register_next_step_handler(
            mess, lambda message: save_exersise(theme_id, message.text)
        )

    else:
        bot.send_message(
            chat_id,
            f"Выберите тип упражнения",
            reply_markup=markups.get_exersises_types_markup(chat_id),
        )


def edit_exersise_handler(bot, chat_id: int, user_id: int, text, exersise_id: int):
    if text == "✏️ Изменить заголовок":
        mess = bot.send_message(
            chat_id,
            "Введите новое название упражнения:",
            reply_markup=markups.remove_markup(),
        )
        bot.register_next_step_handler(
            mess,
            lambda message: change_name(
                bot, chat_id, user_id, message.text, "exersise", exersise_id
            ),
        )

    elif text == "✏️ Изменить контент":
        change_exersise_content(bot, chat_id, user_id, exersise_id)

    else:
        if exersise_id:
            state.set_state(chat_id, f"{state.get_state(chat_id)}/{exersise_id}")

        bot.send_message(
            chat_id,
            f"Выберите действие",
            reply_markup=markups.get_edit_exersise_markup(),
        )


def change_exersise_content(bot, chat_id: int, user_id: int, exersise_id: int):
    http_client = HttpClient(chat_id)
    exersise = http_client.get(f"/exercises/{exersise_id}")
    ExersiseFactory.create_exersise(exersise, bot, chat_id).change()
