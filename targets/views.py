from fastapi import APIRouter
from typing import List

from database.db import connect_to_db, select_data, close_connection, insert_data, del_target
from targets.models import Target

targets = APIRouter()


@targets.get("/todo", response_model=List[Target])
def get_all_targets():
    db_conn = connect_to_db()
    data = select_data(db_conn)
    close_connection(db_conn)
    return data


@targets.post('/todo')
def add_target(target: Target):
    db_conn = connect_to_db()
    insert_data(db_conn, target.dict())
    close_connection(db_conn)


@targets.delete('/todo/{target_title}')
def delete_target(target_title: str):
    db_conn = connect_to_db()
    del_target(db_conn, target_title)
    close_connection(db_conn)
