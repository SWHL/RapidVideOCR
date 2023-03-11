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

from .utils import CropByProject, mkdir

CUR_DIR = Path(__file__).resolve().parent


class RapidVideOCR():
    def __init__(self, is_concat_rec: bool = False, concat_batch: int = 10):
        """Init

        Args:
            is_concat_rec (bool, optional): Whether to single recognition. Defaults to False.
            concat_batch (int, optional): The batch of concating image nums in concat recognition mode. Defaults to 10.
        """
        self.rapid_ocr = RapidOCR(width_height_ratio=-1)
        self.cropper = CropByProject()

        self.batch_size = concat_batch
        self.is_concat_rec = is_concat_rec

    def __call__(self,
                 video_sub_finder_dir: Union[str, Path],
                 save_dir: Union[str, Path],
                 out_format: str = 'all') -> None:
        """call

        Args:
            video_sub_finder_dir (Union[str, Path]): RGBImages or TXTImages from VideoSubFinder app.
            save_dir (Union[str, Path]): The directory of saving the srt/txt file.
            out_format (str, optional): Output format of subtitle(srt, txt, all). Defaults to 'all'.

        Raises:
            RapidVideOCRError: meet some error.
        """
        video_sub_finder_dir = Path(video_sub_finder_dir)
        if not video_sub_finder_dir.exists():
            raise RapidVideOCRError(f'{video_sub_finder_dir} does not exist.')

        dir_name = Path(video_sub_finder_dir).name
        is_txt_dir = 'TXTImages' in dir_name

        save_dir = Path(save_dir)
        mkdir(save_dir)

        img_list = list(Path(video_sub_finder_dir).glob('*.jpeg'))
        img_list = sorted(img_list, key=lambda x: self.get_sort_key(x))
        if not img_list:
            raise RapidVideOCRError(
                f'{video_sub_finder_dir} has not images with jpeg as suffix.')

        if self.is_concat_rec:
            print('Running with concat recognition.')
            srt_result, txt_result = self.concat_rec(img_list, is_txt_dir)
        else:
            print('Running with single recognition.')
            srt_result, txt_result = self.single_rec(img_list, is_txt_dir)

        self.export_file(save_dir, srt_result, txt_result, out_format)

    @staticmethod
    def get_sort_key(x):
        return int(''.join(str(x.stem).split('_')[:4]))

    def single_rec(self, img_list: List[str],
                   is_txt_dir: bool) -> Tuple[List, List]:
        srt_result, txt_result = [], []
        for i, img_path in enumerate(tqdm(img_list, desc='OCR')):
            time_str = self.get_time(img_path)

            img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
            dt_boxes, rec_res = self.run_ocr(img, img.shape[0],
                                             is_txt_dir)
            if rec_res:
                txts = self.process_same_line(dt_boxes, rec_res)
                srt_result.append(f'{i+1}\n{time_str}\n{txts}\n')
                txt_result.append(f'{txts}\n')
        return srt_result, txt_result

    def concat_rec(self, img_list: List[np.ndarray],
                   is_txt_dir: bool) -> Tuple[List, List]:
        srt_result, txt_result = [], []

        img_nums = len(img_list)
        for start_i in tqdm(range(0, img_nums, self.batch_size), desc='OCR'):
            end_i = min(img_nums, start_i + self.batch_size)

            concat_img, img_coordinates, img_paths = self.get_batch(img_list,
                                                                    start_i,
                                                                    end_i)
            dt_boxes, rec_res = self.run_ocr(concat_img,
                                             padding_pixel=0,
                                             is_txt_dir=is_txt_dir)
            if not rec_res:
                continue

            srt_part, txt_part = self.get_match_results(start_i,
                                                        img_coordinates,
                                                        dt_boxes,
                                                        rec_res,
                                                        img_paths)
            srt_result.extend(srt_part)
            txt_result.extend(txt_part)
        return srt_result, txt_result

    def get_batch(self, img_list: List[str],
                  start: int, end: int) -> Tuple[np.ndarray, np.ndarray, List]:
        select_imgs = img_list[start: end]

        img_list, img_coordinates, batch_img_paths = [], [], []
        for i, img_path in enumerate(select_imgs):
            batch_img_paths.append(img_path)

            img = cv2.imread(str(img_path))

            img_list.append(img)

            h, w = img.shape[:2]
            img_coordinates.append([(0, i * h), (w, (i + 1) * h)])

        concat_img = np.vstack(img_list)
        return concat_img, np.array(img_coordinates), batch_img_paths

    def get_match_results(self, start_i: int,
                          img_coordinates: np.ndarray,
                          dt_boxes: np.ndarray,
                          rec_res: List,
                          img_paths: list) -> Tuple[List, List]:
        srt_result_part, txt_result_part = [], []

        match_dict = {}
        y_points = img_coordinates[:, :, 1]
        left_top_boxes = dt_boxes[:, 0, :]
        for i, one_left in enumerate(left_top_boxes):
            y = one_left[1]
            condition = (y >= y_points[:, 0]) & (y <= y_points[:, 1])
            index = np.argwhere(condition)
            if not index.size:
                match_dict[i] = ''
                continue

            matched_index = index.squeeze().tolist()
            matched_path = img_paths[matched_index]
            match_dict.setdefault(matched_index, []).append([matched_path,
                                                             dt_boxes[i],
                                                             rec_res[i]])

        for k, v in match_dict.items():
            cur_frame_idx = start_i + k
            img_path, boxes, recs = list(zip(*v))

            time_str = self.get_time(img_path[0])
            txts = self.process_same_line(boxes, recs)
            srt_result_part.append(f'{cur_frame_idx+1}\n{time_str}\n{txts}\n')
            txt_result_part.append(f'{txts}\n')
        return srt_result_part, txt_result_part

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

    def run_ocr(self, img: np.ndarray, padding_pixel: int,
                is_txt_dir: bool) -> Tuple[np.ndarray, List]:

        def padding_img(img: np.ndarray,
                        padding_value: Tuple[int, int, int, int],
                        padding_color: Tuple = (0, 0, 0)) -> np.ndarray:
            padded_img = cv2.copyMakeBorder(img,
                                            padding_value[0],
                                            padding_value[1],
                                            padding_value[2],
                                            padding_value[3],
                                            cv2.BORDER_CONSTANT,
                                            value=padding_color)
            return padded_img

        padding_value = padding_pixel, padding_pixel, 0, 0
        padding_color = 0, 0, 0
        if is_txt_dir:
            img = self.cropper(img)
            padding_value = 0, 0, int(img.shape[0] / 2), int(img.shape[0] / 2)
            padding_color = 255, 255, 255

        frame = padding_img(img, padding_value, padding_color)
        ocr_result, _ = self.rapid_ocr(frame)
        if ocr_result is None:
            return None, None

        dt_boxes, rec_res, _ = list(zip(*ocr_result))
        return np.array(dt_boxes), rec_res

    def process_same_line(self, dt_boxes, rec_res):
        rec_len = len(rec_res)
        if rec_len == 1:
            return rec_res[0]

        dt_boxes_centroids = [self._compute_centroid(np.array(v))
                              for v in dt_boxes]
        y_centroids = np.array(dt_boxes_centroids)[:, 1].tolist()
        bool_res = self.is_same_line(y_centroids)

        pair_points = list(zip(range(rec_len), range(1, rec_len)))

        final_res, used = [], [False] * rec_len
        for is_same_line, pair_point in zip(bool_res, pair_points):
            if is_same_line:
                concat_str = []
                for v in pair_point:
                    used[v] = True
                    concat_str.append(rec_res[v])
                final_res.append(' '.join(concat_str))
            else:
                for v in pair_point:
                    if not used[v]:
                        final_res.append(rec_res[v])
        return '\n'.join(final_res)

    def export_file(self, save_dir: Union[str, Path],
                    srt_result: List,
                    txt_result: List,
                    out_format: str) -> None:
        if isinstance(save_dir, str):
            save_dir = Path(save_dir)

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


class RapidVideOCRError(Exception):
    pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--img_dir', type=str,
                        help='The full path of RGBImages or TXTImages.')
    parser.add_argument('-s', '--save_dir', type=str,
                        help='The path of saving the recognition result.')
    parser.add_argument('-o', '--out_format', type=str, default='all',
                        choices=['srt', 'txt', 'all'],
                        help='Output file format. Default is "all"')
    parser.add_argument('-m', '--mode', type=str, default='single',
                        choices=['single', 'concat'],
                        help='Which mode to run (concat recognition or single recognition), default is "single"')
    parser.add_argument('-b', '--concat_batch', type=int, default=10,
                        help='The batch of concating image nums in concat recognition mode. Default is 10.')
    args = parser.parse_args()

    is_concat_rec = 'concat' in args.mode
    extractor = RapidVideOCR(is_concat_rec=is_concat_rec,
                             concat_batch=args.concat_batch)
    extractor(args.img_dir, args.save_dir, args.out_format)


if __name__ == '__main__':
    main()
