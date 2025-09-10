---
comments: true
---

### 📣 Subsequent update logs will be moved to [Release](https://github.com/SWHL/RapidVideOCR/releases), and will no longer be updated here

#### 🚩2023-10-08 v2.2.8 update

- Adapt the relevant parameters of `rapidocr_onnxruntime`, which can be passed in through the RapidVideOCR class, so as to more flexibly specify models of different languages.

#### ♦ 2023-08-05 v2.2.4 update

- Fix the index error in batch recognition mode.

- Add a logging module to facilitate the use of the desktop version, quickly record problems, and facilitate feedback.

#### 🛶2023-07-19 v2.2.3 update

- Added adaptation to VSF parameters. When in command line mode and during class initialization, you can specify the same-name parameters of the VSF command. For detailed usage, please refer to [link](https://github.com/SWHL/RapidVideOCR/wiki/RapidVideOCR%E9%AB%98%E7%BA%A7%E6%95%99%E7%A8%8B%EF%BC%88%E6%9C%89python%E5%9F%BA%E7%A1%80%E7%9A%84%E5%B0%8F%E4%BC%99%E4%BC%B4%EF%BC%89)

#### 🤓2023-07-08 v2.2.2 update

- Fixed the problem that Chinese paths cannot be read during batch recognition
- Fixed the problem of skipping in SRT when missing axes. Currently, when an axis fails to be recognized, a position will be vacated for easy proofreading.
- Keep the intermediate results of VSF recognition

#### 🐲2023-06-22 v2.2.0 update

- This version is compatible with `v2.1.x`, which means that the previous usage is still possible.
- Integrate VSF's CLI into the library, just specify the full path of `VideoSubFinderWXW.exe`.
- Added batch recognition function, specify the video directory, and automatically extract all video subtitles in the directory
- For usage examples, see: [demo.py](https://github.com/SWHL/RapidVideOCR/blob/main/demo.py)

#### 😀2023-05-12 v2.1.7 update

- Optimized code
- Added `save_name` parameter, which can flexibly specify the name of the saved `srt | txt` file, the default is `result`

#### 🐱2023-03-27 v2.1.6 update

- Fixed the timeline misalignment problem, see [issue 23](https://github.com/SWHL/RapidVideOCR/issues/23) for details

#### 👽2023-03-23 v2.1.5 update

- Added control parameter `is_print_console` for printing to the screen
- Adjust the `out_format` parameter position to the initialization class

#### 😀2023-03-14 v2.1.3 update

- Fix the error when passing in the `TXTImages` directory and identifying duplicate characters

#### 😜2023-03-12 v2.1.2 update

- Fix index error, [#22](https://github.com/SWHL/RapidVideOCR/issues/22)

#### 🎢2023-03-11 v2.1.1 update

- Fix the difference between single image recognition and previous versions

- The default recognition mode is changed to single image recognition. Whether to use duplicate image recognition is up to you

#### 🥇2023-03-10 v2.1.0 update

- Added duplicate character recognition function, faster, and the default is duplicate character recognition function

#### 🎈2023-03-02 v2.0.5~7 update

- Fix format errors in generated srt files, [#19](https://github.com/SWHL/RapidVideOCR/issues/19)

#### 🎫2023-02-17 v2.0.4 update

- Optimized passing in the `TXTImages` directory. Compared with passing in `RGBImages`, it will be faster and more accurate. It is recommended to pass in the `TXTImages` directory

#### 💎2023-02-17 v2.0.2 update

- Fix the problem of missing spaces in peer subtitle recognition

#### 🎈2023-01-29 v1.1.10 update

- Fix the error of empty index when converting frame index to timestamp

#### 🧨2023-01-28 v1.1.9 update

- Fix the problem of timeline misalignment

#### 👊 2023-01-15 v1.1.4 update

- Add the option of outputting txt format. Currently, the v1.1.4 version outputs srt and txt formats by default

- Add the option to adjust the box size of subtitle selection according to the screen size of the running program

#### 🌈2023-01-10 v1.0.3 update

- Replace decord with OpenCV because decord has a memory leak when processing MP4. For details, see: [#208](https://github.com/dmlc/decord/issues/208)

#### 🎄2022-12-04 update

- Added interactive subtitle positioning function, which is enabled by default and is more user-friendly. For details, please refer to the GIF below. Thanks to @[Johndirr](https://github.com/Johndirr) for the suggestion.
- Optimize the code structure, put RapidOCR related models and configuration files in the `rapidocr` directory
- The configuration files of `rapidvideocr` are also placed in the corresponding directory

#### 🌼2022-05-08 update

- Add interactive determination of the threshold of the binary subtitle image, which only supports Windows and can be used by `is_select_threshold = True`
- Optimize the code

#### 🎉2022-05-03 update

- Add GPU support, for specific configuration tutorials, see: [onnxruntime-gpu version inference configuration](https://github.com/RapidAI/RapidOCR/blob/main/python/onnxruntime_infer/README.md#onnxruntime-gpu%E7%89%88%E6%8E%A8%E7%90%86%E9%85%8D%E7%BD%AE)
- Added support for Japanese, which can support more languages. For details, see: [Supported Language List](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99)

#### 💡2022-05-01 update

- Added speech module part is located in the branch `asr_module`

- Added speech recognition module. Since the decoding part of this module can only run on Linux and Mac, if you want to use this module, please use Linux and Mac.
- Currently, the speech recognition code comes from the [RapidASR/python](https://github.com/RapidAI/RapidASR/tree/main/python/base_paddlespeech) part. The model comes from [PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/examples/aishell/asr0)
- After a simple test, the speech recognition module is not very accurate. -_-!

#### 2022-03-09 update

- Added [FAQ module](./faq.md) to help everyone skip common small problems

#### 2021-12-14 update

- [x] Background removal is not effective, resulting in the loss of some frames

- Tried to use the image segmentation method. After testing, the inference speed under CPU is too slow, so it is temporarily abandoned

- Currently using a fixed binary threshold

- [x] (2021-12-14) Improve the corresponding English document

- [x] (2021-12-14) Add running time benchmark

- [x] Add specific parameter description

- [x] Make a project logo

- [ ] More tests
