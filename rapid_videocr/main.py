# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from .rapid_videocr import RapidVideOCR
from .video_sub_finder import VideoSubFinder


class RapidVideoSubFinderOCR():
    def __init__(self) -> None:
        self.vsf = VideoSubFinder()
        self.video_ocr = RapidVideOCR()

    def __call__(self, video_path: str, output_dir: str):
        print('Running VideoSubFinder... It maybe be a long time. Be patient!')
        self.vsf(video_path, output_dir)

        rgb_dir = Path(output_dir) / 'RGBImages'
        self.video_ocr(rgb_dir, 'result', save_name='a')
