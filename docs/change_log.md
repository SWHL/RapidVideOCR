
#### 🎢2023-03-11 v2.1.1 update:
- 修复单图识别与之前版本差异问题
- 默认识别模式更改为单图识别，是否使用叠图识别，请自行决定

#### 🥇2023-03-10 v2.1.0 update:
- 添加叠字识别功能，速度更快，默认是叠字识别功能

#### 🎈2023-03-02 v2.0.5~7 update:
- 修复生成的srt文件中的格式错误， [#19](https://github.com/SWHL/RapidVideOCR/issues/19)

#### 🎫2023-02-17 v2.0.4 update:
- 针对传入的`TXTImages`目录，作了优化处理。相比于传入`RGBImages`，会更快和更准。推荐传入`TXTImages`目录

#### 💎2023-02-17 v2.0.2 update:
- 修复同行字幕识别丢失空格问题

#### 🎈2023-01-29 v1.1.10 update:
- 修复帧索引转时间戳时，索引为空错误

#### 🧨2023-01-28 v1.1.9 update:
- 修复时间轴对不齐问题

#### 🧨2023-01-28 v1.1.9 update:
- 修复时间轴对不齐问题

#### 👊 2023-01-15 v1.1.4 update:
- 添加输出txt格式的选项，目前v1.1.4版本默认输出srt和txt两种格式
- 添加根据运行程序屏幕大小，调节选择字幕的框大小

#### 🌈2023-01-10 v1.0.3 update:
- 将decord替换为OpenCV，因为decord处理MP4时，存在内存泄漏问题。详情参见：[#208](https://github.com/dmlc/decord/issues/208)

#### 🎄2022-12-04 update:
- 添加交互式框定字幕位置功能，默认开启，更加好用，详情可参考下面的GIF图。感谢@[Johndirr](https://github.com/Johndirr)的建议。
- 优化代码结构，将RapidOCR相关模型和配置文件放到`rapidocr`目录下
- `rapidvideocr`的配置文件也放到对应目录下

#### 🌼2022-05-08 update:
- 添加交互式确定二值化字幕图像阈值操作，仅仅支持Windows系统，可以通过`is_select_threshold = True`来使用
- 优化代码

#### 🎉2022-05-03 update:
- 添加GPU支持，具体配置教程参见：[onnxruntime-gpu版推理配置](https://github.com/RapidAI/RapidOCR/blob/main/python/onnxruntime_infer/README.md#onnxruntime-gpu%E7%89%88%E6%8E%A8%E7%90%86%E9%85%8D%E7%BD%AE)
- 添加日文的支持，可以支持更多语种，具体参见：[支持语种列表](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99)

#### 💡2022-05-01 update:
- 添加语音模块部分位于分支`asr_module`
- 添加语音识别模块，由于该模块中解码部分只能在Linux和Mac上运行，因此如果想要使用该模块，请在Linux和Mac上。
- 目前语音识别代码来自[RapidASR/python](https://github.com/RapidAI/RapidASR/tree/main/python/base_paddlespeech)部分。模型来自[PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/examples/aishell/asr0)
- 经过简单测试，语音识别模块不是太准。-_-!

#### 2022-03-09 update:
- 添加[常见问题模块](./FAQ.md)，可以帮助大家跳过常见的小问题

#### 2021-12-14 update:
- [x] 背景去除效果不好，导致丢失某些帧
  - 尝试采用图像分割的方法，经过测试，CPU下推理速度太慢，暂时放弃
  - 目前采用的固定的二值化阈值
- [x] (2021-12-14)完善对应的英文文档
- [x] (2021-12-14)添加运行耗时基准
- [x] 添加具体参数说明
- [x] 制作项目Logo
- [ ] 更多的测试
