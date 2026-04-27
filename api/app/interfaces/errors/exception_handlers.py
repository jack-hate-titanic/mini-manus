import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from app.application.errors import AppException
from app.interfaces.schemas import Response

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.error("AppException: %s", exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content=Response(
                code=exc.code,
                msg=exc.message,
                data=exc.data if exc.data is not None else {},
            ).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.error("HTTPException: %s", exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content=Response(
                code=exc.status_code,
                msg=str(exc.detail),
                data={},
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("An unexpected error occurred: %s", exc)
        return JSONResponse(
            status_code=500,
            content=Response(
                code=500,
                msg="An unexpected error occurred. Please try again later.",
                data={},
            ).model_dump(),
        )
