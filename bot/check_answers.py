

def lang_answer(text):
    for lang in get_langs():
        if text == f'{lang[2]} {lang[1]}':
            return lang


def course_answer(text):
    for course in get_courses():
        if text == f'{course[1]} {course[2]}':
            return course


def role_answer(text):
    for role in get_roles():
        if text == role[1]:
            return role

def module_answer(text, user_id):
    for role in get_modules(user_id):
        if text == role[1]:
            return role
        
def exersise_types_answer(text):
    for type in get_exersises_types():
        if text == type[1]:
            return type