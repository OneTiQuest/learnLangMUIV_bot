from query import upsert_settings, get_user_langs

def student_start_script(users_state, user_id):
    user_has_lang = get_user_langs(user_id)
    user_has_course = upsert_settings(user_id)["course_id"]

    if not user_has_lang:
        users_state[user_id] = '1_step'

    elif not user_has_course:
        users_state[user_id] = '2_step'

    else:
        users_state[user_id] = 'main'
