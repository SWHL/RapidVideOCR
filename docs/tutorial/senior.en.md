---
comments: true
hide:
  - toc
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
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

# RapidVideOCRInput initialization parameters:
# is_batch_rec: Use concat recognition or not. Default False (single-image recognition).
# batch_size: Number of images concatenated per batch in concat mode. Default 10.
# out_format: Output format [srt, ass, txt, all]. Default all.
# ocr_params: Custom params passed through to RapidOCR (dotted keys). Default None.
# log_level: Log level [debug/info/warning/error/critical]. Default info.
ocr_input_params = RapidVideOCRInput(
    is_batch_rec=False
)
extractor = RapidVideOCR(ocr_input_params)

rgb_dir = "tests/test_files/RGBImages"
save_dir = "outputs"
save_name = "a"

# outputs/a.srt  outputs/a.ass  outputs/a.txt
extractor(rgb_dir, save_dir, save_name=save_name)
```

{{% /tab %}}
{{% tab tabName="Extract + OCR" %}}

```python linenums="1"
from rapid_videocr import (
    RapidVideoSubFinderOCR,
    RapidVideOCRInput,
    VideoSubFinderInput,
)

vsf_exe = r"G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe"
vsf_input_params = VideoSubFinderInput(vsf_exe_path=vsf_exe)
ocr_input_params = RapidVideOCRInput(is_batch_rec=True)

extractor = RapidVideoSubFinderOCR(vsf_input_params, ocr_input_params)

# video_path can be directory path or video full path.
video_path = 'test_files/tiny/2.mp4'
save_dir = 'outputs'
extractor(video_path, save_dir)
```

{{% /tab %}}
{{< /tabs >}}

### 4. Inference backend (OCR defaults to CPU)

RapidVideOCR depends on RapidOCR 3.x (currently aligned to **3.10.0**). **OCR
inference runs on CPU by default** (RapidOCR's ONNX engine) — it works out of the
box with no extra dependencies and is more than sufficient for offline subtitle
extraction.

- To customize any RapidOCR parameter (e.g. language, or enabling GPU yourself),
  pass it through via `RapidVideOCRInput(ocr_params={...})` — it is forwarded
  to `RapidOCR` as-is, with no magic injection.
- The frame-extraction tool **VideoSubFinder** can still use its own GPU via
  `--vsf_use_cuda` (short `-vc`); this switch is unrelated to the OCR engine.

#### Enabling GPU (optional / advanced)

This project **ships no GPU dependencies by default** — OCR inference uses
RapidOCR's ONNX-CPU engine and works out of the box. If you do need GPU
acceleration, you must **install the matching GPU runtime yourself** and enable it
explicitly via `RapidVideOCRInput(ocr_params=...)`; this project performs no
automatic switching.

> ⚠️ Note
>
> - For offline subtitle extraction, CPU is usually sufficient. The GPU path is
>   **neither bundled nor tested in CI** — you are on your own to verify it.
> - `ocr_params` uses **dotted keys** (e.g. `EngineConfig.onnxruntime.use_cuda`).
>   Fields such as `engine_type` / `model_type` / `ocr_version` / `task_type` **must
>   be RapidOCR Enum objects** — passing a plain string raises `TypeError`.

**Option 1: enable CUDA on the ONNX engine (the default engine)**

The default engine is already `onnxruntime`; just turn `use_cuda` on — no need to
touch `engine_type`:

```bash
# install the GPU build of onnxruntime (replacing the CPU build) and set up CUDA / cuDNN
pip uninstall onnxruntime
pip install onnxruntime-gpu
```

```python
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

input_args = RapidVideOCRInput(
    ocr_params={"EngineConfig.onnxruntime.use_cuda": True},
)
extractor = RapidVideOCR(input_args)
```

**Option 2: switch to the Paddle engine and enable CUDA**

Install `paddlepaddle-gpu` (with CUDA), and set `engine_type` of `Det` / `Cls` /
`Rec` to `EngineType.PADDLE` (an Enum, not a string) before turning on Paddle's
`use_cuda`:

```bash
pip install paddlepaddle-gpu
```

```python
from rapidocr import EngineType
from rapid_videocr import RapidVideOCR, RapidVideOCRInput

input_args = RapidVideOCRInput(
    ocr_params={
        "Det.engine_type": EngineType.PADDLE,
        "Cls.engine_type": EngineType.PADDLE,
        "Rec.engine_type": EngineType.PADDLE,
        "EngineConfig.paddle.use_cuda": True,
    },
)
extractor = RapidVideOCR(input_args)
```

> 💡 Tip: if you keep the CPU runtime but set `use_cuda=True` (e.g. still using
> `onnxruntime` while enabling CUDA), the runtime will fail because it cannot find a
> CUDA execution provider. Keep the **runtime build** and the **switch** in sync.

### 5. Command line usage

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
            [-o {srt,ass,txt,all}] [--is_batch_rec] [-b BATCH_SIZE] [-p]
            [-vsf VSF_EXE_PATH] [-c] [-r] [-ccti] [-ces CREATE_EMPTY_SUB]
            [-cscti CREATE_SUB_FROM_CLEARED_TXT_IMAGES]
            [-cstxt CREATE_SUB_FROM_TXT_RESULTS] [-ovocv] [-ovffmpeg] [-vc]
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
--is_batch_rec        Which mode to run (concat recognition or single
                        recognition). Default is False.
-b BATCH_SIZE, --batch_size BATCH_SIZE
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
-vc, --vsf_use_cuda   (VideoSubFinder) use CUDA for frame extraction
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

### 6. View results

Go to the `save_dir` directory to view the results.

{{< alert context="info" text="If you want the video playback software to automatically mount the srt file or ass file, you need to change the srt or ass filename to be the same as the video file and put it in the same directory, or manually specify it." />}}
