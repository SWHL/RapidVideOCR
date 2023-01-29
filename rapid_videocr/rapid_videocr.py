# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import copy
from pathlib import Path
from typing import Dict, List, Tuple, Union

import cv2
import numpy as np
import yaml
from rapidocr_onnxruntime import RapidOCR
from tqdm import tqdm

from .utils import (ExportResult, ProcessImg, VideoReader, calc_l2_dis_frames,
                    calc_str_similar, convert_frame_to_time,
                    convert_time_to_frame, get_screen_w_h)

CUR_DIR = Path(__file__).resolve().parent
CONFIG_PATH = CUR_DIR / 'config_videocr.yaml'


class RapidVideOCR():
    def __init__(self, config_path: Union[str, Path] = CONFIG_PATH):
        self.rapid_ocr = RapidOCR()
        self.text_det = self.rapid_ocr.text_detector

        config = self._read_yaml(config_path)
        self.error_thr = config['error_thr']
        self.is_dilate = config['is_dilate']
        self.time_start = config['time_start']
        self.time_end = config['time_end']

        self.select_nums = 3
        self.str_similar_ratio = 0.6
        self.batch_size = 100

        self.process_img = ProcessImg()
        self.export_res = ExportResult()

        self.screen_w, self.screen_h = get_screen_w_h()

    def __call__(self, video_path: str, out_format: str = 'all') -> List:
        self.vr = VideoReader(video_path)

        selected_frames = self.vr.get_random_frames(self.select_nums)
        rois = self._select_roi(selected_frames)
        y_start, y_end, padding_pixel = self._get_crop_range(rois)
        binary_thr = self._select_threshold(selected_frames, y_start, y_end)

        fps = self.vr.get_fps()
        num_frames = self.vr.get_num_frames()
        start_idx, end_idx = self._get_range_frame(fps, num_frames)

        key_frames, duplicate_frames = self.get_key_frames(start_idx,
                                                           end_idx,
                                                           y_start, y_end,
                                                           binary_thr)

        frames_ocr_res, invalid_keys = self.run_ocr(key_frames, padding_pixel)

        duplicate_frames = self.remove_invalid(duplicate_frames, invalid_keys)

        filter_frames, invalid_keys = self.merge_frames(frames_ocr_res,
                                                        duplicate_frames)
        filter_frames = self.truncate_overlap(filter_frames)
        extract_result = self.generate_srt(frames_ocr_res, fps,
                                           filter_frames, invalid_keys)
        self.export_res(video_path, extract_result, out_format.strip().lower())
        return extract_result

    @staticmethod
    def _read_yaml(yaml_path: Union[str, Path]) -> dict:
        with open(str(yaml_path), 'rb') as f:
            data = yaml.load(f, Loader=yaml.Loader)
        return data

    def _select_roi(self, selected_frames: np.ndarray) -> np.ndarray:
        roi_list = []
        for i, frame in enumerate(selected_frames):
            frame, map_ratio = self.get_adjust_frame(frame)
            roi = cv2.selectROI(
                f'[{i+1}/{self.select_nums}] Select a ROI and then press SPACE or ENTER button! Cancel the selection process by pressing c button!',
                frame, showCrosshair=True, fromCenter=False)

            if sum(roi) > 0:
                roi = [round(v * map_ratio) for v in roi]
                roi_list.append(roi)
        cv2.destroyAllWindows()
        return np.array(roi_list)

    def get_adjust_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, float]:
        h, w = frame.shape[:2]
        try:
            img_ratio = w / h
        except ZeroDivisionError as exc:
            raise ValueError(f'{exc}\nThe height of frame is zero!')

        resized_w = self.screen_w
        resized_h = round(resized_w / img_ratio)
        map_ratio = w / self.screen_w
        return cv2.resize(frame, (resized_w, resized_h)), map_ratio

    def _get_crop_range(self, rois: np.ndarray) -> Tuple[int, int, int]:
        crop_y_start = int(np.min(rois[:, 1]))
        select_box_h = int(np.max(rois[:, 3]))
        crop_y_end = crop_y_start + select_box_h
        return crop_y_start, crop_y_end, select_box_h

    def _select_threshold(self,
                          selected_frames: np.ndarray,
                          y_start: int,
                          y_end: int) -> int:
        threshold = 127
        crop_frames = selected_frames[:, y_start:y_end, ...]
        for i, frame in enumerate(crop_frames):
            frame, _ = self.get_adjust_frame(frame)
            new_thresh = self.process_img.vis_binary(i, frame,
                                                     threshold,
                                                     self.select_nums)
            threshold = new_thresh if new_thresh > threshold else threshold
        return threshold

    def _get_range_frame(self, fps: int, num_frames: int) -> Tuple[int, int]:
        start_idx = convert_time_to_frame(self.time_start, fps)
        end_idx = num_frames - 1
        if self.time_end:
            end_idx = convert_time_to_frame(self.time_end, fps)

        if end_idx < start_idx:
            raise ValueError('time_start is later than time_end')
        return start_idx, end_idx

    def get_key_frames(self,
                       start_idx: int,
                       end_idx: int,
                       y_start: int, y_end: int,
                       binary_thr: int) -> Tuple[Dict, Dict]:

        def get_batch_size(end_idx: int) -> int:
            if self.batch_size > end_idx:
                return end_idx - 1
            return self.batch_size

        key_frames: Dict = {}
        duplicate_frames: Dict = {}
        batch_size = get_batch_size(end_idx)

        pbar = tqdm(total=end_idx, desc='Obtain key frame', unit='frame')

        cur_idx, next_idx = start_idx, 1
        is_cur_idx_change = True
        while next_idx + batch_size <= end_idx:
            if is_cur_idx_change:
                cur_crop_frame = self.vr[cur_idx][y_start:y_end, :, :]
                cur_frame = self.process_img.remove_bg(cur_crop_frame,
                                                       self.is_dilate,
                                                       binary_thr)
                is_cur_idx_change = False

            if cur_idx not in key_frames:
                key_frames[cur_idx] = cur_crop_frame

            next_batch_idxs = np.array(range(next_idx, next_idx + batch_size))
            next_frames = self.vr.get_continue_batch(next_batch_idxs)
            next_crop_frames = next_frames[:, y_start:y_end, :, :]
            next_frames = self.process_img.remove_bg(next_crop_frames,
                                                     self.is_dilate,
                                                     binary_thr)

            l2_dis = calc_l2_dis_frames(cur_frame, next_frames)
            dissimilar_idxs = next_batch_idxs[~(l2_dis < self.error_thr)]
            if dissimilar_idxs.size == 0:
                next_idx += batch_size
                update_step = batch_size

                duplicate_frames.setdefault(
                    cur_idx, []).extend(next_batch_idxs)
            else:
                first_dissimilar_idx = dissimilar_idxs[0]
                similar_last_idx = first_dissimilar_idx - cur_idx
                next_batch_idxs = next_batch_idxs[:similar_last_idx]

                duplicate_frames.setdefault(
                    cur_idx, []).extend(next_batch_idxs)

                cur_idx = first_dissimilar_idx
                next_idx = cur_idx + 1

                update_step = first_dissimilar_idx - pbar.n + 1

                is_cur_idx_change = True

            if next_idx != end_idx and next_idx + batch_size > end_idx:
                batch_size = end_idx - next_idx

            pbar.update(update_step)
        pbar.close()
        return key_frames, duplicate_frames

    def run_ocr(self,
                key_frames: Dict,
                padding_pixel: int) -> Tuple[List, List]:
        def padding_img(img: np.ndarray, padding_pixel: int) -> np.ndarray:
            padded_img = cv2.copyMakeBorder(img,
                                            padding_pixel * 2,
                                            padding_pixel * 2,
                                            0, 0,
                                            cv2.BORDER_CONSTANT,
                                            value=(0, 0))
            return padded_img

        frames_ocr_res: List = []
        invalid_keys: List = []
        for key, frame in tqdm(key_frames.items(), desc='OCR', unit='frame'):
            frame = padding_img(frame, padding_pixel)

            rec_res = []
            ocr_result, _ = self.rapid_ocr(frame)
            if ocr_result:
                _, rec_res, _ = list(zip(*ocr_result))

            if not rec_res:
                invalid_keys.append(key)
                continue
            frames_ocr_res.append('\n'.join(rec_res))
        return frames_ocr_res, invalid_keys

    @staticmethod
    def remove_invalid(duplicate_frames: Dict, invalid_keys: List) -> Dict:
        return {k: v for k, v in duplicate_frames.items()
                if k not in invalid_keys}

    def merge_frames(self,
                     frames_ocr_res: List[Union[str, str, str]],
                     duplicate_frames: Dict) -> Tuple[Dict, List]:
        keys = list(duplicate_frames)
        invalid_keys = []

        cur_idx, next_idx = 0, 1
        n = len(frames_ocr_res)
        while next_idx < n:
            cur_rec = frames_ocr_res[cur_idx]
            next_rec = frames_ocr_res[next_idx]

            str_ratio = calc_str_similar(cur_rec, next_rec)
            if str_ratio > self.str_similar_ratio:
                # 相似→合并两个list
                cur_key = keys[cur_idx]
                similar_idxs = duplicate_frames[keys[next_idx]]
                duplicate_frames[cur_key].extend(similar_idxs)
                duplicate_frames[cur_key] = list(set(duplicate_frames[cur_key]))
                duplicate_frames[cur_key].sort()
                invalid_keys.append(next_idx)
            else:
                # 不相似
                cur_idx = next_idx
            next_idx += 1
        return duplicate_frames, invalid_keys

    @staticmethod
    def truncate_overlap(duplicate_frames: Dict) -> Dict:
        tmp_duplicate_frames = copy.deepcopy(duplicate_frames)
        key_idxs = list(duplicate_frames.keys())
        for i, (k, v) in enumerate(tmp_duplicate_frames.items()):
            if not v:
                continue

            other_keys = key_idxs[i:]
            for other_key in other_keys:
                if other_key in v:
                    loc_idx = v.index(other_key)
                    duplicate_frames[k] = v[:loc_idx]
        return duplicate_frames

    def generate_srt(self,
                     frames_ocr_res: List[Union[str, str, str]],
                     fps: int,
                     filter_frames: Dict,
                     invalid_keys: List) -> List:
        extract_result = []
        for i, (k, v) in enumerate(filter_frames.items()):
            if i in invalid_keys or not v:
                continue

            start_time = convert_frame_to_time(v[0], fps)
            end_time = convert_frame_to_time(v[-1], fps)
            extract_result.append([k, start_time, end_time, frames_ocr_res[i]])
        return extract_result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-mp4', '--mp4_path', type=str,
                        help='The full path of mp4 video.')
    parser.add_argument('-o', '--out_format', type=str, default='all',
                        choices=['srt', 'txt', 'all'],
                        help='Output file format. Default is "all"')
    args = parser.parse_args()

    mp4_path = args.mp4_path
    if not Path(mp4_path).exists():
        raise FileExistsError(f'{mp4_path} does not exists.')

    extractor = RapidVideOCR()
    ocr_result = extractor(mp4_path)
    print(ocr_result)


if __name__ == '__main__':
    main()
