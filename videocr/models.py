
from typing import List

from fuzzywuzzy import fuzz


class PredictedFrame:
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


class PredictedSubtitle:
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
