## rapid_videocr Package
<p align="left">
    <a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/75dae6e9804dec6e61bef98334601908dc9ec9fb/assets/RapidVideOCRDemo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pepy.tech/project/rapid-videocr">
        <img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads">
    </a>
    <a href='https://rapidvideocr.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/rapidvideocr/badge/?version=latest' alt='Documentation Status'/>
    </a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>


### 1. Install package by pypi.
```bash
pip install rapid_videocr
```

### 2. Run by script.
- Only OCR:
    ```python
    from rapid_videocr import RapidVideOCR

    extractor = RapidVideOCR(is_concat_rec=True,
                            concat_batch=10,
                            out_format='srt')

    rgb_dir = 'RGBImages'
    save_dir = 'outputs'
    extractor(video_sub_finder_dir=rgb_dir, save_dir=save_dir)
    ```
- Extract + OCR:
    ```python
    from rapid_videocr import RapidVideoSubFinderOCR

    vsf_exe = r"G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe"
    extractor = RapidVideoSubFinderOCR(vsf_exe_path=vsf_exe, is_concat_rec=True)

    # video_path can be directory path or video full path.
    video_path = 'test_files/tiny/2.mp4'
    save_dir = 'outputs'
    extractor(video_path, save_dir)
    ```

### 3. Run by command line.
- Usage:
    ```bash
    $ rapid_videocr -h
    usage: rapid_videocr [-h] [-vsf VSF_EXE_PATH] [-video_dir VIDEO_DIR] [-i IMG_DIR] [-s SAVE_DIR] [-o {srt,txt,all}] [-m {single,concat}] [-b CONCAT_BATCH] [-p {0,1}]

    options:
    -h, --help            show this help message and exit
    -vsf VSF_EXE_PATH, --vsf_exe_path VSF_EXE_PATH
                            The full path of VideoSubFinderWXW.exe.
    -video_dir VIDEO_DIR, --video_dir VIDEO_DIR
                            The full path of video or the path of video directory.
    -i IMG_DIR, --img_dir IMG_DIR
                            The full path of RGBImages or TXTImages.
    -s SAVE_DIR, --save_dir SAVE_DIR
                            The path of saving the recognition result. Default is "outputs" under the current directory.
    -o {srt,txt,all}, --out_format {srt,txt,all}
                            Output file format. Default is "all".
    -m {single,concat}, --mode {single,concat}
                            Which mode to run (concat recognition or single recognition). Default is "single".
    -b CONCAT_BATCH, --concat_batch CONCAT_BATCH
                            The batch of concating image nums in concat recognition mode. Default is 10.
    -p {0,1}, --print_console {0,1}
                            Whether to print the subtitle results to console. 1 means to print results to console. Default is 0.
    ```
- Example:
  - Only OCR:
    ```bash
    $ rapid_videocr -i RGBImages
    ```
  - Extract + OCR:
    ```bash
    $ rapid_videocr -vsf G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe -video_dir G:\ProgramFiles\RapidVideOCR\test_files\tiny
    ```

See details for [RapidVideOCR](https://github.com/SWHL/RapidVideOCR).