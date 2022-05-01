# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time

from rapid_videocr import ExtractSubtitle
from rapidocr import TextDetector, TextSystem

det_model_path = "resources/models/ch_PP-OCRv2_det_infer.onnx"
cls_model_path = "resources/models/ch_ppocr_mobile_v2.0_cls_infer.onnx"
rec_model_path = "resources/models/ch_mobile_v2.0_rec_infer.onnx"
dict_path = "resources/ppocr_keys_v1.txt"


if __name__ == '__main__':
    s = time.time()

    ocr_system = TextSystem(det_model_path,
                            rec_model_path,
                            cls_model_path,
                            dict_path)
    text_det = TextDetector(det_model_path)

    batch_size = 100
    subtitle_height = None
    is_dilate = True
    error_num = 0.005
    mp4_path = 'assets/test_video/2.mp4'
    output_format = 'all'  # txt, srt, docx, all

    time_start = '00:00:00'
    time_end = '-1'

    videor = ExtractSubtitle(ocr_system, subtitle_height,
                             error_num=error_num, output_format=output_format,
                             text_det=text_det, is_dilate=is_dilate)
    result = videor(mp4_path, time_start, time_end, batch_size)
    print(result)
    print(f'elapse: {time.time() - s}s')
