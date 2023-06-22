# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import functools
import logging
import sys
from pathlib import Path
from typing import List

import colorlog
import cv2
import numpy as np

logger_initialized = {}


class CropByProject:
    """投影法裁剪"""

    def __init__(self, threshold=250):
        self.threshold = threshold

    def __call__(self, origin_img):
        image = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)

        # 将图片二值化
        retval, img = cv2.threshold(image, self.threshold, 255, cv2.THRESH_BINARY_INV)

        # 使文字增长成块
        closed = cv2.dilate(img, None, iterations=1)

        # 水平投影
        x0, x1 = self.get_project_loc(closed, direction='width')

        # 竖直投影
        y0, y1 = self.get_project_loc(closed, direction='height')

        return origin_img[y0:y1, x0:x1]

    @staticmethod
    def get_project_loc(img, direction):
        """获得裁剪的起始和终点索引位置
        Args:
            img (ndarray): 二值化后得到的图像
            direction (str): 'width/height'
        Raises:
            ValueError: 不支持的求和方向
        Returns:
            tuple: 起始索引位置
        """
        if direction == 'width':
            axis = 0
        elif direction == 'height':
            axis = 1
        else:
            raise ValueError(f'direction {direction} is not supported!')

        loc_sum = np.sum(img == 255, axis=axis)
        loc_range = np.argwhere(loc_sum > 0)
        i0, i1 = loc_range[0][0], loc_range[-1][0]
        return i0, i1


def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def read_txt(txt_path: str) -> List:
    if not isinstance(txt_path, str):
        txt_path = str(txt_path)

    with open(txt_path, 'r', encoding='utf-8') as f:
        data = list(map(lambda x: x.rstrip('\n'), f))
    return data


@functools.lru_cache()
def get_logger(name='rapid_videocr'):
    logger = logging.getLogger(name)
    if name in logger_initialized:
        return logger

    for logger_name in logger_initialized:
        if name.startswith(logger_name):
            return logger

    fmt_string = '%(log_color)s[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
    log_colors = {
        'DEBUG': 'white',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'purple',
    }
    fmt = colorlog.ColoredFormatter(fmt_string, log_colors=log_colors)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.INFO)
    logger_initialized[name] = True
    logger.propagate = False
    return logger
