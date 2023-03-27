# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_videocr import RapidVideOCR


extractor = RapidVideOCR(is_concat_rec=True, is_print_console=False)

rgb_dir = 'test_files/RGBImagesTiny'
save_dir = 'result'
extractor(rgb_dir, save_dir)
