<div align="center">
   <img src="assets/logo.png"  width="75%" height="75%">
</div>
<br/>

---

简体中文 | [English](./README_en.md)

<p align="left">
    <a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/main/RapidVideOCR.ipynb" target="_blank"><img src="./assets/colab-badge.svg" alt="Open in Colab"></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/LICENSE-Apache%202-dfd.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/Python-3.6+-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
</p>

- 支持字幕语言：中文 | 英文 | 日文 （其他可以支持的语言参见：[支持语种列表](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99))

- 想法源自 [videocr](https://github.com/apm1467/videocr)
- 可加入QQ群：**706807542**
- 更快更准确地提取内嵌在视频的字幕，并提供`txt|SRT|docx`三种格式
  - **更快**：
    - 采用[Decord](https://github.com/dmlc/decord)作为读取视频的库，更快;对于整个输入的视频，并不全部提取，因为存在大量重复字幕内容；
    - 这里采用预先找到出现不同字幕的关键帧，再送入OCR部分，因此更快
  - **更准**：整个项目完全为全离线CPU运行，OCR部分采用的是[RapidOCR](https://github.com/RapidAI/RapidOCR)，模型均来自[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.4/README_ch.md#pp-ocr%E7%B3%BB%E5%88%97%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8%E6%9B%B4%E6%96%B0%E4%B8%AD)。
    - 当然也可以在GPU运行，只要根据机器配置，安装对应版本的`onnxruntime-gpu`，即可自动在英伟达显卡上运行。具体教程参见：[onnxruntime-gpu版推理配置](https://github.com/RapidAI/RapidOCR/blob/main/python/onnxruntime_infer/README.md#onnxruntime-gpu%E7%89%88%E6%8E%A8%E7%90%86%E9%85%8D%E7%BD%AE)
  - **更方便**：采用大小仅为2M左右的ONNXRuntime推理引擎，不安装PaddlePaddle框架，部署更加方便

- 🐱如果想要识别**纯英文、日文**的字幕，可以在`main.py`中更改对应模型和字典文件即可。
  ```python
  det_model_path = "resources/models/ch_PP-OCRv2_det_infer.onnx"
  cls_model_path = "resources/models/ch_ppocr_mobile_v2.0_cls_infer.onnx"

  # 纯英文模型
  rec_model_path = "resources/models/en_number_mobile_v2.0_rec_infer.onnx"
  dict_path = "resources/en_dict.txt"

  # 日文
  rec_model_path = "resources/rapid_ocr/models/japan_rec_crnn.onnx"
  dict_path = "resources/rapid_ocr/japan_dict.txt"
  ```

### 分支说明
- `add_remove_bg_module`: 基于图像分割UNet算法来去除字母图像背景图，只剩下文字内容，训练对应代码为[pytorch-unet](https://github.com/SWHL/pytorch-unet)

### 更新日志
#### 🎉2022-05-03 update
- 添加GPU支持，具体配置教程参见：[onnxruntime-gpu版推理配置](https://github.com/RapidAI/RapidOCR/blob/main/python/onnxruntime_infer/README.md#onnxruntime-gpu%E7%89%88%E6%8E%A8%E7%90%86%E9%85%8D%E7%BD%AE)
- 添加日文的支持，可以支持更多语种，具体参见：[支持语种列表](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99)

#### 💡2022-05-01 update:
- 添加语音模块部分位于分支`asr_module`
- 添加语音识别模块，由于该模块中解码部分只能在Linux和Mac上运行，因此如果想要使用该模块，请在Linux和Mac上。
- 目前语音识别代码来自[RapidASR/python](https://github.com/RapidAI/RapidASR/tree/main/python/base_paddlespeech)部分。模型来自[PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/examples/aishell/asr0)
- 经过简单测试，语音识别模块不是太准。-_-!

#### 2022-03-09 update:
- 添加[常见问题模块](./FAQ.md)，可以帮助大家跳过常见的小问题

#### 2021-12-14 update:
- [x] 背景去除效果不好，导致丢失某些帧
  - 尝试采用图像分割的方法，经过测试，CPU下推理速度太慢，暂时放弃
  - 目前采用的固定的二值化阈值
- [x] (2021-12-14)完善对应的英文文档
- [x] (2021-12-14)添加运行耗时基准
- [x] 添加具体参数说明
- [x] 制作项目Logo
- [ ] 更多的测试


### 整体框架
<div align="center">
   <img src="assets/RapidVideOCR-Framework.png"  width="75%" height="75%">
</div>

### 常见问题 [FAQ](./FAQ.md)

### 视频OCR
#### 比赛动态
- [【2022-03-13 update】ICPR 2022 | 多模态字幕识别竞赛正式启动！](https://mp.weixin.qq.com/s/HxcrgXOQmaqDpPsGN1PFjw)

#### 学术动态
- [【NeurIPS2021】A Bilingual, OpenWorld Video Text Dataset and End-to-end Video Text Spotter with Transformer](https://arxiv.org/abs/2112.04888) | [博客解读](https://blog.csdn.net/shiwanghualuo/article/details/122712872?spm=1001.2014.3001.5501)
- [【ACM MM 2019】You only recognize once: Towards fast video text spotting](https://arxiv.org/pdf/1903.03299)

### 未来的应用场景探索
- 基于视频文本OCR的视频内容理解，结合图像特征+图像中文本特征
- 视频字幕自动翻译
- 基于视频文本特征的视频检索

### 耗时基准
|配置|测试MP4|总帧数|每帧大小|耗时(s)|
|:---:|:---:|:---:|:---:|:---:|
|`Intel(R) Core(TM) i7-6700 CPU @3.40GHz 3.41 GHz`|`assets/test_video/2.mp4`|71|1920x800|4.681s|
|`Intel(R) Core(TM) i5-4210M CPU @2.60GHz 2.59 GHz`|`assets/test_video/2.mp4`|71|1920x800|6.832s|


### 使用步骤
1. 下载RapidOCR使用的识别模型和字典文件([百度网盘:drf1](https://pan.baidu.com/s/103kx0ABtU7Lif57cv397oQ) | [Google Drive](https://drive.google.com/drive/folders/1ttDQKp8-MhF1ZqyYZR5LJRBaqu8nhp2C?usp=sharing))

2. 将下载好的`models`目录和`ppocr_keys_v1.txt`放到`resources/rapid_ocr`下，具体目录如下：
   ```text
   resources/
   ├── rapid_asr
   │   ├── models
   │   │   ├── asr0_deepspeech2_online_aishell_ckpt_0.2.0.onnx
   │   │   └── language_model
   │   │       └── zh_giga.no_cna_cmn.prune01244.klm
   │   └── model.yaml
   └── rapid_ocr
      ├── en_dict.txt
      ├── models
      │   ├── ch_mobile_v2.0_rec_infer.onnx
      │   ├── ch_ppocr_mobile_v2.0_cls_infer.onnx
      │   └── ch_PP-OCRv2_det_infer.onnx
      └── ppocr_keys_v1.txt
   ```

3. 搭建运行环境
   - 推荐Windows，整个项目目前只在Windows下测试过
   - 安装相应的包
      ```bash
      cd RapidVideOCR

      pip install -r requirements.txt -i https://pypi.douban.com/simple/
      ```
   - 也可以在[Google Colab](https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/main/RapidVideOCR.ipynb)下快速查看运行Demo。

4. 运行
   - 代码
      ```bash
      cd RapidVideOCR

      python main.py
      ```
   - 输出日志如下：
     ```text
     Loading assets/test_video/2.mp4
     Get the key frame: 100%|██████| 71/71 [00:03<00:00, 23.46it/s]
     Extract content: 100%|██████| 4/4 [00:03<00:00,  1.32it/s]
     The srt has been saved in the assets\test_video\2.srt.
     The txt has been saved in the assets\test_video\2.txt.
     The docx has been saved in the assets\test_video\2.docx.
     ```

5. 可以去**video所在目录**查看输出的文件

6. 想要使用asr模块,怎么做？
   - 首先去参考[RapidASR](https://github.com/RapidAI/RapidASR/tree/main/python/base_paddlespeech)的README部分。将其中对应模型放到`resources/rapid_asr`目录下，具体目录结构参考上面给出的。
   - 在`main.py`中给出了`asr`模块类实例的用法。如果不想使用，直接将`ExtractSubtitle`中参数`asr_executor=None`即可。

### `main.py`中相关参数
|参数名称|取值范围|含义|
|:---:|:---:|:---:|
|batch_size|[1, all_frames]|获取关键帧时，批量比较的batch大小，理论上，越大越快|
|is_dilate|bool|是否腐蚀字幕所在背景图像|
|subtitle_height|default:None|字幕文本的高度,默认自动获取|
|error_num|[0, 1]， default:0.005|值越小，两张图之间差异点会更敏感|
|output_format|['txt', 'srt', 'docx', 'all']|输出最终字幕文件，`all`前面三个格式都输出|
|time_start|整个视频所有的时间点|开始提取字幕的起始时间点|
|time_end|整个视频所有的时间点,大于time_start, -1表示到最后|结束提取字幕的终止时间点|
