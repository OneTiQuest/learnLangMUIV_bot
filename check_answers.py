from query import get_langs, get_courses, set_user_lang, upsert_settings


def lang_answer(bot, message):
    for lang in get_langs():
        if message.text == f'{lang[2]} {lang[1]}':
            set_user_lang(message.chat.id, lang[0])
            bot.send_message(message.chat.id, f'Текущий язык для обучения: {message.text}')
            return True


            
def course_answer(bot, message):
    for course in get_courses():
        if message.text == f'{course[1]} {course[2]}':
            upsert_settings(message.chat.id, "course_id", course[0])
            bot.send_message(message.chat.id, f'Текущий выбранный курс: {message.text}')
            return True