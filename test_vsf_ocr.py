# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com

from rapid_videocr import RapidVideoSubFinderOCR


vsf_ocr = RapidVideoSubFinderOCR()

video_path = r'test_files/王子现身_720_10分钟.mp4'
tmp_dir = 'temp'

vsf_ocr(video_path, tmp_dir)
