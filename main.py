from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

#
class Target(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime = Field(default_factory=datetime.utcnow, read_only=True)


class UpdateTarget(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, read_only=True)


targets = [
    {"id": 1, "title": "Купить молоко", "description": "Нужно купить молоко в магазине", "completed": False,
     "created_at": datetime.utcnow()},
    {"id": 2, "title": "Помыть машину", "description": "Нужно помыть машину на автомойке", "completed": True,
     "created_at": datetime.utcnow()},
    {"id": 3, "title": "Сходить в спортзал", "description": "Нужно сходить в спортзал в 18:00", "completed": False,
     "created_at": datetime.utcnow()}]


@app.get("/todo", response_model=List[Target])
def get_all_targets():
    return targets


@app.post('/todo', response_model=Target)
def add_target(target: Target):
    targets.append(target)
    return target


@app.put("/todo/{target_title}", response_model=Target)
def update_target(target_title: str, updated_target: UpdateTarget):
    for index, existing_target in enumerate(targets):
        if existing_target["title"] == target_title:
            if updated_target.title is not None:
                existing_target["title"] = updated_target.title
            if updated_target.description is not None:
                existing_target["description"] = updated_target.description
            if updated_target.completed is not None:
                existing_target["completed"] = updated_target.completed
            return existing_target
    raise HTTPException(status_code=404, detail='Target not found')


@app.delete('/todo/{target_title}', response_model=Target)
def delete_target(target_title: str):
    for index, existing_target in enumerate(targets):
        if existing_target['title'] == target_title:
            deleted_target = targets.pop(index)
            return deleted_target
    raise HTTPException(status_code=404, detail='Target is not found')
