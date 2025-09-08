from query import upsert_settings, get_user_langs, get_exercise

def student_start_script(users_state, user_id):
    user_has_lang = get_user_langs(user_id)
    user_has_course = upsert_settings(user_id)["course_id"]

    if not user_has_lang:
        users_state[user_id] = '1_step'

    elif not user_has_course:
        users_state[user_id] = '2_step'

    else:
        users_state[user_id] = 'main'

def select_theme_script(bot, theme_id, users_state, user_id):
    first_exersise = get_exercise(theme_id)
    if not first_exersise:
        bot.send_message(user_id, "К сожалению доступных заданий для вашей темы не найдено :(")
        users_state[user_id] = 'main'

    users_state[user_id] = f"theme/{theme_id}/{first_exersise[0]}"

    bot.send_message(user_id, f"БУ БУ БУ. Введите ответ на задавние:\n{first_exersise[1]}")
