# todo: Написать скрипт создания базы данных(ER-модели) TestSystem
# Скрипт  create_db.py  должен создавать таблицы, индексы , констрейнты в СУБД PostgresSQL
# В задании использовать библиотеку psycopg

#Ссылка на документацию
#https://www.psycopg.org/psycopg3/docs/basic/usage.html
#Для подключения использовать пользователя и базу отличную от postgres

import psycopg

with psycopg.connect("dbname=db_psy user=user_psycopg password=1234") as conn:
    with conn.cursor() as cur:

        #создание таблиц
        cur.execute("""
            CREATE TABLE "group" (
                "id_group" serial PRIMARY KEY,
                "group_name" varchar(100))
            """)
        cur.execute("""
            CREATE TABLE "student" (
                "id_student" serial PRIMARY KEY,
                "id_group" integer not null,
                "surname" varchar(100),
                "name" varchar(100),
                "patronity" varchar(100),
                "age" integer)
            """)

        #создание констрейнта
        cur.execute("""
            alter table "student" add constraint "cnst_student_ref_group"
            foreign key ("id_group") references "group"("id_group")
            on delete restrict;
            """)

        #создание индекса
        cur.execute("""
            CREATE INDEX "idx_student_id_group" ON "student" ("id_group");
            """)
