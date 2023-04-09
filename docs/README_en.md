<div align="center">
   <img src="https://raw.githubusercontent.com/SWHL/RapidVideOCR/main/assets/logo.png"  width="75%" height="75%">
</div>
<br/>


English | [简体中文](https://github.com/SWHL/RapidVideOCR/blob/main/README.md)

<p align="left">
    <a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/75dae6e9804dec6e61bef98334601908dc9ec9fb/assets/RapidVideOCRDemo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pepy.tech/project/rapid-videocr"><img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
</p>

<details>
    <summary>Contents</summary>

- [Introduction](#introduction)
- [TODO](#todo)
- [Overall framework](#overall-framework)
- [Steps for usage](#steps-for-usage)
- [Change log (more)](#change-log-more)
- [Announce](#announce)

</details>

### Introduction
- Video hard subtitle extraction, automatically generate the corresponding `srt | txt` file.
- Supported subtitle languages: Chinese | English (For other supported languages, see: [List of supported languages](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99))
- You can join the QQ group: **706807542**
- Extract video hard subtitles faster and more accurately, and provide output in two formats `srt|txt`l:
   - **FASTER**: Combined with [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/) software, extraction of key subtitle frames is faster.
   - **More accurate**: [RapidOCR](https://github.com/RapidAI/RapidOCR) is used as the recognition library.
   - **More convenient**: pip can be used directly after installation.
- **This tool is under development. During use, if you encounter any problems, please submit an issue or join the group for feedback. If you don't want to use it, just don't use it, don't affect your mood.**

### TODO
- [x] Add the processing interface for [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/) software to extract subtitle frame results
- [x] Overlapping recognition function
- [ ] Package the program as an executable
- [ ] Write a cross-platform interface
- [ ] Try to integrate the core functions of VideoSubFinder into this project, through its open CLI mode
- [x] API docs


### Overall framework
```mermaid
flowchart LR
     A(VideoSubFinder) --Extract subtitle key frame--> B(RapidVideOCR) --OCR--> C(SRT)
```

### Steps for usage
1. Install and use VideoSubFinder software
    - Download link: [videosubfinder](https://sourceforge.net/projects/videosubfinder/)
    - Tutorial: [VideoSubFinder use documents](https://juejin.cn/post/7203362527082053691)
    - The final generated `RGBImages` and `TXTImages` directories will generally be in the software installation directory
    - ✧ It is recommended to use the images in the `RGBImages` directory (thanks to feedback from [dyphire](https://github.com/dyphire) in [#21](https://github.com/SWHL/RapidVideOCR/issues/21))

2. Install rapid_videocr
    ```bash
    pip install rapid_videocr
    ```

3. Use the RapidVideOCR tool
    - Run by scripts:
        - RapidVideOCR API
            ```python
            # __init__
            Args:
               is_concat_rec (bool, optional): Whether to single recognition. Defaults to False.
               concat_batch (int, optional): The batch of concating image nums in concat recognition mode. Defaults to 10.
               out_format (str, optional): Output format of subtitle(srt, txt, all). Defaults to 'all'.
               is_print_console (bool, optional): Whether to print the subtitle results to console. 1 means to print results to console. Default is 0.

            # __call__
            Args:
                 video_sub_finder_dir (Union[str, Path]): RGBImages or TXTImages from VideoSubFinder app.
                 save_dir (Union[str, Path]): The directory of saving the srt/txt file.

            Raises:
                RapidVideOCRError: meet some error.
            ```

        - Example:
            ```python
            from rapid_videocr import RapidVideOCR

            extractor = RapidVideOCR(is_concat_rec=True,
                                     concat_batch=10,
                                     out_format='srt',
                                     is_print_console=False)

            rgb_dir = 'RGBImages'
            save_dir = 'result'
            extractor(video_sub_finder_dir=rgb_dir, save_dir=save_dir)
            ```
     - Run by command line:
        - Usage:
            ```bash
            $ rapid_videocr -h
            usage: rapid_videocr [-h] -i IMG_DIR [-s SAVE_DIR] [-o {srt,txt,all}]
                                [-m {single,concat}] [-b CONCAT_BATCH] [-p {0,1}]

            optional arguments:
            -h, --help            show this help message and exit
            -i IMG_DIR, --img_dir IMG_DIR
                                    The full path of RGBImages or TXTImages.
            -s SAVE_DIR, --save_dir SAVE_DIR
                                    The path of saving the recognition result. Default is
                                    "results" under the current directory.
            -o {srt,txt,all}, --out_format {srt,txt,all}
                                    Output file format. Default is "all".
            -m {single,concat}, --mode {single,concat}
                                    Which mode to run (concat recognition or single
                                    recognition). Default is "single".
            -b CONCAT_BATCH, --concat_batch CONCAT_BATCH
                                    The batch of concating image nums in concat
                                    recognition mode. Default is 10.
            -p {0,1}, --print_console {0,1}
                                    Whether to print the subtitle results to console. 1
                                    means to print results to console. Default is 0.
            ```
        - Example:
            ```bash
            $ rapid_videocr -i RGBImages -s Results -o srt -m concat -b 10 -p 1
            ```

4. View the results
    - Go to the `save_dir` directory to view the results.
    - It is worth noting that if you want the video playback software to automatically mount the srt file, you need to change the name of the srt file to the name of the video file, and put it in the same directory, or manually specify the loading.

### Change log ([more](https://github.com/SWHL/RapidVideOCR/blob/main/docs/change_log_en.md))
- 🐱2023-03-27 v2.1.6 update:
    - Fix the problem of timeline misalignment. For details, see [issue 23](https://github.com/SWHL/RapidVideOCR/issues/23)
- 👽2023-03-23 v2.1.5 update:
    - Added print to screen control parameter `is_print_console`
    - Adjust the position of the `out_format` parameter to when initializing the class.
- 😀2023-03-14 v2.1.3 update:
    - Fix the error when inputting the `TXtImages` directory and recognizing the overlap.

### Announce
For international developers, we regard [Discussions](https://github.com/SWHL/RapidVideOCR/discussions) as our international community platform. All ideas and questions can be discussed here in English.