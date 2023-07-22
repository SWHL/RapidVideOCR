# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import subprocess
from pathlib import Path
from typing import Optional

cur_dir = Path(__file__).resolve().parent


class VideoSubFinder:
    def __init__(
        self,
        vsf_exe_path: Optional[str] = None,
        clear_dirs: bool = True,
        run_search: bool = True,
        create_cleared_text_images: bool = True,
        create_empty_sub: Optional[str] = None,
        create_sub_from_cleared_txt_images: Optional[str] = None,
        create_sub_from_txt_results: Optional[str] = None,
        open_video_opencv: bool = True,
        open_video_ffmpeg: bool = False,
        use_cuda: bool = False,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        top_video_image_percent_end: float = 0.2,
        bottom_video_image_percent_end: float = 0.0,
        left_video_image_percent_end: float = 0.0,
        right_video_image_percent_end: float = 1.0,
        general_settings: Optional[str] = None,
        num_threads: int = 2,
        num_ocr_threads: int = 1,
    ) -> None:
        self.exe_path = vsf_exe_path
        if self.exe_path is None:
            raise ValueError("VSF Exe path must not be None.")

        param_dict = {
            "clear_dirs": clear_dirs,
            "run_search": run_search,
            "create_cleared_text_images": create_cleared_text_images,
            "create_empty_sub": create_empty_sub,
            "create_sub_from_cleared_txt_images": create_sub_from_cleared_txt_images,
            "create_sub_from_txt_results": create_sub_from_txt_results,
            "open_video_opencv": open_video_opencv,
            "open_video_ffmpeg": open_video_ffmpeg,
            "use_cuda": use_cuda,
            "start_time": start_time,
            "end_time": end_time,
            "top_video_image_percent_end": top_video_image_percent_end,
            "bottom_video_image_percent_end": bottom_video_image_percent_end,
            "left_video_image_percent_end": left_video_image_percent_end,
            "right_video_image_percent_end": right_video_image_percent_end,
            "general_settings": general_settings,
            "num_threads": num_threads,
            "num_ocr_threads": num_ocr_threads,
        }

        run_list = [self.exe_path]
        for k, v in param_dict.items():
            if v is None or str(v) == "False":
                continue

            if str(v) == "True":
                run_list.append(f"--{str(k)}")
            else:
                run_list.extend([f"--{k}", str(v)])

        self.run_list = run_list

    def __call__(self, video_path: str, output_dir: str) -> str:
        self.run_list.extend(["--input_video", video_path, "--output_dir", output_dir])

        try:
            subprocess.run(
                self.run_list,
                check=False,
            )
            return output_dir
        except Exception as e:
            raise e


class VSFError(Exception):
    pass
