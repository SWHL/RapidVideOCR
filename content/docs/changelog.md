---
weight: 6000
lastmod: "2022-10-08"
draft: false
author: "SWHL"
title: "更新日志"
icon: "update"
toc: true
description: ""
---

### 📣 后续更新日志将移步到[Release](https://github.com/SWHL/RapidVideOCR/releases)界面，这里不再更新

#### 🚩2023-10-08 v2.2.8 update

- 适配`rapidocr_onnxruntime`的相关参数，可以通过RapidVideOCR类传入，从而更加灵活指定不同语言的模型。

#### ♦ 2023-08-05 v2.2.4 update

- 修复批量识别模式下，索引错误。
- 添加日志记录模块，便于使用桌面版，快速记录问题，便于反馈。

#### 🛶2023-07-19 v2.2.3 update

- 增加对VSF的参数的适配，命令行模式和类初始化时，可以指定VSF命令的同名参数。详细使用参见[link](https://github.com/SWHL/RapidVideOCR/wiki/RapidVideOCR%E9%AB%98%E7%BA%A7%E6%95%99%E7%A8%8B%EF%BC%88%E6%9C%89python%E5%9F%BA%E7%A1%80%E7%9A%84%E5%B0%8F%E4%BC%99%E4%BC%B4%EF%BC%89)

#### 🤓2023-07-08 v2.2.2 update

- 修复批量识别时，不能读取中文路径的问题
- 修复漏轴时，SRT中跳过问题。目前当出现某一轴未能识别，则会空出位置，便于校对。
- 保留VSF识别的中间结果

#### 🐲2023-06-22 v2.2.0 update

- 该版本是向`v2.1.x`兼容的，也就是之前用法依然可以。
- 将VSF的CLI整合到库中，只需指定`VideoSubFinderWXW.exe`的全路径即可。
- 增加批量识别功能，指定视频目录，即可自动提取目录下所有视频字幕
- 使用示例, 参见：[demo.py](https://github.com/SWHL/RapidVideOCR/blob/main/demo.py)

#### 😀2023-05-12 v2.1.7 update

- 优化代码
- 添加`save_name`参数，可以灵活指定保存的`srt | txt`文件名称，默认是`result`

#### 🐱2023-03-27 v2.1.6 update

- 修复时间轴对不齐问题，详情参见[issue 23](https://github.com/SWHL/RapidVideOCR/issues/23)

#### 👽2023-03-23 v2.1.5 update

- 添加打印到屏幕的控制参数`is_print_console`
- 调整`out_format`参数位置到初始化类时

#### 😀2023-03-14 v2.1.3 update

- 修复输入`TXTImages`目录且叠字识别时错误

#### 😜2023-03-12 v2.1.2 update

- 修复索引错误，[#22](https://github.com/SWHL/RapidVideOCR/issues/22)

#### 🎢2023-03-11 v2.1.1 update

- 修复单图识别与之前版本差异问题
- 默认识别模式更改为单图识别，是否使用叠图识别，请自行决定

#### 🥇2023-03-10 v2.1.0 update

- 添加叠字识别功能，速度更快，默认是叠字识别功能

#### 🎈2023-03-02 v2.0.5~7 update

- 修复生成的srt文件中的格式错误， [#19](https://github.com/SWHL/RapidVideOCR/issues/19)

#### 🎫2023-02-17 v2.0.4 update

- 针对传入的`TXTImages`目录，作了优化处理。相比于传入`RGBImages`，会更快和更准。推荐传入`TXTImages`目录

#### 💎2023-02-17 v2.0.2 update

- 修复同行字幕识别丢失空格问题

#### 🎈2023-01-29 v1.1.10 update

- 修复帧索引转时间戳时，索引为空错误

#### 🧨2023-01-28 v1.1.9 update

- 修复时间轴对不齐问题

#### 👊 2023-01-15 v1.1.4 update

- 添加输出txt格式的选项，目前v1.1.4版本默认输出srt和txt两种格式
- 添加根据运行程序屏幕大小，调节选择字幕的框大小

#### 🌈2023-01-10 v1.0.3 update

- 将decord替换为OpenCV，因为decord处理MP4时，存在内存泄漏问题。详情参见：[#208](https://github.com/dmlc/decord/issues/208)

#### 🎄2022-12-04 update

- 添加交互式框定字幕位置功能，默认开启，更加好用，详情可参考下面的GIF图。感谢@[Johndirr](https://github.com/Johndirr)的建议。
- 优化代码结构，将RapidOCR相关模型和配置文件放到`rapidocr`目录下
- `rapidvideocr`的配置文件也放到对应目录下

#### 🌼2022-05-08 update

- 添加交互式确定二值化字幕图像阈值操作，仅仅支持Windows系统，可以通过`is_select_threshold = True`来使用
- 优化代码

#### 🎉2022-05-03 update

- 添加GPU支持，具体配置教程参见：[onnxruntime-gpu版推理配置](https://github.com/RapidAI/RapidOCR/blob/main/python/onnxruntime_infer/README.md#onnxruntime-gpu%E7%89%88%E6%8E%A8%E7%90%86%E9%85%8D%E7%BD%AE)
- 添加日文的支持，可以支持更多语种，具体参见：[支持语种列表](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99)

#### 💡2022-05-01 update

- 添加语音模块部分位于分支`asr_module`
- 添加语音识别模块，由于该模块中解码部分只能在Linux和Mac上运行，因此如果想要使用该模块，请在Linux和Mac上。
- 目前语音识别代码来自[RapidASR/python](https://github.com/RapidAI/RapidASR/tree/main/python/base_paddlespeech)部分。模型来自[PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/examples/aishell/asr0)
- 经过简单测试，语音识别模块不是太准。-_-!

#### 2022-03-09 update

- 添加[常见问题模块](./FAQ.md)，可以帮助大家跳过常见的小问题

#### 2021-12-14 update

- [x] 背景去除效果不好，导致丢失某些帧
    - 尝试采用图像分割的方法，经过测试，CPU下推理速度太慢，暂时放弃
    - 目前采用的固定的二值化阈值
- [x] (2021-12-14)完善对应的英文文档
- [x] (2021-12-14)添加运行耗时基准
- [x] 添加具体参数说明
- [x] 制作项目Logo
- [ ] 更多的测试

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
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
