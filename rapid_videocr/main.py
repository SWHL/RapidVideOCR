# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from typing import List, Union

from .export import ExportStrategyFactory, OutputFormat
from .ocr_processor import OCRProcessor
from .utils.crop_by_project import CropByProject
from .utils.logger import logger
from .utils.typings import IMAGE_EXTENSIONS, RapidVideOCRInput
from .utils.utils import mkdir


class RapidVideOCR:
    def __init__(self, input_params: RapidVideOCRInput):
        logger.setLevel(input_params.log_level.upper())

        self.ocr_processor = OCRProcessor(
            input_params.ocr_params, input_params.batch_size
        )

        self.cropper = CropByProject()

        self.is_batch_rec = input_params.is_batch_rec
        self.out_format = input_params.out_format

    def __call__(
        self,
        vsf_dir: Union[str, Path],
        save_dir: Union[str, Path],
        save_name: str = "result",
    ) -> List[str]:
        vsf_dir = Path(vsf_dir)
        if not vsf_dir.exists():
            raise RapidVideOCRExeception(f"{vsf_dir} does not exist.")

        img_list = self.get_img_list(vsf_dir)
        srt_result, ass_result, txt_result = self.ocr_processor(
            img_list, self.is_batch_rec, self.is_txt_dir(vsf_dir)
        )

        self.export_file(Path(save_dir), save_name, srt_result, ass_result, txt_result)
        return txt_result

    def get_img_list(self, vsf_dir: Path) -> List[Path]:
        def get_sort_key(x: Path) -> int:
            return int("".join(str(x.stem).split("_")[:4]))

        img_list = []
        for v in vsf_dir.glob("*.*"):
            if not v.is_file():
                continue

            if v.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            img_list.append(v)

        if not img_list:
            raise RapidVideOCRExeception(f"{vsf_dir} does not have valid images")

        img_list = sorted(img_list, key=get_sort_key)
        return img_list

    @staticmethod
    def is_txt_dir(vsf_dir: Path) -> bool:
        return "TXTImages" in vsf_dir.name

    def export_file(
        self,
        save_dir: Path,
        save_name: str,
        srt_result: List[str],
        ass_result: List[str],
        txt_result: List[str],
    ):
        try:
            strategy = ExportStrategyFactory.create_strategy(self.out_format)
            mkdir(save_dir)
            strategy.export(save_dir, save_name, srt_result, ass_result, txt_result)
            logger.info(f"[OCR] Results saved to directory: {save_dir}")
        except ValueError as e:
            logger.error(f"Export failed: {e}")
            raise

    def print_console(self, txt_result: List):
        for v in txt_result:
            print(v.strip())


class RapidVideOCRExeception(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--img_dir",
        type=str,
        required=True,
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
        "-f",
        "--file_name",
        type=str,
        default="result",
        help='The name of the resulting file name. Default is "result".',
    )
    parser.add_argument(
        "-o",
        "--out_format",
        type=str,
        default=OutputFormat.ALL.value,
        choices=[v.value for v in OutputFormat],
        help='Output file format. Default is "all".',
    )
    parser.add_argument(
        "--is_batch_rec",
        action="store_true",
        default=False,
        help="Which mode to run (concat recognition or single recognition). Default is False.",
    )
    parser.add_argument(
        "-b",
        "--batch_size",
        type=int,
        default=10,
        help="The batch of concating image nums in concat recognition mode. Default is 10.",
    )
    args = parser.parse_args()

    ocr_input_params = RapidVideOCRInput(
        is_batch_rec=args.is_batch_rec,
        batch_size=args.batch_size,
        out_format=args.out_format,
    )
    extractor = RapidVideOCR(ocr_input_params)
    extractor(args.img_dir, args.save_dir, args.file_name)


if __name__ == "__main__":
    main()
