English | [简体中文](https://github.com/SWHL/RapidVideOCR/blob/main/README.md)

<div align="center">
   <img src="https://raw.githubusercontent.com/SWHL/RapidVideOCR/main/assets/logo.png"  width="75%" height="75%">
</div>
<br/>

<p align="left">
    <a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/75dae6e9804dec6e61bef98334601908dc9ec9fb/assets/RapidVideOCRDemo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pepy.tech/project/rapid-videocr"><img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href='https://rapidvideocr.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/rapidvideocr/badge/?version=latest' alt='Documentation Status'/>
    </a>
</p>

<details>
    <summary>Contents</summary>

- [Introduction](#introduction)
- [Overall framework](#overall-framework)
- [Use](#use)
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


### Overall framework
```mermaid
flowchart LR
     A(VideoSubFinder) --Extract subtitle key frame--> B(RapidVideOCR) --OCR--> C(SRT)
```

### Use
- [☆ RapidVideOCR Primary Tutorial (Interface version, download and decompress)](https://github.com/SWHL/RapidVideOCR/wiki/RapidVideOCR%E5%88%9D%E7%BA%A7%E6%95%99%E7%A8%8B%EF%BC%88%E7%95%8C%E9%9D%A2%E7%89%88-%E4%B8%8B%E8%BD%BD%E8%A7%A3%E5%8E%8B%E4%BD%BF%E7%94%A8%EF%BC%89)
- [☆☆ RapidVideOCR Intermediate Tutorial (Python Xiaobai)](https://github.com/SWHL/RapidVideOCR/wiki/RapidVideOCR%E4%B8%AD%E7%BA%A7%E6%95%99%E7%A8%8B%EF%BC%88python%E5%B0%8F%E7%99%BD%EF%BC%89)
- [☆☆☆ RapidVideOCR Advanced Tutorial (Partners with python foundation)](https://github.com/SWHL/RapidVideOCR/wiki/RapidVideOCR%E9%AB%98%E7%BA%A7%E6%95%99%E7%A8%8B%EF%BC%88%E6%9C%89python%E5%9F%BA%E7%A1%80%E7%9A%84%E5%B0%8F%E4%BC%99%E4%BC%B4%EF%BC%89)

### Change log ([more](https://github.com/SWHL/RapidVideOCR/wiki/Changelog))
- ♠ 2023-06-04 Desktop v0.0.2 update:
    - Fix isse #30: Keep the last selected directory.
- 😀2023-05-12 v2.1.7 update:
   - Optimize code
   - Add `save_name` parameter, you can flexibly specify the saved `srt | txt` file name, the default is `result`
- 🐱2023-03-27 v2.1.6 update:
    - Fix the problem of timeline misalignment. For details, see [issue 23](https://github.com/SWHL/RapidVideOCR/issues/23)
- 👽2023-03-23 v2.1.5 update:
    - Added print to screen control parameter `is_print_console`
    - Adjust the position of the `out_format` parameter to when initializing the class.

### Announce
For international developers, we regard [Discussions](https://github.com/SWHL/RapidVideOCR/discussions) as our international community platform. All ideas and questions can be discussed here in English.