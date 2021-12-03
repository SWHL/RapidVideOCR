
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import copy
import sys
from typing import List

import cv2
from fuzzywuzzy import fuzz
from tqdm import tqdm

from . import utils
from .utils import is_similar


class PredictedFrame(object):
    index: int  # 0-based index of the frame
    confidence: int  # total confidence of all words
    text: str

    def __init__(self, index: int, pred_data: str,
                 conf_threshold: int):
        self.index = index
        self.words = []
        self.confidence = []

        for info in pred_data:
            if info is not None:
                text, score = info
                if score >= conf_threshold:
                    self.words.append(text)
                    self.confidence.append(score)

        self.confidence = sum(self.confidence)
        self.text = '\n'.join(self.words)

    def is_similar_to(self, other, threshold=70) -> bool:
        return fuzz.ratio(self.text, other.text) >= threshold


class PredictedSubtitle(object):
    frames: List[PredictedFrame]
    sim_threshold: int
    text: str

    def __init__(self, frames: List[PredictedFrame],
                 frames_list,
                 sim_threshold: int):
        self.frames = [f for f in [frames] if f.confidence > 0]
        self.sim_threshold = sim_threshold
        self.frames_list = frames_list

        if self.frames:
            self.text = max(self.frames, key=lambda f: f.confidence).text
        else:
            self.text = ''

    @property
    def index_start(self) -> int:
        if self.frames_list:
            return self.frames_list[0]
        return 0

    @property
    def index_end(self) -> int:
        if self.frames_list:
            return self.frames_list[-1]
        return 0

    def is_similar_to(self, other) -> bool:
        return fuzz.partial_ratio(
            self.text, other.text) >= self.sim_threshold

    def __repr__(self):
        return '{} - {}. {}'.format(
            self.index_start, self.index_end, self.text)


class Capture(object):
    def __init__(self, video_path):
        self.path = video_path

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.path)
        if not self.cap.isOpened():
            raise IOError('Can not open video {}.'.format(self.path))
        return self.cap

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()


class Video(object):
    path: str
    lang: str
    use_fullframe: bool
    num_frames: int
    fps: float
    height: int
    pred_frames: List[PredictedFrame]
    pred_subs: List[PredictedSubtitle]

    def __init__(self, path: str, ocr_system):
        self.path = path
        self.ocr_system = ocr_system

        print('Init Video instance')
        with Capture(path) as v:
            self.num_frames = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = v.get(cv2.CAP_PROP_FPS)
            self.height = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # self.threshold_y = self.height - self.height // 3

    def run_ocr(self, time_start: str, time_end: str,
                conf_threshold: int, use_fullframe: bool):
        self.use_fullframe = use_fullframe

        if time_start:
            ocr_start = utils.get_frame_index(time_start, self.fps)
        else:
            ocr_start = 0

        if time_end:
            ocr_end = utils.get_frame_index(time_end, self.fps)
        else:
            ocr_end = self.num_frames

        if ocr_end < ocr_start:
            raise ValueError('time_start is later than time_end')
        num_ocr_frames = ocr_end - ocr_start

        # get frames from ocr_start to ocr_end
        with Capture(self.path) as v:
            v.set(cv2.CAP_PROP_POS_FRAMES, ocr_start)
            frames = [v.read()[1] for _ in range(0, num_ocr_frames)]
            print(f'Obtain frame nums: {len(frames)}')

        # 计算相邻两帧的相似度，如果十分相似，则予以丢弃
        print('Get the key point frame...')
        slow, fast = 0, 0
        n = len(frames)
        self.key_point_dict = {}
        while fast < n:
            a = frames[slow][self.height - 40:, :]
            b = frames[fast][self.height - 40:, :]
            if is_similar(a, b, threshold=0.95):
                if slow in self.key_point_dict:
                    self.key_point_dict[slow].append(fast)
                else:
                    self.key_point_dict[slow] = [slow]
            else:
                slow = fast
            fast += 1

        it_ocr = []
        temp_key_point = copy.deepcopy(self.key_point_dict)
        for key in tqdm(temp_key_point.keys(), desc='Extract'):
            frame = frames[key]
            dt_boxes, rec_res = self._image_to_data(frame)
            filter_result = self.filter_rec(dt_boxes, rec_res)
            if all(filter_result):
                print(f'{key}\t{filter_result[1]}')
                it_ocr.append(filter_result[1])
            else:
                del self.key_point_dict[key]

        self.pred_frames = [
            PredictedFrame(i + ocr_start, data, conf_threshold)
            for i, data in enumerate(it_ocr) if data is not None
        ]

    def _image_to_data(self, img):
        if not self.use_fullframe:
            img = img[self.height * 4 // 5:, :]

        try:
            dt_boxes, rec_res = self.ocr_system(img)
            return dt_boxes, rec_res
        except Exception as e:
            sys.exit('{}: {}'.format(e.__class__.__name__, e))

    def filter_rec(self, dt_box, one_rec):
        if one_rec is not None \
                and dt_box is not None \
                and len(dt_box) > 0:
            return dt_box, one_rec
        else:
            return None, None

    def get_subtitles(self, sim_threshold: int) -> str:
        self._generate_subtitles(sim_threshold)
        result = []
        for i, sub in enumerate(self.pred_subs):
            start_index = utils.get_srt_timestamp(sub.index_start, self.fps)
            end_index = utils.get_srt_timestamp(sub.index_end, self.fps)
            result.append(f'{i}\n{start_index} --> {end_index}\n{sub.text}\n')
        return ''.join(result)

    def _generate_subtitles(self, sim_threshold: int) -> None:
        self.pred_subs = []

        if self.pred_frames is None:
            raise AttributeError(
                'Please call self.run_ocr() first to perform ocr on frames')

        for i, (k, v) in enumerate(self.key_point_dict.items()):
            self.pred_subs.append(PredictedSubtitle(self.pred_frames[i], v,
                                                    sim_threshold))
