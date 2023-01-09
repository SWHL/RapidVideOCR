
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import random
from datetime import timedelta
from pathlib import Path
from typing import List, Tuple, Union

import cv2
import numpy as np
import yaml
from rapidocr_onnxruntime import RapidOCR
from tqdm import tqdm

from .utils import (ExportResult, ProcessImg, VideoReader, calc_l2_dis_frames,
                    calc_str_similar, get_srt_timestamp)

CUR_DIR = Path(__file__).resolve().parent


class RapidVideOCR():
    def __init__(self,
                 config_path: Union[str, Path] = CUR_DIR / 'config_videocr.yaml'):
        self.rapid_ocr = RapidOCR()
        self.text_det = self.rapid_ocr.text_detector

        config = self._read_yaml(config_path)
        self.error_threshold = config['error_threshold']
        self.is_dilate = config['is_dilate']
        self.time_start = config['time_start']
        self.time_end = config['time_end']

        self.select_nums = 3
        self.str_similar_ratio = 0.6
        self.batch_size = 100

        self.process_img = ProcessImg()
        self.export_res = ExportResult()

    def __call__(self, video_path: str) -> List:
        print(f'Loading {video_path}')
        self.vr = VideoReader(video_path)
        num_frames = self.vr.get_num_frames()
        fps = self.vr.get_fps()
        selected_frames = self.vr.get_random_frames(self.select_nums)

        rois = self._select_roi(selected_frames)
        crop_y_start, crop_y_end, select_box_h = self._get_crop_range(rois)

        binary_threshold = self._select_threshold(selected_frames)

        start_frame, end_frame = self._get_phrase_frame(fps, num_frames)

        self.get_key_frame()
        self.run_ocr()
        extract_result = self.get_subtitles()
        self.export_res(video_path, extract_result)
        return extract_result

    def convert_time_to_frame(self, time_str: str, fps: int) -> int:
        if not time_str:
            return 0

        time_parts = list(map(float, time_str.split(':')))
        len_time = len(time_parts)
        if len_time == 3:
            td = timedelta(hours=time_parts[0],
                           minutes=time_parts[1],
                           seconds=time_parts[2])
        elif len_time == 2:
            td = timedelta(minutes=time_parts[0], seconds=time_parts[1])
        else:
            raise ValueError(
                f'Time data "{time_str}" does not match format "%H:%M:%S"')

        frame_index = int(td.total_seconds() * fps)
        return frame_index

    def get_key_frame(self, ) -> None:
        """获得视频的字幕关键帧"""

        self.duplicate_frame: dict = {}
        self.key_frames: dict = {}

        with tqdm(total=self.end_frame,
                  desc='Obtain key frame', unit='frame') as pbar:
            # Use two fast and slow pointers to filter duplicate frame.
            if self.batch_size > self.end_frame:
                self.batch_size = self.end_frame - 1

            slow, fast = 0, 1
            slow_change = True
            while fast + self.batch_size <= self.end_frame:
                if slow_change:
                    ori_slow_frame = self.vr[slow][self.crop_start: self.crop_end, :, :]

                    # Remove the background of the frame.
                    slow_frame = self.process_img.remove_bg(ori_slow_frame,
                                                            is_dilate=self.is_dilate,
                                                            binary_thr=self.binary_threshold)

                    slow_change = False

                batch_list = list(range(fast, fast+self.batch_size))
                fast_frames = self.vr.get_continue_batch(batch_list)
                fast_frames = fast_frames[:,
                                          self.crop_start: self.crop_end, :, :]

                fast_frames = self.process_img.remove_batch_bg(fast_frames,
                                                               is_dilate=self.is_dilate,
                                                               binary_thr=self.binary_threshold)

                # Compare the similarity between the frames.
                compare_result = calc_l2_dis_frames(slow_frame,
                                                    fast_frames,
                                                    threshold=self.error_threshold)
                batch_array = np.array(batch_list)
                not_similar_index = batch_array[np.logical_not(compare_result)]

                duplicate_frame = []
                if not_similar_index.size == 0:
                    # All are similar with the slow frame.
                    duplicate_frame = batch_list

                    pbar.update(self.batch_size)
                    fast += self.batch_size

                    self._record_key_info(
                        slow, duplicate_frame, ori_slow_frame)
                else:
                    # Exist the non similar frame.
                    index = not_similar_index[0] - slow
                    duplicate_frame = batch_list[:index]

                    # record
                    self._record_key_info(
                        slow, duplicate_frame, ori_slow_frame)

                    slow = not_similar_index[0]
                    fast = slow + 1
                    pbar.update(slow - pbar.n + 1)

                    slow_change = True

                # Take care the left frames, which can't up to the batch_size.
                if fast != self.end_frame \
                        and fast + self.batch_size > self.end_frame:
                    self.batch_size = self.end_frame - fast

    def run_ocr(self,) -> None:
        self.pred_frames = []
        for key, frame in tqdm(self.key_frames.items(),
                               desc='OCR Key Frame', unit='frame'):
            frame = cv2.copyMakeBorder(frame.squeeze(),
                                       self.subtitle_height * 2,
                                       self.subtitle_height * 2,
                                       0, 0,
                                       cv2.BORDER_CONSTANT,
                                       value=(0, 0))

            rec_res = []
            ocr_result, _ = self.rapid_ocr(frame)
            if ocr_result:
                _, rec_res, _ = list(zip(*ocr_result))

            if not rec_res:
                del self.duplicate_frame[key]
                continue
            self.pred_frames.append('\n'.join(rec_res))

    def get_subtitles(self, ) -> List:
        # TODO: List类型注解需要具化
        """合并最终OCR提取字幕文件，并输出
        """
        slow, fast = 0, 1
        n = len(self.pred_frames)
        key_list = list(self.duplicate_frame.keys())
        invalid_keys = []
        while fast < n:
            slow_rec, fast_rec = self.pred_frames[slow], self.pred_frames[fast]
            str_ratio = calc_str_similar(slow_rec, fast_rec)
            if str_ratio > self.str_similar_ratio:
                # 相似→合并两个list
                self.duplicate_frame[key_list[slow]].extend(
                    self.duplicate_frame[key_list[fast]])
                self.duplicate_frame[key_list[slow]].sort()
                invalid_keys.append(fast)
            else:
                # 不相似
                slow = fast
            fast += 1

        extract_result = []
        for i, (k, v) in enumerate(self.duplicate_frame.items()):
            if i in invalid_keys:
                continue

            start_time = get_srt_timestamp(v[0], self.fps)
            end_time = get_srt_timestamp(v[-1], self.fps)
            extract_result.append([k, start_time, end_time,
                                   self.pred_frames[i]])
        return extract_result

    def _select_roi(self, selected_frames: np.ndarray) -> np.ndarray:
        roi_list = []
        for i, frame in enumerate(selected_frames):
            roi = cv2.selectROI(
                f'[{i+1}/{self.select_nums}] Select a ROI and then press SPACE or ENTER button! Cancel the selection process by pressing c button!',
                frame, showCrosshair=True, fromCenter=False)
            if sum(roi) > 0:
                roi_list.append(roi)
        cv2.destroyAllWindows()
        return np.array(roi_list)

    def _get_crop_range(self, rois: np.ndarray) -> Tuple[int, int, int]:
        crop_y_start = int(np.min(rois[:, 1]))
        select_box_h = int(np.max(rois[:, 3]))
        crop_y_end = crop_y_start + select_box_h
        return crop_y_start, crop_y_end, select_box_h

    def _select_threshold(self, selected_frames: np.ndarray) -> int:
        threshold_list : List = []
        for i, frame in enumerate(selected_frames):
            crop_img = frame[self.crop_start: self.crop_end, :, :]
            if i == 0:
                threshold = self.process_img.vis_binary(i + 1, crop_img)
            else:
                threshold = self.process_img.vis_binary(i + 1, crop_img,
                                                        threshold_list[-1])
            threshold_list.append(threshold)
        return int(np.max(threshold_list))

    def _get_phrase_frame(self, fps: int, num_frames: int) -> Tuple[int, int]:
        start_frame = self.convert_time_to_frame(self.time_start, fps)
        end_frame = num_frames - 1
        if self.time_end:
            end_frame = self.convert_time_to_frame(self.time_end, fps)

        if end_frame < start_frame:
            raise ValueError('time_start is later than time_end')
        return start_frame, end_frame

    def _record_key_info(self, slow: int,
                         dup_frame: List,
                         slow_frame: np.ndarray) -> None:
        self.duplicate_frame.setdefault(slow, []).extend(dup_frame)

        if slow not in self.key_frames:
            self.key_frames[slow] = slow_frame

    @staticmethod
    def _read_yaml(yaml_path: Union[str, Path]) -> dict:
        with open(str(yaml_path), 'rb') as f:
            data = yaml.load(f, Loader=yaml.Loader)
        return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mp4_path', type=str)
    parser.add_argument('--format', choices=['srt', 'txt', 'docx', 'all'],
                        default='srt')
    args = parser.parse_args()

    mp4_path = args.mp4_path
    if not Path(mp4_path).exists():
        raise FileExistsError(f'{mp4_path} does not exists.')

    extractor = RapidVideOCR()
    ocr_result = extractor(mp4_path)
    print(ocr_result)


if __name__ == '__main__':
    main()
