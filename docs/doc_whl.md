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
- RapidVideOCR API
    ```python
    # __init__
    Args:
       is_single_res (bool, optional): Whether to single recognition. Defaults to False.
       concat_batch (int, optional): The batch of concating image nums in concat recognition mode. Defaults to 10.

    # __call__
    Args:
         video_sub_finder_dir (Union[str, Path]): RGBImages or TXTImages from VideoSubFinder app.
         save_dir (Union[str, Path]): The directory of saving the srt/txt file.
         out_format (str, optional): Output format of subtitle(srt, txt, all). Defaults to 'all'.

    Raises:
        RapidVideOCRError: meet some error.
    ```

- Example:
    ```python
    from rapid_videocr import RapidVideOCR

    extractor = RapidVideOCR(is_single_res=True, concat_batch=10)

    rgb_dir = 'RGBImages'
    save_dir = 'result'
    extractor(video_sub_finder_dir=rgb_dir, save_dir=save_dir, out_format='srt')
    ```

### 3. Run by command line.
- Usage:
    ```bash
    $ rapid_videocr -h
    usage: rapid_videocr [-h] [-i IMG_DIR] [-s SAVE_DIR] [-o {srt,txt,all}]
                        [-m {single,concat}]

    optional arguments:
    -h, --help            show this help message and exit
    -i IMG_DIR, --img_dir IMG_DIR
                            The full path of RGBImages or TXTImages.
    -s SAVE_DIR, --save_dir SAVE_DIR
                            The path of saving the recognition result.
    -o {srt,txt,all}, --out_format {srt,txt,all}
                            Output file format. Default is "all"
    -m {single,concat}, --mode {single,concat}
                            Which mode to run (concat recognition or single
                            recognition), default is "concat"
    -b CONCAT_BATCH, --concat_batch CONCAT_BATCH
                            The batch of concating image nums in concat
                            recognition mode. Default is 10.
    ```
- Example:
    ```bash
    $ rapid_videocr -i RGBImages -s Results -o srt -m concat -b 10
    ```
