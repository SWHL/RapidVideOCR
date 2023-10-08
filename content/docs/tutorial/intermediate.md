---
weight: 3502
title: "中级教程（python小白）"
description: ""
icon: local_library
date: 2023-10-08
draft: false
---

## 引言
- 本篇文章旨在帮助不会python编程的小伙伴，快速使用RapidVideOCR视频硬字幕提取工具。
- 可以运行的操作系统: `Windows | Mac | Linux``

## 配置环境
### 1. 安装VideoSubFinder软件（用于提取字幕关键帧）
-  [[RapidVideOCR周边] VideoSubFinder提取字幕关键帧教程](https://blog.csdn.net/shiwanghualuo/article/details/129174857?spm=1001.2014.3001.5501)

### 2. 安装python软件（用于运行RapidVideOCR）
{{< alert context="info" text="声明：以下部分图像来自[终极保姆教程之安装python的教程_3.10.7版本](https://www.cnblogs.com/zyc-666/p/16689739.html)" />}}

#### 1. 下载python安装包
打开python官网 → https://www.python.org，选择自己系统进入下载界面（VideoSubFinder工具目前只有Windows的）
<div align="center">
    <img src="https://camo.githubusercontent.com/0e8df5aedcb7ef493c9330db04e87a7b588300957c662386737c1f3852df7582/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f38616462323364653731663334626665396139323337376130343961373731342e706e67237069635f63656e746572">
</div>

#### 2. 找到自己想要的版本，
以python 3.10.7 为例。如果网速下载较慢的话，可以加入RapidVideOCR QQ群（706807542），群文件获取。
<div align="center">
    <img src="https://camo.githubusercontent.com/e208d3dcbe65b4b7e70d9b4aac83cb1ddc534d997777e5cddb3d6a38ed8ab7ae/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f61383330613232366539613234373435623038373963313166653263363034332e706e67237069635f63656e746572">
</div>

#### 3. 下载完成之后，双击打开这个exe，即可开始准备安装。
点击自定义安装，选择安装位置。同时，记得勾选最后一项`Add Python 3.10 to PATH`
<div align="center">
    <img src="https://camo.githubusercontent.com/31e44a4651201b39f9674a2bc3e5d8e82419cc73d681de6c29514003c2c0beae/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f65336336663939343966343934663665396266343832313632663662383764612e706e67237069635f63656e746572" width="80%">
</div>

#### 4. 直接点击下一步
<div align="center">
    <img src="https://camo.githubusercontent.com/6d2acb7814c8e924305e1941d55cbc33e2d24476b72b7d64a4fc2ed7542e4b25/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f39636638363533616135333934303666623732336163303165616439396165652e706e67237069635f63656e746572" width="80%">
</div>

#### 5. 勾选改路径
<div align="center">
    <img src="https://camo.githubusercontent.com/41018f5856ede2ac02ca80a270a41a1449f16a40c1ec837235f1cd47aadd1067/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f36653463343038303766383534393231613334363365323133343365363938662e706e67237069635f63656e746572" width="80%">
</div>

#### 6. 点击Install，等待安装完毕即可。
<div align="center">
    <img src="https://camo.githubusercontent.com/0a9055c53a23bdb7dfc4f3b9682e09fd01f1d3ddd4f4e17c82845991cb91e7ce/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f35313665613137333663663734343532623232656630663362636231363963612e706e67237069635f63656e746572" width="80%">
</div>

#### 7. `Win + r` 输入`cmd`，回车，进入命令窗口
<div align="center">
    <img src="https://camo.githubusercontent.com/845f93c9cbd1dc8ae02b49dd67a0b14ce817e07fbd6cdde76115fbf56e323ce3/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f38623237343037303036643434383134383039336437356632346330663462622e706e67237069635f63656e746572" width="60%">
</div>

#### 8. 输入python，看是否出现类似下图样子，如出现，证明安装成功
<div align="center">
    <img src="https://camo.githubusercontent.com/9df67f9efb0d37683ced44085e9cb0cf6376f3b59ccaf66d7eb240ead51b0dd9/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f61373461333166383733333834353362623863366138663831376164633138642e706e67237069635f63656e746572">
</div>

#### 9. 添加`Scripts`目录到环境变量中
-  `Win + q` 输入“编辑” → 点击**编辑系统环境变量**
    <div align="center">
        <img src="https://camo.githubusercontent.com/231e76a3857341f592e008257517cbd581b5b4b60164d1cea87af0e96eb1ff58/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f34653338323466356338653534666431613538366638383765646133366336392e706e67237069635f63656e746572">
    </div>

- 打开**环境变量** → **用户变量** → **Path** → **编辑**
    <div align="center">
        <img src="https://camo.githubusercontent.com/72c01f68a20f3fe083dfeb61bb9004b8ae24b2d9ca4257b2cc341eae4e73fd53/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f64613931373638326638643434363734623936656563333461303235666166642e706e67237069635f63656e746572">
    </div>

- 新建Python安装目录下的Script目录路径，如下图所示，记得点击保存哈。
<div align="center">
    <img src="https://camo.githubusercontent.com/28bd4e944f834d5e878db4c1e8b781698ffaa1ed09ccb29eed7d504dd37798e6/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f37313736386539343466623634363036623364336165323961393265653566662e706e67237069635f63656e746572">
</div>

### 3. 安装RapidVideOCR工具
#### 1. `Win + r` 输入`cmd`，回车，进入命令窗口
<div align="center">
    <img src="https://camo.githubusercontent.com/f87a24d66de7a385e46a9dbd25940d4a735dc9b6f4cf36337adfc00785427b15/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f62326230393839383264636534373865383730323766613730303934323966302e706e67237069635f63656e746572">
</div>

#### 2. 安装`rapid_videocr`
```bash {linenos=table}
pip install rapid_videocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
<div align="center">
    <img src="https://camo.githubusercontent.com/154f1949fd26afedb1d577d01e1295c8f69279a04182b97f9da7092052e91888/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f31363136636562633066356534363161626562653562323062623437366439322e706e67237069635f63656e746572">
