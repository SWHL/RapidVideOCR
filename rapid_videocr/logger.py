# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import logging


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fmt = "%(asctime)s - %(levelname)s: %(message)s"
    format_str = logging.Formatter(fmt)

    # 注意这里，想要写到不同log文件中，这里会存在写到同一个log文件中问题
    if not logger.handlers:
        sh = logging.StreamHandler()
        logger.addHandler(sh)
        sh.setFormatter(format_str)
    return logger


logger = get_logger()
