import logging

from core.config import get_settings


def _resolve_log_level(level: str | int) -> int:
    if isinstance(level, int):
        return level

    normalized_level = str(level).upper()
    level_value = logging.getLevelNamesMapping().get(normalized_level)
    if level_value is None:
        raise ValueError(f"Invalid log level: {level!r}")

    return level_value


def setup_logging():
    settings = get_settings()
    # 获取根日志处理器
    root_logger = logging.getLogger()

    # 设置日志级别
    log_level = _resolve_log_level(settings.log_level)
    root_logger.setLevel(log_level)


    # 4.日志输出格式化
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    
    # 5.控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.info('日志初始化完成')
