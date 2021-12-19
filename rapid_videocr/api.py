# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from .video import Video


def get_subtitles(video_path: str,
                  ocr_system,
                  batch_size=24,
                  subtitle_height=45,
                  time_start='0:00',
                  time_end='',
                  error_num=0.1,
                  output_format='srt',
                  text_det=None,
                  is_dilate=False):

    v = Video(video_path, ocr_system, batch_size, subtitle_height,
              error_num, output_format, text_det, is_dilate)
    v.run_ocr(time_start, time_end)
    return v.get_subtitles()

