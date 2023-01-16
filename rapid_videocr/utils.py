# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from __future__ import annotations

import tkinter as tk
import copy
import datetime
import difflib
from enum import Enum
from pathlib import Path
import random
from typing import List, Union, Any, Tuple

import cv2
import numpy as np

ExtractType = List[List[Union[int, str, str, str]]]


class VideoReader():
    def __init__(self, video_path: str) -> None:
        self.cap = cv2.VideoCapture(video_path)

    def __getitem__(self, idx: int) -> Any:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        is_success, frame = self.cap.read()
        if is_success:
            return frame
        return None

    def __len__(self, ) -> int:
        return self.get_num_frames()

    def get_fps(self,) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FPS))

    def get_num_frames(self, ) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_continue_batch(self, idx_list: np.ndarray) -> np.ndarray:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx_list[0])
        batch_frame = [self.cap.read()[1] for _ in range(len(idx_list))]
        return np.stack(batch_frame)

    def get_random_frames(self, select_num: int) -> np.ndarray:
        random_idx = random.choices(range(self.get_num_frames()), k=select_num)
        selected_frames = np.stack([self.__getitem__(i) for i in random_idx])
        return selected_frames

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


def convert_frame_to_time(frame_index: int, fps: int) -> str:
    td = datetime.timedelta(seconds=frame_index / fps)
    ms = td.microseconds // 1000
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def calc_l2_dis_frames(img_a: np.ndarray, img_batch: np.ndarray) -> np.ndarray:
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
    return error


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
    def vis_binary(cur_num: int,
                   img: np.ndarray,
                   pos: int = 127,
                   run_nums: int = 3) -> int:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = copy.deepcopy(img)
        h, w = img.shape[:2]

        def update_theta(x: Any) -> None:
            pass

        window_name = f'[{cur_num}/{run_nums}] Select the best threshold of' \
                      ' binary, press Enter to confirm.'
        tracker_name = 'threshold'

        cv2.namedWindow(window_name)
        cv2.resizeWindow(window_name, w, h)
        cv2.createTrackbar(tracker_name, window_name, 0, 255, update_theta)
        cv2.setTrackbarPos(trackbarname=tracker_name,
                           winname=window_name,
                           pos=pos)

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
        """根据阈值移除图像背景

        Args:
            img (np.ndarray): H x W x C
            is_dilate (bool, optional): _description_. Defaults to True.
            binary_thr (int, optional): _description_. Defaults to 243.

        Returns:
            np.ndarray: 1 x H x W
        """
        result_img = []
        img = self.rgb_to_grey(img)
        for img_one in img:
            if is_dilate:
                binaried_img = self.binary_img(img_one, binary_thr)
                img_one = self.dilate_img(binaried_img)
            result_img.append(img_one)
        return np.array(result_img)


class OutputFormat(Enum):
    SRT = 'srt'
    TXT = 'txt'
    ALL = 'all'


class ExportResult():
    def __init__(self) -> None:
        pass

    def __call__(self, video_path: str,
                 extract_res: ExtractType,
                 out_format: str = 'all') -> None:
        save_stem = Path(video_path).parent / Path(video_path).stem

        if out_format == OutputFormat.SRT.value:
            content = self.get_srt_content(extract_res)
            save_path = f'{save_stem}.{OutputFormat.SRT.value}'
            self.save_file(save_path, content)
        elif out_format == OutputFormat.TXT.value:
            content = self.get_txt_content(extract_res)
            save_path = f'{save_stem}.{OutputFormat.TXT.value}'
            self.save_file(save_path, content)
        elif out_format == OutputFormat.ALL.value:
            content = self.get_srt_content(extract_res)
            save_path = f'{save_stem}.{OutputFormat.SRT.value}'
            self.save_file(save_path, content)

            content = self.get_txt_content(extract_res)
            save_path = f'{save_stem}.{OutputFormat.TXT.value}'
            self.save_file(save_path, content)
        else:
            raise ValueError(f'{out_format} is not supported!')

    def get_srt_content(self, extract_res: ExtractType) -> List:
        content = []
        for i, start_time, end_time, text in extract_res:
            content.append(f'{i}\n{start_time} --> {end_time}\n{text}\n')
        return content

    def get_txt_content(self, extract_res: ExtractType) -> List:
        return [text for _, _, _, text in extract_res]

    @staticmethod
    def save_file(save_path: Union[str, Path],
                  content: list,
                  mode: str = 'w') -> None:
        if not isinstance(save_path, str):
            save_path = str(save_path)

        if not isinstance(content, list):
            content = [content]

        with open(save_path, mode, encoding='utf-8') as f:
            for value in content:
                f.write(f'{value}\n')
        print(f'The file has been saved in the {save_path}')


def get_screen_w_h() -> Tuple[int, int]:
    win = tk.Tk()
    width = win.winfo_screenwidth()
    height = win.winfo_screenheight()
    win.destroy()
    return height, width
