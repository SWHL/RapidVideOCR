# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com

from rapid_videocr import RapidVideOCR

extractor = RapidVideOCR()

rgb_dir = 'test_files/TXTImages'
save_dir = 'result'
extractor(rgb_dir, save_dir)
