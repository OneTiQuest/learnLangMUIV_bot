import psycopg2

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host="localhost", port=5432)
conn.autocommit = True

def get_user_by_chat_id(chat_id: int):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM users WHERE chat_id={chat_id}")
        return cur.fetchone()

def save_user(user_info):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO users (name, last_name, login, chat_id, role_id) VALUES (%s, %s, %s, %s, 1)", 
            (user_info.first_name, user_info.last_name, user_info.username, user_info.id)
            )