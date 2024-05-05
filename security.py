import uvicorn
import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

TOKEN = "qwerty123"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_token(token:str=Depends(oauth2_scheme)):
#     if token == TOKEN:
#         return token
#     raise HTTPException(status_code=401, detail="Токен не действителен")
#
# @app.get("/token")
# def get_token():
#     return {"token": TOKEN}
#
# @app.get("/secure-route")
# def secure_route(token: str = Depends(verify_token)):
#         return {"message": "Доступ разрешён!"}

@app.get("/get_time")
def get_time():
    print(datetime.datetime.now())
    return {"time": datetime.datetime.now()}

class BodyContentChecker:
    def __init__(self, name: str):
        self.name = name

    async def __call__(self, body: dict):
        if self.name in body:
            return self.name
        return {"Параметр отсутствует"}

checker = BodyContentChecker("foo")

@app.post("/check/")
async def read_body_check(name_included: Annotated[bool, Depends(checker)]):
    return{"body_contains_name": name_included}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")