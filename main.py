from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def f_index():
    return {"ФИО": "Полыгалов Вячеслав Владимирович"}

@app.get('/tools')
async def f_indexT():
    return "Занимаюсь программирование на языке С#. Имею навыки работы с PostgreSQL, MS SQL!"

@app.get('/users')
async def f_indexT():
    return {"Телефон": "88005553535", "Электронная почта": "nicegeaming@yandex.ru"}