# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: temp.py
# @Author: SWHL
# @Contact: liekkaskono@163.com
import cv2
import numpy as np
from rapidocr import TextDetector


def draw_text_det_res(dt_boxes, img_path):
    src_im = cv2.imread(img_path)
    for box in dt_boxes:
        box = np.array(box).astype(np.int32).reshape(-1, 2)
        cv2.polylines(src_im, [box], True,
                      color=(255, 255, 0), thickness=2)
    return src_im

model_path = 'resources/models/ch_PP-OCRv2_det_infer.onnx'
text_detector = TextDetector(model_path)

image_path = '2021-12-19_10-50-34.jpg'
img = cv2.imread(image_path)

dt_boxes, elapse = text_detector(img)
middle_h = int(img.shape[0] / 2)

mask = np.where(dt_boxes[:, 0, 0] > middle_h, True, False)
dt_boxes = dt_boxes[mask]
max_h = np.max(dt_boxes[:, :, 1], axis=1) - np.min(dt_boxes[:, :, 1], axis=1)

src_im = draw_text_det_res(dt_boxes, image_path)
cv2.imwrite('det_results.jpg', src_im)
print('图像已经保存为det_results.jpg了')