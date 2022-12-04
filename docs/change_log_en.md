#### 🎄2022-12-04 update:
- Add the function of interactively framing the subtitle position, which is enabled by default and is more useful. For details, please refer to the GIF image below. Thanks to @[Johndirr](https://github.com/Johndirr) for the suggestion.
- Optimize the code structure, put RapidOCR related models and configuration files in the `rapidocr` directory
- The configuration file of `rapidvideocr` is also placed in the corresponding directory.


#### ✨2022-06-26 update:
- Parameterized configuration of relevant parameters, including `rapid_ocr` and `rapid_videocr` parts, more flexible

#### 🌼2022-05-08 update:
- Add an interactive operation to determine the threshold value of the binarized subtitle image, only supports Windows system, can be used by `is_select_threshold = True`
- Optimized code

#### 🎉2022-05-03 update:
- Add GPU support, see the specific configuration tutorial: [onnxruntime-gpu version inference configuration](https://github.com/RapidAI/RapidOCR/blob/main/python/onnxruntime_infer/README.md#onnxruntime-gpu%E7%89%88%E6%8E%A8%E7%90%86%E9%85%8D%E7%BD%AE)
- Added support for Japanese, more languages can be supported, see: [List of supported languages](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99)

#### 💡2022-05-01 update:
- Add the speech recognition module. Since the decoding part of this module can only run on Linux and Mac, if you want to use this module, please use Linux and Mac.
- The current speech recognition code comes from the [RapidASR/python](https://github.com/RapidAI/RapidASR/tree/main/python/base_paddlespeech) section. Model from [PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/examples/aishell/asr0).
- After a simple test, the voice recognition module is not too accurate. -_-!

#### 2022-03-09 update:
- Add [FAQ](./FAQ.md) module.

#### 2021-12-14 update:
  - [x] Add specific parameter descrition.
  - [x] Make the project logo.
  - [x] Add sample vidoe to run time-consuming benchmark.