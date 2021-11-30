
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from typing import List
from fuzzywuzzy import fuzz
import multiprocessing

import cv2
from tqdm import tqdm

from . import utils


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

    def __init__(self, frames: List[PredictedFrame], sim_threshold: int):
        self.frames = [f for f in frames if f.confidence > 0]
        self.sim_threshold = sim_threshold

        if self.frames:
            self.text = max(self.frames, key=lambda f: f.confidence).text
        else:
            self.text = ''

    @property
    def index_start(self) -> int:
        if self.frames:
            return self.frames[0].index
        return 0

    @property
    def index_end(self) -> int:
        if self.frames:
            return self.frames[-1].index
        return 0

    def is_similar_to(self, other) -> bool:
        return fuzz.partial_ratio(self.text, other.text) >= self.sim_threshold

    def __repr__(self):
        return '{} - {}. {}'.format(self.index_start, self.index_end, self.text)


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
                conf_threshold: int, use_fullframe: bool) -> None:
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
        # with Capture(self.path) as v, multiprocessing.Pool() as pool:
        with Capture(self.path) as v, multiprocessing.Pool() as pool:
            v.set(cv2.CAP_PROP_POS_FRAMES, ocr_start)
            frames = (v.read()[1] for _ in range(num_ocr_frames))

            # perform ocr to frames in parallel
            it_ocr = pool.imap(self._image_to_data, frames, chunksize=10)
            self.pred_frames = [
                PredictedFrame(i + ocr_start, data, conf_threshold)
                for i, data in enumerate(it_ocr)
            ]

        # with Capture(self.path) as v:
        #     v.set(cv2.CAP_PROP_POS_FRAMES, ocr_start)
        #     frames = [v.read()[1] for _ in range(0, num_ocr_frames)]
        #     print(f'Obtain frame nums: {len(frames)}')

        #     it_ocr = []
        #     for i, frame in enumerate(tqdm(frames, desc='Extract')):
        #         dt_boxes, rec_res = self._image_to_data(frame)
        #         filter_result = self.filter_rec(dt_boxes, rec_res)
        #         if all(filter_result):
        #             print(f'{i}\t{filter_result[1]}')
        #             it_ocr.append(filter_result[1])

        #     # it_ocr = pool.imap(self._image_to_data, frames, chunksize=10)
        #     self.pred_frames = [
        #         PredictedFrame(i + ocr_start, data, conf_threshold)
        #         for i, data in enumerate(it_ocr) if data is not None
        #     ]

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

        # divide ocr of frames into subtitle paragraphs using sliding window
        WIN_BOUND = int(self.fps // 2)  # 1/2 sec sliding window boundary
        bound = WIN_BOUND
        i, j = 0, 1
        while j < len(self.pred_frames):
            fi, fj = self.pred_frames[i], self.pred_frames[j]

            if fi.is_similar_to(fj):
                bound = WIN_BOUND
            elif bound > 0:
                bound -= 1
            else:
                # divide subtitle paragraphs
                para_new = j - WIN_BOUND
                self._append_sub(PredictedSubtitle(
                    self.pred_frames[i:para_new], sim_threshold))
                i = para_new
                j = i
                bound = WIN_BOUND

            j += 1

        # also handle the last remaining frames
        if i < len(self.pred_frames) - 1:
            self._append_sub(PredictedSubtitle(
                self.pred_frames[i:], sim_threshold))

    def _append_sub(self, sub: PredictedSubtitle) -> None:
        if len(sub.text) == 0:
            return

        # merge new sub to the last subs if they are similar
        while self.pred_subs and sub.is_similar_to(self.pred_subs[-1]):
            ls = self.pred_subs[-1]
            del self.pred_subs[-1]
            sub = PredictedSubtitle(ls.frames + sub.frames, sub.sim_threshold)

        self.pred_subs.append(sub)
