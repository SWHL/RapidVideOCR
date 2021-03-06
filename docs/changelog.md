#### 🌼2022-05-08 update
- 添加交互式确定二值化字幕图像阈值操作，仅仅支持Windows系统，可以通过`is_select_threshold = True`来使用
- 优化代码

#### 🎉2022-05-03 update
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
