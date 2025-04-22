# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import platform
import subprocess
import tarfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Union

from .utils.download_file import download_file

cur_dir = Path(__file__).resolve().parent

VSF_MODEL_DICT = {
    "Linux": "https://github.com/eritpchy/videosubfinder-cli/releases/download/6.10.2-ci/videosubfinder-cli-cpu-static-linux-x64.tar.gz"
}


@dataclass
class VideoSubFinderInput:
    vsf_exe_path: Optional[str] = None
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
        cur_platform = platform.system()

        if input_params.vsf_exe_path is None:
            # 自动下载指定版本
            cur_platform = "Linux"
            vsf_url = VSF_MODEL_DICT[cur_platform]
            save_path = cur_dir / f"{Path(vsf_url).name}"
            download_file(vsf_url, save_path)
            untar(save_path, cur_dir / "vsf")
            run_cmd([f"cd {cur_dir}/vsf", "chmod +x ./VideoSubFinderCli.run"])
            input_params.vsf_exe_path = str(cur_dir / "vsf" / "VideoSubFinderCli.run")

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
            run_cmd(self.run_list)
            return output_dir
        except Exception as e:
            raise e


def untar(file_path: Union[str, Path], save_dir: Union[str, Path]):
    with tarfile.open(file_path, "r") as tar:
        tar.extractall(path=save_dir)


def run_cmd(cmd: List[str]):
    try:
        process = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Run {cmd} meets error. \n{e.stderr}") from e
