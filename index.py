from fastapi import FastAPI
# from routes.router import books
from routes.router import student

app = FastAPI()
# app.include_router(books)
app.include_router(student)
