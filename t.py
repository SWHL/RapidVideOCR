# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from tqdm import tqdm

from pathlib import Path


a = Path('test_files/RGBImages').rglob('*.*')

for i in tqdm(a, desc='ddd'):
    pass
