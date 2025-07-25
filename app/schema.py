from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
     title:str
     content:str
     published:bool = True

class CreatePost(PostBase):
     pass

class UpdatePost(PostBase):
     pass

class PostRes(PostBase):
     id:int
     created_at: datetime

     class Config:
          orm_mode=True