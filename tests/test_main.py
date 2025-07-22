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

test_dir = cur_dir / "test_files"


@pytest.fixture
def setup_and_teardown():
    save_dir = test_dir / "tmp"
    mkdir(save_dir)

    srt_path = save_dir / "result.srt"
    ass_path = save_dir / "result.ass"
    txt_path = save_dir / "result.txt"

    yield save_dir, srt_path, ass_path, txt_path

    shutil.rmtree(save_dir)


@pytest.mark.parametrize(
    "img_dir",
    [test_dir / "RGBImages", test_dir / "TXTImages"],
)
def test_single_rec(setup_and_teardown, img_dir):
    save_dir, srt_path, ass_path, txt_path = setup_and_teardown

    extractor = RapidVideOCR(RapidVideOCRInput())
    extractor(img_dir, save_dir)

    srt_data = read_txt(srt_path)
    assert len(srt_data) == 16
    assert srt_data[2] == "空间里面他绝对赢不了的"
    assert srt_data[-2] == "你们接着善后"

    ass_data = read_txt(ass_path)
    assert len(ass_data) == 17
    assert ass_data[13].split(",", 9)[-1] == "空间里面他绝对赢不了的"
    assert ass_data[-1].split(",", 9)[-1] == "你们接着善后"

    txt_data = read_txt(txt_path)
    assert len(txt_data) == 8
    assert txt_data[-2] == "你们接着善后"


@pytest.mark.parametrize("img_dir", [test_dir / "RGBImages"])
def test_concat_rec(setup_and_teardown, img_dir):
    save_dir, srt_path, ass_path, txt_path = setup_and_teardown

    input_param = RapidVideOCRInput(is_batch_rec=True)
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, save_dir)

    srt_data = read_txt(srt_path)
    assert len(srt_data) == 16
    assert srt_data[2] == "空间里面他绝对赢不了的"
    assert srt_data[-2] == "你们接着善后"

    ass_data = read_txt(ass_path)
    assert len(ass_data) == 17
    assert ass_data[13].split(",", 9)[-1] == "空间里面他绝对赢不了的"
    assert ass_data[-1].split(",", 9)[-1] == "你们接着善后"

    txt_data = read_txt(txt_path)
    assert len(txt_data) == 8
    assert txt_data[-2] == "你们接着善后"


@pytest.mark.parametrize(
    "img_dir",
    [test_dir / "RGBImage", test_dir / "TXTImage"],
)
def test_empty_dir(img_dir):
    extractor = RapidVideOCR(RapidVideOCRInput())
    mkdir(img_dir)

    with pytest.raises(RapidVideOCRExeception) as exc_info:
        extractor(img_dir, test_dir)
    assert exc_info.type is RapidVideOCRExeception

    shutil.rmtree(img_dir)


@pytest.mark.parametrize(
    "img_dir",
    [test_dir / "RGBImage", test_dir / "TXTImage"],
)
def test_nothing_dir(img_dir):
    extractor = RapidVideOCR(RapidVideOCRInput())
    mkdir(img_dir)
    with pytest.raises(RapidVideOCRExeception) as exc_info:
        extractor(img_dir, test_dir)
    assert exc_info.type is RapidVideOCRExeception

    shutil.rmtree(img_dir)


def test_out_only_srt(setup_and_teardown):
    save_dir, srt_path, ass_path, txt_path = setup_and_teardown

    img_dir = test_dir / "RGBImages"
    input_param = RapidVideOCRInput(is_batch_rec=True, out_format="srt")
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, save_dir)

    srt_data = read_txt(srt_path)
    assert len(srt_data) == 16
    assert srt_data[2] == "空间里面他绝对赢不了的"
    assert srt_data[-2] == "你们接着善后"


def test_out_only_ass(setup_and_teardown):
    save_dir, srt_path, ass_path, txt_path = setup_and_teardown

    img_dir = test_dir / "RGBImages"
    input_param = RapidVideOCRInput(is_batch_rec=True, out_format="ass")
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, save_dir)

    ass_data = read_txt(ass_path)
    assert len(ass_data) == 17
    assert ass_data[13].split(",", 9)[-1] == "空间里面他绝对赢不了的"
    assert ass_data[-1].split(",", 9)[-1] == "你们接着善后"


def test_out_only_txt(setup_and_teardown):
    save_dir, srt_path, ass_path, txt_path = setup_and_teardown

    img_dir = test_dir / "RGBImages"
    input_param = RapidVideOCRInput(is_batch_rec=True, out_format="txt")
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, save_dir)

    txt_data = read_txt(txt_path)
    assert len(txt_data) == 8
    assert txt_data[-2] == "你们接着善后"

@pytest.mark.parametrize("img_dir", [test_dir / "RGBImages"])
def test_ocr_multi_configs(setup_and_teardown, img_dir):
    save_dir, srt_path, ass_path, txt_path = setup_and_teardown

    ocr_params_list = [
        {
            "Det.limit_side_len": 4000,
            "Det.limit_type": "max",
        },
        {
            "Det.limit_side_len": 640,
            "Det.limit_type": "min",
        }
    ]
    input_param = RapidVideOCRInput(is_batch_rec=False, ocr_params_list=ocr_params_list)
    extractor = RapidVideOCR(input_param)
    extractor(img_dir, save_dir)

    srt_data = read_txt(srt_path)
    assert len(srt_data) == 16
    assert srt_data[2] == "空间里面他绝对赢不了的"
    assert srt_data[-2] == "你们接着善后"

    ass_data = read_txt(ass_path)
    assert len(ass_data) == 17
    assert ass_data[13].split(",", 9)[-1] == "空间里面他绝对赢不了的"
    assert ass_data[-1].split(",", 9)[-1] == "你们接着善后"

    txt_data = read_txt(txt_path)
    assert len(txt_data) == 8
    assert txt_data[-2] == "你们接着善后"