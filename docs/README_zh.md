<div align="center">
  <img src="https://raw.githubusercontent.com/SWHL/RapidVideOCR/main/assets/logo.png" width="55%" height="55%"/>

<div>&nbsp;</div>

<a href="https://www.modelscope.cn/studios/liekkas/RapidVideOCR/summary" target="_blank"><img src="https://img.shields.io/badge/ModelScope-Demo-blue"></a>
<a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/main/assets/RapidVideOCRDemo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
<a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
<a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
<a href="https://pepy.tech/project/rapid-videocr"><img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

简体中文 | [English](https://github.com/SWHL/RapidVideOCR)
</div>

### 简介

- 视频硬字幕提取，自动生成对应`srt | ass | txt`文件。
- 支持字幕语言：中文 | 英文 （其他可以支持的语言参见：[支持语种列表](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99))
- 优势如下：
    - **提取更快**：与[VideoSubFinder](https://sourceforge.net/projects/videosubfinder/)软件结合使用，提取关键字幕帧更快。
    - **识别更准**：采用[RapidOCR](https://github.com/RapidAI/RapidOCR)作为识别库。
    - **使用更方便**：pip直接安装即可使用。

- 桌面EXE版，请移步[RapidVideOCRDesktop](https://github.com/SWHL/RapidVideOCRDesktop)
- 如果有帮助到您的话，请给个小星星⭐。

### [在线Demo](https://www.modelscope.cn/studios/liekkas/RapidVideOCR/summary)

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/OnlineDemo.gif" alt="Demo" width="100%" height="100%">
</div>

### 整体框架

```mermaid
flowchart LR
    A[/Video/] --Extract subtitle key frame--> B(VideoSubFinder) --OCR-->C(RapidVideOCR)
    C --Convert--> D[/"SRT | ASS | TXT"/]
```

### 安装

```bash
pip install rapid_videocr
```

### 使用

> [!NOTE]
>
> `rapid_videocr`输入图像路径必须是**VideoSubFinder**软件输出的RGBImages或TXTImages的路径。

```bash
rapid_videocr -i RGBImages
```

或者python脚本：

```python
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

input_args = RapidVideOCRInput(is_batch_rec=False)
extractor = RapidVideOCR(input_args)

rgb_dir = "tests/test_files/RGBImages"
save_dir = "outputs"
save_name = "a"

# outputs/a.srt  outputs/a.ass  outputs/a.txt
extractor(rgb_dir, save_dir, save_name=save_name)
```

### 文档

完整文档请移步：[docs](https://swhl.github.io/RapidVideOCR/)

### 贡献者

<p align="left">
  <a href="https://github.com/SWHL/RapidVideOCR/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=SWHL/RapidVideOCR" width="20%"/>
  </a>
</p>

### 贡献指南

我们感谢所有的贡献者为改进和提升 RapidVideOCR 所作出的努力。

欢迎提交请求。对于重大更改，请先打开issue讨论您想要改变的内容。

请确保适当更新测试。

### 加入我们

- 微信扫描以下二维码，关注 **RapidAI公众号**，回复video即可加入RapidVideOCR微信交流群：
    <div align="center">
        <img src="https://raw.githubusercontent.com/RapidAI/.github/main/assets/RapidAI_WeChatAccount_round_corner.png" width="25%" height="25%" align="center">
    </div>

- 扫码加入QQ群（706807542）：
    <div align="center">
        <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/QQGroup.png" width="25%" height="25%" align="center">
    </div>

### [赞助](https://swhl.github.io/RapidVideOCR/docs/sponsor/)

如果您想要赞助该项目，可直接点击当前页最上面的Sponsor按钮，请写好备注( **您的Github账号名称** )，方便添加到赞助列表中。

### 开源许可证

该项目采用 [Apache 2.0 license](../LICENSE) 开源许可证。
