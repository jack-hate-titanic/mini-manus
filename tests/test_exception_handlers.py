from pathlib import Path
import sys
import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException


API_ROOT = Path(__file__).resolve().parents[1] / "api"
sys.path.insert(0, str(API_ROOT))

from app.application.errors import AppException
from app.interfaces.errors.exception_handlers import register_exception_handlers


class ExceptionHandlerTests(unittest.TestCase):
    def test_http_exception_returns_response_message_from_detail(self) -> None:
        app = FastAPI()
        register_exception_handlers(app)

        @app.get("/missing")
        async def missing_endpoint() -> None:
            raise HTTPException(status_code=404, detail="missing")

        with TestClient(app) as client:
            response = client.get("/missing")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"code": 404, "msg": "missing", "data": {}},
        )

    def test_app_exception_returns_custom_status_code_and_message(self) -> None:
        app = FastAPI()
        register_exception_handlers(app)

        @app.get("/app-error")
        async def app_error_endpoint() -> None:
            raise AppException(
                message="bad input",
                status_code=422,
                code=1001,
                data={"field": "name"},
            )

        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/app-error")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {"code": 1001, "msg": "bad input", "data": {"field": "name"}},
        )


if __name__ == "__main__":
    unittest.main()
