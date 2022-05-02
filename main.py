# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time

from rapid_videocr import ExtractSubtitle
from rapid_ocr import TextDetector, TextSystem

# ocr module
det_model_path = "resources/rapid_ocr/models/ch_PP-OCRv2_det_infer.onnx"
cls_model_path = "resources/rapid_ocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx"
rec_model_path = "resources/rapid_ocr/models/ch_mobile_v2.0_rec_infer.onnx"
dict_path = "resources/rapid_ocr/ppocr_keys_v1.txt"


ocr_system = TextSystem(det_model_path, rec_model_path,
                        cls_model_path, dict_path)

text_det = TextDetector(det_model_path)


if __name__ == '__main__':
    batch_size = 100
    subtitle_height = None
    is_dilate = True
    error_num = 0.005
    mp4_path = 'assets/test_video/2.mp4'
    output_format = 'all'  # txt, srt, docx, all

    time_start = '00:00:00'
    time_end = '-1'

    extractor = ExtractSubtitle(ocr_system, subtitle_height,
                                error_num=error_num,
                                output_format=output_format,
                                text_det=text_det,
                                is_dilate=is_dilate)

    start_time = time.time()
    ocr_result = extractor(mp4_path, time_start, time_end, batch_size)
    print(ocr_result)
    print(f'elapse: {time.time() - start_time}s')
