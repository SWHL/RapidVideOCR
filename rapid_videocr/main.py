# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from rapidocr import RapidOCR
from tqdm import tqdm

from .export import ExportStrategyFactory, OutputFormat
from .utils.crop_by_project import CropByProject
from .utils.logger import Logger
from .utils.utils import (
    compute_centroid,
    compute_poly_iou,
    is_inclusive_each_other,
    mkdir,
    padding_img,
    read_img,
)


class RapidVideOCR:
    def __init__(
        self,
        is_batch_rec: bool = False,
        batch_size: int = 10,
        out_format: str = OutputFormat.ALL.value,
        ocr_params: Optional[Dict[str, Any]] = None,
    ):
        self.logger = Logger(logger_name=__name__).get_log()

        self.ocr_processor = OCRProcessor(ocr_params, batch_size)

        self.cropper = CropByProject()

        self.is_batch_rec = is_batch_rec
        self.out_format = out_format

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
        srt_result, txt_result = self.ocr_processor(
            img_list, self.is_batch_rec, self.is_txt_dir(vsf_dir)
        )

        self.export_file(Path(save_dir), save_name, srt_result, txt_result)
        return txt_result

    def get_img_list(self, vsf_dir: Path) -> List[Path]:
        def get_sort_key(x: Path) -> int:
            return int("".join(str(x.stem).split("_")[:4]))

        img_list = list(vsf_dir.glob("*.jpeg"))
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
        txt_result: List[str],
    ):
        try:
            strategy = ExportStrategyFactory.create_strategy(self.out_format)

            mkdir(save_dir)
            strategy.export(save_dir, save_name, srt_result, txt_result)
            self.logger.info("[OCR] Results saved to directory: %s", save_dir)
        except ValueError as e:
            self.logger.error("Export failed: %s", str(e))
            raise

    def print_console(self, txt_result: List):
        for v in txt_result:
            print(v.strip())


