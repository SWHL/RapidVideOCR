# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from __future__ import annotations

import copy
import datetime
import difflib
from pathlib import Path
from typing import List, Optional, Tuple, Union, Any

import cv2
import numpy as np


class VideoReader():
    """OpenCV version
    """
    def __init__(self, video_path: str) -> None:
        self.cap = cv2.VideoCapture(video_path)

    def __getitem__(self, idx: int) -> Optional[np.ndarray]:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        is_success, frame = self.cap.read()
        if is_success:
            return frame
        return None

    def __len__(self, ) -> int:
        return self.get_frame_count()

    def get_avg_fps(self,) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FPS))

    def get_frame_count(self, ) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_continue_batch(self, idx_list: List) -> np.ndarray:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx_list[0])
        batch_frame = [self.cap.read()[1] for _ in range(len(idx_list))]
        return np.stack(batch_frame)

    def __enter__(self) -> VideoReader:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.cap.release()


def calc_str_similar(str1: str, str2: str) -> float:
    return difflib.SequenceMatcher(None, str1, str2).ratio()


def convert_time_to_frame(time_str: str, fps: int) -> int:
    if not time_str:
        return 0

    time_parts = list(map(float, time_str.split(':')))
    len_time = len(time_parts)
    if len_time == 3:
        td = datetime.timedelta(hours=time_parts[0],
                                minutes=time_parts[1],
                                seconds=time_parts[2])
    elif len_time == 2:
        td = datetime.timedelta(minutes=time_parts[0],
                                seconds=time_parts[1])
    else:
        raise ValueError(
            f'Time data "{time_str}" does not match format "%H:%M:%S"')

    frame_index = int(td.total_seconds() * fps)
    return frame_index


def get_srt_timestamp(frame_index: int, fps: float) -> str:
    # convert frame index into SRT timestamp
    td = datetime.timedelta(seconds=frame_index / fps)
    ms = td.microseconds // 1000
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def calc_l2_dis_frames(img_a: np.ndarray,
                       img_batch: np.ndarray,
                       threshold: float = 0.000) -> Tuple[bool]:
    img_a_tmp = copy.deepcopy(img_a)
    img_batch_tmp = copy.deepcopy(img_batch)

    img_a_tmp /= 255
    img_batch_tmp /= 255

    # 70 x 74 x 1920
    difference = (img_a_tmp - img_batch_tmp) ** 2

    # 70 x (74 x 1920)
    difference = difference.reshape(img_batch_tmp.shape[0], -1)

    # np.sum() → (70, ) → (70, )
    error = np.sum(difference, axis=1) / img_a_tmp.size
    return error < threshold


class ProcessImg():
    def __init__(self) -> None:
        pass

    @staticmethod
    def rgb_to_grey(img: np.ndarray) -> np.ndarray:
        if img.ndim == 3:
            img = img[np.newaxis, :, :, :]
        return img[..., 0] * 0.114 + img[..., 1] * 0.587 + img[..., 2] * 0.299

    @staticmethod
    def binary_img(img: np.ndarray, binary_threshold: int = 243) -> np.ndarray:
        _, img = cv2.threshold(img, binary_threshold, 255, cv2.THRESH_BINARY)
        return img

    @staticmethod
    def vis_binary(i: int, img: np.ndarray, default_pos: int = 127) -> int:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = copy.deepcopy(img)

        def update_theta(x): pass

        window_name = f'[{i}/3] Select the best threshold of binary,'\
            'press Enter to confirm.'
        tracker_name = 'threshold'

        cv2.namedWindow(window_name)
        cv2.createTrackbar(tracker_name, window_name, 0, 255, update_theta)
        cv2.setTrackbarPos(trackbarname=tracker_name,
                           winname=window_name,
                           pos=default_pos)

        while True:
            cv2.imshow(window_name, img)
            threshold = cv2.getTrackbarPos(tracker_name, window_name)
            _, img = cv2.threshold(img2, threshold, 255, cv2.THRESH_BINARY)
            if cv2.waitKeyEx(1) == 13:
                break
        cv2.destroyAllWindows()
        return threshold

    @staticmethod
    def dilate_img(img: np.ndarray) -> np.ndarray:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        img = cv2.dilate(img, kernel, iterations=1)
        return img

    def remove_bg(self, img: np.ndarray,
                  is_dilate: bool = True,
                  binary_thr: int = 243) -> np.ndarray:
        # TODO: 优化
        img = self.rgb_to_grey(img).squeeze()
        if is_dilate:
            img = self.dilate_img(self.binary_img(img, binary_thr))
        img = img[np.newaxis, :, :]
        return img

    def remove_batch_bg(self, img_batch: np.ndarray,
                        is_dilate: bool = True,
                        binary_thr: int = 243) -> np.ndarray:
        # TODO: 优化
        img_batch = self.rgb_to_grey(img_batch)
        new_img_batch = []
        for img_one in img_batch:
            if is_dilate:
                img_one = self.dilate_img(self.binary_img(img_one, binary_thr))

            new_img_batch.append(img_one)
        img_batch = np.array(new_img_batch)
        return img_batch


class ExportResult():
    def __init__(self) -> None:
        pass

    def __call__(self, video_path: str, extract_result) -> None:
        # TODO: List[List[Union[int, str, str, str]]]
        content = []
        for i, start_time, end_time, text in extract_result:
            content.append(f'{i}\n{start_time} --> {end_time}\n{text}\n')

        full_path = Path(video_path).parent / f'{Path(video_path).stem}.srt'
        self.write_txt(full_path, content)
        print(f'The srt has been saved in the {full_path}.')

    @staticmethod
    def write_txt(save_path: Union[str, Path],
                  content: list,
                  mode: str = 'w') -> None:
        if not isinstance(save_path, str):
            save_path = str(save_path)

        if not isinstance(content, list):
            content = [content]

        with open(save_path, mode, encoding='utf-8') as f:
            for value in content:
                f.write(f'{value}\n')


def debug_vis_box(i: int, dt_boxes: np.ndarray, one_frame: np.ndarray) -> None:
    for box in dt_boxes:
        box = np.array(box).astype(np.int32).reshape(-1, 2)
        cv2.polylines(one_frame, [box], True,
                      color=(255, 255, 0), thickness=2)
    cv2.imwrite(f'temp/{i}.jpg', one_frame)
