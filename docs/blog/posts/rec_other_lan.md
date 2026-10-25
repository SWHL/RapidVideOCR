---
title: 如何识别其他语言字幕？
date: 2025-09-10
authors: [SWHL]
slug: how-to-rec-other-lan
categories:
  - General
comments: true
---


### 引言

- 当前，RapidVideOCR 默认使用 [RapidOCR](https://github.com/RapidAI/RapidOCR) 3.x（`rapidocr`）的默认配置，默认仅识别中英文的字幕文字。
- RapidVideOCR 通过 `RapidVideOCRInput(ocr_params=...)` 把任意 RapidOCR 参数**原样透传**给底层 `RapidOCR`，因此具备可扩展性：只需把其他语种的识别模型通过 `ocr_params` 传入即可，本工具不做任何魔法注入。
- 本篇文章以 [discussions #40](https://github.com/SWHL/RapidVideOCR/discussions/40) 中提出的识别法语字幕为例说明，其他语种同理可得。

### 1. 正确安装使用 RapidVideOCR

请参考教程 [link](https://swhl.github.io/RapidVideOCR/docs/tutorial/senior/)

### 2. 借助 PaddleOCRConvert 工具把法语识别模型转换为 ONNX

请参考教程 [link](https://github.com/RapidAI/PaddleOCRModelConvert)

其中，

模型路径：`https://paddleocr.bj.bcebos.com/dygraph_v2.0/multilingual/french_mobile_v2.0_rec_infer.tar`

字典路径：`https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/dygraph/ppocr/utils/dict/french_dict.txt`

其他语言的模型下载地址参见：[paddleocr whl](https://files.pythonhosted.org/packages/8f/d0/1a2f9430f61781beb16556182baa938e8f93c8b46c27ad5865a5655fae05/paddleocr-2.7.0.3-py3-none-any.whl) 源码中 `paddleocr.py` 文件

字典链接参见：[link](https://github.com/PaddlePaddle/PaddleOCR/tree/799c144ab3b0b5d19a37c7e88ff27c643d/ppocr/utils/dict)

RapidOCR 3.x 默认使用 ONNX 推理引擎，因此最终需要得到一个 ONNX 格式的识别模型：`french_mobile_v2.0_rec_infer.onnx`

### 3. 识别法语字幕

!!! note

    `rapid_videocr>=v3.0.0`（底层依赖 `rapidocr>=3.10.0`）

```python linenums="1"
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

input_args = RapidVideOCRInput(
    is_batch_rec=False,
    # 点号路径透传：把自定义法语识别模型传给 RapidOCR 的 Rec 模块
    ocr_params={"Rec.model_path": "french_mobile_v2.0_rec_infer.onnx"},
)
extractor = RapidVideOCR(input_args)

rgb_dir = "test_files/RGBImagesTiny"
save_dir = "outputs"
save_name = "a"

# outputs/a.srt  outputs/a.ass  outputs/a.txt
extractor(rgb_dir, save_dir, save_name=save_name)
```

!!! tip

    更多可透传的 RapidOCR 参数（语言、检测 / 分类模型、推理后端等）均为点号路径，例如 `Det.model_path`、`Cls.model_path` 等，详见 RapidOCR 文档与 [高级教程](https://swhl.github.io/RapidVideOCR/docs/tutorial/senior/)。