class OCRProcessor:
    def __init__(self, ocr_params, batch_size: int):
        self.logger = Logger(logger_name=__name__).get_log()

        default_params = {"Global.width_height_ratio": -1}
        if ocr_params is not None:
            ocr_params.update(default_params)
        else:
            ocr_params = default_params
        self.ocr_engine = RapidOCR(params=ocr_params)

        self.batch_size = batch_size

    def __call__(self, img_list: List[Path], is_batch_rec: bool, is_txt_dir: bool):
        self.is_txt_dir = is_txt_dir
        process_func = self.batch_rec if is_batch_rec else self.single_rec
        srt_result, txt_result = process_func(img_list)
        return srt_result, txt_result

    def single_rec(self, img_list: List[Path]) -> Tuple[List[str], List[str]]:
        self.logger.info("[OCR] Running with single recognition.")

        srt_result, txt_result = [], []
        for i, img_path in enumerate(tqdm(img_list, desc="OCR")):
            time_str = self.get_srt_timestamp(img_path)

            img = read_img(img_path)
            img = padding_img(img, (img.shape[0], img.shape[0], 0, 0))

            dt_boxes, rec_res = self.get_ocr_result(img)
            if dt_boxes is None or rec_res is None:
                txts = ""
            else:
                txts = self.process_same_line(dt_boxes, rec_res)

            srt_result.append(f"{i+1}\n{time_str}\n{txts}\n")
            txt_result.append(f"{txts}\n")
        return srt_result, txt_result

    @staticmethod
    def get_srt_timestamp(file_path: Path) -> str:
        split_paths = file_path.stem.split("_")
        start_time = split_paths[:4]
        start_time[0] = f"{start_time[0]:0>2}"
        start_str = ":".join(start_time[:3]) + f",{start_time[3]}"

        end_time = split_paths[5:9]
        end_time[0] = f"{end_time[0]:0>2}"
        end_str = ":".join(end_time[:3]) + f",{end_time[3]}"
        return f"{start_str} --> {end_str}"

    def batch_rec(self, img_list: List[Path]) -> Tuple[List, List]:
        self.logger.info("[OCR] Running with concat recognition.")

        img_nums = len(img_list)
        srt_result, txt_result = [], []
        for start_i in tqdm(range(0, img_nums, self.batch_size), desc="Concat Rec"):
            end_i = min(img_nums, start_i + self.batch_size)

            concat_img, img_coordinates, img_paths = self.get_batch_img_info(
                img_list, start_i, end_i
            )
            dt_boxes, rec_res = self.get_ocr_result(concat_img)
            if rec_res is None or dt_boxes is None:
                continue

            srt_part, txt_part = self.get_match_results(
                start_i, img_coordinates, dt_boxes, rec_res, img_paths
            )
            srt_result.extend(srt_part)
            txt_result.extend(txt_part)
        return srt_result, txt_result

    def get_batch_img_info(
        self, img_list: List[Path], start: int, end: int
    ) -> Tuple[np.ndarray, np.ndarray, List[Path]]:
        select_imgs = img_list[start:end]

        padding_value = 10
        array_img_list, img_coordinates, batch_img_paths = [], [], []
        for i, img_path in enumerate(select_imgs):
            batch_img_paths.append(img_path)

            img = read_img(img_path)

            if self.is_txt_dir:
                img = cv2.resize(img, None, fx=0.25, fy=0.25)

            pad_img = padding_img(img, (0, padding_value, 0, 0))
            array_img_list.append(pad_img)

            h, w = img.shape[:2]
            x0, y0 = 0, i * (h + padding_value)
            x1, y1 = w, (i + 1) * (h + padding_value)
            img_coordinates.append([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

        concat_img = np.vstack(array_img_list)
        return concat_img, np.array(img_coordinates), batch_img_paths

    def get_match_results(
        self,
        start_i: int,
        img_coordinates: np.ndarray,
        dt_boxes: np.ndarray,
        rec_res: Tuple[str],
        img_paths: List[Path],
    ) -> Tuple[List[str], List[str]]:
        match_dict: Dict[int, List[Union[Path, np.ndarray, str]]] = {
            k: [] for k in range(len(img_coordinates))
        }
        visited_idx = []
        for i, frame_boxes in enumerate(img_coordinates):
            for idx, dt_box in enumerate(dt_boxes):
                if idx in visited_idx:
                    continue

                box_iou = compute_poly_iou(frame_boxes, dt_box)
                if is_inclusive_each_other(frame_boxes, dt_box) or box_iou > 0.1:
                    matched_path = img_paths[i]
                    match_dict.setdefault(i, []).append(
                        [matched_path, dt_box, rec_res[idx]]
                    )
                    visited_idx.append(idx)

        srt_result_part, txt_result_part = [], []
        for k, v in match_dict.items():
            cur_frame_idx = start_i + k
            if v:
                img_path, boxes, recs = list(zip(*v))
                time_str = self.get_srt_timestamp(img_path[0])
                txts = self.process_same_line(boxes, recs)
            else:
                time_str = self.get_srt_timestamp(img_paths[k])
                txts = ""

            srt_result_part.append(f"{cur_frame_idx+1}\n{time_str}\n{txts}\n")
            txt_result_part.append(f"{txts}\n")
        return srt_result_part, txt_result_part

    def get_ocr_result(
        self, img: np.ndarray
    ) -> Tuple[Optional[np.ndarray], Optional[Tuple[str]]]:
        ocr_result = self.ocr_engine(img)
        if ocr_result.boxes is None:
            return None, None
        return ocr_result.boxes, ocr_result.txts

    def process_same_line(self, dt_boxes: np.ndarray, rec_res: List[str]) -> str:
        """处理同一行文本的识别结果

        Args:
            dt_boxes: 检测框坐标数组
            rec_res: 识别结果列表

        Returns:
            合并后的文本结果字符串
        """
        if len(rec_res) == 1:
            return rec_res[0]

        y_centroids = [compute_centroid(box)[1] for box in dt_boxes]
        line_groups = self._group_by_lines(y_centroids)
        return self._merge_line_text(line_groups, rec_res)

    def _group_by_lines(self, y_centroids: List[float]) -> List[List[int]]:
        """将文本框按行分组"""
        bool_res = self.is_same_line(y_centroids)
        groups = []
        current_group = [0]
        for i, is_same in enumerate(bool_res, 1):
            if is_same:
                current_group.append(i)
            else:
                groups.append(current_group)
                current_group = [i]

        groups.append(current_group)
        return groups

    def _merge_line_text(self, line_groups: List[List[int]], rec_res: List[str]) -> str:
        lines = []
        for group in line_groups:
            line_text = " ".join(rec_res[i] for i in group)
            lines.append(line_text)
        return "\n".join(lines)

    @staticmethod
    def is_same_line(points: List) -> List[bool]:
        threshold = 5

        align_points = list(zip(points, points[1:]))
        bool_res = [False] * len(align_points)
        for i, point in enumerate(align_points):
            y0, y1 = point
            if abs(y0 - y1) <= threshold:
                bool_res[i] = True
        return bool_res


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
        "-o",
        "--out_format",
        type=str,
        default="all",
        choices=["srt", "txt", "all"],
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
    parser.add_argument(
        "-p",
        "--print_console",
        type=bool,
        default=0,
        choices=[0, 1],
        help="Whether to print the subtitle results to console. 1 means to print results to console. Default is 0.",
    )
    args = parser.parse_args()

    extractor = RapidVideOCR(
        is_batch_rec=args.is_batch_rec,
        batch_size=args.batch_size,
        out_format=args.out_format,
    )
    extractor(args.img_dir, args.save_dir)


if __name__ == "__main__":
    main()
