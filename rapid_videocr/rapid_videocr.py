
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
import random
import tempfile

import cv2
import numpy as np
from decord import VideoReader, cpu
from pydub import AudioSegment
from tqdm import tqdm

from .utils import (get_frame_from_time, get_srt_timestamp, is_similar_batch,
                    remove_batch_bg, remove_bg, string_similar,
                    save_docx, save_srt, save_txt)


class ExtractSubtitle(object):
    def __init__(self, ocr_system, subtitle_height=None,
                 error_num=0.1, output_format='srt', text_det=None,
                 asr_executor=None, is_dilate=True):
        self.ocr_system = ocr_system
        self.text_det = text_det

        self.asr_executor = asr_executor

        self.error_num = error_num
        self.output_format = output_format
        self.is_dilate = is_dilate
        self.subtitle_height = subtitle_height

    def __call__(self, video_path, time_start, time_end, batch_size):
        self.video_path = video_path

        print(f'Loading {video_path}')
        self.vr = VideoReader(video_path, ctx=cpu(0))

        if self.asr_executor is not None:
            self.audio = AudioSegment.from_file(
                video_path, 'mp4').set_frame_rate(16000)
        else:
            self.audio = None

        self.num_frames = len(self.vr)
        self.fps = int(self.vr.get_avg_fps())

        self.height = int(self.vr[0].shape[0])
        if self.subtitle_height is None:
            self.get_subtitle_height()
        else:
            self.subtitle_height = self.subtitle_height
            print(f'Manual setting subtitle height: {self.subtitle_height}')
        self.crop_h = self.height - self.subtitle_height

        if batch_size is None:
            self.batch_size = self.fps * 2
        else:
            self.batch_size = batch_size

        self.run_ocr(time_start, time_end)
        return self.get_subtitles()

    def get_subtitle_height(self):
        # 随机挑选几帧做文本检测，确定文本高度
        print('Auto set the subtitle height....')
        if self.text_det is not None:
            random_index = random.choices(range(len(self.vr)), k=5)
            frames = self.vr.get_batch(random_index).asnumpy()
            subtitle_h_list = []
            for i, one_frame in enumerate(frames):
                dt_boxes, _ = self.text_det(one_frame)

                # Debug
                # for box in dt_boxes:
                #     box = np.array(box).astype(np.int32).reshape(-1, 2)
                #     cv2.polylines(one_frame, [box], True,
                #                 color=(255, 255, 0), thickness=2)
                # cv2.imwrite(f'temp/{i}.jpg', one_frame)

                if dt_boxes.size > 0 and dt_boxes is not None:
                    middle_h = int(self.height / 2)
                    mask = np.where(dt_boxes[:, 0, 1] > middle_h, True, False)
                    dt_boxes = dt_boxes[mask]

                    if dt_boxes.size > 0:
                        max_h = np.max(np.max(dt_boxes[:, :, 1], axis=1)
                                       - np.min(dt_boxes[:, :, 1], axis=1))
                        bottom_margin = self.height - np.max(dt_boxes[:, :, 1])
                        subtitle_h_list.append(int(max_h + 2 * bottom_margin))

            if len(subtitle_h_list) > 0 and not self.is_dilate:
                self.subtitle_height = int(np.max(subtitle_h_list)) * 2
            else:
                self.subtitle_height = 152
        else:
            self.subtitle_height = 152
        print(f'The subtitle value: {self.subtitle_height}')

    def record_info(self, slow, duplicate_frame, slow_frame):
        # Record
        if slow in self.key_point_dict:
            self.key_point_dict[slow].extend(duplicate_frame)
        else:
            self.key_point_dict[slow] = duplicate_frame

        if slow not in self.key_frames.keys():
            self.key_frames[slow] = slow_frame

    def get_key_frame(self):
        self.key_point_dict = {}
        self.key_frames = {}

        with tqdm(total=self.ocr_end, desc='Get the key frame') as pbar:
            # Use two fast and slow pointers to filter duplicate frame.
            if self.batch_size > self.ocr_end:
                self.batch_size = self.ocr_end - 1

            slow, fast = 0, 1
            while fast + self.batch_size <= self.ocr_end:
                slow_frame = self.vr[slow].asnumpy()[self.crop_h:, :, :]

                # Remove the background of the frame.
                slow_frame = remove_bg(slow_frame, is_dilate=self.is_dilate)

                batch_list = list(range(fast, fast+self.batch_size))
                fast_frames = self.vr.get_batch(batch_list).asnumpy()
                fast_frames = fast_frames[:, self.crop_h:, :, :]

                fast_frames = remove_batch_bg(fast_frames,
                                              is_dilate=self.is_dilate)
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

                    self.record_info(slow, duplicate_frame, slow_frame)
                else:
                    # Exist the non similar frame.
                    index = not_similar_index[0] - slow
                    duplicate_frame = batch_list[:index]

                    # record
                    self.record_info(slow, duplicate_frame, slow_frame)

                    slow = not_similar_index[0]
                    fast = slow + 1
                    pbar.update(slow - pbar.n + 1)

                # Take care the left frames, which can't up to the batch_size.
                if fast != self.ocr_end \
                        and fast + self.batch_size > self.ocr_end:
                    self.batch_size = self.ocr_end - fast

    def run_ocr(self, time_start, time_end):
        self.ocr_start = get_frame_from_time(time_start, self.fps)

        if time_end == '-1':
            self.ocr_end = self.num_frames - 1
        else:
            self.ocr_end = get_frame_from_time(time_end, self.fps)

        if self.ocr_end < self.ocr_start:
            raise ValueError('time_start is later than time_end')

        self.get_key_frame()

        # Extract the filtered frames content.
        self.pred_frames = []
        key_index_frames = list(self.key_point_dict.keys())
        frames = np.stack(list(self.key_frames.values()), axis=0)

        # i = 0
        for key, frame in tqdm(list(zip(key_index_frames, frames)),
                               desc='Extract content'):
            frame = cv2.copyMakeBorder(frame.squeeze(),
                                       self.subtitle_height * 2,
                                       self.subtitle_height * 2,
                                       0, 0,
                                       cv2.BORDER_CONSTANT,
                                       value=(0, 0))
            frame = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_GRAY2BGR)
            # Debug
            # cv2.imwrite(f'temp/key_frame/{i}.jpg', frame)
            # i += 1

            _, rec_res = self.ocr_system(frame)

            if rec_res is None or len(rec_res) <= 0:
                del self.key_point_dict[key]
            else:
                text, confidence = list(zip(*rec_res))
                text = '\n'.join(text)
                confidence = sum(confidence) / len(confidence)
                self.pred_frames.append((text, confidence))

    def get_subtitles(self):
        slow, fast = 0, 1
        n = len(self.pred_frames)
        key_list = list(self.key_point_dict.keys())
        invalid_keys = []
        while fast < n:
            if string_similar(self.pred_frames[slow][0],
                              self.pred_frames[fast][0]) > 0.6:
                # 相似→合并两个list
                self.key_point_dict[key_list[slow]].extend(
                    self.key_point_dict[key_list[fast]])
                self.key_point_dict[key_list[slow]].sort()
                invalid_keys.append(fast)
            else:
                # 不相似
                slow = fast
            fast += 1

        [self.key_point_dict.pop(key_list[i]) for i in invalid_keys]
        self.pred_frames = [v for i, v in enumerate(self.pred_frames)
                            if i not in invalid_keys]

        self.extract_result = []
        asr_result = []
        for i, (k, v) in enumerate(self.key_point_dict.items()):
            start_index, start_seconds = get_srt_timestamp(v[0], self.fps)
            end_index, end_seconds = get_srt_timestamp(v[-1], self.fps)

            # asr识别
            if self.asr_executor is not None:
                print('asr rec...')

                clip_audio = self.audio[start_seconds:end_seconds]
                with tempfile.TemporaryDirectory() as tmp_dir_name:
                    wav_tmp_path = str(Path(tmp_dir_name) / f'{i}.wav')

                    clip_audio.export(wav_tmp_path, format='wav')

                    text = self.asr_executor(audio_file=wav_tmp_path)

                    asr_result.append(text)

            self.extract_result.append([k, start_index,
                                        end_index, self.pred_frames[i][0]])
        self.save_output()
        return self.extract_result, asr_result

    def save_output(self):
        if self.output_format == 'srt':
            save_srt(self.video_path, self.extract_result)
        elif self.output_format == 'txt':
            save_txt(self.video_path, self.extract_result)
        elif self.output_format == 'docx':
            save_docx(self.video_path, self.extract_result, self.vr)
        elif self.output_format == 'all':
            save_srt(self.video_path, self.extract_result)
            save_txt(self.video_path, self.extract_result)
            save_docx(self.video_path, self.extract_result, self.vr)
        else:
            raise ValueError(f'The {self.output_format} is not supported!')