# Импорт необходимых библиотек
import psycopg2
from database.config_db import host, db_name, db_password, db_user, port


# Подключение к базе данных
def connect_to_db():
    try:
        db_conn = psycopg2.connect(
            host=host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=port
        )
        print(f"[INFO] Соединение с базой данных '{db_name}' установлено.")
        db_conn.autocommit = True
        return db_conn

    except Exception as e:
        print("[INFO] Ошибка при работе с PostgreSQL:", e)
    return None


# Закрытие соединения с базой данных
def close_connection(db_conn):
    if db_conn:
        db_conn.close()
        print(f"[INFO] Соединение с базой данных '{db_name}' закрыто.")


def select_data(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT * FROM targets')
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in data]


def insert_data(db_conn, data):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO targets (title, description, completed, created_at) VALUES (%s, %s, %s, %s)",
            (data['title'], data['description'], data['completed'], data['created_at'])
        )


def update_target(db_conn, title, new_title, new_description, new_completed):
    with db_conn.cursor() as cursor:
        cursor.execute('UPDATE targets SET title=%s, description=%s, completed=%s WHERE title = %s',
                       (new_title, new_description, new_completed, title))
        print(f'Цель {title} обновлена')


def change_status(db_conn, title: str, completed: bool):
    with db_conn.cursor() as cursor:
        cursor.execute('UPDATE targets SET completed=%s WHERE title= %s', (completed, title))


def del_target(db_conn, title):
    with db_conn.cursor() as cursor:
        cursor.execute('DELETE FROM targets WHERE title = %s', (title,))
