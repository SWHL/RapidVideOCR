---
weight: 3701
title: "How can I do OCR for subtitles in languages other than Chinese and English?"
description: ""
icon: article
date: 2023-10-08
draft: false
---

### Introduction
- Currently, RapidVideOCR directly uses the default configuration of `rapidocr_onnxruntime`, so it can only do OCR for subtitles in Chinese and English.
- Since `rapidocr_onnxruntime` has an interface for passing in other multilingual recognition models, RapidVieOCR has scalability. This article is here to explain how to use it.
- This article takes the French OCR solution proposed in [discussions #40](https://github.com/SWHL/RapidVideOCR/discussions/40) as an example, and other languages can be done in the same way.

### 1. Correctly install and use RapidVideOCR
Please refer to this [link](https://swhl.github.io/RapidVideOCR/en/docs/tutorial/senior/)

### 2. Use PaddleOCR Convert tool to convert French recognition model to ONNX
{{< alert text="Refer to the tutorial [link](https://github.com/RapidAI/PaddleOCRModelConvert)" />}}

Using,
- Model path: `https://paddleocr.bj.bcebos.com/dygraph_v2.0/multilingual/french_mobile_v2.0_rec_infer.tar`,
- Dictionary path: `https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/dygraph/ppocr/utils/dict/french_dict.txt`

For model download links for other languages, please refer to: [paddleocr whl](https://files.pythonhosted.org/packages/8f/d0/1a2f9430f61781beb16556182baa938e8f93c8b46c27ad5865a5655fae05/paddleocr-2.7.0.3-py3-none-any.whl) in the source `paddleocr.py` file

For dictionary models, see: [link](https://github.com/PaddlePaddle/PaddleOCR/tree/799c144ab3b0b5d19a37c7e85c47e88ff27c643d/ppocr/utils/dict)

Finally, a French recognition model can be obtained: `french_mobile_v2.0_rec_infer.onnx`

### 3. OCR French subtitles
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
data-repo-id="MDEwOlJlcG9zaXRvcnk0MDU1ODkwMjk=" data-category="Q&A"
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
