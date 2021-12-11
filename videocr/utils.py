# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import datetime

import cv2
import numpy as np
from decord import VideoReader, cpu
import copy
import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()


class Capture(object):
    def __init__(self, video_path):
        self.path = video_path

    def __enter__(self):
        with open(self.path, 'rb') as f:
            self.vr = VideoReader(f, ctx=cpu(0))
        return self.vr

    def __exit__(self, exc_type, exc_value, traceback):
        self.vr.__del__()


def get_frame_from_time(time_str, fps):
    if time_str:
        frame_index = get_frame_index(time_str, fps)
    else:
        frame_index = 0
    return frame_index


def get_frame_index(time_str: str, fps: float):
    # convert time string to frame index
    t = time_str.split(':')
    t = list(map(float, t))
    if len(t) == 3:
        td = datetime.timedelta(hours=t[0], minutes=t[1], seconds=t[2])
    elif len(t) == 2:
        td = datetime.timedelta(minutes=t[0], seconds=t[1])
    else:
        raise ValueError(
            f'Time data "{time_str}" does not match format "%H:%M:%S"')
    index = int(td.total_seconds() * fps)
    return index


def get_srt_timestamp(frame_index: int, fps: float):
    # convert frame index into SRT timestamp
    td = datetime.timedelta(seconds=frame_index / fps)
    ms = td.microseconds // 1000
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def is_similar_batch(img_a, img_batch, threshold=0.000):
    img_a = copy.deepcopy(img_a)
    img_a /= 255

    img_batch = copy.deepcopy(img_batch)
    img_batch /= 255
    difference = (img_a - img_batch) ** 2
    difference = difference.reshape(img_batch.shape[0], -1)
    error = np.sum(difference, axis=1) / img_a.size
    return error < threshold


def rgb_to_grey(img):
    if img.ndim == 3:
        img = img[np.newaxis, :, :, :]
    return img[..., 0] * 0.114 + img[..., 1] * 0.587 + img[..., 2] * 0.299


def binary_img(img):
    _, img = cv2.threshold(img, 243, 255, cv2.THRESH_BINARY)
    return img


def dilate_img(img):
    img = cv2.dilate(img, None, iterations=1)
    return img


def remove_bg(img):
    img = rgb_to_grey(img).squeeze()
    img = dilate_img(binary_img(img))
    img = img[np.newaxis, :, :]
    return img


def remove_batch_bg(img_batch):
    img_batch = rgb_to_grey(img_batch)
    new_img_batch = []
    for img_one in img_batch:
        temp_img = dilate_img(binary_img(img_one))
        new_img_batch.append(temp_img)
    img_batch = np.array(new_img_batch)
    return img_batch


def write_txt(save_path: str, content: list, mode='w'):
    """
    将list内容写入txt中
    @param
    content: list格式内容
    save_path: 绝对路径str
    @return:None
    """
    with open(save_path, mode, encoding='utf-8') as f:
        for value in content:
            f.write(value + '\n')
