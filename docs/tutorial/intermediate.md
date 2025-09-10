---
comments: true
---


## 引言

- 本篇文章旨在帮助不会python编程的小伙伴，快速使用RapidVideOCR视频硬字幕提取工具。
- 可以运行的操作系统: `Windows | Mac | Linux`

## 配置环境

### 1. 安装VideoSubFinder软件（用于提取字幕关键帧）

- [[RapidVideOCR周边] VideoSubFinder提取字幕关键帧教程](https://blog.csdn.net/shiwanghualuo/article/details/129174857?spm=1001.2014.3001.5501)

### 2. 安装python软件（用于运行RapidVideOCR）

{{< alert context="info" text="声明：以下部分图像来自[终极保姆教程之安装python的教程_3.10.7版本](https://www.cnblogs.com/zyc-666/p/16689739.html)" />}}

#### 1. 下载python安装包

打开python官网 → <https://www.python.org>，选择自己系统进入下载界面（VideoSubFinder工具目前只有Windows的）>
<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/1.png">
</div>

#### 2. 找到自己想要的版本

以python 3.10.7 为例。如果网速下载较慢的话，可以加入RapidVideOCR QQ群（706807542），群文件获取。
<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/2.png">
</div>

#### 3. 下载完成之后，双击打开这个exe，即可开始准备安装

点击自定义安装，选择安装位置。同时，记得勾选最后一项`Add Python 3.10 to PATH`
<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/3.png" width=80%>
</div>

#### 4. 直接点击下一步

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/4.png" width=80%>
</div>

#### 5. 勾选改路径

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/5.png" width=80%>
</div>

#### 6. 点击Install，等待安装完毕即可

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/6.png" width=80%>
</div>

#### 7. `Win + r` 输入`cmd`，回车，进入命令窗口

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/7.png" width=80%>
</div>

#### 8. 输入python，看是否出现类似下图样子，如出现，证明安装成功

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/8.png">
</div>

#### 9. 添加`Scripts`目录到环境变量中

- `Win + q` 输入“编辑” → 点击**编辑系统环境变量**
    <div align="center">
        <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/9.png" width=80%>
    </div>

- 打开**环境变量** → **用户变量** → **Path** → **编辑**
    <div align="center">
        <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/10.png">
    </div>

- 新建Python安装目录下的Script目录路径，如下图所示，记得点击保存哈。

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/11.png">
</div>

### 3. 安装RapidVideOCR工具

#### 1. `Win + r` 输入`cmd`，回车，进入命令窗口

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/12.png">
</div>

#### 2. 安装`rapid_videocr`

```bash linenums="1"
pip install rapid_videocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/13.png">
</div>

#### 3. 测试是否安装成功，输入`rapid_videocr -h`,如果出现类似下图输出，则说明安装成功

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/14.png">
</div>

#### 4. 命令行使用

`Win + r` 输入`cmd`，回车，进入命令行窗口

```bash linenums="1"
rapid_videocr -i RGBImages -s result -m concat
```

其中`RGBImages`为VideoSubFinder软件生成，可以自定义，例如：`G:\ProgramFiles\_self\RapidVideOCR\test_files\RGBImages` 等等。

<div align="center">
    <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/15.png">
</div>

#### 5. 脚本使用

1. 在桌面上新建TXT文件，命名为`rapid_videocr.py`，注意后缀名改为`*.py`。
2. 用记事本打开，将以下代码拷贝到`rapid_videocr.py`里面

    ```python linenums="1"
    from rapid_videocr import RapidVideOCR, RapidVideOCRInput

    # RapidVideOCRInput有两个初始化参数
    # is_concat_rec: 是否用单张图识别，默认是False，也就是默认用单图识别
    # concat_batch: 叠图识别的图像张数，默认10，可自行调节
    # out_format: 输出格式选择，[srt, ass, txt, all], 默认是 all
    # is_print_console: 是否打印结果，[0, 1], 默认是0，不打印
    input_args = RapidVideOCRInput(
        is_batch_rec=False, ocr_params={"Global.with_paddle": True}
    )
    extractor = RapidVideOCR(input_args)

    rgb_dir = "tests/test_files/RGBImages"
    save_dir = "outputs"
    save_name = "a"

    # outputs/a.srt  outputs/a.ass  outputs/a.t
    extractor(rgb_dir, save_dir, save_name=save_name)
    ```

3. 更改`rgb_dir` 后面的目录为VideoSubFinder生成的`RGBImages`目录路径。
{{< tabs tabTotal="2">}}
{{% tab tabName="Windows下路径写法" %}}

```python linenums="1"
rgb_dir = r'G:\ProgramFiles\_self\RapidVideOCR\test_files\RGBImages'
```

{{% /tab %}}
{{% tab tabName="Linux/Mac下路径写法" %}}

```python linenums="1"
rgb_dir = 'test_files/TXTImages'
```

{{% /tab %}}
{{< /tabs >}}
4. `Win + r` 打开终端输入以下代码，回车执行即可。
    ```bash linenums="1"
    $ cd Desktop
    $ python rapid_videocr.py
    ```
    <div align="center">
        <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/16.png">
    </div>
