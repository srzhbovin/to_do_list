from fastapi import FastAPI
from src.targets.views import targets as todo_targets

app = FastAPI()

app.include_router(todo_targets)


class A:
    x = 10
