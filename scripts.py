from query import upsert_settings, get_user_langs, get_exercise, get_user_answers
from exersise_handlers import ExersiseFactory
import markups
import state


def init_settings_script(user_id):
    user_has_lang = get_user_langs(user_id)
    user_has_course = upsert_settings(user_id)["course_id"]

    if not user_has_lang:
        state.set_state(user_id, '1_step')

    elif not user_has_course:
        state.set_state(user_id, '2_step')

    else:
        state.set_state(user_id, 'main')


def select_theme_script(bot, theme_id, user_id):
    first_exersise = get_exercise(theme_id)
    if not first_exersise:
        bot.send_message(user_id, "К сожалению доступных заданий для вашей темы не найдено :(")
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
        parse_mode="HTML"
    )

    return grade
