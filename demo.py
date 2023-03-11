# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_videocr import RapidVideOCR


extractor = RapidVideOCR(is_concat_rec=True)

rgb_dir = 'tests/test_files/RGBImages'
save_dir = 'result'
extractor(rgb_dir, save_dir)
