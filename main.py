from fastapi import FastAPI

app=FastAPI(title="Tasks API")
from pydantic import BaseModel, Field


class createTask(BaseModel):
   title:str =Field(min)
   done: bool = False

class Task(createTask):
    id:int
    


   
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