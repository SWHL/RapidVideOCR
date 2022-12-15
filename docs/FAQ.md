### 常见问题

#### Q2: 如果想识别其他语言字幕怎么办？
**A**: 🐱如果想要识别**纯英文、日文、韩文**等字幕，可以在[`config_ocr.yaml`](./rapid_ocr/config_ocr.yaml)中更改对应模型文件即可。
  - 纯英文模型
    ```yaml
    Rec:
        module_name: ch_ppocr_v3_rec
        class_name: TextRecognizer
        model_path: models/en_number_mobile_v2.0_rec_infer.onnx
    ```
  - 日文模型
    ```yaml
    Rec:
        module_name: ch_ppocr_v3_rec
        class_name: TextRecognizer
        model_path: models/japan_rec_crnn.onnx
    ```

#### Q1: 装完环境之后，运行`python main.py`之后，报错**OSError: [WinError 126] 找不到指定的模組**
**A**: 原因是Shapely库没有正确安装，如果是在Windows，可以在[Shapely whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)下载对应的whl包，离线安装即可；另外一种解决办法是用conda安装也可。(@[hongyuntw](https://github.com/hongyuntw))
