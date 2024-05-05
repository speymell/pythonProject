import uvicorn
from fastapi import FastAPI, Response, Path, Body, Header
from fastapi.responses import PlainTextResponse
from Public.router_users import users_router
from datetime import datetime
from db import *
app = FastAPI()
# f_builder()
f()
app.include_router(users_router)

@app.on_event("startup")
def on_startup():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
#    init_db()

@app.on_event("shutdown")
def shutdown():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: End\n')



#@app.get('/')
#def main():
#    return FileResponse("files/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)