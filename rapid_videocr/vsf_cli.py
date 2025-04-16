# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

cur_dir = Path(__file__).resolve().parent


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
    def __init__(self, input_params: VideoSubFinderInput):
        param_dict = asdict(input_params)
        run_list = [input_params.vsf_exe_path]
        for k, v in param_dict.items():
            if v is None or str(v) == "False":
                continue

            run_list.append(f"--{str(k)}" if str(v) == "True" else f"--{k} {v}")
        self.run_list = run_list

    def __call__(self, video_path: str, output_dir: str) -> str:
        self.run_list.extend(["--input_video", video_path, "--output_dir", output_dir])
        try:
            subprocess.run(self.run_list, check=False)
            return output_dir
        except Exception as e:
            raise e


class VSFError(Exception):
    pass
