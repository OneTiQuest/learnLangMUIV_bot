-- public.courses определение

-- Drop table

-- DROP TABLE public.courses;

CREATE TABLE public.courses (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	code varchar NULL,
	CONSTRAINT course_pk PRIMARY KEY (id)
);


-- public.exercise_type определение

-- Drop table

-- DROP TABLE public.exercise_type;

CREATE TABLE public.exercise_type (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	CONSTRAINT exercise_type_pk PRIMARY KEY (id)
);


-- public.langs определение

-- Drop table

-- DROP TABLE public.langs;

CREATE TABLE public.langs (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NOT NULL,
	short_name varchar NULL,
	CONSTRAINT langs_pk PRIMARY KEY (id)
);


-- public.roles определение

-- Drop table

-- DROP TABLE public.roles;

CREATE TABLE public.roles (
	id int8 NOT NULL,
	"name" varchar NULL,
	CONSTRAINT roles_pk PRIMARY KEY (id)
);


-- public.settings определение

-- Drop table

-- DROP TABLE public.settings;

CREATE TABLE public.settings (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	settings varchar NULL,
	user_id int8 NOT NULL,
	CONSTRAINT settings_pk PRIMARY KEY (id)
);


-- public.modules определение

-- Drop table

-- DROP TABLE public.modules;

CREATE TABLE public.modules (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	lang_id int8 NULL,
	CONSTRAINT modules_pk PRIMARY KEY (id),
	CONSTRAINT modules_langs_fk FOREIGN KEY (lang_id) REFERENCES public.langs(id)
);


-- public.themes определение

-- Drop table

-- DROP TABLE public.themes;

CREATE TABLE public.themes (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	"order" int4 DEFAULT 0 NULL,
	module_id int8 NULL,
	CONSTRAINT themes_pk PRIMARY KEY (id),
	CONSTRAINT themes_modules_fk FOREIGN KEY (module_id) REFERENCES public.modules(id) ON DELETE CASCADE
);


-- public.users определение

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	"name" varchar NULL,
	last_name varchar NULL,
	login varchar NULL,
	chat_id int8 NOT NULL,
	role_id int8 NULL,
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	created_at date DEFAULT now() NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id),
	CONSTRAINT users_roles_fk FOREIGN KEY (role_id) REFERENCES public.roles(id)
);
CREATE INDEX users_chat_id_idx ON public.users USING btree (chat_id);


-- public.users_langs определение

-- Drop table

-- DROP TABLE public.users_langs;

CREATE TABLE public.users_langs (
	user_id int8 NULL,
	lang_id int8 NULL,
	CONSTRAINT users_langs_langs_fk FOREIGN KEY (lang_id) REFERENCES public.langs(id)
);


-- public.courses_modules определение

-- Drop table

-- DROP TABLE public.courses_modules;

CREATE TABLE public.courses_modules (
	course_id int8 NULL,
	module_id int8 NULL,
	CONSTRAINT courses_modules_courses_fk FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE,
	CONSTRAINT courses_modules_modules_fk FOREIGN KEY (module_id) REFERENCES public.modules(id) ON DELETE CASCADE
);


-- public.exercise определение

-- Drop table

-- DROP TABLE public.exercise;

CREATE TABLE public.exercise (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	title varchar NULL,
	"order" int4 DEFAULT 0 NULL,
	another_data varchar NULL,
	theme_id int8 NULL,
	type_id int8 NULL,
	CONSTRAINT exercise_pk PRIMARY KEY (id),
	CONSTRAINT exercise_exercise_type_fk FOREIGN KEY (type_id) REFERENCES public.exercise_type(id),
	CONSTRAINT exercise_themes_fk FOREIGN KEY (theme_id) REFERENCES public.themes(id) ON DELETE CASCADE
);


-- public.grades определение

-- Drop table

-- DROP TABLE public.grades;

CREATE TABLE public.grades (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	user_id int8 NULL,
	theme_id int8 NULL,
	grade int4 NULL,
	CONSTRAINT grades_pk PRIMARY KEY (id),
	CONSTRAINT grades_themes_fk FOREIGN KEY (theme_id) REFERENCES public.themes(id) ON DELETE CASCADE
);


-- public.answers определение

-- Drop table

-- DROP TABLE public.answers;

CREATE TABLE public.answers (
	user_id int8 NOT NULL,
	exercise_id int8 NOT NULL,
	answer varchar NULL,
	CONSTRAINT answers_exercise_fk FOREIGN KEY (exercise_id) REFERENCES public.exercise(id)
);


