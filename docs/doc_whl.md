## rapid_videocr Package
<p align="left">
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pepy.tech/project/rapid-videocr"><img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
</p>

### 1. Install package by pypi.
```bash
pip install rapid_videocr
```

### 2. Run by script.
- RapidVideOCR has the default `out_format`, which is one of `['srt', 'txt', 'all']`, the default value is `all`.
- 📌 `2.mp4` source: [link](https://github.com/SWHL/RapidVideOCR/blob/269beb52397c0cb18fc65f696ff5ddb546d1e711/assets/test_video/2.mp4)

```python
from rapid_videocr import RapidVideOCR

extractor = RapidVideOCR()

rgb_dir = 'TXTImages'
save_dir = 'result'
extractor(rgb_dir, save_dir)

```

### 3. Run by command line.
- Usage:
    ```bash
    $ rapid_videocr -h
    usage: rapid_videocr [-h] [-i IMG_DIR] [-s SAVE_DIR] [-o {srt,txt,all}]

    optional arguments:
    -h, --help            show this help message and exit
    -i IMG_DIR, --img_dir IMG_DIR
                            The full path of mp4 video.
    -s SAVE_DIR, --save_dir SAVE_DIR
                            The path of saving the recognition result.
    -o {srt,txt,all}, --out_format {srt,txt,all}
                            Output file format. Default is "all"
    ```
- Example:
  ```bash
  $ rapid_videocr -i TXTImages -s Results -o srt
  ```
