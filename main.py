from fastapi import FastAPI, HTTPException

app=FastAPI(title="Tasks API")
from pydantic import BaseModel, Field


class createTask(BaseModel):
   title:str = Field(min_length=1, max_length=200)
   done: bool = False

class Task(createTask):
    id:int

class TaskUpdate(BaseModel):  
  title: str | None = Field(default=None, min_length=1, max_length=200)
  done: bool | None = None


   
@app.get("/hello")
def hello ()-> dict[str,str]:
    return {"message":"hello"}



tasks:dict[str,Task]={}
next_id=1
@app.post("/tasks", status_code=201)
def create_task(body:createTask)->Task:
    global next_id
    task=Task(id=next_id,**body.model_dump())
    tasks[task.id] = task
    next_id += 1
    return task
    
@app.get("/tasks")
def list_tasks() -> list[Task]:
     return list(tasks.values())



@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    task=tasks.get(task_id)
    if task is None:
      raise HTTPException(status_code=404,detail="task not found")
    return task



@app.patch("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate) -> Task:
    task= get_task(task_id)
    changes=body.model_dump(exclude_unset=True)
    tasks[task_id]=task.model_copy(update=changes)
    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    get_task(task_id)
    del tasks[task_id]
