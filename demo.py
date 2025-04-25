# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com

# 提取 + 识别
from rapid_videocr import RapidVideOCRInput, RapidVideoSubFinderOCR, VideoSubFinderInput

vsf_exe_path = (
    r"G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe"
)
vsf_input_params = VideoSubFinderInput(vsf_exe_path=vsf_exe_path)
ocr_input_params = RapidVideOCRInput(is_batch_rec=False)
vsf_ocr = RapidVideoSubFinderOCR(vsf_input_params, ocr_input_params)

# video_path可以是目录或者具体video路径
video_path = "test_files/tiny/2.mp4"
save_dir = "outputs"
vsf_ocr(video_path, save_dir)


# # 只识别
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

ocr_input_params = RapidVideOCRInput(is_batch_rec=False)
extractor = RapidVideOCR(ocr_input_params)

rgb_dir = "tests/test_files/RGBImages"
save_dir = "outputs"
save_name = "a"

# outputs/a.srt  outputs/a.txt
extractor(rgb_dir, save_dir, save_name=save_name)
