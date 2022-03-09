# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import copy
import datetime
import difflib

import cv2
import numpy as np
from decord import VideoReader, cpu
from numpy.lib.type_check import _is_type_dispatcher


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
    img_a_tmp = copy.deepcopy(img_a)
    img_batch_tmp = copy.deepcopy(img_batch)

    img_a_tmp /= 255
    img_batch_tmp /= 255

    difference = (img_a_tmp - img_batch_tmp) ** 2
    difference = difference.reshape(img_batch_tmp.shape[0], -1)

    error = np.sum(difference, axis=1) / img_a_tmp.size
    return error < threshold


def rgb_to_grey(img):
    if img.ndim == 3:
        img = img[np.newaxis, :, :, :]
    return img[..., 0] * 0.114 + img[..., 1] * 0.587 + img[..., 2] * 0.299


def binary_img(img):
    _, img = cv2.threshold(img, 243, 255, cv2.THRESH_BINARY)
    return img


def dilate_img(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    img = cv2.dilate(img, kernel, iterations=1)
    return img


def remove_bg(img, is_dilate=True):
    img = rgb_to_grey(img).squeeze()
    if is_dilate:
        img = dilate_img(binary_img(img))
    img = img[np.newaxis, :, :]
    return img


def remove_batch_bg(img_batch, is_dilate=True):
    img_batch = rgb_to_grey(img_batch)
    new_img_batch = []
    for img_one in img_batch:
        if is_dilate:
            img_one = dilate_img(binary_img(img_one))

        new_img_batch.append(img_one)
    img_batch = np.array(new_img_batch)
    return img_batch
