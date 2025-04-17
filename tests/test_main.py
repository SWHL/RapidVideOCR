# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import shutil
import sys
from pathlib import Path

import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from rapid_videocr import RapidVideOCR, RapidVideOCRExeception, RapidVideOCRInput
from rapid_videocr.utils.utils import mkdir, read_txt

test_file_dir = cur_dir / "test_files"
srt_path = test_file_dir / "result.srt"
txt_path = test_file_dir / "result.txt"


@pytest.mark.parametrize(
    "img_dir",
    [
        test_file_dir / "RGBImages",
        test_file_dir / "TXTImages",
    ],
)
def test_single_rec(img_dir):
    extractor = RapidVideOCR(RapidVideOCRInput())
    extractor(img_dir, test_file_dir)

    srt_data = read_txt(srt_path)
    txt_data = read_txt(txt_path)

    assert len(srt_data) == 16
    assert srt_data[2] == "空间里面他绝对赢不了的"
    assert srt_data[-2] == "你们接着善后"

    assert len(txt_data) == 8
    assert txt_data[-2] == "你们接着善后"

    srt_path.unlink()
    txt_path.unlink()


@pytest.mark.parametrize(
    "img_dir",
    [test_file_dir / "RGBImages"],
)
def test_concat_rec(img_dir):
    input_param = RapidVideOCRInput(is_batch_rec=True)
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, test_file_dir)

    srt_data = read_txt(srt_path)
    txt_data = read_txt(txt_path)

    assert len(srt_data) == 16
    assert srt_data[2] == "空间里面他绝对赢不了的"
    assert srt_data[-2] == "你们接着善后"

    assert len(txt_data) == 8
    assert txt_data[-2] == "你们接着善后"

    srt_path.unlink()
    txt_path.unlink()


@pytest.mark.parametrize(
    "img_dir",
    [
        test_file_dir / "RGBImage",
        test_file_dir / "TXTImage",
    ],
)
def test_empty_dir(img_dir):
    extractor = RapidVideOCR(RapidVideOCRInput())
    mkdir(img_dir)

    with pytest.raises(RapidVideOCRExeception) as exc_info:
        extractor(img_dir, test_file_dir)
    assert exc_info.type is RapidVideOCRExeception

    shutil.rmtree(img_dir)


@pytest.mark.parametrize(
    "img_dir",
    [
        test_file_dir / "RGBImage",
        test_file_dir / "TXTImage",
    ],
)
def test_nothing_dir(img_dir):
    extractor = RapidVideOCR(RapidVideOCRInput())
    mkdir(img_dir)
    with pytest.raises(RapidVideOCRExeception) as exc_info:
        extractor(img_dir, test_file_dir)
    assert exc_info.type is RapidVideOCRExeception

    shutil.rmtree(img_dir)


def test_out_only_srt():
    img_dir = test_file_dir / "RGBImages"
    input_param = RapidVideOCRInput(is_batch_rec=True, out_format="srt")
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, test_file_dir)

    srt_data = read_txt(srt_path)

    assert len(srt_data) == 16
    assert srt_data[2] == "空间里面他绝对赢不了的"
    assert srt_data[-2] == "你们接着善后"

    srt_path.unlink()


def test_out_only_txt():
    img_dir = test_file_dir / "RGBImages"
    input_param = RapidVideOCRInput(is_batch_rec=True, out_format="txt")
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, test_file_dir)

    txt_data = read_txt(txt_path)

    assert len(txt_data) == 8
    assert txt_data[-2] == "你们接着善后"

    txt_path.unlink()
