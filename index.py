from fastapi import FastAPI, Request
from routes.bookRoutes import book
from routes.studentRoutes import student
from redisServer.redisClient import rate_limit_middleware
from redisServer.redisClient import get_api_limits

app = FastAPI()


@app.middleware("http")
async def rate_limit(request : Request, call_next):
    return await rate_limit_middleware(request, call_next)


@app.get("/")
def read_root():
    return {"Hello, My name is Faishal Rahman, migrate to endoints - '/books' or '/students' and '/api/limits' to know your api requests limit"}

app.include_router(book)
app.include_router(student)

@app.get("/api/limits")
def get_api_limits_endpoint(request: Request):
    ip = request.client.host
    api_limits = get_api_limits(ip)
    return api_limits



