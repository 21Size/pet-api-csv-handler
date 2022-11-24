import uvicorn
from fastapi import FastAPI

from app.api import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def health_check():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
