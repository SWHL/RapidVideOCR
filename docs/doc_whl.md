## rapid_videocr Package
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
</p>


### 1. Install package by pypi.
```bash
$ pip install rapid_videocr
```

### 2. Run by script.
```python
from rapid_videocr import ExtractSubtitle

extractor = ExtractSubtitle()
mp4_path = 'assets/test_video/2.mp4'
ocr_result = extractor(mp4_path)
print(ocr_result)
```

### 3. Run by command line.
```bash
$ rapid_videocr --mp4_path xxx.mp4 --format srt
```

### 4. Result.
- Return value.
    ```text
    [
        [0, '00:00:00,041', '00:00:00,416', '空间里面他绝对赢不了的'],
        [10, '00:00:00,458', '00:00:01,166', '我进去帮他'],
        [37, '00:00:01,583', '00:00:02,541', '你们接着善后']
    ]
    ```