</div>

#### 3. 测试是否安装成功，输入`rapid_videocr -h`,如果出现类似下图输出，则说明安装成功。
<div align="center">
    <img src="https://camo.githubusercontent.com/a785df6c909c40b260a3c5391827029b81f94d647b38c9dffec33a1fcfebb344/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f62393464653664396262663934656330383939363566353336386532626437622e706e67237069635f63656e746572">
</div>

#### 4. 命令行使用
`Win + r` 输入`cmd`，回车，进入命令行窗口

```bash {linenos=table}
rapid_videocr -i RGBImages -s result -m concat
```
其中`RGBImages`为VideoSubFinder软件生成，可以自定义，例如：`G:\ProgramFiles\_self\RapidVideOCR\test_files\RGBImages` 等等。

<div align="center">
    <img src="https://camo.githubusercontent.com/621eee585dd7a13607e1afad6b61aea322c1e9441603b894211c448ceac0e60c/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f35346132353539363130643434356238626265353234363635383464306234382e706e67237069635f63656e746572">
</div>

#### 5. 脚本使用
1. 在桌面上新建TXT文件，命名为`rapid_videocr.py`，注意后缀名改为`*.py`。
2. 用记事本打开，将以下代码拷贝到`rapid_videocr.py`里面
    ```python {linenos=table}
    from rapid_videocr import RapidVideOCR

    # RapidVideOCR有两个初始化参数
    # is_concat_rec: 是否用单张图识别，默认是False，也就是默认用单图识别
    # concat_batch: 叠图识别的图像张数，默认10，可自行调节
    # out_format: 输出格式选择，[srt, txt, all], 默认是 all
    # is_print_console: 是否打印结果，[0, 1], 默认是0，不打印
    extractor = RapidVideOCR(is_concat=False, out_format='all', is_print_console=False)

    rgb_dir = 'test_files/TXTImages'

    save_dir = 'result'
    extractor(rgb_dir, save_dir)
    ```
3. 更改`rgb_dir` 后面的目录为VideoSubFinder生成的`RGBImages`目录路径。
{{< tabs tabTotal="2">}}
{{% tab tabName="Windows下路径写法" %}}

```python {linenos=table}
rgb_dir = r'G:\ProgramFiles\_self\RapidVideOCR\test_files\RGBImages'
```

{{% /tab %}}
{{% tab tabName="Linux/Mac下路径写法" %}}

```python {linenos=table}
rgb_dir = 'test_files/TXTImages'
```

{{% /tab %}}
{{< /tabs >}}
4. `Win + r` 打开终端输入以下代码，回车执行即可。
    ```bash {linenos=table}
    $ cd Desktop
    $ python rapid_videocr.py
    ```
    <div align="center">
        <img src="https://camo.githubusercontent.com/4a6b1382cb984f9192d882203cc59affef8302570e8104659201be86a75c158c/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f33323932623831616430313634326561396638316362373031396263333131382e706e67">
    </div>
