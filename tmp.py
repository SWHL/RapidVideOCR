# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import os

from pydub import AudioSegment

# os.putenv('PATH', r'E:\Program Files\ffmpeg-n5.0-latest-win64-lgpl-shared-5.0\bin')

mp4_path = 'assets/test_video/2.mp4'
audio = AudioSegment.from_file(mp4_path, 'mp4').set_frame_rate(16000)

# 毫秒
start = 1583
end = 2541

part = audio[start:end]

part.export('1.wav', format='wav')
