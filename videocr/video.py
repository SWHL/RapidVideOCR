
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import numpy as np
from decord import VideoReader, cpu
from tqdm import tqdm

from .utils import (get_frame_from_time, get_srt_timestamp, is_similar_batch,
                    remove_batch_bg, remove_bg)


class Video(object):
    def __init__(self,
                 video_path,
                 ocr_system,
                 batch_size=None,
                 subtitle_height=45,
                 error_num=0.1):
        self.video_path = video_path
        self.ocr_system = ocr_system
        self.error_num = error_num

        print(f'Loading {self.video_path}')
        self.vr = VideoReader(self.video_path, ctx=cpu(0))
        self.num_frames = len(self.vr)
        self.fps = int(self.vr.get_avg_fps())

        self.height = int(self.vr[0].shape[0])
        self.subtitle_height = subtitle_height
        self.crop_h = self.height - self.subtitle_height

        if batch_size is None:
            self.batch_size = self.fps * 2
        else:
            self.batch_size = batch_size

    def get_key_point(self):
        self.key_point_dict = {}
        self.key_frames = {}
        with tqdm(total=self.ocr_end, desc='Get the key point') as pbar:
            # Use two fast and slow pointers to filter duplicate frame.
            slow, fast = 0, 1
            if self.batch_size > self.ocr_end:
                self.batch_size = self.ocr_end - 1
            while fast + self.batch_size <= self.ocr_end:
                slow_frame = self.vr[slow].asnumpy()[self.crop_h:, :, :]

                batch_list = list(range(fast, fast+self.batch_size))
                fast_frames = self.vr.get_batch(batch_list).asnumpy()
                fast_frames = fast_frames[:, self.crop_h:, :, :]

                # Remove the background of the frame.
                slow_frame = remove_bg(slow_frame)
                fast_frames = remove_batch_bg(fast_frames)

                # Compare the similarity between the frames.
                compare_result = is_similar_batch(slow_frame,
                                                  fast_frames,
                                                  threshold=self.error_num)
                batch_array = np.array(batch_list)
                not_similar_index = batch_array[np.logical_not(compare_result)]

                duplicate_frame = []
                if not_similar_index.size == 0:
                    # All are similar with the slow frame.
                    duplicate_frame = batch_list

                    pbar.update(self.batch_size)
                    fast += self.batch_size
                else:
                    # Exist the non similar frame.
                    index = not_similar_index[0] - slow
                    duplicate_frame = batch_list[:index]

                    slow = not_similar_index[0]
                    fast = slow + 1
                    pbar.update(slow - pbar.n + 1)

                # Record
                if slow in self.key_point_dict:
                    self.key_point_dict[slow].extend(duplicate_frame)
                else:
                    self.key_point_dict[slow] = duplicate_frame

                if slow not in self.key_frames.keys():
                    self.key_frames[slow] = slow_frame

                # Take care the left frames, which can't up to the batch_size.
                if fast != self.ocr_end \
                        and fast + self.batch_size > self.ocr_end:
                    self.batch_size = self.ocr_end - fast

    def run_ocr(self, time_start, time_end):
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
        frames = np.stack(list(self.key_frames.values()), axis=0)

        i = 0
        import cv2
        for key, frame in tqdm(list(zip(key_index_frames, frames)),
                               desc='Extract content'):
            frame = cv2.copyMakeBorder(frame.squeeze(),
                                       self.subtitle_height * 2,
                                       self.subtitle_height * 2,
                                       0, 0,
                                       cv2.BORDER_CONSTANT,
                                       value=(0, 0))
            cv2.imwrite(f'temp/{i}.jpg', frame)
            frame = np.expand_dims(frame, axis=2)
            frame = np.concatenate([frame, frame, frame], axis=-1)
            _, rec_res = self.ocr_system(frame, i)

            if rec_res is None or len(rec_res) <= 0:
                del self.key_point_dict[key]
            else:
                text, confidence = list(zip(*rec_res))
                text = '\n'.join(text)
                confidence = sum(confidence) / len(confidence)
                self.pred_frames.append((text, confidence))
            i += 1

    def get_subtitles(self):
        result = []
        for i, v in enumerate(self.key_point_dict.values()):
            start_index = get_srt_timestamp(v[0], self.fps)
            end_index = get_srt_timestamp(v[-1], self.fps)
            result.append(
                f'{i}  {start_index} -> {end_index} : {self.pred_frames[i][0]}')
        return result
