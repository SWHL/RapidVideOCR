<div align="center">
   <img src="assets/logo.png"  width="75%" height="75%">
</div>
<br/>

简体中文 | [English](./docs/README_en.md)

<p align="left">
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img src="https://img.shields.io/pypi/dm/rapid-videocr?color=9cf"></a>
</p>

<details>
    <summary>目录</summary>

- [简介](#简介)
- [TODO](#todo)
- [整体框架](#整体框架)
- [更新日志（more）](#更新日志more)
  - [🎇2023-02-12 v2.0.1 update:](#2023-02-12-v201-update)
- [使用步骤](#使用步骤)
  - [写在最后](#写在最后)

</details>

### 简介
- 视频硬字幕提取，自动生成对应`srt`文件。
- 支持字幕语言：中文 | 英文 （其他可以支持的语言参见：[支持语种列表](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99))
- 可加入QQ群：**706807542**
- 更快更准确地提取视频硬字幕，并提供`srt| txt`l两种格式的输出：
  - **更快**：与VideoSubFinder软件结合使用，提取关键字幕帧更快。
  - **更准**：采用[RapidOCR](https://github.com/RapidAI/RapidOCR)作为识别库。
  - **更方便**：pip直接安装即可使用。
- **该工具处于发展中。在使用过程中，如果遇到任何问题，欢迎提issue或者入群反馈。如果不愿意用的话，不用就好，不要影响自己心情。**

### TODO
- [x] 增加对[VideoSubFinder](https://sourceforge.net/projects/videosubfinder/)软件提取字幕帧结果的处理接口
- [ ] 尝试将VideoSubFinder核心功能整合到本项目中，通过其开放的CLI mode


### 整体框架
```mermaid
flowchart LR
    A(VideoSubFinder) --提取字幕关键帧--> B(RapidVideOCR)  --OCR--> C(SRT)
```


### 更新日志（[more](./docs/change_log.md)）
#### 🎇2023-02-12 v2.0.1 update:
- 修复视频时长大于1个小时，字幕帧时间变为0的bug.


### 使用步骤
1. 安装使用VideoSubFinder软件
   - 下载地址：[videosubfinder](https://sourceforge.net/projects/videosubfinder/)
   - 使用教程：[【字幕学习教程】使用VideoSubFinder/esrXP提取硬字幕](https://www.bilibili.com/video/BV12z4y1D7qC/?share_source=copy_web&vd_source=345b117e20ba7c605f01cdf5a1cda168)
2. 使用该软件抽取关键字幕帧图像 → 得到`RGBImages`目录。一般会在软件安装目录下。
3. 安装rapid_videocr
   ```bash
   pip install rapid_videocr -i https://pypi.douban.com/simple/
   ```
4. 使用RapidVideOCR工具
   - 脚本运行：
        ```python
        from rapid_videocr import RapidVideOCR

        extractor = RapidVideOCR()

        rgb_dir = 'test_files/RGBImages'
        save_dir = 'result'
        extractor(rgb_dir, save_dir)
        ```
    - 命令行运行：
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
         $ rapid_videocr -i RGBImages -s Results -o srt
         ```
5. 查看结果
   - 前往`save_dir`目录下即可查看结果。
   - 值得注意的是，如果想要让视频播放软件自动挂载srt文件，需要更改srt文件名字为视频文件名字，且放到同一目录下，亦或者手动指定加载。


#### 写在最后
- 本仓库发版遵循语义化版本号命名，详情参考[语义化版本号2.0](https://semver.org/lang/zh-CN/)
