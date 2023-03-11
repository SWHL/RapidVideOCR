# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

import shutil

import sys
import pytest


cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from rapid_videocr import RapidVideOCR, RapidVideOCRError
from rapid_videocr.utils import read_txt, mkdir


test_file_dir = cur_dir / 'test_files'
srt_path = test_file_dir / 'result.srt'
txt_path = test_file_dir / 'result.txt'


def test_single_rec():
    extractor = RapidVideOCR(is_concat_rec=False)
    img_dir = test_file_dir / 'RGBImages'
    extractor(img_dir, test_file_dir)

    srt_data = read_txt(srt_path)
    txt_data = read_txt(txt_path)

    assert len(srt_data) == 12
    assert srt_data[2] == '空间里面他绝对赢不了的'
    assert srt_data[-2] == '你们接着善后'

    assert len(txt_data) == 6
    assert txt_data[-2] == '你们接着善后'

    srt_path.unlink()
    txt_path.unlink()


def test_concat_rec():
    extractor = RapidVideOCR(is_concat_rec=True)
    img_dir = test_file_dir / 'RGBImages'
    extractor(img_dir, test_file_dir)

    srt_data = read_txt(srt_path)
    txt_data = read_txt(txt_path)

    assert len(srt_data) == 12
    assert srt_data[2] == '空间里面他绝对赢不了的'
    assert srt_data[-2] == '你们接着善后'

    assert len(txt_data) == 6
    assert txt_data[-2] == '你们接着善后'

    srt_path.unlink()
    txt_path.unlink()


def test_empty_dir():
    extractor = RapidVideOCR(is_concat_rec=False)
    img_dir = test_file_dir / 'RGBImage'
    mkdir(img_dir)

    with pytest.raises(RapidVideOCRError) as exc_info:
        extractor(img_dir, test_file_dir)
    assert exc_info.type is RapidVideOCRError

    shutil.rmtree(img_dir)


def test_nothing_dir():
    extractor = RapidVideOCR(is_concat_rec=False)
    img_dir = test_file_dir / 'RGBImage'
    mkdir(img_dir)
    with pytest.raises(RapidVideOCRError) as exc_info:
        extractor(img_dir, test_file_dir)
    assert exc_info.type is RapidVideOCRError

    shutil.rmtree(img_dir)
