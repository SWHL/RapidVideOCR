# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapidocr import TextSystem
from videocr import get_subtitles

det_model_path = "resources/models/ch_ppocr_mobile_v2.0_det_infer.onnx"
cls_model_path = "resources/models/ch_ppocr_mobile_v2.0_cls_infer.onnx"
rec_model_path = "resources/models/ch_mobile_v2.0_rec_infer.onnx"
dict_path = "resources/ppocr_keys_v1.txt"

ocr_system = TextSystem(det_model_path,
                        rec_model_path,
                        cls_model_path,
                        dict_path)


if __name__ == '__main__':
    result = get_subtitles('assets/1.mp4',
                           ocr_system,
                           sim_threshold=70,
                           conf_threshold=0.8,
                           use_fullframe=False)
    print(result)
