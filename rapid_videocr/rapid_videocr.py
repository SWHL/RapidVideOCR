# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from typing import List, Tuple, Union

import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from tqdm import tqdm

from .utils import CropByProject

CUR_DIR = Path(__file__).resolve().parent


class RapidVideOCR():
    def __init__(self):
        self.rapid_ocr = RapidOCR()
        self.cropper = CropByProject()

    def __call__(self,
                 video_sub_finder_dir: str,
                 save_dir: str,
                 out_format: str = 'all') -> None:
        dir_name = Path(video_sub_finder_dir).name
        self.is_txt_dir = True if dir_name == 'TXTImages' else False

        img_list = list(Path(video_sub_finder_dir).iterdir())

        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        srt_result, txt_result = [], []
        for i, img_path in enumerate(tqdm(img_list, desc='OCR')):
            time_str = self.get_time(img_path)

            img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
            ocr_res = self.run_ocr(img, img.shape[0])
            if ocr_res:
                srt_result.append(f'{i+1}\n{time_str}\n{ocr_res}\n')
                txt_result.append(f'{ocr_res}\n')

        srt_path = save_dir / 'result.srt'
        txt_path = save_dir / 'result.txt'
        if out_format == 'txt':
            self.save_file(txt_path, txt_result)
        elif out_format == 'srt':
            self.save_file(srt_path, srt_result)
        elif out_format == 'all':
            self.save_file(txt_path, txt_result)
            self.save_file(srt_path, srt_result)
        else:
            raise ValueError(f'The {out_format} dost not support.')
        print(f'The result has been saved to {save_dir} directory.')

    @staticmethod
    def get_time(file_path: Path) -> str:
        """根据文件名称解析对应时间戳

        Args:
            file_path (Path): 字幕关键帧图像路径

        Returns:
            str: 字幕开始和截止时间戳字符串
        """
        split_paths = file_path.stem.split('_')
        start_time = split_paths[:4]
        start_time[0] = start_time[0].ljust(2, '0')
        start_str = ':'.join(start_time[:3]) + f',{start_time[3]}'

        end_time = split_paths[5:9]
        end_time[0] = end_time[0].ljust(2, '0')
        end_str = ':'.join(end_time[:3]) + f',{end_time[3]}'
        return f'{start_str} --> {end_str}'

    def run_ocr(self,
                img: np.ndarray,
                padding_pixel: int) -> Tuple[List, List]:
        def padding_img(img: np.ndarray,
                        padding_value: Tuple[int],
                        padding_color: Tuple = (0, 0, 0)) -> np.ndarray:
            padded_img = cv2.copyMakeBorder(img,
                                            padding_value[0],
                                            padding_value[1],
                                            padding_value[2],
                                            padding_value[3],
                                            cv2.BORDER_CONSTANT,
                                            value=padding_color)
            return padded_img

        if self.is_txt_dir:
            img = self.cropper(img)
            padding_value = 0, 0, int(img.shape[0] / 2), int(img.shape[0] / 2)
            padding_color = 255, 255, 255
        else:
            padding_value = padding_pixel, padding_pixel, 0, 0
            padding_color = 0, 0, 0

        frame = padding_img(img, padding_value, padding_color)
        ocr_result, _ = self.rapid_ocr(frame)
        if ocr_result is None:
            return None

        dt_boxes, rec_res, _ = list(zip(*ocr_result))
        if len(rec_res) == 1:
            return rec_res[0]

        dt_boxes_centroids = [self._compute_centroid(np.array(v))
                              for v in dt_boxes]
        y_centroids = np.array(dt_boxes_centroids)[:, 1].tolist()

        bool_res = self.is_same_line(y_centroids)

        final_res = ''
        for i, is_same_line in enumerate(bool_res):
            if is_same_line:
                final_res += ' '.join(rec_res[i:i+2])
            else:
                final_res += '\n'.join(rec_res[i:i+2])
        return final_res

    @staticmethod
    def save_file(save_path: Union[str, Path],
                  content: list,
                  mode: str = 'w') -> None:
        if not isinstance(save_path, str):
            save_path = str(save_path)

        if not isinstance(content, list):
            content = [content]

        with open(save_path, mode, encoding='utf-8') as f:
            for value in content:
                f.write(f'{value}\n')
        print(f'The file has been saved in the {save_path}')

    @staticmethod
    def _compute_centroid(points: np.ndarray) -> List:
        """计算所给框的质心坐标

        :param points ([type]): (4, 2)
        :return: [description]
        """
        x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
        y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
        return [(x_min + x_max) / 2, (y_min + y_max) / 2]

    @staticmethod
    def is_same_line(points: List) -> List[bool]:
        threshold = 5

        align_points = list(zip(points, points[1:]))
        bool_res = [False] * len(align_points)
        for i, point in enumerate(align_points):
            y0, y1 = point
            if abs(y0 - y1) <= threshold:
                bool_res[i] = True
        return bool_res


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--img_dir', type=str,
                        help='The full path of mp4 video.')
    parser.add_argument('-s', '--save_dir', type=str,
                        help='The path of saving the recognition result.')
    parser.add_argument('-o', '--out_format', type=str, default='all',
                        choices=['srt', 'txt', 'all'],
                        help='Output file format. Default is "all"')
    args = parser.parse_args()

    extractor = RapidVideOCR()
    extractor(args.img_dir, args.save_dir, args.out_format)


if __name__ == '__main__':
    main()
