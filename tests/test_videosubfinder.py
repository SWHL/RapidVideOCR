# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import shutil
import sys
from pathlib import Path


cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from rapid_videocr import VideoSubFinder


test_file_dir = cur_dir / 'test_files'
vsf = VideoSubFinder(num_threads=2)


def test_video():
    video_path = test_file_dir / '2.mp4'
    out_dir = test_file_dir / 'temp'

    vsf(str(video_path), str(out_dir))

    rgb_dir = out_dir / 'RGBImages'

    img_list = list(rgb_dir.glob('*.*'))
    assert len(img_list) == 4

    shutil.rmtree(out_dir)
