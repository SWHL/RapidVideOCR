# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time

from rapid_videocr import ExtractSubtitle
from rapid_ocr import TextDetector, TextSystem
from rapid_asr import ASRExecutor

# ocr module
det_model_path = "resources/rapid_ocr/models/ch_PP-OCRv2_det_infer.onnx"
cls_model_path = "resources/rapid_ocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx"
rec_model_path = "resources/rapid_ocr/models/ch_mobile_v2.0_rec_infer.onnx"
dict_path = "resources/rapid_ocr/ppocr_keys_v1.txt"

# asr module
config_path = 'resources/rapid_asr/model.yaml'
model_path = 'resources/rapid_asr/models/asr0_deepspeech2_online_aishell_ckpt_0.2.0.onnx'
lan_model_path = 'resources/rapid_asr/models/language_model/zh_giga.no_cna_cmn.prune01244.klm'


if __name__ == '__main__':
    ocr_system = TextSystem(det_model_path,
                            rec_model_path,
                            cls_model_path,
                            dict_path)
    text_det = TextDetector(det_model_path)

    asr_executor = ASRExecutor(sample_rate=16000,
                               config_path=config_path,
                               onnx_path=model_path,
                               lan_model_path=lan_model_path)

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
                                text_det=text_det, asr_executor=asr_executor,
                                is_dilate=is_dilate)

    start_time = time.time()
    ocr_result, asr_result = extractor(mp4_path, time_start,
                                       time_end, batch_size)
    print(f'elapse: {time.time() - start_time}s')
