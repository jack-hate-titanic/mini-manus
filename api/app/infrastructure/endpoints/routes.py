from fastapi import APIRouter
from .status_routes import router as status_routes


def create_api_router() -> APIRouter:
    router = APIRouter()

    router.include_router(status_routes)
    return router

router = create_api_router()
