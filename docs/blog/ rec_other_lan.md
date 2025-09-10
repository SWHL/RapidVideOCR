---
weight: 3701
title: "如何识别除中英文以外的其他字幕语言？"
description: ""
icon: article
date: 2023-10-08
draft: false
---

### 引言
- 当前，RapidVideOCR是直接使用的`rapidocr_onnxruntime`的默认配置，因此仅能识别中英文的字幕文字。
- 由于`rapidocr_onnxruntime`具备传入其他多语言识别模型的接口，因此RapidVieOCR具备了可扩展性，本篇文章特此来说明如何操作使用。
- 本篇文章以[discussions #40](https://github.com/SWHL/RapidVideOCR/discussions/40)中提出的识别法语字幕为例说明，其他语种同理可得。

### 1. 正确安装使用RapidVideOCR
请参考[link](https://swhl.github.io/RapidVideOCR/docs/tutorial/senior/)

### 2. 借助PaddleOCRConvert工具来转换法语识别模型为ONNX
{{< alert text="参考教程[link](https://github.com/RapidAI/PaddleOCRModelConvert)" />}}

其中，
- 模型路径：`https://paddleocr.bj.bcebos.com/dygraph_v2.0/multilingual/french_mobile_v2.0_rec_infer.tar`，
- 字典路径：`https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/dygraph/ppocr/utils/dict/french_dict.txt`

其他语言的模型下载地址参见：[paddleocr whl](https://files.pythonhosted.org/packages/8f/d0/1a2f9430f61781beb16556182baa938e8f93c8b46c27ad5865a5655fae05/paddleocr-2.7.0.3-py3-none-any.whl)源码中`paddleocr.py`文件中

字典链接参见：[link](https://github.com/PaddlePaddle/PaddleOCR/tree/799c144ab3b0b5d19a37c7e85c47e88ff27c643d/ppocr/utils/dict)

最终可以得到一个法语识别模型：`french_mobile_v2.0_rec_infer.onnx`

### 3. 识别法语字幕
{{< alert context="info" text="`rapid_videocr>=v3.0.0`" />}}

```python {linenos=table}
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

input_args = RapidVideOCRInput(
    is_batch_rec=False,
    ocr_params={"Rec.model_path": "french_mobile_v2.0_rec_infer.onnx"},
)
extractor = RapidVideOCR(input_args)

rgb_dir = "test_files/RGBImagesTiny"
save_dir = "outputs"
save_name = "a"

# outputs/a.srt  outputs/a.ass  outputs/a.txt
extractor(rgb_dir, save_dir, save_name=save_name)
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
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
