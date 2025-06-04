# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import subprocess
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class VideoSubFinderInput:
    vsf_exe_path: str
    clear_dirs: bool = True
    run_search: bool = True
    create_cleared_text_images: bool = True
    create_empty_sub: Optional[str] = None
    create_sub_from_cleared_txt_images: Optional[str] = None
    create_sub_from_txt_results: Optional[str] = None
    open_video_opencv: bool = True
    open_video_ffmpeg: bool = False
    use_cuda: bool = False
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    top_video_image_percent_end: float = 0.2
    bottom_video_image_percent_end: float = 0.0
    left_video_image_percent_end: float = 0.0
    right_video_image_percent_end: float = 1.0
    general_settings: Optional[str] = None
    num_threads: int = 2
    num_ocr_threads: int = 1


class VideoSubFinder:
    SHORT_FLAG_MAP = {
        "clear_dirs": "-c",
        "run_search": "-r",
        "create_cleared_text_images": "-ccti",
        "create_empty_sub": "-ces",
        "create_sub_from_cleared_txt_images": "-cscti",
        "create_sub_from_txt_results": "-cstxt",
        "open_video_opencv": "-ovocv",
        "open_video_ffmpeg": "-ovffmpeg",
        "use_cuda": "-uc",
        "start_time": "-s",
        "end_time": "-e",
        "top_video_image_percent_end": "-te",
        "bottom_video_image_percent_end": "-be",
        "left_video_image_percent_end": "-le",
        "right_video_image_percent_end": "-re",
        "general_settings": "-gs",
        "num_threads": "-nthr",
        "num_ocr_threads": "-nocrthr",
    }

    def __init__(self, input_params: VideoSubFinderInput):
        param_dict = asdict(input_params)
        run_list = [input_params.vsf_exe_path]
        for k, v in param_dict.items():
            if k == "vsf_exe_path":
                continue

            if v is None or str(v) == "False":
                continue

            flag = self.SHORT_FLAG_MAP[k]
            run_list.append(f"{flag}" if str(v) == "True" else f"{flag} {v}")
        self.run_list = run_list

    def __call__(self, video_path: str, output_dir: str) -> str:
        self.run_list.extend(["--input_video", video_path, "--output_dir", output_dir])
        try:
            subprocess.run(self.run_list, check=False)
            return output_dir
        except Exception as e:
            raise e
