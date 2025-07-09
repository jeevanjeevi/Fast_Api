from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response,status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session


#used to create the tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#connection to the database
'''while True:
     try:
          con = psycopg2.connect(host='localhost', database='fastmedia', user='postgres', password='postgres',cursor_factory=RealDictCursor,port=5433)
          cursor = con.cursor()
          print("database connection is successful")
          break
     except Exception as e:
          print("database connection failed...",e)
          #time.sleep(3)'''





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

@app.get("/sqlalchemy")
def root(db:Session=Depends(get_db)):
    data= db.query(models.Post).all()
    return {"message":data}

@app.get("/posts",response_model=List[schema.PostRes])
def get_posts(db:Session=Depends(get_db)):
     #cursor.execute("""select * from posts""")
     #posts=cursor.fetchall()
     data= db.query(models.Post).all()
     return data

@app.get("/posts/{id}",response_model=schema.PostRes)
def get_posts(id:int,db : Session= Depends(get_db)):
     #cursor.execute("""select * from posts where id = %s""",(str(id),))
     data=db.query(models.Post).filter(models.Post.id == id).first()
     #print(data.first())
     if data == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post is not found")
     return data




@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schema.PostRes)
def create_posts(data :schema.CreatePost,db:Session=Depends(get_db)):
    # cursor.execute("""insert into posts(title,content,published) values(%s,%s,%s) returning *""",(data.title,data.content,data.published))
    # rps=cursor.fetchone()
     #con.commit()
     #res=models.Post(title=data.title, content= data.content, published=data.published)
     res=models.Post(**data.dict())
     db.add(res)
     db.commit()
     db.refresh(res)
     return res

@app.delete("/posts/{id}")
def delete_post(id:int, db:Session=Depends(get_db)):
     #cursor.execute("""delete from posts where id=%s returning *""",(str(id),))
     res=db.query(models.Post).filter(models.Post.id == id)
     if res.first()==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post not found")
     res.delete(synchronize_session=False)   
     db.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schema.PostRes)
def update(id:int,data:schema.CreatePost, db:Session=Depends(get_db)):
     #cursor.execute("""update posts set title=%s, content=%s,published=%s where id = %s returning *""",(data.title,data.content,data.published,str(id)))
     res= db.query(models.Post).filter(models.Post.id == id)
     #print(type(res.first()))
     if res.first() == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no posts found for the given id")
     res.update(data.dict(),synchronize_session=False)
     db.commit()
     return res.first()