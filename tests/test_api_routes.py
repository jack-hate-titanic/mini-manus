from importlib import import_module
from pathlib import Path
import sys
import unittest

from fastapi import APIRouter


API_ROOT = Path(__file__).resolve().parents[1] / "api"


class ApiRoutesTests(unittest.TestCase):
    def test_importing_api_router_includes_status_routes(self) -> None:
        original_sys_path = sys.path.copy()
        sys.path.insert(0, str(API_ROOT))

        for module_name in (
            "app.infrastructure.endpoints.routes",
            "app.infrastructure.endpoints.status_routes",
        ):
            sys.modules.pop(module_name, None)

        try:
            routes_module = import_module("app.infrastructure.endpoints.routes")
        finally:
            sys.path[:] = original_sys_path

        self.assertIsInstance(routes_module.router, APIRouter)
        route_paths = {route.path for route in routes_module.router.routes}
        self.assertIn("/status", route_paths)


if __name__ == "__main__":
    unittest.main()
