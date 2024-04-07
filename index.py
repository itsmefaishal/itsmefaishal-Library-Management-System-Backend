from fastapi import FastAPI
from routes.router import book
from routes.router import student

app = FastAPI()
app.include_router(book)
app.include_router(student)
