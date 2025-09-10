---
comments: true
hide:
  - navigation
  - toc
---

{{< alert text="The input for this library must be a path to an RGBImages or TXTImages directory outputted by VideoSubFinder. VideoSubFinder tutorial (note: this blog post is written in Chinese)：[link](https://blog.csdn.net/shiwanghualuo/article/details/129174857?spm=1001.2014.3001.5501)" />}}

### 1. Installation

```bash linenums="1"
pip install rapid_videocr
```

### 2. Usage

{{< tabs tabTotal="2">}}
{{% tab tabName="Terminal" %}}

```bash linenums="1"
rapid_videocr -i test_files/RGBImages
```

{{% /tab %}}
{{% tab tabName="Python" %}}

```python linenums="1"
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
