import redis
import os
from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import JSONResponse

load_dotenv()

redis_client = None
MAX_REQUEST = 5
TIME_LIMIT = 120

def get_redis_client():
    global redis_client
    if not redis_client :
        
        try:
            host = os.getenv('REDIS_HOST')
            port = os.getenv('REDIS_PORT')
            password = os.getenv('REDIS_PASSWORD')
            
            redis_client = redis.Redis(
                host = host,
                port = port,
                password = password            
            )
        
            print(redis_client.ping())
        except Exception as e:
            print(e)
            
    return redis_client

def rate_limiter(ip):
    key = f"ratelimit:{ip}"
    redis_client = get_redis_client()
    
    if redis_client.exists(key):
        count = redis_client.incr(key)
    else:
        count = redis_client.setex(key, TIME_LIMIT, 1)
    
    if count and int(count) > MAX_REQUEST :
        return True
    
    return False

async def rate_limit_middleware(request : Request, call_next):
    ip = request.client.host
    if rate_limiter(ip):
        return JSONResponse(content={"detail": "Rate limit exceeded"}, status_code=429)
    
    response = await call_next(request)
    
    return response
            

def get_api_limits(ip):
    key = f"ratelimit:{ip}"
    redis_client = get_redis_client()

    remaining_requests = MAX_REQUEST - int(redis_client.get(key) or 0)
    reset_time = redis_client.ttl(key)

    return {"remaining_requests": remaining_requests, "reset_time": reset_time}