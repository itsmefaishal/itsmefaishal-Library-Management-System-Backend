from fastapi import FastAPI
from routes.bookRoutes import book
from routes.studentRoutes import student

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello, My name is Faishal Rahman, migrate to endoints - '/books' or '/students'"}

app.include_router(book)
app.include_router(student)
