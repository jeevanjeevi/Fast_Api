from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"welcome to fast api...!!!"}

@app.get("/posts")
def get_posts():
     return {"data":"fetching the posts...."}

@app.post("/posts")
def create_posts():
     return {"data":"creating the posts...."}