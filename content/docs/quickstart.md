---
weight: 300
lastmod: "2022-08-10"
draft: false
author: "SWHL"
title: "快速开始"
icon: "rocket_launch"
description: "故事的开始，只需3步。"
toc: true
---

### 1. 安装
```bash {linenos=table}
pip install rapid_videocr
```

### 2. 使用
{{< tabs tabTotal="2">}}
{{% tab tabName="终端使用" %}}

```bash {linenos=table}
rapid_videocr -i test_files/RGBImages
```

{{% /tab %}}
{{% tab tabName="Python使用" %}}

```python {linenos=table}
from rapid_videocr import RapidVideOCR

extractor = RapidVideOCR(is_concat_rec=False,
                         out_format='all',
                         is_print_console=False)

rgb_dir = 'test_files/RGBImages'
save_dir = 'result'
extractor(rgb_dir, save_dir)
```
{{% /tab %}}
{{< /tabs >}}
