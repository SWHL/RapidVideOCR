# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time

from rapid_videocr import RapidVideOCR

extractor = RapidVideOCR()

mp4_path = 'assets/test_video/long.mp4'

start_time = time.time()

ocr_result = extractor(mp4_path)
print(ocr_result)

print(f'elapse: {time.time() - start_time}s')
