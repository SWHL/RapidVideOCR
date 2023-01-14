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
- RapidVideOCR has the default `out_format`, which is one of `['srt', 'txt', 'all']`, the default value is `all`.
- 📌 `2.mp4` source: [link](https://github.com/SWHL/RapidVideOCR/blob/269beb52397c0cb18fc65f696ff5ddb546d1e711/assets/test_video/2.mp4)

```python
from rapid_videocr import RapidVideOCR

extractor = RapidVideOCR()

mp4_path = '2.mp4'
ocr_result = extractor(mp4_path, out_format='srt')
print(ocr_result)
```

### 3. Run by command line.
- Usage:
    ```bash
    $ rapid_videocr -h
    usage: rapid_videocr [-h] [-mp4 MP4_PATH] [-o {srt,txt,all}]

    optional arguments:
    -h, --help            show this help message and exit
    -mp4 MP4_PATH, --mp4_path MP4_PATH
                            The full path of mp4 video.
    -o {srt,txt,all}, --out_format {srt,txt,all}
                            Output file format. Default is "all"
    ```
- Example:
  ```bash
  $ rapid_videocr -o srt -mp4 2.mp4
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