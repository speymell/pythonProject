import uvicorn
from typing import Annotated
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

app = FastAPI()

class BodyContentChecker:
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, body: dict):
        if self.key in body:
            return True
        return False

checker = BodyContentChecker("foo")

@app.post("/body-checker/")
async def read_body_check(body_included: Annotated[bool, Depends(checker)]):
    return{"body_contains_key": body_included}


class NBodyContentChecker:
    def __init__(self, name: str):
        self.name = name

    async def __call__(self, body: dict):
        if self.name in body:
            return self.name
        return {"Параметр отсутствует"}

checker = NBodyContentChecker("foo")
#
# def checkname(name: str):
#     if name != "":
#         return name
#     return {"Параметр отсутствует"}

# @app.post("/check/")
# async def read_body_check(name_included: Annotated[bool, Depends(checker)]):
#     return{"body_contains_name": name_included}

@app.post("/check")
async def get_body(request: Request):
    if request is None:
        return {"Параметр отсутствует"}
    logging.info(f"Request: {request.method} {request.url.path}")
    return await request.json()





# class FixedContentQueryChecker:
#     def __init__(self,fixed_content: str):
#         self.fixed_content = fixed_content
#
#     def __call__(self, q: str=""):
#         if q:
#             return self.fixed_content in q
#         return False
# checker = FixedContentQueryChecker("bar")

# @app.get("/query-checker")
# async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
#     return {"fixed_content_in_query": fixed_content_included}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")