# -*- encoding: utf-8 -*-
from rapid_videocr import VideoSubFinder


video_path = r'G:\ProgramFiles\_self\RapidVideOCR\2.mp4'
tmp_dir = 'temp'
vsf = VideoSubFinder(num_threads=2)
vsf(video_path, tmp_dir)
