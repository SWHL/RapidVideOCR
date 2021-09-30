# VideoOCR
- Forked from [videocr](https://github.com/apm1467/videocr)

#### Use
1. Download the RapidOCR whl package with the `https://github.com/RapidAI/RapidOCR/blob/main/release/python_sdk/sdk_rapidocr_v1.0.0/rapidocr-1.0.0-py3-none-any.whl`
2. `pip install rapidocr-1.0.0-py3-none-any.whl`
3. Download the models and character dict of the RapidOCR by the link [Extract code: drf1](https://pan.baidu.com/s/103kx0ABtU7Lif57cv397oQ)
4. Put the models in the `resources/models`
5. `python example.py`
   ```text
    Extract: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 304/304 [01:30<00:00,  3.35it/s]
    0
    00:00:00,583 --> 00:00:04,375
    我要去杂货店买点东西要我帮你买点牛奶吗？
    Im going grocery shopping.Youwant some milk？
    1
    00:00:08,000 --> 00:00:08,541
    个还是两个？是两个
    对吧？
    Onequart ortwo？It'stwo，right？
   ```
