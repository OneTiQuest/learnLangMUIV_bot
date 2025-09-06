from markups import get_lang_markup, get_course_markup, get_student_start_markup
from query import upsert_settings, get_user_langs
from check_answers import lang_answer, course_answer


def student_start_script(bot, message):
    answer = lang_answer(bot, message)
    if not answer:
        answer = course_answer(bot, message)

    if not get_user_langs(message.chat.id):
        text, markup = get_lang_markup()
    elif not upsert_settings(message.chat.id)["course_id"]:
        text, markup = get_course_markup()
    else:
        text, markup = get_student_start_markup()

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

    return answer

def student_settings_script():
    pass