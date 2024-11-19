from fastapi import APIRouter
from typing import List

from src.database.db import connect_to_db, select_data, close_connection, insert_data, del_target, \
    change_status, change_target
from src.targets.models import Target, UpdateTarget, TargetCreate

targets = APIRouter()


@targets.get("/todo", response_model=List[Target])
async def get_all_targets():
    async with await connect_to_db() as db_conn:
        data = await select_data(db_conn)
        return data


@targets.post('/todo/new_target')
async def add_target(target_create: TargetCreate):
    target = Target(
        title=target_create.title,
        description=target_create.description
    )
    async with await connect_to_db() as db_conn:
        await insert_data(db_conn, target.title, target.description, target.completed, target.created_at)
        return {"message": "Target added successfully"}


@targets.put('/todo/update/{title}')
async def update_target(target: UpdateTarget, title: str):
    async with await connect_to_db() as db_conn:
        await change_target(
            db_conn,
            title,
            target.title,
            target.description)


@targets.put('/todo/complete/{title}')
async def complete_task(title: str):
    async with await connect_to_db() as db_conn:
        await change_status(db_conn, title, True)


@targets.delete('/todo/delete/{target_title}')
async def delete_target(target_title: str):
    async with await connect_to_db() as db_conn:
        await del_target(db_conn, target_title)
