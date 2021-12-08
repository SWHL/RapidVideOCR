# RapidVideoOCR
- Modified from [videocr](https://github.com/apm1467/videocr)
- The part of OCR is accepted the [RapidOCR](https://github.com/RapidAI/RapidOCR).
- Currently, the project only supports subtitles appearing separately under the video. Like the following example:
  <div align="center">
    <img src="./assets/demo.jpg" width="50%" height="50%"/>
  </div>

#### TODO
- [ ] Adapt to the situation where subtitles appear on the video.
- [x] (2021-12-07) Fix the show problem of the tqdm package.
- [x] (2021-12-07) Organize the relevant parameters of the API.
- [x] (2021-12-06) The number of video frames cannot be divisible by batch_size.
- [x] (2021-12-05) Refactor the project code.
- [x] (2021-12-05) Less time to process the video.
  - Accept the Decord package to load frame of the video. The following table is a comparison of the time taken by OpenCV and Decord to extract all the frames in the same video.
      |Method|Cost time(s)|Total Frames|
      |:---: |:---:|:---:|
      |Decord|9.4021|5987|
      |OpenCV|721.5981|5987|
  - Use batch processing to compare the similarity between frames, which greatly speeds up video processing.

- [x] (2021-12-01) Refer the repo [**ClipVideo**](https://github.com/SWHL/ClipVideo). ~~Combined with video editing, given a text field, the program can automatically clip the correspoding video segment.~~

#### Use
1. Download the models and character dict of the [RapidOCR](https://github.com/RapidAI/RapidOCR) by the link [Extract code: drf1](https://pan.baidu.com/s/103kx0ABtU7Lif57cv397oQ) or [Google Drive](https://drive.google.com/drive/folders/1cjfawIhIP0Yq7_HjX4wtr_obcz7VTFtg?usp=sharing).
2. Put the models in the `resources/models`.
3. Run the `python example.py`, and the extracted results will be saved the `results.txt`. The following is the running process display:
   ```text
    Loading assets/1.mp4
    Get the key point: 100%|███████████████████| 303/303 [00:01<00:00, 282.91it/s]
    Extract content: 100%|████████████████████| 4/4 [00:01<00:00,  2.69it/s]
    ['0  00:00:04,458 -> 00:00:08,583 : 我要去杂货店买点东西\n要我帮你买点牛奶吗？\nIm going grocery shopping You want some\nmilk？',
     "1  00:00:05,083 -> 00:00:12,583 : 一个还是两个？\n是两个\n对吧？\nOne\nquartortwo？It'stwo，right？"]
   ```
