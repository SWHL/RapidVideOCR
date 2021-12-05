# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapidocr import TextSystem
from videocr import get_subtitles, write_txt

det_model_path = "resources/models/ch_PP-OCRv2_det_infer.onnx"
cls_model_path = "resources/models/ch_ppocr_mobile_v2.0_cls_infer.onnx"
rec_model_path = "resources/models/ch_mobile_v2.0_rec_infer.onnx"
dict_path = "resources/ppocr_keys_v1.txt"

ocr_system = TextSystem(det_model_path,
                        rec_model_path,
                        cls_model_path,
                        dict_path)


if __name__ == '__main__':
    result = get_subtitles('assets/4.mp4',
                           ocr_system,
                           time_start='00:00:00',
                           time_end='0',
                           use_fullframe=False)
    write_txt('result.txt', result)
    print(result)
