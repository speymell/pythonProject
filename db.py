import asyncio
from Models.good import Base, User
from sqlalchemy import create_engine, text, Insert, Select
from sqlalchemy.orm import sessionmaker
from config import settings
from config import settings

ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA
print(ur_s)
engine_s = create_engine(ur_s, echo=True)
#engine_a = create_async_engine(ur_a, echo=True)
# async def fa():
#     async with engine_a.connect() as conna:
#         answer = await conna.execute(text('select * from users;'))
#         print(f'answer={answer.all()}')
# asyncio.get_event_loop().run_until_complete(fa())
# async def fa_bilder():
#     with engine_a.connect() as conn:
#         query = insert(User).values([
#             {"name": "Joe Biden", "hashed password": "12345", "email":"whitehome@yandex.ru"}
#         ])
def create_tables():
    pass
    # Base.metadata.drop_all(bind=engine_s)
    # Base.metadata.create_all(bind=engine_s)
def f():
    with engine_s.connect() as conn:
        answer = conn.execute(text('select * from users;'))
        print(f"answer = {answer.all()}")
def f_builder():
    with engine_s.connect() as conn:
        query = Insert(User).values([
         {"name": "Emelyanen", "hashed_password": "12345", "email":"hdd@yandex.ru"},
         {"name": "Rusik", "hashed_password": "67890", "email":"hdddd@gmail.com"}
        ])
        conn.execute(query)
        conn.execute(text('commit;'))
        query = Select(User)
        answer = conn.execute(query)
        print(f"answer = {answer.all()}")