from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="./3/templates")

products = [
    {"name": 'Яблоко', 'price': 50},
    {"name": 'Банан', "price": 30},
    {"name": "Апельсин", "price": 20},
]

@app.get("/items/")
async def read_items(request: Request):
    return templates.TemplateResponse(
        "items.html", {"request": request, "products": products}
    )

uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")