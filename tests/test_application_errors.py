from importlib import import_module
from pathlib import Path
import sys
import unittest


API_ROOT = Path(__file__).resolve().parents[1] / "api"


class ApplicationErrorsTests(unittest.TestCase):
    def test_app_exception_is_reexported_from_application_errors_package(self) -> None:
        original_sys_path = sys.path.copy()
        sys.path.insert(0, str(API_ROOT))

        for module_name in (
            "app.application.errors",
            "app.application.errors.exceptions",
        ):
            sys.modules.pop(module_name, None)

        try:
            errors_module = import_module("app.application.errors")
        finally:
            sys.path[:] = original_sys_path

        self.assertTrue(hasattr(errors_module, "AppException"))


if __name__ == "__main__":
    unittest.main()
