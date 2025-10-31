from bot.api import HttpClient

def lang_answer(text, chat_id: int):
    http_client = HttpClient(chat_id)
    l = http_client.get(f"/langs")
    for lang in l:
        if text == f'{lang[2]} {lang[1]}':
            return lang


def course_answer(text, chat_id: int):
    http_client = HttpClient(chat_id)
    с = http_client.get(f"/courses")
    for course in с:
        if text == f'{course[1]} {course[2]}':
            return course


def role_answer(text, chat_id: int):
    http_client = HttpClient(chat_id)
    rs = http_client.get(f"/roles")
    for role in rs:
        if text == role[1]:
            return role


def module_answer(text, chat_id: int, user_id):
    http_client = HttpClient(chat_id)
    ms = http_client.get(f"/users/{user_id}/modules")
    for role in ms:
        if text == role[1]:
            return role


def exersise_types_answer(text, chat_id: int):
    http_client = HttpClient(chat_id)
    et = http_client.get(f"/exercises/types")
    for type in et:
        if text == type[1]:
            return type
