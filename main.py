from fastapi import FastAPI
from views import targets as todo_targets

app = FastAPI()

app.include_router(todo_targets)
