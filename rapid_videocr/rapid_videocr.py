
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import random
from pathlib import Path

import cv2
import psutil
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from tqdm import tqdm

from .utils import (VideoReader, get_frame_from_time, get_srt_timestamp, is_similar_batch,
                    read_yaml, remove_batch_bg, remove_bg, save_docx, save_srt,
                    save_txt, string_similar, vis_binary)

CUR_DIR = Path(__file__).resolve().parent


def get_used_memory():
    mem = psutil.virtual_memory()
    return mem.used / 1024 / 1024 / 1024


class ExtractSubtitle():
    def __init__(self, output_format=None,
                 config_path=str(CUR_DIR / 'config_videocr.yaml')):
        self.ocr_system = RapidOCR()
        self.text_det = self.ocr_system.text_detector

        config = read_yaml(config_path)
        self.error_num = config['error_num']
        if output_format:
            self.output_format = output_format
        else:
            self.output_format = config['output_format']

        self.is_dilate = config['is_dilate']

        self.select_nums = 3
        self.time_start = config['time_start']
        self.time_end = config['time_end']

    def __call__(self, video_path, batch_size=100):
        self.video_path = video_path
        print(f'Loading {video_path}')
        self.vr = VideoReader(video_path)

        self.num_frames = self.vr.get_frame_count()
        self.fps = int(self.vr.get_avg_fps())

        self.random_index = random.choices(range(self.num_frames),
                                           k=self.select_nums)
        self.selected_frames = self.vr.get_batch(self.random_index)

        # 选择字幕区域
        roi_array = self._select_roi()
        self.crop_start = np.min(roi_array[:, 1])
        self.subtitle_height = np.max(roi_array[:, 3])
        self.crop_end = self.crop_start + self.subtitle_height

        # 交互式确定threshold最佳值
        self.binary_threshold = self._select_threshold()
        print(f'The binary threshold: {self.binary_threshold}')

        if batch_size is None:
            self.batch_size = self.fps * 2
        else:
            self.batch_size = batch_size

        self.run_ocr(self.time_start, self.time_end)

        return self.get_subtitles()

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

        import time
        s = time.time()
        self.get_key_frame()
        print(f'get key frame cost: {time.time() - s}')

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

            rec_res = []
            confidence = [0.0]
            ocr_result, _ = self.ocr_system(frame)
            if ocr_result:
                _, rec_res, confidence = list(zip(*ocr_result))
                confidence = list(map(float, confidence))

            if not rec_res:
                del self.key_point_dict[key]

            text = '\n'.join(rec_res)
            confidence = sum(confidence) / len(confidence)
            self.pred_frames.append((text, confidence))

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
                    ori_slow_frame = self.vr[slow][self.crop_start: self.crop_end, :, :]

                    # Remove the background of the frame.
                    slow_frame = remove_bg(ori_slow_frame,
                                           is_dilate=self.is_dilate,
                                           binary_thr=self.binary_threshold)

                    slow_change = False

                batch_list = list(range(fast, fast+self.batch_size))
                fast_frames = self.vr.get_batch(batch_list)
                fast_frames = fast_frames[:, self.crop_start: self.crop_end, :, :]

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
                if fast != self.ocr_end \
                        and fast + self.batch_size > self.ocr_end:
                    self.batch_size = self.ocr_end - fast

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

        _ = [self.key_point_dict.pop(key_list[i]) for i in invalid_keys]
        self.pred_frames = [v for i, v in enumerate(self.pred_frames)
                            if i not in invalid_keys]

        self.extract_result = []
        for i, (k, v) in enumerate(self.key_point_dict.items()):
            start_index, start_seconds = get_srt_timestamp(v[0], self.fps)
            end_index, end_seconds = get_srt_timestamp(v[-1], self.fps)
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

    def _select_roi(self):
        roi_list = []
        for i, frame in enumerate(self.selected_frames):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.selectROI(
                f'[{i+1}/{self.select_nums}] Select a ROI and then press SPACE or ENTER button! Cancel the selection process by pressing c button!',
                frame, True, False)
            if sum(roi) > 0:
                roi_list.append(list(roi))
        cv2.destroyAllWindows()
        return np.array(roi_list)

    def _select_threshold(self):
        threshold_list = []
        for i, frame in enumerate(self.selected_frames):
            crop_img = frame[self.crop_start: self.crop_end, :, :]
            if i == 0:
                threshold = vis_binary(i + 1, crop_img)
            else:
                threshold = vis_binary(i + 1, crop_img,
                                       threshold_list[-1])

            threshold_list.append(threshold)
        return np.max(threshold_list)

    def _record_key_info(self, slow, duplicate_frame, slow_frame):
        if slow in self.key_point_dict:
            self.key_point_dict[slow].extend(duplicate_frame)
        else:
            self.key_point_dict[slow] = duplicate_frame

        if slow not in self.key_frames:
            self.key_frames[slow] = slow_frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mp4_path', type=str)
    parser.add_argument('--format', choices=['srt', 'txt', 'docx', 'all'],
                        default='srt')
    args = parser.parse_args()

    mp4_path = args.mp4_path
    if not Path(mp4_path).exists():
        raise FileExistsError(f'{mp4_path} does not exists.')

    extractor = ExtractSubtitle(output_format=args.format)
    ocr_result = extractor(mp4_path)
    print(ocr_result)


if __name__ == '__main__':
    main()
