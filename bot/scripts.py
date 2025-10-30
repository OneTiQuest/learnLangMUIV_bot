from bot.exersise_handlers import ExersiseFactory
import bot.markups as markups
import bot.state as state
from telebot import TeleBot, types


def init_settings_script(user_id):
    user_has_lang = get_user_langs(user_id)
    user_has_course = upsert_settings(user_id)["course_id"]

    if not user_has_lang:
        state.set_state(user_id, "1_step")

    elif not user_has_course:
        state.set_state(user_id, "2_step")

    else:
        state.set_state(user_id, "main")


def select_theme_script(bot, theme_id, user_id):
    first_exersise = get_exercise(theme_id)
    if not first_exersise:
        bot.send_message(
            user_id, "К сожалению доступных заданий для вашей темы не найдено :("
        )
        state.set_state(user_id, "main")
        return

    state.set_state(user_id, f"theme/{theme_id}/{first_exersise[0]}")

    ExersiseFactory.create_exersise(first_exersise, bot, user_id).send()


def calc_result(bot, user_id: int, theme_id: int):
    answers = get_user_answers(user_id, theme_id)
    max_a = len(answers)
    s_a_counter = 0

    for u_a, s_a in answers:
        if str(u_a).lower() == str(s_a).lower():
            s_a_counter += 1

    test_result = (s_a_counter * 100) / max_a

    prefix = f"успешно"
    grade = 5
    smile = "😊"
    if test_result < 50:
        prefix = f"не"
        grade = 2
        smile = "😞"

    elif test_result < 75:
        grade = 3

    elif test_result < 85:
        grade = 4

    bot.send_message(
        user_id,
        f"<b>Вы {prefix} сдали тест {smile}</b>\n\n{s_a_counter} из {max_a} вопросов решено верно. Ваша оценка {grade}",
        reply_markup=markups.get_next_markup(),
        parse_mode="HTML",
    )

    return grade


def login_form(bot: TeleBot, message: types.Message, success_cb):
    chat_id = message.chat.id
    form = {}

    def auth_question(msg: types.Message, field: str):
        if field == "login":
            form["login"] = msg.text
            bot.send_message(
                chat_id, "Введите пароль:", reply_markup=markups.remove_markup()
            )
            bot.register_next_step_handler(
                message, lambda msg: auth_question(msg, "password")
            )
        elif field == "password":
            form["password"] = msg.text
            success_cb((form.get("login"), form.get("password")))

    bot.send_message(chat_id, "Введите логин:", reply_markup=markups.remove_markup())
    bot.register_next_step_handler(message, lambda msg: auth_question(msg, "login"))


def register_form(bot: TeleBot, message: types.Message, success_cb):
    chat_id = message.chat.id
    form = {}

    def auth_question(msg: types.Message, field: str):
        if field == "login":
            form["login"] = msg.text
            bot.send_message(
                chat_id, "Введите пароль:", reply_markup=markups.remove_markup()
            )
            bot.register_next_step_handler(
                message, lambda msg: auth_question(msg, "password")
            )
        elif field == "password":
            form["password"] = msg.text
            bot.send_message(
                chat_id,
                "Повторите пароль:",
            )
            bot.register_next_step_handler(
                message, lambda msg: auth_question(msg, "repeat_password")
            )
        elif field == "repeat_password":
            form["repeat_password"] = msg.text
            if form.get("password") != form.get("repeat_password"):
                bot.send_message(
                    chat_id,
                    "Пароли не совпадают ❌",
                )
                bot.send_message(
                    chat_id,
                    "Повторите пароль:",
                )
                bot.register_next_step_handler(
                    message, lambda msg: auth_question(msg, "repeat_password")
                )

            else:
                success_cb((form.get("login"), form.get("password")))

    bot.send_message(chat_id, "Введите логин:", reply_markup=markups.remove_markup())
    bot.register_next_step_handler(message, lambda msg: auth_question(msg, "login"))
