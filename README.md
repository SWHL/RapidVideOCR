# RapidVideOCR
简体中文 | [English](./README_en.md)

<p align="left">
    <a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/main/RapidVideOCR.ipynb" target="_blank"><img src="./assets/colab-badge.svg" alt="Open in Colab"></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/LICENSE-Apache%202-dfd.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/Python-3.6+-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
</p>

- 想法源自[videocr](https://github.com/apm1467/videocr)
- 更快更准确地提取内嵌在视频的字幕，并提供`txt|SRT|docx`三种格式
  - **更快**：
    - 采用[Decord](https://github.com/dmlc/decord)作为读取视频的库，更快;对于整个输入的视频，并不全部提取，因为存在大量重复字幕内容；
    - 这里采用预先找到出现不同字幕的关键帧，再送入OCR部分，因此更快
  - **更准**：整个项目完全为全离线CPU运行，OCR部分采用的是[RapidOCR](https://github.com/RapidAI/RapidOCR),依托于百度的PaddleOCR

#### TODO
- [x] (2021-12-08)完善对应的英文文档
- [x] (2021-12-08)添加运行耗时基准
- [ ] 添加具体参数说明
- [ ] 制作项目Logo
- [ ] 更多的测试
- [ ] 尝试接入语音转文本模型

#### 耗时基准
|配置|测试MP4|耗时(s)|
|:---:|:---:|:---:|
|`Intel(R) Core(TM) i7-6700 CPU @3.40GHz 3.41 GHz`|`assets/test_video/2.mp4`|4.681s|


#### 使用步骤
1. 下载RapidOCR使用的识别模型和字典文件([百度网盘:drf1](https://pan.baidu.com/s/103kx0ABtU7Lif57cv397oQ) | [Google Drive](https://drive.google.com/drive/folders/1cjfawIhIP0Yq7_HjX4wtr_obcz7VTFtg?usp=sharing))

2. 将下载好的models目录和`ppocr_keys_v1.txt`放到`resources`下，具体目录如下：
   ```text
   resources
      - models
        - ch_mobile_v2.0_rec_infer.onnx
        - ch_PP-OCRv2_det_infer.onnx
        - ch_ppocr_mobile_v2.0_cls_infer.onnx
      - ppocr_keys_v1.txt
   ```

3. 搭建运行环境
   - 推荐Windows,整个项目目前只在Windows下测试过
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
   - 输入日志如下：
     ```text
     Loading assets/test_video/2.mp4
     Get the key point: 100%|██████| 71/71 [00:03<00:00, 23.46it/s]
     Extract content: 100%|██████| 4/4 [00:03<00:00,  1.32it/s]
     The srt has been saved in the assets\test_video\2.srt.
     The txt has been saved in the assets\test_video\2.txt.
     The docx has been saved in the assets\test_video\2.docx.
     ```

5. 可以去**video所在目录**查看输出的文件