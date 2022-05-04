# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: rapid_remove_bg.py
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort


def reverse_transform(inp):
    inp = inp.transpose((0, 2, 3, 1))
    inp = np.clip(inp, 0, 1)
    inp = (inp * 255).astype(np.uint8)
    return inp


def scale_resize(img, resize_value=(480, 480)):
        '''
        @params:
        img: ndarray
        resize_value: (width, height)
        '''
        # padding
        ratio = resize_value[0] / resize_value[1]  # w / h
        h, w = img.shape[:2]
        if w / h < ratio:
            # 补宽
            t = int(h * ratio)
            w_padding = (t - w) // 2
            img = cv2.copyMakeBorder(img, 0, 0, w_padding, w_padding,
                                        cv2.BORDER_CONSTANT, value=(0, 0, 0))
        else:
            # 补高  (left, upper, right, lower)
            t = int(w / ratio)
            h_padding = (t - h) // 2
            img = cv2.copyMakeBorder(img, h_padding, h_padding, 0, 0,
                                        cv2.BORDER_CONSTANT, value=(0, 0, 0))
        img = cv2.resize(img, resize_value,
                            interpolation=cv2.INTER_LANCZOS4)
        return img


class RemoveBG(object):
    def __init__(self, onnx_path):
        sess_opt = ort.SessionOptions()
        sess_opt.log_severity_level = 4
        sess_opt.enable_cpu_mem_arena = False

        self.session = ort.InferenceSession(onnx_path,
                                            sess_options=sess_opt)

    def __call__(self, img_path):
        if isinstance(img_path, np.ndarray):
            img = img_path
        else:
            img = cv2.imread(img_path)

        if img.ndim == 3:
            img = img[np.newaxis, ...]

        image_all = []
        for one_img in img:
            image = scale_resize(one_img).astype(np.float32)
            image /= 255.0
            image = image.transpose([2, 0, 1])
            image_all.append(image)

        image_all = np.array(image_all)
        input_name = self.session.get_inputs()[0].name
        ort_inputs = {input_name: image_all}

        pred = self.session.run(None, ort_inputs)[0]
        pred = reverse_transform(pred)
        return pred


if __name__ == '__main__':
    onnx_path = r'E:\PythonProjects\RapidVideOCR\resources\rapid_remove_bg\2022-05-04-09-36-54-best.onnx'

    remove_bg = RemoveBG(onnx_path)

    img_path = r'7.jpg'

    pred = remove_bg(img_path)
    cv2.imwrite('tmp.jpg', pred.squeeze())


