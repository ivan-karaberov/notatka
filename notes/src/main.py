import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from errors.api_errors import APIException
from utils.logging_config import configure_logging

configure_logging()
app = FastAPI()


@app.exception_handler(APIException)
async def custom_exception_handler(request: Request, exc: APIException):
    """Обработчик собственных исключений"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8002, reload=True)
