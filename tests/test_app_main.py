from importlib import import_module
from pathlib import Path
import sys
import unittest


API_ROOT = Path(__file__).resolve().parents[1] / "api"


class AppMainImportTests(unittest.TestCase):
    def test_importing_app_main_does_not_raise_name_error(self) -> None:
        original_sys_path = sys.path.copy()
        sys.path.insert(0, str(API_ROOT))

        for module_name in (
            "app.main",
            "app.infrastructure.logging",
            "app.infrastructure.logging.logging",
            "core",
            "core.config",
        ):
            sys.modules.pop(module_name, None)

        try:
            module = import_module("app.main")
        except NameError as exc:  # pragma: no cover - exercised in RED
            self.fail(f"importing app.main raised NameError: {exc}")
        finally:
            sys.path[:] = original_sys_path

        self.assertTrue(hasattr(module, "app"))


if __name__ == "__main__":
    unittest.main()
