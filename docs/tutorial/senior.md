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
    from rapid_videocr import RapidVideOCR

    # RapidVideOCRInput有两个初始化参数
    # is_concat_rec: 是否用单张图识别，默认是False，也就是默认用单图识别
    # concat_batch: 叠图识别的图像张数，默认10，可自行调节
    # out_format: 输出格式选择，[srt, ass, txt, all], 默认是 all
    # is_print_console: 是否打印结果，[0, 1], 默认是0，不打印
    input_args = RapidVideOCRInput(
    is_batch_rec=False, ocr_params={"Global.with_paddle": True}
    )
    extractor = RapidVideOCR(input_args)

    rgb_dir = "tests/test_files/RGBImages"
    save_dir = "outputs"
    save_name = "a"

    # outputs/a.srt  outputs/a.ass  outputs/a.t
    extractor(rgb_dir, save_dir, save_name=save_name)
    ```

=== "Extract + OCR"

    ```python linenums="1"
    from rapid_videocr import RapidVideoSubFinderOCR

    vsf_exe = r"G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe"
    extractor = RapidVideoSubFinderOCR(vsf_exe_path=vsf_exe, is_concat_rec=True)

    # video_path can be directory path or video full path.
    video_path = 'test_files/tiny/2.mp4'
    save_dir = 'outputs'
    extractor(video_path, save_dir)
    ```

### 4. 命令行使用

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

### 5. 查看结果

!!! info

    "如果想要让视频播放软件自动挂载srt文件或ass文件，需要更改srt或ass文件名字为视频文件名字，且放到同一目录下，亦或者手动指定加载。

前往`save_dir`目录下即可查看结果。
