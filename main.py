from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import TaskRow

DbSession = Annotated[Session, Depends(get_db)]

app = FastAPI(title="Tasks API")



class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class Task(TaskCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    done: bool | None = None


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"message": "hello"}




@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate, db: DbSession) -> Task:
    row = TaskRow(**body.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return Task.model_validate(row)


@app.get("/tasks")
def list_tasks(db: DbSession) -> list[Task]:
    rows = db.scalars(select(TaskRow).order_by(TaskRow.id))
    return [Task.model_validate(row) for row in rows]



def find_task(db: Session, task_id: int) -> TaskRow:
    row = db.get(TaskRow, task_id)
    if row is None:
        raise HTTPException(status_code=404, detail="task not found")
    return row

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: DbSession) -> Task:
    return Task.model_validate(find_task(db, task_id))




@app.patch("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate, db: DbSession) -> Task:
    row = find_task(db, task_id)
    for name, value in body.model_dump(exclude_unset=True).items():
        setattr(row, name, value)
    db.commit()
    db.refresh(row)
    return Task.model_validate(row)

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: DbSession) -> None:
    db.delete(find_task(db, task_id))
    db.commit()
