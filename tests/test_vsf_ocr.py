# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import shutil
import sys
from pathlib import Path


cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from rapid_videocr import RapidVideoSubFinderOCR

test_file_dir = cur_dir / 'test_files'

vsf_ocr = RapidVideoSubFinderOCR()


def test_vsf_ocr():
    video_path = test_file_dir / '2.mp4'
    out_dir = test_file_dir / 'temp'
    vsf_ocr(str(video_path), str(out_dir))

    srt_path = out_dir / '2.srt'
    assert srt_path.exists()

    with open(srt_path, 'r', encoding='utf-8') as f:
        data = f.readlines()

    assert len(data) == 12
    assert data[-2] == '你们接着善后\n'

    shutil.rmtree(out_dir)