INSERT INTO public.answers (user_id,exercise_id,answer) VALUES
	 (763450071,4,'are'),
	 (763450071,5,'am'),
	 (1439369229,11,'am'),
	 (1439369229,4,'To'),
	 (1439369229,5,'am'),
	 (1439369229,15,'must'),
	 (1439369229,17,'нет'),
	 (1854065391,4,'eeee'),
	 (1854065391,5,'am');
INSERT INTO public.courses ("name",code) VALUES
	 ('Прикладная информатика','09.03.03'),
	 ('Психолого-педагогическое образование','44.03.02'),
	 ('Туризм ','43.03.02'),
	 ('Юриспруденция ','40.03.01'),
	 ('Бизнес-информатика','38.03.05'),
	 ('Государственное и муниципальное управление','38.03.04'),
	 ('Экономика ','38.03.01');
INSERT INTO public.courses_modules (course_id,module_id) VALUES
	 (4,1),
	 (6,1),
	 (8,1),
	 (9,1),
	 (10,1),
	 (13,1),
	 (1,2),
	 (4,2),
	 (6,2),
	 (8,2);
INSERT INTO public.courses_modules (course_id,module_id) VALUES
	 (9,2),
	 (10,2),
	 (1,4),
	 (1,7),
	 (1,8),
	 (1,9),
	 (1,10),
	 (1,11),
	 (1,12),
	 (1,13);
INSERT INTO public.courses_modules (course_id,module_id) VALUES
	 (1,1),
	 (1,14),
	 (1,24),
	 (1,26);
INSERT INTO public.exercise (title,"order",another_data,theme_id,type_id) VALUES
	 ('Применение глагола',0,'{"content": [{"type": "text", "data": "Глагол to be играет важную роль в английской грамматике. Точнее сказать, роли: это и самостоятельный глагол, и вспомогательный, и глагол-связка. Без глагола to be не получится построить предложения в пассивном залоге и во временах группы Continuous. Кроме того, to be входит в состав некоторых конструкций и фразовых глаголов."}]}',1,5),
	 ('Произношение глагола',1,'{"content": [{"type": "text", "data": "Глагол to be имеет разные формы произношения в зависимости от времени и лица: в настоящем времени это am [æm], is [ɪz] и are [ɑ:]; в прошедшем — was [wɒz] и were [wɜː]; а в прошедшем совершенном времени добавляется форма been [biːn]."}]}',1,5),
	 ('ку2',0,'{"success_answer": "нет"}',118,1),
	 ('______ you our new teacher? ',3,'{"success_answer": "are"}',1,1),
	 ('I ____ a student.',4,'{"answers": ["am", "is", "have", "go"], "success_answer": "am"}',1,2),
	 ('Прослушайте запись',2,'{"path": "./media/audio/3.mp3"}',1,3),
	 ('новое назв',0,'{"content": [{"data": "теория", "type": "text"}]}',118,5),
	 ('I ____ a dog',0,'{"answers": ["am", "da", "net"], "success_answer": "da"}',1,2),
	 ('Теория английского',0,NULL,3,5),
	 ('Тест. 
You ______ finish your homework before you play video games.
a) must
b) can',0,NULL,1,2);
INSERT INTO public.exercise (title,"order",another_data,theme_id,type_id) VALUES
	 ('e',0,'{"answers": ["das", "da"], "success_answer": "da"}',1,2),
	 ('You ______ finish your homework before you play video games.',0,'{"answers": ["must", "may"], "success_answer": "must"}',115,2);
INSERT INTO public.exercise_type ("name") VALUES
	 ('Недостающее слово'),
	 ('Правильный вариант'),
	 ('Аудио'),
	 ('Теория');
INSERT INTO public.grades (user_id,theme_id,grade) VALUES
	 (1854065391,1,3),
	 (763450071,1,5),
	 (1439369229,3,2),
	 (1439369229,1,2),
	 (1439369229,115,5),
	 (1439369229,118,5);
INSERT INTO public.langs ("name",short_name) VALUES
	 ('Английский','🇬🇧'),
	 ('Французский','🇨🇵'),
	 ('Немецкий','🇩🇪');
