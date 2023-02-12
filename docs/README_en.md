<div align="center">
   <img src="../assets/logo.png"  width="75%" height="75%">
</div>
<br/>


[简体中文](../README.md) | English

<p align="left">
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img src="https://img.shields.io/pypi/dm/rapid-videocr?color=9cf"></a>
</p>


<details>
    <summary>Contents</summary>

- [Introduction](#introduction)
- [Overall framework](#overall-framework)
- [Change log (more)](#change-log-more)
  - [🎇2023-02-12 v2.0.1 update:](#2023-02-12-v201-update)
  - [Steps for usage](#steps-for-usage)
  - [Announce](#announce)

</details>

### Introduction
- Video hard subtitle extraction, automatically generate the corresponding `srt` file.
- Supported subtitle languages: Chinese | English (For other supported languages, see: [List of supported languages](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99))
- You can join the QQ group: **706807542**
- Extract video hard subtitles faster and more accurately, and provide output in two formats `srt|txt`l:
   - **FASTER**: Combined with VideoSubFinder software, extraction of key subtitle frames is faster.
   - **More accurate**: [RapidOCR](https://github.com/RapidAI/RapidOCR) is used as the recognition library.
   - **More convenient**: pip can be used directly after installation.
- **This tool is under development. During use, if you encounter any problems, please submit an issue or join the group for feedback. If you don't want to use it, just don't use it, don't affect your mood.**

###TODO
- [x] Add the processing interface for [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/) software to extract subtitle frame results
- [ ] Try to integrate the core functions of VideoSubFinder into this project, through its open CLI mode


### Overall framework
```mermaid
flowchart LR
     A(VideoSubFinder) --Extract subtitle key frame--> B(RapidVideOCR) --OCR--> C(SRT)
```


### Change log ([more](../docs/change_log_en.md))
#### 🎇2023-02-12 v2.0.1 update:
- Fix the bug that the subtitle frame time becomes 0 when the video duration is longer than 1 hour.


#### Steps for usage
1. Install and use VideoSubFinder software
    - Download link: [videosubfinder](https://sourceforge.net/projects/videosubfinder/)
    - Tutorial: [\[Subtitle Learning Tutorial\] Use VideoSubFinder/esrXP to extract hard subtitles](https://www.bilibili.com/video/BV12z4y1D7qC/?share_source=copy_web&vd_source=345b117e20ba7c605f01cdf5a1cda168)
2. Use this software to extract key subtitle frame images → get the `RGBImages` directory. Usually in the software installation directory.
3. Install rapid_videocr
    ```bash
    pip install rapid_videocr
    ```
4. Use the RapidVideOCR tool
    - The script runs:
         ```python
         from rapid_videocr import RapidVideOCR

         extractor = RapidVideOCR()

         rgb_dir = 'test_files/RGBImages'
         save_dir = 'result'
         extractor(rgb_dir, save_dir)
         ```
     - Command line run:
       - Usage:
          ```bash
          $ rapid_videocr -h
          usage: rapid_videocr [-h] [-i IMG_DIR] [-s SAVE_DIR] [-o {srt,txt,all}]

          optional arguments:
          -h, --help show this help message and exit
          -i IMG_DIR, --img_dir IMG_DIR
                                  The full path of mp4 video.
          -s SAVE_DIR, --save_dir SAVE_DIR
                                  The path of saving the recognition result.
          -o {srt,txt,all}, --out_format {srt,txt,all}
                                  Output file format. Default is "all"
          ```
        - Example:
          ```bash
          $ rapid_videocr -i RGBImages -s Results -o srt
          ```
5. View the results
    - Go to the `save_dir` directory to view the results.
    - It is worth noting that if you want the video playback software to automatically mount the srt file, you need to change the name of the srt file to the name of the video file, and put it in the same directory, or manually specify the loading.


#### Announce
- The release of this warehouse follows the semantic version number naming, for details, refer to [Semantic version number 2.0](https://semver.org/lang/zh-CN/).