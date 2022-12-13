# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time

from rapid_videocr import ExtractSubtitle
from rapid_ocr import TextSystem
from fast_asr import FastASR


if __name__ == '__main__':
    ocr_system = TextSystem()
    fast_asr = FastASR()
    extractor = ExtractSubtitle(ocr_system, fast_asr)

    mp4_path = 'assets/test_video/2.mp4'

    start_time = time.time()

    ocr_result = extractor(mp4_path)
    print(ocr_result)

    print(f'elapse: {time.time() - start_time}s')
