import logging
import os
from pathlib import Path
import sys
import unittest


API_ROOT = Path(__file__).resolve().parents[1] / "api"


class SetupLoggingTests(unittest.TestCase):
    def test_setup_logging_accepts_lowercase_log_level(self) -> None:
        original_sys_path = sys.path.copy()
        original_log_level = os.environ.get("LOG_LEVEL")
        root_logger = logging.getLogger()
        original_handlers = root_logger.handlers.copy()
        original_level = root_logger.level

        sys.path.insert(0, str(API_ROOT))
        os.environ["LOG_LEVEL"] = "debug"

        for module_name in (
            "app.infrastructure.logging",
            "app.infrastructure.logging.logging",
            "core",
            "core.config",
        ):
            sys.modules.pop(module_name, None)

        try:
            from core.config import get_settings
            from app.infrastructure.logging import setup_logging

            get_settings.cache_clear()
            root_logger.handlers = []
            root_logger.setLevel(logging.NOTSET)

            try:
                setup_logging()
            except TypeError as exc:  # pragma: no cover - exercised in RED
                self.fail(f"setup_logging raised TypeError for lowercase LOG_LEVEL: {exc}")

            self.assertEqual(root_logger.level, logging.DEBUG)
        finally:
            if "get_settings" in locals():
                get_settings.cache_clear()

            root_logger.handlers = original_handlers
            root_logger.setLevel(original_level)

            if original_log_level is None:
                os.environ.pop("LOG_LEVEL", None)
            else:
                os.environ["LOG_LEVEL"] = original_log_level

            sys.path[:] = original_sys_path


if __name__ == "__main__":
    unittest.main()
