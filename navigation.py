import menu_handlers


def student_nav_handler(bot, users_state, user_id, text):

    current_state = users_state.get(user_id)

    # bot.send_message(user_id, f'Обрабатывается состояние: {current_state}')

    if current_state == '1_step':
        menu_handlers._1_step_handler(bot, users_state, user_id, text)

    elif current_state == '2_step':
        menu_handlers._2_step_handler(bot, users_state, user_id, text)

    elif current_state == 'main':
        menu_handlers.main_menu_handler(bot, users_state, user_id, text)

    elif current_state == 'lang_menu':
        menu_handlers.lang_menu_handler(bot, users_state, user_id, text)
    
    elif current_state == 'course_menu':
        menu_handlers.course_menu_handler(bot, users_state, user_id, text)

    elif current_state == 'settings':
        menu_handlers.settings_menu_handler(bot, users_state, user_id, text)

    else:
        bot.send_message(user_id, "Я не понимаю эту команду")


def teach_nav_handler(bot, users_state, user_id, text):
    pass


def admin_nav_handler(bot, users_state, user_id, text):
    pass