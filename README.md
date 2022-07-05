<div align="center">
   <img src="assets/logo.png"  width="75%" height="75%">
</div>
<br/>

---

简体中文 | [English](./docs/README_en.md)

<p align="left">
    <a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/main/assets/RapidVideOCR.ipynb" target="_blank"><img src="./assets/colab-badge.svg" alt="Open in Colab"></a>
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

- 🐱如果想要识别**纯英文、日文**的字幕，可以在[`config_ocr.yaml`](./config_ocr.yaml)中更改对应模型和字典文件即可。
  - 纯英文模型
    ```yaml
     Rec:
         module_name: ch_ppocr_v2_rec
         class_name: TextRecognizer
         model_path: resources/models/en_number_mobile_v2. 0_rec_infer.onnx

         rec_img_shape: [3, 32, 320]
         rec_batch_num: 6
         keys_path: resources/rapid_ocr/en_dict.txt
    ```

  - 日文模型
    ```yaml
    Rec:
        module_name: ch_ppocr_v2_rec
        class_name: TextRecognizer
        model_path: resources/rapid_ocr/models/japan_rec_crnn.onnx

        rec_img_shape: [3, 32, 320]
        rec_batch_num: 6
        keys_path: resources/rapid_ocr/japan_dict.txt
    ```

### 仓库分支说明
- `add_remove_bg_module`:
  - 基于图像分割UNet算法来去除字幕图像背景图，只剩下文字内容，训练对应代码为[pytorch-unet](https://github.com/SWHL/pytorch-unet)
  - 没有并入主仓库原因：模型较大，处理速度较慢，同时泛化性能不是太好，有提升空间，可自行探索。
- `add_asr_module`:
  - 推理代码来源：[RapidASR](https://github.com/RapidAI/RapidASR/tree/main/python/base_paddlespeech)
  - 没有并入主仓库原因：处理速度较慢，配置环境复杂，效果较差，有提升空间，可自行探索。

### 更新日志（[more](./docs/changelog.md)）
#### ✨2022-06-26 update:
- 参数化配置相关参数，包括`rapid_ocr`和`rapid_videocr`两部分，更加灵活

#### 🌼2022-05-08 update
- 添加交互式确定二值化字幕图像阈值操作，仅仅支持Windows系统，可以通过`is_select_threshold=True`来使用
- 优化代码

### 整体框架
<div align="center">
   <img src="assets/RapidVideOCR-Framework.png"  width="75%" height="75%">
</div>

### 常见问题 [FAQ](./docs/FAQ.md)

### 视频OCR动态
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
1. 下载**RapidOCR**使用的模型和字典文件所在目录`rapidocr`([百度网盘](https://pan.baidu.com/s/1SFVxSS2rDtmjZfP_9iTHIw?pwd=trqi) | [Google Drive](https://drive.google.com/drive/folders/1cX8fbVe4_pCNI98QBIYOp09hU6aGWSZL?usp=sharing))

2. 将所下载的`rapid_ocr`目录放到当前`resources`下，具体目录结构如下：
   ```text
   resources/
   └── rapid_ocr
      ├── en_dict.txt
      ├── ppocr_keys_v1.txt
      └── models
          ├── ch_mobile_v2.0_rec_infer.onnx
          ├── ch_ppocr_mobile_v2.0_cls_infer.onnx
          └── ch_PP-OCRv2_det_infer.onnx
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
   - 当操作系统是Windows和参数`is_select_threshold=True`时，可以交互式选择二值化阈值
     - 左右滑动滑块，使得下面图中文字清晰显示，按`Enter`退出，需要选择三次
     - 示例：
       ![interactive_select_threshold](./assets/interactive_select_threshold.gif)
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


### [`config_videocr.yaml`](./config_videocr.yaml)中相关参数
|参数名称|取值范围|含义|
|:---|:---|:---|
|`batch_size`|`[1, all_frames]`|获取关键帧时，批量比较的batch大小，理论上，越大越快|
|`is_dilate`|`bool`|是否腐蚀字幕所在背景图像|
|`is_select_threshold`|`bool`|是否交互式选择二值化值|
|`subtitle_height`|`default:None`|字幕文本的高度,默认自动获取|
|`error_num`|`[0, 1]`， default:0.005|值越小，两张图之间差异点会更敏感|
|`output_format`|`['txt', 'srt', 'docx', 'all']`|输出最终字幕文件，`all`前面三个格式都输出|
|`time_start`|开始提取字幕的起始时间点|开始提取字幕的起始时间点, 示例：'00:00:00'|
|`time_end`|开始提取字幕的起始时间点|需要大于`time_start`，`-1`表示到最后， 示例：'-1'|
