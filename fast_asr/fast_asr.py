# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
# From
from pathlib import Path

import fastasr
import soundfile as sf

cur_dir = Path(__file__).resolve().parent


class FastASR():
    def __init__(self,
                 model_path=str(cur_dir / 'k2_rnnt2_cli')) -> None:
        self.model = fastasr.Model(model_path, 2)

    def __call__(self, audio_path: str) -> str:
        data, sample_rate = sf.read(audio_path)
        self.model.reset()
        asr_result = self.model.forward(data)
        return asr_result
