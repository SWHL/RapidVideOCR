
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import random
import platform

import cv2
import numpy as np
from decord import VideoReader, cpu
from tqdm import tqdm

from .utils import (debug_vis_box, get_frame_from_time, get_srt_timestamp,
                    is_similar_batch, remove_batch_bg, remove_bg,
                    string_similar, save_docx, save_srt, save_txt, vis_binary)


class ExtractSubtitle(object):
    def __init__(self, ocr_system, subtitle_height=152,
                 error_num=0.1, output_format='srt', text_det=None,
                 is_dilate=True, is_select_threshold=False):
        self.ocr_system = ocr_system
        self.text_det = text_det

        self.error_num = error_num
        self.output_format = output_format
        self.is_dilate = is_dilate
        self.subtitle_height = subtitle_height
        self.is_select_threshold = is_select_threshold

    def __call__(self, video_path, time_start, time_end, batch_size):
        self.video_path = video_path

        print(f'Loading {video_path}')
        self.vr = VideoReader(video_path, ctx=cpu(0))

        self.num_frames = len(self.vr)
        self.fps = int(self.vr.get_avg_fps())

        self.height = int(self.vr[0].shape[0])

        if self.subtitle_height is None:
            self.get_subtitle_height()
        else:
            print(f'Manual setting subtitle height: {self.subtitle_height}')

        self.crop_h = self.height - self.subtitle_height

        # 交互式确定threshold最佳值，仅仅限于Windows系统
        if platform.system() == 'Windows' and self.is_select_threshold:
            self.binary_threshold = self.select_threshold()
            print(f'The binary threshold: {self.binary_threshold}')
        else:
            print('Using the default value: 243')
            self.binary_threshold = 243

        if batch_size is None:
            self.batch_size = self.fps * 2
        else:
            self.batch_size = batch_size

        self.run_ocr(time_start, time_end)

        return self.get_subtitles()

    def get_subtitle_height(self):
        """随机挑选几帧做文本检测，确定字幕高度"""

        print('Auto set the subtitle height....')
        if self.text_det is not None:
            random_index = random.choices(range(len(self.vr)), k=5)
            frames = self.vr.get_batch(random_index).asnumpy()
            subtitle_h_list = []
            for i, one_frame in enumerate(frames):
                dt_boxes, _ = self.text_det(one_frame)

                if dt_boxes is not None and dt_boxes.size > 0:
                    middle_h = int(self.height / 4)
                    mask = np.where(dt_boxes[:, 0, 1] > middle_h, True, False)
                    filter_dt_boxes = dt_boxes[mask]
                    if filter_dt_boxes.size <= 0:
                        continue

                    # Debug
                    # debug_vis_box(i, filter_dt_boxes, one_frame)

                    # 字幕中最高的距离
                    all_y = filter_dt_boxes[:, :, 1]
                    max_h = np.max(np.max(all_y, axis=1) - np.min(all_y, axis=1))

                    # 最下面字幕距离图像最底部的距离
                    bottom_margin = self.height - np.max(all_y)

                    # max_h + bottom_margin: 字幕+字幕距图像最下面的距离
                    if filter_dt_boxes.shape[0] > 1:
                        # 说明可能是两行字幕
                        subtitle_h_list.append(int(2 * max_h
                                                   + 2 * bottom_margin))
                    else:
                        # 单行字幕
                        subtitle_h_list.append(int(max_h + 2 * bottom_margin))

            if len(subtitle_h_list) > 0:
                self.subtitle_height = int(np.min(subtitle_h_list))
            else:
                self.subtitle_height = 152
        else:
            self.subtitle_height = 152

        print(f'The subtitle value: {self.subtitle_height}')

    def _record_key_info(self, slow, duplicate_frame, slow_frame):
        if slow in self.key_point_dict:
            self.key_point_dict[slow].extend(duplicate_frame)
        else:
            self.key_point_dict[slow] = duplicate_frame

        if slow not in self.key_frames.keys():
            self.key_frames[slow] = slow_frame

    def get_key_frame(self):
        """获得视频的字幕关键帧"""

        self.key_point_dict = {}
        self.key_frames = {}

        with tqdm(total=self.ocr_end,
                  desc='Obtain key frame', unit='frame') as pbar:
            # Use two fast and slow pointers to filter duplicate frame.
            if self.batch_size > self.ocr_end:
                self.batch_size = self.ocr_end - 1

            slow, fast = 0, 1
            slow_change = True
            while fast + self.batch_size <= self.ocr_end:
                if slow_change:
                    ori_slow_frame = self.vr[slow].asnumpy()[self.crop_h:, :, :]

                    # Remove the background of the frame.
                    slow_frame = remove_bg(ori_slow_frame,
                                           is_dilate=self.is_dilate,
                                           binary_thr=self.binary_threshold)

                    slow_change = False

                batch_list = list(range(fast, fast+self.batch_size))
                fast_frames = self.vr.get_batch(batch_list).asnumpy()
                fast_frames = fast_frames[:, self.crop_h:, :, :]

                fast_frames = remove_batch_bg(fast_frames,
                                              is_dilate=self.is_dilate,
                                              binary_thr=self.binary_threshold)

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

                    self._record_key_info(slow, duplicate_frame, ori_slow_frame)
                else:
                    # Exist the non similar frame.
                    index = not_similar_index[0] - slow
                    duplicate_frame = batch_list[:index]

                    # record
                    self._record_key_info(slow, duplicate_frame, ori_slow_frame)

                    slow = not_similar_index[0]
                    fast = slow + 1
                    pbar.update(slow - pbar.n + 1)

                    slow_change = True

                # Take care the left frames, which can't up to the batch_size.
                if fast != self.ocr_end \
                        and fast + self.batch_size > self.ocr_end:
                    self.batch_size = self.ocr_end - fast

    def run_ocr(self, time_start, time_end):
        """对所给字幕图像进行OCR识别

        :param time_start: 起始时间点
        :param time_end: 结束时间点，-1表示到最后
        """

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

        for key, frame in tqdm(list(zip(key_index_frames, frames)),
                               desc='OCR Key Frame', unit='frame'):
            frame = cv2.copyMakeBorder(frame.squeeze(),
                                       self.subtitle_height * 2,
                                       self.subtitle_height * 2,
                                       0, 0,
                                       cv2.BORDER_CONSTANT,
                                       value=(0, 0))

            _, rec_res = self.ocr_system(frame)

            if rec_res is None or len(rec_res) <= 0:
                del self.key_point_dict[key]
            else:
                text, confidence = list(zip(*rec_res))
                text = '\n'.join(text)
                confidence = sum(confidence) / len(confidence)
                self.pred_frames.append((text, confidence))

    def get_subtitles(self):
        """合并最终OCR提取字幕文件，并输出
        """

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
        for i, (k, v) in enumerate(self.key_point_dict.items()):
            start_index, _ = get_srt_timestamp(v[0], self.fps)
            end_index, _ = get_srt_timestamp(v[-1], self.fps)

            self.extract_result.append([k, start_index,
                                        end_index,
                                        self.pred_frames[i][0]])
        self._save_output()
        return self.extract_result

    def _save_output(self):
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

    def select_threshold(self):
        """交互式选择二值化字幕阈值"""
        random_index = random.choices(range(len(self.vr)), k=3)
        frames = self.vr.get_batch(random_index).asnumpy()

        threshold_list = []
        for i, frame in enumerate(frames):
            crop_img = frame[self.crop_h:, :, :]

            if i == 0:
                threshold = vis_binary(i + 1, crop_img)
            else:
                threshold = vis_binary(i + 1, crop_img,
                                              threshold_list[-1])

            threshold_list.append(threshold)
        return np.max(threshold_list)
