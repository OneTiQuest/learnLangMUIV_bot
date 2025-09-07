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

def get_roles():
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, name FROM roles")
        return cur.fetchall()

def get_modules(user_id: int):
    with conn.cursor() as cur:
        cur.execute(f"""
            WITH lang_modules AS (
            	SELECT
            		m.id AS module_id,
            		user_id
            	FROM 
            		users_langs ul
            	JOIN
            		modules m
            	ON 
            		m.lang_id = ul.lang_id
            ), course_modules AS (
            	SELECT
            		module_id,
            		user_id AS cui
            	FROM 
            		courses_modules cm
            	JOIN
            		settings s
            	ON 
            		cm.course_id = (s.settings::json->>'course_id')::int
            ), m_ids AS (
            	SELECT 
            		*
            	FROM
            		lang_modules lm
            	FULL JOIN
            		course_modules cm
            	USING(module_id)
            )
            SELECT
            	id,
            	name
            FROM 
            	m_ids
            JOIN
            	modules m
            ON
            	m_ids.module_id = m.id
            WHERE 
            	m_ids.user_id = {user_id}
            	AND 
            	m_ids.cui = {user_id}
        """)
        return cur.fetchall()
    
def get_themes_by_module_id(module_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                SELECT
                	*
                FROM 
                	themes t
                WHERE
                	module_id = {module_id}
                ORDER BY t."order" ASC
            """)

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
                "course_id": None
            }

            cur.execute(
                f"INSERT INTO settings (settings, user_id) VALUES (%s, %s)",
                (json.dumps(settings), chat_id)
            )

        if setting_name and value:

            settings[setting_name] = value

            cur.execute(
                f"UPDATE settings SET settings = %s, user_id = %s WHERE user_id={chat_id}",
                (json.dumps(settings), chat_id)
            )

        return settings
    
def set_user_lang(user_id: int, lang_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"\
            DELETE FROM users_langs WHERE user_id={user_id}; \
            INSERT INTO users_langs (user_id, lang_id) VALUES (%s, %s) \
            ",
            (user_id, lang_id)
        )

def get_user_langs(user_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM users_langs LEFT JOIN langs ON langs.id = users_langs.lang_id WHERE user_id={user_id}"
        )
        return cur.fetchall()