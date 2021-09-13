# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import cv2
from rapidocr import TextSystem

det_model_path = "resources/models/ch_PP-OCRv2_det_infer.onnx"
cls_model_path = "resources/models/ch_ppocr_mobile_v2.0_cls_infer.onnx"
rec_model_path = "resources/models/ch_mobile_v2.0_rec_infer.onnx"
dict_path = "resources/ppocr_keys_v1.txt"

ocr_system = TextSystem(det_model_path,
                        rec_model_path,
                        cls_model_path,
                        dict_path)


if __name__ == '__main__':
    image_path = 'tmp.jpg'
    img = cv2.imread(image_path)

    dt_boxes, rec_res = ocr_system(img)
    txts = [rec_res[i][0] for i in range(len(rec_res))]

    for txt in txts:
        print(txt)
