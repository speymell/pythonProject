from typing import Union, Annotated, List, Optional
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, Integer, Identity, Float, Sequence , Boolean, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from enum import Enum
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=1), primary_key = True)
    name = Column(String)
    hashed_password = Column(String)
    email = Column(String)

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))
    #company = relationship("Company", back_populates="workers")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    #workers = relationship("User", back_populates="company")

# class Reader(Base):
#     __tablename__ = "readers"
#     id = Column(Integer, Identity(start=1), primary_key = True)
#     name = Column(String)
#     hashed_password = Column(String)
#     email = Column(String)
#     ticket = relationship("Ticket", back_populates="readers")
#
# class Ticket(Base):
#     __tablename__ = "tickets"
#     kod_vidachi = Column(Integer, Identity(start=1), primary_key=True)
#     kod_klienta = Column(Integer, ForeignKey("readers.id"))
#     data_vidachi = Column(String)
#     data_okonchania = Column(String)
#     reader = relationship("Reader", back_populates="tickets")

    #goods = relationship("Good", back_populates="owner")
    #class Good(metadata):
    #__tablename__ = "goods"
    #id = Column(Integer, primary_key=True, index=True)
    #name = Column(String, index=True)
    #description = Column(String, index=True)
    #price = Column(Float)
    #nalog = Column(Float)
    #user_id = Column(Integer, ForeignKey("users.id"))
    #owner = relationship("User", back_populates=goods)

class Person(BaseModel):
    lastName: str = Field(default="lastName", min_length=3, max_length=35)
    age: int = Field(default=100, ge=10, lt=200)

class Foto(BaseModel):
    url:HttpUrl
    name:Union[str,None] = None

class Tags(Enum):
    users = "users"
    advents = "advents"
    info = "info"
    good = "good"
    workers = "workers"

class Main_User(BaseModel):
    name: Union[str, None] = None
    id: Annotated[Union[int,None], Field(default=100, ge=1, lt=200)] = None

class Main_UserDB(Main_User):
    password: Annotated[Union[str, None], Field(max_length=200,min_length=8)] = None

class New_Respons(BaseModel):
    message: str

class Good(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=10, lt=200)] = None
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = 0
    nalog: Union[float, None] = 13.6