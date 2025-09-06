from query import get_langs, get_courses, set_user_lang, upsert_settings


def lang_answer(bot, text):
    for lang in get_langs():
        if text == f'{lang[2]} {lang[1]}':
            return lang


            
def course_answer(bot, text):
    for course in get_courses():
        if text == f'{course[1]} {course[2]}':
            return course
