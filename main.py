# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import time
import yaml

from rapid_videocr import ExtractSubtitle
from rapid_ocr import TextSystem


def read_yaml(yaml_path):
    with open(yaml_path, 'rb') as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data


if __name__ == '__main__':
    ocr_system = TextSystem('config_ocr.yaml')

    config = read_yaml('config_videocr.yaml')
    extractor = ExtractSubtitle(ocr_system, **config)

    mp4_path = 'assets/test_video/2.mp4'
    time_start = '00:00:00'
    time_end = '-1'

    start_time = time.time()
    ocr_result = extractor(mp4_path, time_start, time_end)
    print(ocr_result)
    print(f'elapse: {time.time() - start_time}s')
