# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import os

from pydub import AudioSegment

# os.putenv('PATH', r'E:\Program Files\ffmpeg-n5.0-latest-win64-lgpl-shared-5.0\bin')

mp4_path = 'assets/test_video/2.mp4'
audio = AudioSegment.from_file(mp4_path, 'mp4')

# 毫秒
start = 458
end = 1166

part = audio[start:end]

part.export('1.mp3', format='mp3')
