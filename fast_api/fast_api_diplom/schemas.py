# schemas.py

from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str = None
    is_done: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
