# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
from rapidocr import RapidOCR
from tqdm import tqdm

from .utils.logger import Logger
from .utils.utils import (
    compute_centroid,
    compute_poly_iou,
    is_inclusive_each_other,
    padding_img,
    read_img,
)


class OCRProcessor:
    def __init__(self, ocr_params: Optional[Dict] = None, batch_size: int = 10):
        self.logger = Logger(logger_name=__name__).get_log()
        self.ocr_engine = self._init_ocr_engine(ocr_params)
        self.batch_size = batch_size

    def _init_ocr_engine(self, ocr_params: Optional[Dict] = None) -> RapidOCR:
        return RapidOCR(params=ocr_params)

    def __call__(
        self, img_list: List[Path], is_batch_rec: bool, is_txt_dir: bool
    ) -> Tuple[List[str], List[str], List[str]]:
        self.is_txt_dir = is_txt_dir
        process_func = self.batch_rec if is_batch_rec else self.single_rec
        rec_results = process_func(img_list)
        srt_results = self._generate_srt_results(rec_results)
        ass_results = self._generate_ass_results(rec_results)
        txt_results = self._generate_txt_result(rec_results)
        return srt_results, ass_results, txt_results

    def single_rec(self, img_list: List[Path]) -> List[Tuple[int, str, str, str]]:
        self.logger.info("[OCR] Running with single recognition.")

        rec_results = []
        for i, img_path in enumerate(tqdm(img_list, desc="OCR")):
            time_str = self._get_srt_timestamp(img_path)
            ass_time_str = self._get_ass_timestamp(img_path)
            img = self._preprocess_image(img_path)

            dt_boxes, rec_res = self.get_ocr_result(img)
            txts = (
                self.process_same_line(dt_boxes, rec_res)
                if dt_boxes is not None
                else ""
            )
            rec_results.append([i, time_str, txts, ass_time_str])
        return rec_results

    @staticmethod
    def _get_srt_timestamp(file_path: Path) -> str:
        """0_00_00_041__0_00_00_415_0070000000019200080001920.jpeg"""

        def format_time(time_parts):
            time_parts[0] = f"{time_parts[0]:0>2}"
            return ":".join(time_parts[:3]) + f",{time_parts[3]}"

        split_paths = file_path.stem.split("_")
        start_time = split_paths[:4]
        end_time = split_paths[5:9]
        return f"{format_time(start_time)} --> {format_time(end_time)}"

    @staticmethod
    def _get_ass_timestamp(file_path: Path) -> str:
        s = file_path.stem

        h1   = int(s[0:1])
        m1   = int(s[2:4])
        sec1 = int(s[5:7])
        ms1  = int(s[8:11])

        h2   = int(s[13:14])
        m2   = int(s[15:17])
        sec2 = int(s[18:20])
        ms2  = int(s[21:24])

        # compute absolute times in milliseconds
        bt = (h1 * 3600 + m1 * 60 + sec1) * 1000 + ms1
        et = (h2 * 3600 + m2 * 60 + sec2) * 1000 + ms2

        def to_ass(ts_ms: int) -> str:
            # centiseconds (drop the last digit, no rounding)
            cs_total = ts_ms // 10  
            cs = cs_total % 100
            total_s = ts_ms // 1000
            s = total_s % 60
            total_m = total_s // 60
            m = total_m % 60
            h = total_m // 60
            # H:MM:SS.CC
            return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

        return f"{to_ass(bt)},{to_ass(et)}"

    @staticmethod
    def _preprocess_image(img_path: Path) -> np.ndarray:
        img = read_img(img_path)
        img = padding_img(img, (img.shape[0], img.shape[0], 0, 0))
        return img

    @staticmethod
    def _generate_srt_results(rec_results: List[Tuple[int, str, str, str]]) -> List[str]:
        return [f"{i+1}\n{time_str}\n{txt}\n" for i, time_str, txt, _ in rec_results]

    @staticmethod
    def _generate_ass_results(rec_results: List[Tuple[int, str, str, str]]) -> List[str]:
        return [f"Dialogue: 0,{ass_time_str},Default,,0,0,0,,{txt}" for _, _, txt, ass_time_str in rec_results]

    @staticmethod
    def _generate_txt_result(rec_results: List[Tuple[int, str, str, str]]) -> List[str]:
        return [f"{txt}\n" for _, _, txt, _ in rec_results]

    @staticmethod
    def _is_same_line(points: List) -> List[bool]:
        threshold = 5

        align_points = list(zip(points, points[1:]))
        bool_res = [False] * len(align_points)
        for i, point in enumerate(align_points):
            y0, y1 = point
            if abs(y0 - y1) <= threshold:
                bool_res[i] = True
        return bool_res

    def batch_rec(self, img_list: List[Path]) -> List[Tuple[int, str, str, str]]:
        self.logger.info("[OCR] Running with concat recognition.")

        img_nums = len(img_list)
        rec_results = []
        for start_i in tqdm(range(0, img_nums, self.batch_size), desc="Concat Rec"):
            end_i = min(img_nums, start_i + self.batch_size)

            concat_img, img_coordinates, img_paths = self._prepare_batch(
                img_list[start_i:end_i]
            )
            dt_boxes, rec_res = self.get_ocr_result(concat_img)
            if rec_res is None or dt_boxes is None:
                continue

            one_batch_rec_results = self._process_batch_results(
                start_i, img_coordinates, dt_boxes, rec_res, img_paths
            )
            rec_results.extend(one_batch_rec_results)
        return rec_results

    def _prepare_batch(
        self, img_list: List[Path]
    ) -> Tuple[np.ndarray, np.ndarray, List[Path]]:
        padding_value = 10
        array_img_list, img_coordinates = [], []
        for i, img_path in enumerate(img_list):
            img = read_img(img_path)
            if self.is_txt_dir:
                img = cv2.resize(img, None, fx=0.25, fy=0.25)

            pad_img = padding_img(img, (0, padding_value, 0, 0))
            array_img_list.append(pad_img)

            h, w = img.shape[:2]
            x0, y0 = 0, i * (h + padding_value)
            x1, y1 = w, (i + 1) * (h + padding_value)
            img_coordinates.append([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

        return np.vstack(array_img_list), np.array(img_coordinates), img_list

    def _process_batch_results(
        self,
        start_i: int,
        img_coordinates: np.ndarray,
        dt_boxes: np.ndarray,
        rec_res: Tuple[str],
        img_paths: List[Path],
    ) -> List[Tuple[int, str, str, str]]:
        match_dict = self._match_boxes_to_images(
            img_coordinates, dt_boxes, rec_res, img_paths
        )

        results = []
        for k, v in match_dict.items():
            cur_frame_idx = start_i + k
            if v:
                img_path, boxes, recs = list(zip(*v))
                time_str = self._get_srt_timestamp(img_path[0])
                ass_time_str = self._get_ass_timestamp(img_path[0])
                txts = self.process_same_line(boxes, recs)
            else:
                time_str = self._get_srt_timestamp(img_paths[k])
                ass_time_str = self._get_ass_timestamp(img_paths[k])
                txts = ""

            results.append([cur_frame_idx, time_str, txts, ass_time_str])
        return results

    def _match_boxes_to_images(
        self,
        img_coordinates: np.ndarray,
        dt_boxes: np.ndarray,
        rec_res: List[str],
        img_paths: List[Path],
    ) -> Dict[int, List[Tuple[Path, np.ndarray, str]]]:
        """将检测框匹配到对应图像"""
        match_dict = {k: [] for k in range(len(img_coordinates))}
        visited_idx = set()

        for i, frame_boxes in enumerate(img_coordinates):
            for idx, (dt_box, txt) in enumerate(zip(dt_boxes, rec_res)):
                if idx in visited_idx:
                    continue

                if self._is_box_matched(frame_boxes, dt_box):
                    match_dict[i].append((img_paths[i], dt_box, txt))
                    visited_idx.add(idx)

        return match_dict

    def _is_box_matched(self, frame_boxes: np.ndarray, dt_box: np.ndarray) -> bool:
        """判断检测框是否匹配到图像"""
        box_iou = compute_poly_iou(frame_boxes, dt_box)
        return is_inclusive_each_other(frame_boxes, dt_box) or box_iou > 0.1

    def get_ocr_result(
        self, img: np.ndarray
    ) -> Tuple[Optional[np.ndarray], Optional[Tuple[str]]]:
        ocr_result = self.ocr_engine(img)
        if ocr_result.boxes is None:
            return None, None
        return ocr_result.boxes, ocr_result.txts

    def process_same_line(self, dt_boxes: np.ndarray, rec_res: List[str]) -> str:
        if len(rec_res) == 1:
            return rec_res[0]

        y_centroids = [compute_centroid(box)[1] for box in dt_boxes]
        line_groups = self._group_by_lines(y_centroids)
        return self._merge_line_text(line_groups, rec_res)

    def _group_by_lines(self, y_centroids: List[float]) -> List[List[int]]:
        """将文本框按行分组"""
        bool_res = self._is_same_line(y_centroids)
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
