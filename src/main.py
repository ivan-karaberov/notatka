import uvicorn
from fastapi import FastAPI

from api.routers import router as api_v1_router

app = FastAPI()

app.include_router(api_v1_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)