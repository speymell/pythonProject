from typing import Optional

import uvicorn
from fastapi import Cookie, FastAPI

app = FastAPI

@app.get("/items")
async def read_items(ads_id: Optional[str] = Cookie(default=None)):
    return{"ads_id": ads_id}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")