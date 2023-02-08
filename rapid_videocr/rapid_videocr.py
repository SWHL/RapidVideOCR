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

CUR_DIR = Path(__file__).resolve().parent


class RapidVideOCR():
    def __init__(self):
        self.rapid_ocr = RapidOCR()

    def __call__(self,
                 video_sub_finder_dir: str,
                 save_dir: str,
                 out_format: str = 'all') -> None:
        img_list = list(Path(video_sub_finder_dir).iterdir())

        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        srt_result, txt_result = [], []
        for img_path in tqdm(img_list, desc='OCR'):
            time_str = self.get_time(img_path)

            img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
            ocr_res = self.run_ocr(img, int(img.shape[1] / 2))
            if ocr_res:
                srt_result.append(f'{time_str}\n{ocr_res}\n')
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
        split_paths = file_path.stem.split('_')
        start_time = split_paths[:4]
        start_time[0] = '00'
        start_str = ':'.join(start_time[:3]) + f',{start_time[3]}'

        end_time = split_paths[5:9]
        end_time[0] = '00'
        end_str = ':'.join(end_time[:3]) + f',{end_time[3]}'
        return f'{start_str} --> {end_str}'

    def run_ocr(self,
                img: np.ndarray,
                padding_pixel: int) -> Tuple[List, List]:
        def padding_img(img: np.ndarray, padding_pixel: int) -> np.ndarray:
            padded_img = cv2.copyMakeBorder(img,
                                            padding_pixel,
                                            padding_pixel,
                                            0, 0,
                                            cv2.BORDER_CONSTANT,
                                            value=(0, 0))
            return padded_img

        frame = padding_img(img, padding_pixel)
        ocr_result, _ = self.rapid_ocr(frame)
        if ocr_result:
            _, rec_res, _ = list(zip(*ocr_result))

            if not rec_res:
                return None
            return '\n'.join(rec_res)
        return None

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
