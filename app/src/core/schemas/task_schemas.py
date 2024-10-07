from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    status: str = Optional
    title: str
    description: str