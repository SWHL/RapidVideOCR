
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import numpy as np
from decord import VideoReader, cpu
from tqdm import tqdm

from .utils import (get_frame_from_time, get_srt_timestamp, is_similar,
                    is_similar_batch)


class Video(object):
    def __init__(self, path, ocr_system):
        self.path = path
        self.ocr_system = ocr_system

        print('Init Video instance')
        self.vr = VideoReader(path, ctx=cpu(0))
        self.num_frames = len(self.vr)
        self.fps = self.vr.get_avg_fps()
        self.height = int(self.vr[0].shape[0])

    def get_key_point(self):
        self.key_point_dict = {}
        batch_size = int(self.fps) * 2
        with tqdm(total=self.ocr_end, desc='Get the key point') as pbar:
            # Use two fast and slow pointers to filter duplicate frame.
            slow, fast = 0, 1
            while fast + batch_size <= self.ocr_end:
                pbar.update(batch_size)

                slow_frame = self.vr[slow].asnumpy()[self.height-40:, :, :]

                batch_list = list(range(fast, fast+batch_size))
                fast_frames = self.vr.get_batch(batch_list).asnumpy()
                fast_frames = fast_frames[:, self.height-40:, :, :]

                compare_result = is_similar_batch(slow_frame, fast_frames,
                                                  threshold=0.95)
                batch_array = np.array(batch_list)
                not_similar_index = batch_array[np.logical_not(compare_result)]
                if not_similar_index.size == 0:
                    # All are similar with the slow frame.
                    if slow in self.key_point_dict:
                        self.key_point_dict[slow].extend(batch_list)
                    else:
                        self.key_point_dict[slow] = batch_list

                    fast += batch_size
                else:
                    # Exist the non similar frame.
                    slow = not_similar_index[0]
                    fast = slow + 1

                # Fix the left frame.
                if fast != self.ocr_end and fast + batch_size >= self.ocr_end:
                    batch_size = self.ocr_end - fast
                    pass

    def run_ocr(self, time_start, time_end, use_fullframe):
        self.ocr_start = get_frame_from_time(time_start, self.fps)

        if time_end == '0':
            self.ocr_end = self.num_frames - 1
        else:
            self.ocr_end = get_frame_from_time(time_end, self.fps)

        if self.ocr_end < self.ocr_start:
            raise ValueError('time_start is later than time_end')

        self.get_key_point()

        # Extract the filtered frames content.
        self.pred_frames = []
        key_index_frames = list(self.key_point_dict.keys())
        frames = self.vr.get_batch(key_index_frames).asnumpy()

        for key, frame in tqdm(list(zip(key_index_frames, frames)),
                               desc='Extract content'):
            if not use_fullframe:
                frame = frame[self.height * 4 // 5:, :, :]

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
