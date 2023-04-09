<div align="center">
   <img src="https://raw.githubusercontent.com/SWHL/RapidVideOCR/main/assets/logo.png"  width="75%" height="75%">
</div>
<br/>

简体中文 | [English](https://github.com/SWHL/RapidVideOCR/blob/main/docs/README_en.md)

<p align="left">
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapid-videocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid_videocr"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pepy.tech/project/rapid-videocr">
        <img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads">
    </a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href='https://rapidvideocr.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/rapidvideocr/badge/?version=latest' alt='Documentation Status'/>
    </a>
</p>

<details>
    <summary>目录</summary>

- [简介](#简介)
- [TODO](#todo)
- [整体框架](#整体框架)
- [保姆级使用步骤（小白）](#保姆级使用步骤小白)
- [使用步骤（有python基础）](#使用步骤有python基础)
- [更新日志（more）](#更新日志more)
- [写在最后](#写在最后)

</details>

### 简介
- 视频硬字幕提取，自动生成对应`srt | txt`文件。
- 支持字幕语言：中文 | 英文 （其他可以支持的语言参见：[支持语种列表](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99))
- 可加入QQ群：**706807542**
- 更快更准确地提取视频硬字幕，并提供`srt| txt`两种格式的输出：
  - **更快**：与[VideoSubFinder](https://sourceforge.net/projects/videosubfinder/)软件结合使用，提取关键字幕帧更快。
  - **更准**：采用[RapidOCR](https://github.com/RapidAI/RapidOCR)作为识别库。
  - **更方便**：pip直接安装即可使用。
- **该工具处于发展中。在使用过程中，如果遇到任何问题，欢迎提issue或者入群反馈。**
- **如果不愿意用的话，不用就好，不要影响自己心情。**
- 如果有帮助到您的话，请给个小星星⭐或者赞助一杯咖啡（点击页面最上面的Sponsor中链接）。

### TODO
- [x] 增加对[VideoSubFinder](https://sourceforge.net/projects/videosubfinder/)软件提取字幕帧结果的处理接口
- [x] 叠字识别功能
- [ ] 将程序打包为可执行文件
- [ ] 编写跨平台的界面
- [ ] 尝试将VideoSubFinder核心功能整合到本项目中，通过其开放的CLI mode
- [ ] API docs


### 整体框架
```mermaid
flowchart LR
    A(VideoSubFinder) --提取字幕关键帧--> B(RapidVideOCR)  --OCR--> C(SRT)
```

### 保姆级使用步骤（小白）
- 请移步[[RapidVideOCR周边] RapidVideOCR保姆级教程（从小白到上手使用）](https://blog.csdn.net/shiwanghualuo/article/details/129788386?spm=1001.2014.3001.5501)

### 使用步骤（有python基础）
1. 安装使用VideoSubFinder软件
   - 下载地址：Windows & Linux ([videosubfinder官网](https://sourceforge.net/projects/videosubfinder/) / QQ群（706807542）共享文件) | [Mac版](https://github.com/eritpchy/videosubfinder-cli)
   - 使用教程：[VideoSubFinder提取字幕关键帧教程](https://juejin.cn/post/7203362527082053691)
   - 最终生成的`RGBImages`和`TXTImages`目录一般会在软件安装目录下
   - ✧ 推荐用`RGBImages`目录中图像（感谢小伙伴[dyphire](https://github.com/dyphire)在[#21](https://github.com/SWHL/RapidVideOCR/issues/21)的反馈）
2. 安装rapid_videocr
   ```bash
   pip install rapid_videocr
   ```
3. 使用RapidVideOCR工具
   - 脚本运行：
        ```python
        from rapid_videocr import RapidVideOCR

        # RapidVideOCR有两个初始化参数
        # is_concat_rec: 是否用单张图识别，默认是False，也就是默认用单图识别
        # concat_batch: 叠图识别的图像张数，默认10，可自行调节
        # out_format: 输出格式选择，[srt, txt, all], 默认是 all
        # is_print_console: 是否打印结果，[0, 1], 默认是0，不打印
        extractor = RapidVideOCR(is_concat=False,
                                 out_format='all',
                                 is_print_console=False)

        rgb_dir = 'test_files/TXTImages'
        save_dir = 'result'
        extractor(rgb_dir, save_dir)
        ```
    - 命令行运行：
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
4. 查看结果
   - 前往`save_dir`目录下即可查看结果。
   - 值得注意的是，如果想要让视频播放软件自动挂载srt文件，需要更改srt文件名字为视频文件名字，且放到同一目录下，亦或者手动指定加载。


### 更新日志（[more](https://github.com/SWHL/RapidVideOCR/blob/main/docs/change_log.md)）
- 🐱2023-03-27 v2.1.6 update:
  - 修复时间轴对不齐问题，详情参见[issue 23](https://github.com/SWHL/RapidVideOCR/issues/23)

- 👽2023-03-23 v2.1.5 update:
  - 添加打印到屏幕的控制参数`is_print_console`
  - 调整`out_format`参数位置到初始化类时

- 😀2023-03-14 v2.1.3 update:
  - 修复输入`TXTImages`目录且叠字识别时错误


### 写在最后
- 扫码加入组织：
    <div align="center">
        <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/QQGroup.jpg" width="25%" height="25%" align="center">
    </div>
