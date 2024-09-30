import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import router as api_v1_router
from errors.api_errors import APIException

app = FastAPI()

@app.exception_handler(APIException)
async def custom_exception_handler(request: Request, exc: APIException):
    """Обработчик собственных исключений"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


app.include_router(api_v1_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)