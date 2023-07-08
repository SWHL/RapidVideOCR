# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import tempfile
from pathlib import Path

from .rapid_videocr import RapidVideOCR
from .utils import get_logger
from .video_sub_finder import VideoSubFinder


class RapidVideoSubFinderOCR:
    def __init__(self, vsf_exe_path: str = None, **ocr_params) -> None:
        if vsf_exe_path is None:
            raise ValueError("vsf_exe_path must not be None.")

        self.vsf = VideoSubFinder(vsf_exe_path)
        self.video_ocr = RapidVideOCR(**ocr_params)
        self.video_formats = [".mp4", ".avi", ".mov", ".mkv"]
        self.logger = get_logger()

    def __call__(self, video_path: str, output_dir: str = "outputs"):
        if Path(video_path).is_dir():
            video_list = Path(video_path).rglob("*.*")
            video_list = [
                v for v in video_list if v.suffix.lower() in self.video_formats
            ]
        else:
            video_list = [video_path]

        self.logger.info(
            "Extracting subtitle images with VideoSubFinder (takes quite a long time) ..."
        )
        video_num = len(video_list)
        for i, one_video in enumerate(video_list):
            self.logger.info(
                f"[{i+1}/{video_num}] Starting to extract {one_video} key frame"
            )
            with tempfile.TemporaryDirectory() as tmp_dir:
                try:
                    self.vsf(str(one_video), tmp_dir)
                except Exception as e:
                    self.logger.error(f"Extract {one_video} error, {e}, skip")
                    continue

                self.logger.info(f"[{i+1}/{video_num}] Starting to run {one_video} ocr")

                rgb_dir = Path(tmp_dir) / "RGBImages"
                if not list(rgb_dir.iterdir()):
                    self.logger.warning(
                        f"Extracting frames from {one_video} is 0, skip"
                    )
                    continue

                save_name = Path(one_video).stem
                save_srt_dir = Path(output_dir) / save_name
                self.video_ocr(rgb_dir, save_srt_dir, save_name=save_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-vsf",
        "--vsf_exe_path",
        type=str,
        default=None,
        help="The full path of VideoSubFinderWXW.exe.",
    )
    parser.add_argument(
        "-video_dir",
        "--video_dir",
        type=str,
        default=None,
        help="The full path of video or the path of video directory.",
    )
    parser.add_argument(
        "-i",
        "--img_dir",
        type=str,
        default=None,
        help="The full path of RGBImages or TXTImages.",
    )
    parser.add_argument(
        "-s",
        "--save_dir",
        type=str,
        default="outputs",
        help='The path of saving the recognition result. Default is "outputs" under the current directory.',
    )
    parser.add_argument(
        "-o",
        "--out_format",
        type=str,
        default="all",
        choices=["srt", "txt", "all"],
        help='Output file format. Default is "all".',
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="single",
        choices=["single", "concat"],
        help='Which mode to run (concat recognition or single recognition). Default is "single".',
    )
    parser.add_argument(
        "-b",
        "--concat_batch",
        type=int,
        default=10,
        help="The batch of concating image nums in concat recognition mode. Default is 10.",
    )
    parser.add_argument(
        "-p",
        "--print_console",
        type=bool,
        default=0,
        choices=[0, 1],
        help="Whether to print the subtitle results to console. 1 means to print results to console. Default is 0.",
    )
    args = parser.parse_args()

    is_concat_rec = "concat" in args.mode

    if not (args.vsf_exe_path is None and args.video_dir is None):
        raise ValueError(
            "--vsf_exe_path or --video_dir must not be None at the same time."
        )

    if args.vsf_exe_path and args.video_dir:
        extractor = RapidVideoSubFinderOCR(
            vsf_exe_path=args.vsf_exe_path,
            is_concat_rec=is_concat_rec,
            concat_batch=args.concat_batch,
            out_format=args.out_format,
            is_print_console=args.print_console,
        )
        extractor(args.video_dir, args.save_dir)

    if args.img_dir:
        extractor = RapidVideOCR(
            is_concat_rec=is_concat_rec,
            concat_batch=args.concat_batch,
            out_format=args.out_format,
            is_print_console=args.print_console,
        )
        extractor(args.img_dir, args.save_dir)


if __name__ == "__main__":
    main()
