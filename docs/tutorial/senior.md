---
comments: true
hide:
  - toc
---

### 1. 安装使用VideoSubFinder软件

下载地址：Windows & Linux ([videosubfinder官网](https://sourceforge.net/projects/videosubfinder/) / QQ群（706807542）共享文件) | [Mac版](https://github.com/eritpchy/videosubfinder-cli)

使用教程：[VideoSubFinder提取字幕关键帧教程](https://juejin.cn/post/7203362527082053691)

最终生成的`RGBImages`和`TXTImages`目录一般会在软件安装目录下

✧ 推荐用`RGBImages`目录中图像（感谢小伙伴[dyphire](https://github.com/dyphire)在[#21](https://github.com/SWHL/RapidVideOCR/issues/21)的反馈）

### 2. 安装rapid_videocr

```bash linenums="1"
pip install rapid_videocr
```

### 3. Python使用

=== "Only OCR"

    ```python linenums="1"
    from rapid_videocr import RapidVideOCR, RapidVideOCRInput

    # RapidVideOCRInput 初始化参数：
    # is_batch_rec: 是否用叠图(concat)识别，默认 False（单图识别）
    # batch_size: 叠图识别时每批拼接的图像张数，默认 10
    # out_format: 输出格式 [srt, ass, txt, all]，默认 all
    # ocr_params: 透传给 RapidOCR 的自定义参数（点号路径），默认 None
    # log_level: 日志级别 [debug/info/warning/error/critical]，默认 info
    input_args = RapidVideOCRInput(
        is_batch_rec=False
    )
    extractor = RapidVideOCR(input_args)

    rgb_dir = "tests/test_files/RGBImages"
    save_dir = "outputs"
    save_name = "a"

    # outputs/a.srt  outputs/a.ass  outputs/a.txt
    extractor(rgb_dir, save_dir, save_name=save_name)
    ```

=== "Extract + OCR"

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

### 4. 推理后端（OCR 默认 CPU）

RapidVideOCR 依赖 RapidOCR 3.x（已适配至 3.10.0）。**OCR 推理默认走 CPU**（RapidOCR 的 ONNX 引擎），开箱即用、无需额外依赖，对字幕提取这类离线任务完全够用。

- 如需自定义 RapidOCR 的任意参数（例如指定语言、或自行开启 GPU），可通过
  `RapidVideOCRInput(ocr_params={...})` 原样透传给 `RapidOCR`，本项目不做任何魔法注入。
- 抽帧工具 **VideoSubFinder** 仍可通过 `--vsf_use_cuda`（短写 `-vc`）开启其自身的 GPU
  加速，该开关与 OCR 推理引擎无关。

#### 启用 GPU（可选 / 进阶）

本项目**默认不内置任何 GPU 依赖**，OCR 推理走 RapidOCR 的 ONNX-CPU 引擎，开箱即用。如果你确有 GPU 加速需求，需要**自行安装对应的 GPU 运行时**，并通过 `RapidVideOCRInput(ocr_params=...)` 显式开启——本项目不做任何自动切换。

> ⚠️ 注意
>
> - 对字幕提取这类离线任务，CPU 通常已足够；GPU 路径我们**不内置、也不在 CI 中测试**，需自行验证。
> - `ocr_params` 使用**点号路径**（如 `EngineConfig.onnxruntime.use_cuda`）。其中
>   `engine_type` / `model_type` / `ocr_version` / `task_type` 这类字段**必须是 RapidOCR 的 Enum 对象**，
>   传字符串会直接报错（`TypeError`）。

**方式一：ONNX 引擎（默认引擎）开启 CUDA**

默认引擎就是 `onnxruntime`，只需把 `use_cuda` 打开即可，无需改动 `engine_type`：

```bash
# 先自行安装 GPU 版 onnxruntime（替换掉 CPU 版），并配好 CUDA / cuDNN
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

**方式二：切到 Paddle 引擎开启 CUDA**

需先安装 `paddlepaddle-gpu`（并配好 CUDA），且必须把 `Det` / `Cls` / `Rec` 的 `engine_type`
都改为 `EngineType.PADDLE`（注意是 Enum，不是字符串），再打开 Paddle 的 `use_cuda`：

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

> 💡 提示：若只装了 CPU 版运行时却把 `use_cuda` 设为 `True`（例如仍用 `onnxruntime`
> 却开启 CUDA），运行时会因找不到 CUDA 执行提供器而报错。请务必让「运行时版本」与「开关」保持一致。

### 5. 命令行使用

=== "Only OCR"

    ```bash linenums="1"
    rapid_videocr -i RGBImages
    ```

=== "Extract + OCR"

    ```bash linenums="1"
    rapid_videocr -vsf G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe -video_dir G:\ProgramFiles\RapidVideOCR\test_files\tiny
    ```

<details>

    <summary>详细参数</summay>

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

### 5. 查看结果

!!! info

    "如果想要让视频播放软件自动挂载srt文件或ass文件，需要更改srt或ass文件名字为视频文件名字，且放到同一目录下，亦或者手动指定加载。

前往`save_dir`目录下即可查看结果。
