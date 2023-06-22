# -*- encoding: utf-8 -*-
import os
import subprocess
import sys
import time
from datetime import datetime
from shutil import move

from rapid_videocr import RapidVideOCR


def extract_subtitle(video_path: str) -> None:
    """videosubfinder提取关键帧"""
    print(
        "Extracting subtitle images with VideoSubFinder (takes quite a long time) ..."
    )
    startTime = time.time()
    subprocess.run(
        [
            videosubexe,
            "--clear_dirs",
            "--run_search",
            "--create_cleared_text_images",
            "--input_video",
            video_path,
            "--output_dir",
            tmp_dir,
            "--num_threads",
            str(30),  # 数字越大，速度越快，跟CPU性能也有关
            "--num_ocr_threads",
            str(30),
            "--top_video_image_percent_end",
            str(0.25),  # 字幕区域顶部所在百分比，根据要处理的视频来调整，
            "--bottom_video_image_percent_end",
            str(0.0),  # 字幕区域底部所在百分比，
        ],
        capture_output=True,
        check=False,
    )
    endTime = time.time()
    print("Completed! Took " + str(endTime - startTime) + "s")


def get_subtitle_RapidVideOCR(result_dir: str):
    """这个是RapidVideOCR提取字幕"""

    extractor = RapidVideOCR(
        is_concat_rec=False, out_format='all', is_print_console=False
    )

    # Windows端，需要这样写： rgb_dir = r'G:\ProgramFiles\_self\RapidVideOCR\test_files\RGBImages'
    # Linux / Mac 下面这样写
    rgb_dir = tmp_dir + r'\RGBImages'

    start_time = datetime.now()
    print(f"开始提取字幕...... {start_time:%H:%M:%S}")

    extractor(rgb_dir, result_dir)

    end_time = datetime.now()
    print(f"字幕提取结束...... {end_time:%H:%M:%S}")


if __name__ == '__main__':
    # 这里是需要提取字幕的视频所在的目录，放多个视频，批量处理。
    # videos/1.mp4, videos/2.mp4 这样存放，系统会读取所有的视频文件
    # 经测试，视频文件名是中文也可以
    # 通过参数传递，比如 python ocr_auto.py "D:\projects\videos"
    videos_dir = sys.argv[1]

    # 修改成自己电脑上VideoSubFinderWXW.exe所在路径
    videosubexe = r"G:\ProgramFiles\_self\VideoSubFinder-Setup\VideoSubFinder_5.60_x64\Release_x64\VideoSubFinderWXW.exe"

    # 这个不用管，会在上面videos_dir中增加一个临时文件夹
    tmp_dir = videos_dir + r"\tmp"

    # 读取要处理的文件，创建视频名的子文件夹，并将视频移进去
    video_formats = ('.mp4', '.avi', '.mov', '.mkv')  # 支持的视频格式
    for file in os.listdir(videos_dir):
        if file.endswith(video_formats):
            # Get video name without extension
            video_name = os.path.splitext(file)[0]
            print(video_name)
            # Create subfolder with video name
            video_subfolder = os.path.join(videos_dir, video_name)
            os.mkdir(video_subfolder)
            # Move file to subfolder
            move(os.path.join(videos_dir, file), video_subfolder)

    # 读取子文件夹目录
    def get_immediate_subdirectories(videos_dir):
        return [
            name
            for name in os.listdir(videos_dir)
            if os.path.isdir(os.path.join(videos_dir, name))
        ]

    subfolder_names = get_immediate_subdirectories(videos_dir)

    # 开始执行任务
    startAt = datetime.now()
    print(f"开始任务，本次任务共计{len(subfolder_names)}个视频……{startAt:%H:%M:%S}")

    for subfolder in subfolder_names:
        sub_path = os.path.join(videos_dir, subfolder)

        if os.path.exists(os.path.join(sub_path, "result.txt")):
            print("已有字幕, 跳过...")  # 自动跳过已经有字幕的文件
            continue

        video_name = [f for f in os.listdir(sub_path) if f.endswith(video_formats)]
        if not video_name:
            print("No video files found")
            continue

        video_name = video_name[0]
        video_path = os.path.join(sub_path, video_name)

        print("正在提取文件：" + video_path)
        extract_subtitle(video_path)
        get_subtitle_RapidVideOCR(sub_path)

    endAt = datetime.now()
    totalTime = str(endAt - startAt)
    print(f"全部提取结束，本次任务共计{len(subfolder_names)}个视频,耗时  {totalTime} 秒")
