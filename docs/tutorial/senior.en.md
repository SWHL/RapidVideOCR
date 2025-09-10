---
comments: true
---

### 1. Install and use VideoSubFinder

- Download link: Windows & Linux ([videosubfinder](https://sourceforge.net/projects/videosubfinder/) / QQ group (706807542) shared files) | [Mac version](https://github.com/eritpchy/videosubfinder-cli)
- Tutorial: [Tutorial for extracting subtitle keyframes with VideoSubFinder](https://juejin.cn/post/7203362527082053691)
- The final `RGBImages` and `TXTImages` are usually in the installation directory for VideoSubFinder
- ✧ It is recommended to use `RGBImages` (thanks to [dyphire](https://github.com/dyphire) for the feedback in [#21](https://github.com/SWHL/RapidVideOCR/issues/21))

### 2. Install rapid_videocr

```bash linenums="1"
pip install rapid_videocr
```

### 3. Python usage

{{< tabs tabTotal="2">}}
{{% tab tabName="Only OCR" %}}

```python linenums="1"
from rapid_videocr import RapidVideOCR

# RapidVideOCRInput has two initialization parameters
# is_concat_rec: Use a single image for recognition or not. The default is False, which means that a single image is used for recognition by default.
# concat_batch: The number of images to be used in overlay is 10 by default and can be adjusted
# out_format: Output format selection, [srt, ass, txt, all], the default is all
# is_print_console: Whether to print the result, [0, 1], the default is 0 for not printing
ocr_input_params = RapidVideOCRInput(
is_batch_rec=False, ocr_params={"Global.with_paddle": True}
)
extractor = RapidVideOCR(ocr_input_params)

rgb_dir = "tests/test_files/RGBImages"
save_dir = "outputs"
save_name = "a"

# outputs/a.srt  outputs/a.ass  outputs/a.t
extractor(rgb_dir, save_dir, save_name=save_name)
```

{{% /tab %}}
{{% tab tabName="Extract + OCR" %}}

```python linenums="1"
from rapid_videocr import RapidVideoSubFinderOCR

vsf_exe = r"G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe"
extractor = RapidVideoSubFinderOCR(vsf_exe_path=vsf_exe, is_concat_rec=True)

# video_path can be directory path or video full path.
video_path = 'test_files/tiny/2.mp4'
save_dir = 'outputs'
extractor(video_path, save_dir)
```

{{% /tab %}}
{{< /tabs >}}

### 4. Command line usage

{{< tabs tabTotal="2">}}
{{% tab tabName="Only OCR" %}}

```bash linenums="1"
rapid_videocr -i RGBImages
```

{{% /tab %}}
{{% tab tabName="Extract + OCR" %}}

```bash linenums="1"
rapid_videocr -vsf G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe -video_dir G:\ProgramFiles\RapidVideOCR\test_files\tiny
```

{{% /tab %}}
{{< /tabs >}}

Parameter details:
<details>

```bash linenums="1"
$ rapid_videocr -h
usage: rapid_videocr [-h] [-video_dir VIDEO_DIR] [-i IMG_DIR] [-s SAVE_DIR]
            [-o {srt,ass,txt,all}] [--is_concat_rec] [-b CONCAT_BATCH] [-p]
            [-vsf VSF_EXE_PATH] [-c] [-r] [-ccti] [-ces CREATE_EMPTY_SUB]
            [-cscti CREATE_SUB_FROM_CLEARED_TXT_IMAGES]
            [-cstxt CREATE_SUB_FROM_TXT_RESULTS] [-ovocv] [-ovffmpeg] [-uc]
            [--start_time START_TIME] [--end_time END_TIME]
            [-te TOP_VIDEO_IMAGE_PERCENT_END]
            [-be BOTTOM_VIDEO_IMAGE_PERCENT_END]
            [-le LEFT_VIDEO_IMAGE_PERCENT_END]
            [-re RIGHT_VIDEO_IMAGE_PERCENT_END] [-gs GENERAL_SETTINGS]
            [-nthr NUM_THREADS] [-nocrthr NUM_OCR_THREADS]

optional arguments:
-h, --help            show this help message and exit

VideOCRParameters:
-video_dir VIDEO_DIR, --video_dir VIDEO_DIR
                        The full path of video or the path of video directory.
-i IMG_DIR, --img_dir IMG_DIR
                        The full path of RGBImages or TXTImages.
-s SAVE_DIR, --save_dir SAVE_DIR
                        The path of saving the recognition result. Default is
                        "outputs" under the current directory.
-o {srt,ass,txt,all}, --out_format {srt,ass,txt,all}
                        Output file format. Default is "all".
--is_concat_rec       Which mode to run (concat recognition or single
                        recognition). Default is False.
-b CONCAT_BATCH, --concat_batch CONCAT_BATCH
                        The batch of concating image nums in concat
                        recognition mode. Default is 10.
-p, --print_console   Whether to print the subtitle results to console. -p
                        means to print.

VSFParameters:
-vsf VSF_EXE_PATH, --vsf_exe_path VSF_EXE_PATH
                        The full path of VideoSubFinderWXW.exe.
-c, --clear_dirs      Clear Folders (remove all images), performed before
                        any other steps. Default is True
-r, --run_search      Run Search (find frames with hardcoded text (hardsub)
                        on video) Default is True
-ccti, --create_cleared_text_images
                        Create Cleared Text Images. Default is True
-ces CREATE_EMPTY_SUB, --create_empty_sub CREATE_EMPTY_SUB
                        Create Empty Sub With Provided Output File Name (*.ass
                        or *.srt)
-cscti CREATE_SUB_FROM_CLEARED_TXT_IMAGES, --create_sub_from_cleared_txt_images CREATE_SUB_FROM_CLEARED_TXT_IMAGES
                        Create Sub From Cleared TXT Images With Provided
                        Output File Name (*.ass or *.srt)
-cstxt CREATE_SUB_FROM_TXT_RESULTS, --create_sub_from_txt_results CREATE_SUB_FROM_TXT_RESULTS
                        Create Sub From TXT Results With Provided Output File
                        Name (*.ass or *.srt)
-ovocv, --open_video_opencv
                        open video by OpenCV (default). Default is True
-ovffmpeg, --open_video_ffmpeg
                        open video by FFMPEG
-uc, --use_cuda       use cuda
--start_time START_TIME
                        start time, default = 0:00:00:000 (in format
                        hour:min:sec:milisec)
--end_time END_TIME   end time, default = video length
-te TOP_VIDEO_IMAGE_PERCENT_END, --top_video_image_percent_end TOP_VIDEO_IMAGE_PERCENT_END
                        top video image percent offset from image bottom, can
                        be in range [0.0,1.0], default = 1.0
-be BOTTOM_VIDEO_IMAGE_PERCENT_END, --bottom_video_image_percent_end BOTTOM_VIDEO_IMAGE_PERCENT_END
                        bottom video image percent offset from image bottom,
                        can be in range [0.0,1.0], default = 0.0
-le LEFT_VIDEO_IMAGE_PERCENT_END, --left_video_image_percent_end LEFT_VIDEO_IMAGE_PERCENT_END
                        left video image percent end, can be in range
                        [0.0,1.0], default = 0.0
-re RIGHT_VIDEO_IMAGE_PERCENT_END, --right_video_image_percent_end RIGHT_VIDEO_IMAGE_PERCENT_END
                        right video image percent end, can be in range
                        [0.0,1.0], default = 1.0
-gs GENERAL_SETTINGS, --general_settings GENERAL_SETTINGS
                        general settings (path to general settings *.cfg file,
                        default = settings/general.cfg)
-nthr NUM_THREADS, --num_threads NUM_THREADS
                        number of threads used for Run Search
-nocrthr NUM_OCR_THREADS, --num_ocr_threads NUM_OCR_THREADS
                        number of threads used for Create Cleared TXT Images
```

</details>

### 5. View results

Go to the `save_dir` directory to view the results.

{{< alert context="info" text="If you want the video playback software to automatically mount the srt file or ass file, you need to change the srt or ass filename to be the same as the video file and put it in the same directory, or manually specify it." />}}
