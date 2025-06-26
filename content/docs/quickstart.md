---
weight: 2000
lastmod: "2022-08-10"
draft: false
author: "SWHL"
title: "快速开始"
icon: "rocket_launch"
description: "故事的开始，只需3步。"
toc: true
---

{{< alert text="该库的输入必须是来自VideoSubFinder软件输出的RGBImages或者TXTImages目录的路径。VideoSubFinder教程：[link](https://blog.csdn.net/shiwanghualuo/article/details/129174857?spm=1001.2014.3001.5501)" />}}

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
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

input_args = RapidVideOCRInput(is_batch_rec=False)
extractor = RapidVideOCR(input_args)

rgb_dir = "tests/test_files/RGBImages"
save_dir = "outputs"
save_name = "a"

# outputs/a.srt  outputs/a.ass  outputs/a.txt
extractor(rgb_dir, save_dir, save_name=save_name)
```

{{% /tab %}}
{{< /tabs >}}

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
