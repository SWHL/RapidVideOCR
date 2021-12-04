
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
    def __init__(self, path: str, ocr_system):
        self.path = path
        self.ocr_system = ocr_system

        print('Init Video instance')
        with Capture(path) as v:
            self.num_frames = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = v.get(cv2.CAP_PROP_FPS)
            self.height = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def run_ocr(self,
                time_start: str,
                time_end: str,
                use_fullframe: bool):
        self.use_fullframe = use_fullframe

        # From the time string to specified frame index.
        ocr_start = get_frame_from_time(time_start, self.fps)
        ocr_end = get_frame_from_time(time_end, self.fps)
        ocr_end = self.num_frames if ocr_end == 0 else ocr_end

        if ocr_end < ocr_start:
            raise ValueError('time_start is later than time_end')

        # All frame between the start and end frame index.
        num_ocr_frames = ocr_end - ocr_start

        self.key_point_dict = {}
        with tqdm(total=num_ocr_frames-1, desc='Get the key point') as pbar, \
                Capture(self.path) as v:

            # Use two fast and slow pointers to filter duplicate frame.
            slow, fast = 0, ocr_start
            while fast < num_ocr_frames - 1:
                pbar.update(1)

                slow_frame = get_specified_frame(v, slow)[self.height-40:, :]
                fast_frame = get_specified_frame(v, fast)[self.height-40:, :]

                if is_similar(slow_frame, fast_frame, threshold=0.95):
                    if slow in self.key_point_dict:
                        self.key_point_dict[slow].append(fast)
                    else:
                        self.key_point_dict[slow] = [slow]
                else:
                    slow = fast
                fast += 1

        # Extract the filtered frames content.
        it_ocr = []
        self.pred_frames = []
        temp_key_point = copy.deepcopy(self.key_point_dict)
        for key in tqdm(temp_key_point.keys(), desc='Extract content'):
            frame = get_specified_frame(v, key, self.path)

            _, rec_res = self._image_to_data(frame)

            if rec_res is None or len(rec_res) <= 0:
                del self.key_point_dict[key]
            else:
                it_ocr.append(rec_res)
                text, confidence = list(zip(*rec_res))
                text = '\n'.join(text)
                confidence = sum(confidence) / len(confidence)

                self.pred_frames.append((text, confidence))

        self.pred_frames = []
        for data in it_ocr:
            if data is not None:
                text, confidence = list(zip(*data))
                text = '\n'.join(text)

                confidence = sum(confidence) / len(confidence)

                self.pred_frames.append((text, confidence))

    def _image_to_data(self, img):
        if not self.use_fullframe:
            img = img[self.height * 4 // 5:, :]

        try:
            dt_boxes, rec_res = self.ocr_system(img)
            return dt_boxes, rec_res
        except Exception as e:
            sys.exit('{}: {}'.format(e.__class__.__name__, e))

    def get_subtitles(self):
        result = []
        for i, v in enumerate(self.key_point_dict.values()):
            start_index = get_srt_timestamp(v[0], self.fps)
            end_index = get_srt_timestamp(v[-1], self.fps)
            result.append(
                f'\n{i}  {start_index} -> {end_index} : {self.pred_frames[i][0]}\n')
        return ''.join(result)
