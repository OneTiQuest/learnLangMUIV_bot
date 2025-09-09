import psycopg2
import json

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host="localhost", port=5432)
conn.autocommit = True

def run_sql(query: str, is_one: bool = False, is_log: bool = False):
    if is_log:
        print(query)

    with conn.cursor() as cur:
        cur.execute(query)

        if is_one:
            return cur.fetchone()
        
        return cur.fetchall()

def get_user_by_chat_id(chat_id: int):
    return run_sql(f"SELECT name, last_name, login, chat_id, role_id FROM users WHERE chat_id={chat_id}", True)

def save_user(user_info):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO users (name, last_name, login, chat_id, role_id) VALUES (%s, %s, %s, %s, 1) RETURNING *", 
            (user_info.first_name, user_info.last_name, user_info.username, user_info.id)
        )
        return cur.fetchone()
    
def get_langs():
    return run_sql(f"SELECT id, name, short_name FROM langs")

def get_courses():
    return run_sql(f"SELECT id, name, code FROM courses")

def get_roles():
    return run_sql(f"SELECT id, name FROM roles")

def get_modules(user_id: int):
    return run_sql(
        f"""
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
        """
    )
    
def get_themes_by_module_id(module_id: int):
    return run_sql(
        f"""
            SELECT
            	id,
                name
            FROM 
            	themes t
            WHERE
            	module_id = {module_id}
            ORDER BY t."order" ASC
        """
    )


"""
Получение текущего упражнения ученика
"""
def get_exercise(theme_id: int, prev_ex_id: int=None):
    cut_cond = ''
    if prev_ex_id:
        cut_cond += f"JOIN prev_ex_limit pel ON te.row_n = pel.row_n + 1"

    return run_sql(
        f"""
            WITH theme_ex AS (
                SELECT
                	row_number() OVER() AS row_n,
                	*
                FROM
                	exercise e
                WHERE theme_id = {theme_id}
                ORDER BY e.order ASC
            ), prev_ex_limit AS (
                SELECT
            		row_n
                FROM
            		theme_ex
                WHERE id = {prev_ex_id or 1}
            )
            SELECT
                te.id,
                te.title,
                te.order,
                te.another_data,
                te.theme_id,
                te.type_id
            FROM
                theme_ex te
            {cut_cond}
            LIMIT 1
        """,
        True
    )

def save_answer(ex_id: int, user_id: int, answer: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                DELETE FROM answers WHERE exercise_id = {ex_id} AND user_id = {user_id};
                INSERT INTO answers (exercise_id, user_id, answer) VALUES ({ex_id}, {user_id}, %s);
            """,
            (answer,)
        )

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
    return run_sql(f"SELECT * FROM users_langs LEFT JOIN langs ON langs.id = users_langs.lang_id WHERE user_id={user_id}")