INSERT INTO public.modules ("name",lang_id) VALUES
	 ('Pre-Intermediate (A2)',2),
	 ('Intermediate (B1)',2),
	 ('Upper-Intermediate (B2)',2),
	 ('Advanced (C1)',2),
	 ('Уровень А1 (Anfänger)',1),
	 ('Уровень А2 (Grundlagen)',1),
	 ('Уровень В1 (Aufbau 1)
',1),
	 ('Уровень B2 (Aufbau 2)',1),
	 ('Уровень С1 (Fortgeschrittene 1)',1),
	 ('Уровень С2 (Fortgeschrittene 2)',1);
INSERT INTO public.modules ("name",lang_id) VALUES
	 ('Модуль 1',3),
	 ('Модуль 2',3),
	 ('англ яз 2',2),
	 ('Beginer (A1)',2),
	 ('ba4',2),
	 ('у1',2);
INSERT INTO public.roles (id,"name") VALUES
	 (1,'Ученик'),
	 (2,'Преподаватель'),
	 (3,'Администратор');
INSERT INTO public.settings (settings,user_id) VALUES
	 ('{"course_id": 1}',1854065391),
	 ('{"course_id": 1}',763450071),
	 ('{"course_id": 1}',1439369229),
	 ('{"course_id": null}',6177171034);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Глагол to be',0,1),
	 ('Типы предложений',0,1),
	 ('Артикли',0,1),
	 ('Описательный оборот there is/are',0,1),
	 ('Предлоги времени',0,2),
	 ('т1',0,26),
	 ('Порядок слов в вопросительных предложениях',0,2),
	 ('Притяжательные местоимения mine, his, hers, its, yours, ours, theirs

',0,2),
	 ('Something/anything/nothing

',0,2),
	 ('Глаголы состояния

',0,3);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Придаточные определительные предложения с that/who/which/where

',0,3),
	 ('Герундий',0,3),
	 ('Модальные глаголы have to, must, should, may, might

',0,3),
	 ('Нулевой артикль

',0,4),
	 ('Предположения с модальными глаголами can’t, might, must

',0,4),
	 ('Квантификаторы a little/little, a few/few, plenty of/a lot of, all, every, both, no/none, most

',0,4),
	 ('Косвенные вопросы

',0,4),
	 ('Модальные глаголы в прошедшем времени

',0,5),
	 ('Условные предложения смешанного типа

',0,5),
	 ('Обратный порядок слов в предложении

',0,5);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Каузативные глаголы get/have

',0,5),
	 ('Алфавит (Alphabet)',0,7),
	 ('Существительные и артикли (Nomen und Artikel)',0,7),
	 ('Личные местоимения (Personalpronomen)',0,7),
	 ('Глаголы: настоящее время (Verben: Präsens)',0,7),
	 ('rere',0,24),
	 ('Настоящее время (Präsens)',0,8),
	 ('Совершенное время (Perfekt)',0,8),
	 ('Сравнительные союзы (Vergleichssätze)',0,8),
	 ('Повелительное наклонение (Imperativ)',0,8);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Глаголы с предлогами (Verben mit Präpositionen)',0,9),
	 ('Условные предложения (Bedingungssätze)',0,9),
	 ('Прошедшее время (Perfekt, Präteritum)',0,9),
	 ('Косвенная речь (Indirekte Rede)',0,9),
	 ('Пассивный залог (Passiv)',0,10),
	 ('Относительные предложения (Relativsätze)',0,10),
	 ('Способы выражения будущего времени (Futurformen)',0,10),
	 ('Немецкие падежи (Nominativ, Genitiv, Dativ, Akkusativ)',0,10),
	 ('Герундий и инверсия (Gerundium und Inversion)',0,11),
	 ('Причастные конструкции (Die Partizipialkonstruktionen)',0,11);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Инфинитивные конструкции (Die Infinitivkonstruktionen)',0,11),
	 ('Различные виды придаточных предложений (Die verschiedenen Arten von Nebensätzen)',0,11),
	 ('Степени сравнения (Die Steigerungsformen)',0,12),
	 ('Различные виды сравнений (Komparationen)',0,12),
	 ('Сложные предлоги и союзы (Zusammengesetzte Präpositionen und Konjunktionen)',0,12),
	 ('Различные виды прямой речи (Indirekte Rede)',0,12);
INSERT INTO public.users ("name",last_name,login,chat_id,role_id,created_at) VALUES
	 ('Andrew',NULL,'Maverpir',1854065391,2,'2025-09-19'),
	 ('Максим',NULL,'OneTiQuest',763450071,2,'2025-09-10'),
	 ('Вероника',NULL,NULL,1439369229,1,'2025-09-10'),
	 ('Максим',NULL,NULL,6177171034,1,'2025-09-14');
INSERT INTO public.users_langs (user_id,lang_id) VALUES
	 (763450071,2),
	 (1854065391,2),
	 (1439369229,3);
