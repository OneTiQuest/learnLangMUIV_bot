from check_answers import lang_answer, course_answer
import markups
from query import get_langs, get_courses, set_user_lang, upsert_settings

def _1_step_handler(bot, users_state, user_id: int, text: str):
    answer = lang_answer(bot, text)
    if answer:
        set_user_lang(user_id, answer[0])
        bot.send_message(user_id, f'Текущий язык для обучения: {text}')

        users_state[user_id] = '2_step'
        bot.send_message(
            user_id, 
            "Смена курса обучения:", 
            reply_markup=markups.get_course_markup()
        )

    else:
        bot.send_message(
            user_id, 
            "Смена языка обучения:", 
            reply_markup=markups.get_lang_markup()
        )

def _2_step_handler(bot, users_state, user_id: int, text: str):
    answer = course_answer(bot, text)
    if answer:
        upsert_settings(user_id, "course_id", answer[0])
        bot.send_message(user_id, f'Текущий выбранный курс: {text}')

        users_state[user_id] = 'main'
        bot.send_message(
            user_id, 
            "Выбери пункт меню:", 
            reply_markup=markups.get_main_markup()
        )

    else:
        bot.send_message(
            user_id, 
            "Смена курса обучения:", 
            reply_markup=markups.get_course_markup()
        )

def main_menu_handler(bot, users_state, user_id: int, text: str):
    if text == 'Модули':
        pass

    elif text == 'Настройки':
        users_state[user_id] = 'settings'
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())

    else:
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_main_markup())


def lang_menu_handler(bot, users_state, user_id: int, text: str):
    answer = lang_answer(bot, text)
    if answer:
        set_user_lang(user_id, answer[0])
        bot.send_message(user_id, f'Текущий язык для обучения: {text}')

        users_state[user_id] = 'settings'
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())

    else:
        bot.send_message(user_id, "Смена языка обучения:", reply_markup=markups.get_lang_markup())


def course_menu_handler(bot, users_state, user_id: int, text: str):
    answer = course_answer(bot, text)
    if answer:
        upsert_settings(user_id, "course_id", answer[0])
        bot.send_message(user_id, f'Текущий выбранный курс: {text}')

        users_state[user_id] = 'settings'
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())

    else:
        bot.send_message(user_id, "Смена курса обучения:", reply_markup=markups.get_course_markup())

def settings_menu_handler(bot, users_state, user_id: int, text: str):
    if text == "Изменить изучаемый язык":
        users_state[user_id] = 'lang_menu'
        bot.send_message(user_id, "Смена языка обучения:", reply_markup=markups.get_lang_markup())
    
    elif text == "Изменить курс обучения":
        users_state[user_id] = 'course_menu'
        bot.send_message(user_id, "Смена курса обучения:", reply_markup=markups.get_course_markup())

    elif text == "Изменить роль (тестовая функция)":
        pass
        
    else:
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())
