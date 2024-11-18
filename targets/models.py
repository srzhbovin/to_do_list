from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Target(BaseModel):
    id: Optional[int] = None  # id необязательно, так как он генерируется базой данных
    title: str
    description: str
    completed: bool
    created_at: datetime = Field(default_factory=datetime.utcnow, read_only=True)


class UpdateTarget(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
