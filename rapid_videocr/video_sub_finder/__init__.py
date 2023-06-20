# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
import subprocess

cur_dir = Path(__file__).resolve().parent


class VideoSubFinder():
    def __init__(self, num_threads: int = -1,
                 top_video_image_percent_end: float = 0.2,
                 ) -> None:
        self.te = top_video_image_percent_end
        self.num_threads = num_threads
        self.exe_path = str(cur_dir / 'libs' / 'VideoSubFinderWXW.exe')

    def __call__(self, video_path: str, output_dir: str):
        subprocess.run([
            self.exe_path,
            "--clear_dirs",
            "--run_search",
            "--create_cleared_text_images",
            "--num_threads", str(self.num_threads),
            "--input_video", video_path,
            "--use_cuda",
            "--output_dir", output_dir,
            "--top_video_image_percent_end", str(self.te),
        ])

        return output_dir
