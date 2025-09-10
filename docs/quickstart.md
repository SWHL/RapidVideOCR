---
comments: true
hide:
  - navigation
  - toc
---


{{< alert text="该库的输入必须是来自VideoSubFinder软件输出的RGBImages或者TXTImages目录的路径。VideoSubFinder教程：[link](https://blog.csdn.net/shiwanghualuo/article/details/129174857?spm=1001.2014.3001.5501)" />}}

### 1. 安装

```bash linenums="1"
pip install rapid_videocr
```

### 2. 使用

{{< tabs tabTotal="2">}}
{{% tab tabName="终端使用" %}}

```bash linenums="1"
rapid_videocr -i test_files/RGBImages
```

{{% /tab %}}
{{% tab tabName="Python使用" %}}

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
