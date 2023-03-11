<div align="center">
   <img src="../assets/logo.png"  width="75%" height="75%">
</div>
<br/>


English | [简体中文](../README.md)

<p align="left">
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
- [ ] Try to integrate the core functions of VideoSubFinder into this project, through its open CLI mode
- [ ] API docs


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

            extractor = RapidVideOCR(is_concat_rec=True, concat_batch=10)

            rgb_dir = 'RGBImages'
            save_dir = 'result'
            extractor(video_sub_finder_dir=rgb_dir, save_dir=save_dir, out_format='srt')
            ```
     - Run by command line:
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
                                    recognition), default is "single"
            -b CONCAT_BATCH, --concat_batch CONCAT_BATCH
                                    The batch of concating image nums in concat
                                    recognition mode. Default is 10.
            ```
        - Example:
            ```bash
            $ rapid_videocr -i RGBImages -s Results -o srt -m concat -b 10
            ```

4. View the results
    - Go to the `save_dir` directory to view the results.
    - It is worth noting that if you want the video playback software to automatically mount the srt file, you need to change the name of the srt file to the name of the video file, and put it in the same directory, or manually specify the loading.

### Change log ([more](../docs/change_log_en.md))
- 🎢2023-03-11 v2.1.1 update:
   - Fix the difference between single image recognition and the previous version.
   - The default recognition mode is changed to single image recognition, please decide whether to use overlapping image recognition.

- 🥇2023-03-10 v2.1.0 update:
  - Added overlap recognition function, faster speed, the default is concat recognition mode.

- 🎈2023-03-02 v2.0.5~7 update:
    - Fix format error in generated srt file, [#19](https://github.com/SWHL/RapidVideOCR/issues/19)

### Announce
For international developers, we regard [Discussions](https://github.com/SWHL/RapidVideOCR/discussions) as our international community platform. All ideas and questions can be discussed here in English.