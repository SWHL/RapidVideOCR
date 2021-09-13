# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from .video import Video


def get_subtitles(video_path: str,
                  ocr_system,
                  time_start='0:00',
                  time_end='',
                  conf_threshold=65,
                  sim_threshold=90,
                  use_fullframe=False) -> str:

    v = Video(video_path, ocr_system)
    v.run_ocr(time_start, time_end,
              conf_threshold, use_fullframe)
    return v.get_subtitles(sim_threshold)


def save_subtitles_to_file(video_path: str,
                           file_path='subtitle.srt',
                           time_start='0:00',
                           time_end='',
                           conf_threshold=65,
                           sim_threshold=90,
                           use_fullframe=False) -> None:
    with open(file_path, 'w+', encoding='utf-8') as f:
        f.write(get_subtitles(
            video_path, time_start, time_end, conf_threshold,
            sim_threshold, use_fullframe))
