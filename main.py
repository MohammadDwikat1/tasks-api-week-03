from fastapi import FastAPI

app=FastAPI(title="Tasks API")
from pydantic import BaseModel,Field


class createTask(BaseModel):
   title:str =Field(min)
   done: bool = False

class Task(createTask):
    id:int
    


   
@app.get("/hello")
def hello ()-> dict[str,str]:
    return {"message":"hello"}
