---
weight: 1000
lastmod: "2022-08-01"
draft: false
author: "SWHL"
title: "Overview"
icon: "circle"
toc: true
description: ""
---
<div align="center">
  <img src="https://raw.githubusercontent.com/SWHL/RapidVideOCR/main/assets/logo.png" width="55%" height="55%"/>

<div>&nbsp;</div>

<a href="https://huggingface.co/spaces/SWHL/RapidVideOCR" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Hugging Face Demo-blue"></a>
<a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/main/assets/RapidVideOCRDemo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
<a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
<a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
<a href="https://pepy.tech/project/rapid-videocr"><img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

[简体中文](https://github.com/SWHL/RapidVideOCR/blob/main/docs/README_zh.md) | English
</div>

### Introduction

- Video hard subtitle extraction, automatically generate the corresponding `srt | ass | txt` file.
- Supported subtitle languages: Chinese | English (For other supported languages, see: [List of supported languages](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99))
- The advantages are as follows:
    - **Faster extraction**: Used in conjunction with [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/) software to extract key subtitle frames faster.
    - **More accurate recognition**: Use [RapidOCR](https://github.com/RapidAI/RapidOCR) as the recognition library.
    - **More convenient to use**: pip can be installed directly and used.

- For desktop EXE version, please go to [RapidVideOCRDesktop](https://github.com/SWHL/RapidVideOCRDesktop).
- If it helps you, please give a star ⭐.

### Overall framework

```mermaid
flowchart LR
    A[/Video/] --Extract subtitle key frame--> B(VideoSubFinder) --OCR-->C(RapidVideOCR)
    C --Convert--> D[/"SRT | ASS | TXT"/]
```
<script src="https://giscus.app/client.js"
        data-repo="SWHL/RapidVideOCR"
        data-repo-id="MDEwOlJlcG9zaXRvcnk0MDU1ODkwMjk="
        data-category="Q&A"
        data-category-id="DIC_kwDOGCzMJc4CUluM"
        data-mapping="title"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
