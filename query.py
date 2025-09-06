import psycopg2
import json

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host="localhost", port=5432)
conn.autocommit = True

def get_user_by_chat_id(chat_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT id, name, last_name, login, chat_id, role_id FROM users WHERE chat_id={chat_id}"
        )
        return cur.fetchone()

def save_user(user_info):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO users (name, last_name, login, chat_id, role_id) VALUES (%s, %s, %s, %s, 1) RETURNING *", 
            (user_info.first_name, user_info.last_name, user_info.username, user_info.id)
        )
        return cur.fetchone()
    
def get_langs():
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, name, short_name FROM langs")
        return cur.fetchall()

def get_courses():
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, name, code FROM courses")
        return cur.fetchall()
    

def create_lang(name, short_name):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO langs (name, short_name) VALUES (%s, %s)", 
            (name, short_name)
        )
    
def upsert_settings(chat_id: int, setting_name=None, value=None):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT settings FROM settings WHERE user_id={chat_id}"
        )
        res = cur.fetchone()
        settings = res and json.loads(res[0])

        if not settings:
            settings = {
                "lang": None,
                "course_id": None
            }

        if setting_name and value:

            settings[setting_name] = value

            cur.execute(
                f"INSERT INTO settings (settings, user_id) VALUES (%s, %s)",
                (json.dumps(settings), chat_id)
            )

        return settings
    
def set_user_lang(user_id: int, lang_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO users_langs (user_id, lang_id) VALUES (%s, %s)",
            (user_id, lang_id)
        )

def get_user_langs(user_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM users_langs LEFT JOIN langs ON langs.id = users_langs.lang_id WHERE user_id={user_id}"
        )
        return cur.fetchall()