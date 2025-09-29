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
    
def get_langs(user_id: int = None):
    by_user = ''
    if user_id:
        by_user = (
            f"""
                JOIN 
                    users_langs ul 
                ON
                    ul.lang_id = l.id 
                WHERE
                    ul.user_id = {user_id}
            """
        )
        
    return run_sql(
        f"""
            SELECT 
                id, 
                name, 
                short_name 
            FROM 
                langs l
           	{by_user}
        """
    )

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
            ORDER BY id ASC
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
                	row_number() OVER(ORDER BY e.order ASC) AS row_n,
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

    
def set_user_grade(user_id: int, theme_id: int, grade: int):
    with conn.cursor() as cur:
        cur.execute(
            f"\
                DELETE FROM grades WHERE user_id={user_id} AND theme_id = {theme_id}; \
                INSERT INTO grades (user_id, theme_id, grade) VALUES ({user_id}, {theme_id}, {grade}) \
            "
        )

def get_user_langs(user_id: int):
    return run_sql(f"SELECT * FROM users_langs LEFT JOIN langs ON langs.id = users_langs.lang_id WHERE user_id={user_id}")

def get_user_answers(user_id: int):
    return run_sql(
        f"""
            SELECT
            	a.answer,
            	e.another_data::json->>'success_answer'
            FROM 
            	answers a
            JOIN
            	exercise e 
            ON 
            	a.exercise_id = e.id
            WHERE 
            	e.type_id IN (1, 2, 4)
            	AND a.user_id = {user_id}
        """
    )

def update_role(user_id: int, role_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                UPDATE 
                    users 
                SET 
                    role_id = {role_id} 
                WHERE chat_id = {user_id}
            """
        )

def get_teacer_stat(teacher_id: int):
    return run_sql(
        f"""
            WITH cl AS (
            	SELECT
            		lang_id,
            		(settings::json->>'course_id')::int AS course_id
            	FROM
            		users u
            	JOIN
            		users_langs ul
            	ON u.chat_id = ul.user_id
            	JOIN
            		settings s
            	ON
            		s.user_id = u.chat_id 
            	WHERE u.chat_id = {teacher_id}
            ), modules_t AS (
            	SELECT 
            		m.id AS module_id,
            		m.name AS module_name,
            		json_agg(ex_by_themes) AS ex_by_themes
            	FROM
            		modules m
            	JOIN
            		courses_modules cm 
            	ON m.id = cm.module_id
            	JOIN
            		cl
            	ON cl.lang_id = m.lang_id 
            	AND cl.course_id = cm.course_id 
            	JOIN
            		(
            			SELECT
            				t.id,
				            t.name AS theme_name,
				            t.module_id,
				            json_agg(
				            	json_build_object(
				            		'grade', g.grade, 
				            		'user', u
				            	)
				            ) as grades_data
            			FROM
            				themes t
            			JOIN
            				grades g
            			ON 	g.theme_id = t.id
            			JOIN
            				users u
            			ON u.chat_id = g.user_id 
            			GROUP BY t.id
            		) AS ex_by_themes
            	ON m.id = ex_by_themes.module_id
            	GROUP BY m.id
            )
            SELECT * FROM modules_t 
        """
    )

def get_users():
    return run_sql(
        f"""
            SELECT
            	u.chat_id,
            	u.name,
            	last_name,
            	login,
            	r.name AS role,
            	created_at
            FROM 
            	users u
            JOIN
            	roles r 
            ON
            	r.id = u.role_id
        """
    )

def get_exersises(theme_id: int):
    return run_sql(
        f"""
            SELECT 
                *
            FROM
                exercise e 
            WHERE
                e.theme_id = {theme_id}
        """
    )

def get_exersises_types():
    return run_sql(
        f"""
            SELECT 
                *
            FROM
                exercise_type et
        """
    )

def update_module(module_id: int, name: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                UPDATE 
                    modules 
                SET 
                    name = %s
                WHERE id = %s
            """
        , (name, module_id))

def update_theme(theme_id: int, name: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                UPDATE 
                    themes
                SET 
                    name = %s
                WHERE id = %s
            """
        , (name, theme_id))

def update_exersise(exersise_id: int, name: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                UPDATE 
                    exercise
                SET 
                    title = %s
                WHERE id = %s
            """
        , (name, exersise_id))

def delete_module(module_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                DELETE FROM courses_modules WHERE module_id = {module_id};
                DELETE FROM modules WHERE id = {module_id};
            """
        )

def delete_theme(theme_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                DELETE FROM exercise WHERE theme_id = {theme_id};
                DELETE FROM themes WHERE id = {theme_id};
            """
        )

def create_module(name: str, lang_id: int, user_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                WITH s_m as (
                    INSERT INTO 
                        modules
                    (
                        name,
                        lang_id
                    )
                    VALUES (
                        %s,
                        %s
                    )
                    RETURNING id
                ), course_module as (
                    SELECT
                        (s.settings::json->>'course_id')::int,
                        (SELECT * FROM s_m)
                    FROM
                        settings s 
                    WHERE
                        s.user_id = {user_id}
                    LIMIT 1
                )
                INSERT INTO 
                    courses_modules 
                (
                    course_id, 
                    module_id
                ) 
                ( SELECT * FROM course_module );
            """
        , (name, lang_id))

def create_theme(name: str, module_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                INSERT INTO 
                    themes
                (
                    name,
                    module_id
                )
                VALUES (
                    %s,
                    %s
                )
            """
        , (name, module_id))

def create_exersise(theme_id: int, type_id: int, title: str):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO exercise (theme_id, type_id, title) VALUES ({theme_id}, {type_id}, '{title}') RETURNING *"
        )
        return cur.fetchone()
    
def get_exersise_by_id(id: int):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM exercise WHERE id = {id}")
        return cur.fetchone()
    
def update_exersise(id: int, data: dict = None, title: str = None):
    change_data_query = ''
    change_title_query = ''

    if data:
        local_data = data.copy()
        key, value = local_data.popitem()
        change_data_query = f"another_data = jsonb_set(COALESCE(another_data, '{{}}')::jsonb, '{{{key}}}', '{json.dumps(value)}'::jsonb),"
    
    if title:
        change_title_query = f"title = '{title}'"

    with conn.cursor() as cur:
        cur.execute(
            f"""
                UPDATE 
                    exercise
                SET 
                    {change_data_query}
                    {change_title_query}
                WHERE id = {id}
            """
        )

def get_grades_by_user_id(user_id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                WITH gr AS (
                    SELECT 
                        t.name, 
                        g.grade,
                        t.module_id 
                    FROM 
                        grades  g
                    JOIN
                        themes t
                    ON
                        t.id = g.theme_id 
                    
                    WHERE 
                        g.user_id = {user_id}
                )
                SELECT
                    m."name",
                    json_agg(gr)
                FROM
                    modules m
                JOIN
                    gr
                ON gr.module_id = m.id
                GROUP BY m.id 
            """
        )
        return cur.fetchall()
