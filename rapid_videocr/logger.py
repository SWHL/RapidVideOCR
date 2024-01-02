# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import functools
import sys
from pathlib import Path

from loguru import logger


@functools.lru_cache()
def get_logger(save_dir: str = "."):
    loguru_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    logger.remove()
    logger.add(
        sys.stderr,
        format=loguru_format,
        level="INFO",
        enqueue=True,
    )

    file_name = "{time:YYYY-MM-DD-HH-mm-ss}.log"
    save_file = Path(save_dir) / file_name
    logger.add(save_file, rotation=None, retention="2 days")
    return logger


log_dir = Path(__file__).resolve().parent / "log"
logger = get_logger(str(log_dir))
