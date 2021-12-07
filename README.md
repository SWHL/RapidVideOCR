# RapidVideoOCR
- The `main` branch is the Decord version, it's faster than the OpenCV version. The OpenCV version is in the branch `opencv_version`.
- Modified from [videocr](https://github.com/apm1467/videocr)
- The part of OCR is accepted the [RapidOCR](https://github.com/RapidAI/RapidOCR).
- Currently, the project only supports subtitles appearing separately under the video. Like the following example:
  <div align="center">
    <img src="./assets/demo.jpg" width="50%" height="50%"/>
  </div>

#### TODO
- [ ] Adapt to the situation where subtitles appear on the video.
- [x] Fix the show problem of the tqdm package.
- [x] Organize the relevant parameters of the API.
- [x] (2021-12-06)The number of video frames cannot be divisible by batch_size.
- [x] (2021-12-05)Refactor the project code.
- [x] (2021-12-05)Less time to process the video.
  - Accept the Decord package to load frame of the video. The following table is a comparison of the time taken by OpenCV and Decord to extract all the frames in the same video.
      |Method|Cost time(s)|Total Frames|
      |:---: |:---:|:---:|
      |Decord|9.4021|5987|
      |OpenCV|721.5981|5987|
  - Use batch processing to compare the similarity between frames, which greatly speeds up video processing.

- [x] (2021-12-01)Refer the repo [**ClipVideo**](https://github.com/SWHL/ClipVideo). ~~Combined with video editing, given a text field, the program can automatically clip the correspoding video segment.~~

#### Use
1. Install the rapidocr package by the following:
   ```shell
   pip install https://github.com/RapidAI/RapidOCR/raw/main/release/python_sdk/sdk_rapidocr_v1.0.0/rapidocr-1.0.0-py3-none-any.whl
   ```
3. Download the models and character dict of the RapidOCR by the link [Extract code: drf1](https://pan.baidu.com/s/103kx0ABtU7Lif57cv397oQ) or [Google Drive](https://drive.google.com/drive/folders/1cjfawIhIP0Yq7_HjX4wtr_obcz7VTFtg?usp=sharing)
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
