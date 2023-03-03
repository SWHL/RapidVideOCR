# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import numpy as np

import cv2
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR


text_sys = RapidOCR()


img_dir = Path('test_files/TXTImages')

img_list = list(img_dir.iterdir())
batch_size = 10

img_nums = len(img_list)

for start_i in range(0, img_nums, batch_size):
    end_i = min(img_nums, start_i + batch_size)
    select_imgs = img_list[start_i: end_i]

    concat_img = []
    points = []
    for i, img_path in enumerate(select_imgs):
        img = cv2.imread(str(img_path))
        h, w = img.shape[:2]
        points.append([(0, i * h), (w, (i + 1) * h)])
        concat_img.append(img)
    result = np.vstack(concat_img)

    ocr_res, _ = text_sys(result)
    y_points = np.array(points)[:, :, 1]
    dt_boxes, rec_res, scores = list(zip(*ocr_res))
    left_top_boxes = np.array(dt_boxes)[:, 0, :]

    match_dict = {}
    for i, one_left in enumerate(left_top_boxes):
        y = one_left[1]
        condition = (y >= y_points[:, 0]) & (y <= y_points[:, 1])
        index = np.argwhere(condition)
        if not index.size:
            match_dict[i] = ''
        match_index = index.squeeze().tolist()
        match_dict.setdefault(match_index, []).append(ocr_res[i])

print('ok')
