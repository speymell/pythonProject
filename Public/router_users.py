from sqlalchemy import create_engine
from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from Models.good import *
#from config import settings
from typing import Union, Annotated
from db import engine_s

session_make = sessionmaker(engine_s)
def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()

users_router = APIRouter(tags=[Tags.users])
info_router = APIRouter(tags=[Tags.info])

def coder_passwd(cod: str):
    return cod * 2

@users_router.get("/{id}", response_model=Union[New_Respons, Main_User], tags=[Tags.info])
# далее идут опуерации пути для CRUD
def get_user_(id: int, DB: Session = Depends(get_session)):
    '''
    получаем пользователя по id
    '''
    user = DB.query(User).filter(User.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, отправляем его
    else:
        return user


@users_router.get("/", response_model=Union[list[Main_User], New_Respons], tags=[Tags.users])
def get_user_db(DB: Session = Depends(get_session)):
    '''
    получаем все записи таблицы
    '''
    users = DB.query(User).all()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if users == None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return users


@users_router.post("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users],
                   status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")],
                DB: Session = Depends(get_session)):
    try:
        user = User(name=item.name, hashed_password=coder_passwd(item.name))

        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(user)
        DB.commit()
        DB.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {user}")


# @users_router.put("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
# def edit_user_(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные для пользователя по id")],
#                DB: Session = Depends(get_session)):
#     # получаем пользователя по id
#     user = DB.query(User).filter(User.id == item.id).first()
#     # если не найден, отправляем статусный код и сообщение об ошибке
#     if user == None:
#         return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
#     # если пользователь найден, изменяем его данные и отправляем обратно клиенту
#     user.name = item.name
#     try:
#         DB.commit()
#         DB.refresh(user)  # сохраняем изменения
#     except HTTPException:
#         return JSONResponse(status_code=404, content={"message": ""})
#     return user


@users_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.users])
def delete_user(id: int, DB: Session = Depends(get_session)):
    # получаем пользователя по id
    user = DB.query(User).filter(User.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        DB.delete(user)
        DB.commit()  # сохраняем изменения
    except HTTPException:
        JSONResponse(content={'message': f'Ошибка'})
    return JSONResponse(content={'message': f'Пользователь удалён {id}'})

@users_router.patch("/{id}", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_user(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные по id")], DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == item.id).first()
    if user == None:
         return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    user.name = item.name
    try:
        DB.commit()
        DB.refresh(user)  # сохраняем изменения
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return user