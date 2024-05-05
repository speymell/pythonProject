from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='./3/templates')

@app.get("/")
async def read_root(request: Request):
    context = {"request": request, "title": "Главная страница"}
    return templates.TemplateResponse("index.html", context)

import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")