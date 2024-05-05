from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status,Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse, FileResponse
import uvicorn

DATABASE_URL = "sqlite:///./users.db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("login", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer),
    sqlalchemy.Column("height", sqlalchemy.Integer)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

class NoteIn(BaseModel):
    login: str
    password: str
    age: int
    height: int

class Note(BaseModel):
    id: int
    login: str
    password: str
    age: int
    height: int

@app.get("/notes/", response_model=List[Note], status_code=200)
async def read_notes():
    query = notes.select()
    spisok = await database.execute(query)
    return await database.fetch_all(query)

@app.post("/sign_up/", response_model=Note, status_code=201)
async def create_note(note: NoteIn):
    query = notes.insert().values(login=note.login, password=note.password, age=note.age, height=note.height)
    last_record_id = await database.execute(query)
    return {**note.model_dump(), "id": last_record_id}

templates = Jinja2Templates(directory="./3/templates")

@app.post("/sign_in/", response_model=Note, status_code=200)
async def create_note(note: NoteIn):
    query = notes.select().where(login=note.login, password=note.password)
    last_record_id = await database.execute(query)
    return {**note.model_dump(), "id": last_record_id}


# async def create_product(product: Product):
#     product.product_id = len(store) + 1
#     store[product.product_id] = product
#     return JSONResponse(
#         {"id": product.product_id},
#         status_code=status.HTTP_201_CREATED,
#     )

uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")