from typing import Optional
from fastapi import FastAPI, HTTPException, Response,status
from fastapi.params import Body
from pydantic import BaseModel
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

#connection to the database
while True:
     try:
          con = psycopg2.connect(host='localhost', database='fastmedia', user='postgres', password='postgres',cursor_factory=RealDictCursor,port=5433)
          cursor = con.cursor()
          print("database connection is successful")
          break
     except Exception as e:
          print("database connection failed...",e)
          #time.sleep(3)


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
     cursor.execute("""select * from posts""")
     posts=cursor.fetchall()
     #print(posts)
     return {"posts":posts}

@app.get("/posts/{id}")
def get_posts(id:int):
     cursor.execute("""select * from posts where id = %s""",(str(id),))
     data=cursor.fetchone()
     if data == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post is not found")
     return {"posts":data}

#defining Schema for posts
class Post(BaseModel):
     title:str
     content:str
     published:bool = True



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(data : Post):
     cursor.execute("""insert into posts(title,content,published) values(%s,%s,%s) returning *""",(data.title,data.content,data.published))
     rps=cursor.fetchone()
     con.commit()
     #cursor.close()
     #con.close()
     return {"data":rps}

@app.delete("/posts/{id}")
def delete_post(id:int):
     cursor.execute("""delete from posts where id=%s returning *""",(str(id),))
     res=cursor.fetchone()
     if res==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post not found")
     con.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update(id:int,data:Post):
     cursor.execute("""update posts set title=%s, content=%s,published=%s where id = %s returning *""",(data.title,data.content,data.published,str(id)))
     res= cursor.fetchone()
     if res == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no posts found for the given id")
     con.commit()
     return {"updated data":res}