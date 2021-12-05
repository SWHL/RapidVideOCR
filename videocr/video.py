
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import copy
import sys

import cv2
from tqdm import tqdm

from .utils import (Capture, is_similar,
                    get_srt_timestamp, get_specified_frame,
                    get_frame_from_time)


class Video(object):
    def __init__(self, path, ocr_system):
        self.path = path
        self.ocr_system = ocr_system

        print('Init Video instance')
        with Capture(path) as v:
            self.num_frames = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = v.get(cv2.CAP_PROP_FPS)
            self.height = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_key_point(self):
        self.key_point_dict = {}
        with tqdm(total=self.ocr_end, desc='Get the key point') as pbar, \
                Capture(self.path) as v:

            # Use two fast and slow pointers to filter duplicate frame.
            slow, fast = 0, self.ocr_start
            while fast < self.ocr_end:
                pbar.update(1)

                slow_frame = get_specified_frame(slow, v=v)[self.height-40:, :]
                fast_frame = get_specified_frame(fast, v=v)[self.height-40:, :]

                if is_similar(slow_frame, fast_frame, threshold=0.95):
                    if slow in self.key_point_dict:
                        self.key_point_dict[slow].append(fast)
                    else:
                        self.key_point_dict[slow] = [slow]
                else:
                    slow = fast
                fast += 1

    def run_ocr(self, time_start, time_end, use_fullframe):
        self.ocr_start = get_frame_from_time(time_start, self.fps)
        ocr_end = get_frame_from_time(time_end, self.fps)
        self.ocr_end = self.num_frames-1 if ocr_end == 0 else ocr_end
        if self.ocr_end < self.ocr_start:
            raise ValueError('time_start is later than time_end')

        self.get_key_point()

        # Extract the filtered frames content.
        self.pred_frames = []
        temp_key_point = copy.deepcopy(self.key_point_dict)
        for key in tqdm(temp_key_point.keys(), desc='Extract content'):
            frame = get_specified_frame(key, self.path)

            if not use_fullframe:
                frame = frame[self.height * 4 // 5:, :]

            _, rec_res = self.ocr_system(frame)

            if rec_res is None or len(rec_res) <= 0:
                del self.key_point_dict[key]
            else:
                text, confidence = list(zip(*rec_res))
                text = '\n'.join(text)
                confidence = sum(confidence) / len(confidence)
                self.pred_frames.append((text, confidence))

    def get_subtitles(self):
        result = []
        for i, v in enumerate(self.key_point_dict.values()):
            start_index = get_srt_timestamp(v[0], self.fps)
            end_index = get_srt_timestamp(v[-1], self.fps)
            result.append(
                f'{i}  {start_index} -> {end_index} : {self.pred_frames[i][0]}')
        return result
