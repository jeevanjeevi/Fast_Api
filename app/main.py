from typing import Optional
from fastapi import FastAPI, HTTPException, Response,status
from fastapi.params import Body
from pydantic import BaseModel
from random import randint

app = FastAPI()

#List to store the posts
All_posts=[]

def findpost(id):
     for i in All_posts:
        if  i["id"]==id:
             return i
        
def find_index(id):
     for i,p in enumerate(All_posts):
        if  p["id"]==id:
             return i

@app.get("/")
def root():
    return {"message":"welcome to fast api...!!!"}

@app.get("/posts")
def get_posts():
     return {"posts":All_posts}

@app.get("/posts/{id}")
def get_posts(id:int):
     data=findpost(id)
     if not data:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post is not found")
     return {"posts":data}

#defining Schema for posts
class Post(BaseModel):
     title:str
     content:str
     published:bool = True
     rating : Optional[float]=None



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(data : Post):
     res=data.dict()
     res["id"]=randint(50,100)
     All_posts.append(res)
     return {"data":res}

@app.delete("/posts/{id}")
def delete_post(id:int):
     ind=find_index(id)
     print(ind)
     if ind==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post not found")
     All_posts.pop(ind)
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update(id:int,data:Post):
     ind=find_index(id)
     if ind==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post not found")
     payload=data.dict()
     payload["id"]=id
     All_posts[ind]=payload
     return {"updated data":payload}