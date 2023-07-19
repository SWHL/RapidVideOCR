## rapid_videocr Package
<p align="left">
    <a href="https://colab.research.google.com/github/SWHL/RapidVideOCR/blob/75dae6e9804dec6e61bef98334601908dc9ec9fb/assets/RapidVideOCRDemo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://github.com/SWHL/RapidVideOCR/stargazers"><img src="https://img.shields.io/github/stars/SWHL/RapidVideOCR?color=ccf"></a>
    <a href="https://pepy.tech/project/rapid-videocr">
        <img src="https://static.pepy.tech/personalized-badge/rapid-videocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads">
    </a>
    <a href='https://rapidvideocr.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/rapidvideocr/badge/?version=latest' alt='Documentation Status'/>
    </a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>


### 1. Install package by pypi.
```bash
pip install rapid_videocr
```

### 2. Run by script.
- Only OCR:
    ```python
    from rapid_videocr import RapidVideOCR

    extractor = RapidVideOCR(is_concat_rec=True,
                             concat_batch=10,
                             out_format='srt')

    rgb_dir = 'RGBImages'
    save_dir = 'outputs'
    extractor(video_sub_finder_dir=rgb_dir, save_dir=save_dir)
    ```
- Extract + OCR:
    ```python
    from rapid_videocr import RapidVideoSubFinderOCR

    vsf_exe = r"G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe"
    extractor = RapidVideoSubFinderOCR(vsf_exe_path=vsf_exe, is_concat_rec=True)

    # video_path can be directory path or video full path.
    video_path = 'test_files/tiny/2.mp4'
    save_dir = 'outputs'
    extractor(video_path, save_dir)
    ```

### 3. Run by command line.
- Usage:
    ```bash
    $ rapid_videocr -h
    usage: rapid_videocr [-h] [-video_dir VIDEO_DIR] [-i IMG_DIR] [-s SAVE_DIR]
                [-o {srt,txt,all}] [--is_concat_rec] [-b CONCAT_BATCH] [-p]
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
    -o {srt,txt,all}, --out_format {srt,txt,all}
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
- Example:
  - Only OCR:
    ```bash
    $ rapid_videocr -i RGBImages
    ```
  - Extract + OCR:
    ```bash
    $ rapid_videocr -vsf G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe -video_dir G:\ProgramFiles\RapidVideOCR\test_files\tiny
    ```

See details for [RapidVideOCR](https://github.com/SWHL/RapidVideOCR).