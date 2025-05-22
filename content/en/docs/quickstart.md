---
weight: 2000
lastmod: "2022-08-10"
draft: false
author: "SWHL"
title: "Quickstart"
icon: "rocket_launch"
description: "Begin your story, with only 3 steps."
toc: true
---

{{< alert text="The input for this library must be a path to an RGBImages or TXTImages directory outputted by VideoSubFinder. VideoSubFinder tutorial (note: this blog post is written in Chinese)：[link](https://blog.csdn.net/shiwanghualuo/article/details/129174857?spm=1001.2014.3001.5501)" />}}

### 1. Installation

```bash {linenos=table}
pip install rapid_videocr
```

### 2. Usage

{{< tabs tabTotal="2">}}
{{% tab tabName="Terminal" %}}

```bash {linenos=table}
rapid_videocr -i test_files/RGBImages
```

{{% /tab %}}
{{% tab tabName="Python" %}}

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
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>

