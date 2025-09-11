---
comments: true
hide:
  - navigation
  - toc
---

<div align="center">
  <img src="https://raw.githubusercontent.com/SWHL/RapidVideOCR/main/assets/logo.png" width="55%" height="55%"/>
<div>&nbsp;</div>

<a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/75dae6e9804dec6e61bef98334601908dc9ec9fb/assets/RapidVideOCRDemo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
<a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
<a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
<a href="https://pepy.tech/project/rapid-videocr"><img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

### 简介

`rapid_videocr`是一个自动视频硬字幕提取，生成对应`srt | ass | txt`文件的工具。

支持字幕语言：[支持语种列表](https://rapidai.github.io/RapidOCRDocs/main/model_list/#_4)，因为该工具依赖`rapidocr`库，因此`rapidocr`支持识别的语言，`rapid_videocr`均是支持的。

优势如下：

- **提取更快**：与[VideoSubFinder](https://sourceforge.net/projects/videosubfinder/)软件结合使用，提取关键字幕帧更快。
- **识别更准**：采用[RapidOCR](https://github.com/RapidAI/RapidOCR)作为识别库。
- **使用更方便**：pip直接安装即可使用。

如果有帮助到您的话，请给个小星星⭐。

### 整体框架

```mermaid
flowchart LR
    A[/Video/] --Extract subtitle key frame--> B(VideoSubFinder) --OCR-->C(RapidVideOCR)
    C --Convert--> D[/"SRT | ASS | TXT"/]
```

### [在线Demo](https://huggingface.co/spaces/SWHL/RapidVideOCR)

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/OnlineDemo.gif" alt="Demo" width="60%" height="60%">
</div>
