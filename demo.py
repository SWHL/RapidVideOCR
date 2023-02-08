# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com

from rapid_videocr import RapidVideOCR

extractor = RapidVideOCR()

rgb_dir = r'G:\ProgramFiles\_self\VideoSubFinder\VideoSubFinder_5.60_x64\clean\RGBImages'
save_dir = 'result'
result = extractor(rgb_dir, save_dir)

print('ok')
