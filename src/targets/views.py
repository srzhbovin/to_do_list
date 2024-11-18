from fastapi import APIRouter
from typing import List

from src.database.db import connect_to_db, select_data, close_connection, insert_data, del_target,  \
    change_status, change_target
from src.targets.models import Target, UpdateTarget, TargetCreate

targets = APIRouter()


@targets.get("/todo", response_model=List[Target])
def get_all_targets():
    db_conn = connect_to_db()
    data = select_data(db_conn)
    close_connection(db_conn)
    return data


@targets.post('/todo/new_target')
def add_target(target_create: TargetCreate):
    target = Target(
        title=target_create.title,
        description=target_create.description
    )
    db_conn = connect_to_db()
    insert_data(db_conn, target.title, target.description, target.completed, target.created_at)
    close_connection(db_conn)
    return {"message": "Target added successfully"}

@targets.put('/todo/update/{title}')
def update_target(target: UpdateTarget, title: str):
    db_conn = connect_to_db()
    change_target(
        db_conn,
        title,
        target.title,
        target.description)
    close_connection(db_conn)


@targets.put('/todo/complete/{title})')
def complete_task(title: str):
    db_conn = connect_to_db()
    change_status(db_conn, title, True)
    close_connection(db_conn)


@targets.delete('/todo/delete/{target_title}')
def delete_target(target_title: str):
    db_conn = connect_to_db()
    del_target(db_conn, target_title)
    close_connection(db_conn)
