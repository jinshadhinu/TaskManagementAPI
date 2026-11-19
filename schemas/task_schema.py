from pydantic import BaseModel,Field,ConfigDict
from typing import Literal

Priority = Literal["Low","Medium","High"]

TaskStatus= Literal["Pending","In Progress", "Completed"]

class TaskCreate(BaseModel):
    title : str =Field(min_length=3,max_length=100)
    description: str =Field(default="",max_length=100)
    priority: Priority
    status: TaskStatus ="Pending"

class TaskUpdate(BaseModel):
    title: str |None =Field(default=None,min_length=3,max_length=100)
    description : str |None =Field(default=None, max_length=500)
    priority : Priority |None =None
    status: TaskStatus |None =None

class TaskStatusUpdate(BaseModel):
    status:TaskStatus

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: Priority
    status: TaskStatus
    model_config= ConfigDict(from_attributes=True)