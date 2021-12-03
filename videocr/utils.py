# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import datetime

import cv2
import numpy as np


# convert time string to frame index
def get_frame_index(time_str: str, fps: float):
    t = time_str.split(':')
    t = list(map(float, t))
    if len(t) == 3:
        td = datetime.timedelta(hours=t[0], minutes=t[1], seconds=t[2])
    elif len(t) == 2:
        td = datetime.timedelta(minutes=t[0], seconds=t[1])
    else:
        raise ValueError(
            'Time data "{}" does not match format "%H:%M:%S"'.format(time_str))
    index = int(td.total_seconds() * fps)
    return index


# convert frame index into SRT timestamp
def get_srt_timestamp(frame_index: int, fps: float):
    td = datetime.timedelta(seconds=frame_index / fps)
    ms = td.microseconds // 1000
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(h, m, s, ms)


def is_similar(img_a, img_b, size=(256, 40), threshold=0.9999999):
    if img_a.ndim == 3:
        img_a = cv2.cvtColor(img_a, cv2.COLOR_RGB2GRAY)
        img_a = cv2.resize(img_a, size)

    if img_b.ndim == 3:
        img_b = cv2.cvtColor(img_b, cv2.COLOR_RGB2GRAY)
        img_b = cv2.resize(img_b, size)

    img_a = img_a / 255
    img_b = img_b / 255

    error = np.sum((img_a - img_b) ** 2) / img_a.size
    return (1 - error) > threshold
