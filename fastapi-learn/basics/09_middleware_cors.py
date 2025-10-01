import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-process-time"] = str(process_time)
    return response

'''
You can add middleware to FastAPI applications.

A "middleware" is a function that works 
- with every request before it is processed by any specific path operation. 
- with every response before returning it.

def call_next -> receive the request as a parameter.

---
The middleware responds to two particular types of HTTP request:
- CORS preflight requests: Optional request
    -> header: Origin and Access-Control-Request-Method
    - Origin = protocol + domain name + port
- Simple requests 
    -> header: Origin 
'''