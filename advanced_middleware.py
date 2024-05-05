from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import uvicorn
import datetime

app = FastAPI()

logging.basicConfig(filename="log.txt", level=logging.INFO)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=['localhost']
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

@app.get("/")
async def main():
    return{"message": "Hello World"}

@app.get("/get_time")
def get_time():
    print(datetime.datetime.now())
    return {"time": datetime.datetime.now()}

@app.post("/check")
async def get_body(request: Request):
    if request is None:
        return {"Параметр отсутствует"}
    return await request.json()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")