import asyncpg
from src.database.config_db import host, db_name, db_password, db_user, port


async def connect_to_db():
    try:
        db_conn = await asyncpg.connect(
            host=host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=port
        )
        print(f"[INFO] Соединение с базой данных '{db_name}' установлено.")
        return db_conn
    except Exception as e:
        print("[INFO] Ошибка при работе с PostgreSQL:", e)
        return None


# Закрытие соединения с базой данных
async def close_connection(db_conn):
    if db_conn:
        await db_conn.close()
        print(f"[INFO] Соединение с базой данных '{db_name}' закрыто.")


async def select_data(db_conn):
    data = await db_conn.fetch('SELECT * FROM targets')
    columns = [desc.name for desc in data[0].keys()]
    return [dict(zip(columns, row)) for row in data]


async def insert_data(db_conn, title, description, completed, created_at):
    await db_conn.execute(
        "INSERT INTO targets (title, description, completed, created_at) VALUES ($1, $2, $3, $4)",
        (title, description, completed, created_at)
    )


async def change_target(db_conn, title, new_title=None, new_description=None):
    if (new_title is None or new_title == 'string') and (new_description is None or new_description == 'string'):
        return None
    if new_title is None or new_title == 'string':
        new_title = await db_conn.fetchval('SELECT title FROM targets WHERE title = $1', (title,))
    if new_description is None or new_description == 'string':
        new_description = await db_conn.fetchval('SELECT description FROM targets WHERE title = $1', (title,))
    await db_conn.execute('UPDATE targets SET title = $1, description =$2 WHERE title = $3',
                          (new_title, new_description, title))
    print(f'Цель {title} обновлена.')


async def change_status(db_conn, title: str, completed: bool):
    await db_conn.execute('UPDATE targets SET completed= $1 WHERE title= $2', (completed, title))
    print(f'Цель {title} выполнена.')


async def del_target(db_conn, title):
    await db_conn.execute('DELETE FROM targets WHERE title = $1', (title,))
    print(f'Цель {title} удалена.')
