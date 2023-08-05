# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from enum import Enum
from pathlib import Path
from typing import List, Union

import cv2
import numpy as np
import shapely
from shapely.geometry import MultiPoint, Polygon

logger_initialized = {}


class RecMode(Enum):
    SINGLE = "single"
    CONCAT = "concat"


class CropByProject:
    """投影法裁剪"""

    def __init__(self, threshold=250):
        self.threshold = threshold

    def __call__(self, origin_img):
        image = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)

        # 将图片二值化
        retval, img = cv2.threshold(image, self.threshold, 255, cv2.THRESH_BINARY_INV)

        # 使文字增长成块
        closed = cv2.dilate(img, None, iterations=1)

        # 水平投影
        x0, x1 = self.get_project_loc(closed, direction="width")

        # 竖直投影
        y0, y1 = self.get_project_loc(closed, direction="height")

        return origin_img[y0:y1, x0:x1]

    @staticmethod
    def get_project_loc(img, direction):
        """获得裁剪的起始和终点索引位置
        Args:
            img (ndarray): 二值化后得到的图像
            direction (str): 'width/height'
        Raises:
            ValueError: 不支持的求和方向
        Returns:
            tuple: 起始索引位置
        """
        if direction == "width":
            axis = 0
        elif direction == "height":
            axis = 1
        else:
            raise ValueError(f"direction {direction} is not supported!")

        loc_sum = np.sum(img == 255, axis=axis)
        loc_range = np.argwhere(loc_sum > 0)
        i0, i1 = loc_range[0][0], loc_range[-1][0]
        return i0, i1


def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def read_txt(txt_path: Union[str, Path]) -> List[str]:
    if not isinstance(txt_path, str):
        txt_path = str(txt_path)

    with open(txt_path, "r", encoding="utf-8") as f:
        data = list(map(lambda x: x.rstrip("\n"), f))
    return data


def compute_poly_iou(a: np.ndarray, b: np.ndarray) -> float:
    """计算两个多边形的IOU

    Args:
        poly1 (np.ndarray): (4, 2)
        poly2 (np.ndarray): (4, 2)

    Returns:
        float: iou
    """
    poly1 = Polygon(a).convex_hull
    poly2 = Polygon(b).convex_hull

    union_poly = np.concatenate((a, b))

    if not poly1.intersects(poly2):
        return 0.0

    try:
        inter_area = poly1.intersection(poly2).area
        union_area = MultiPoint(union_poly).convex_hull.area
    except shapely.geos.TopologicalError:
        print("shapely.geos.TopologicalError occured, iou set to 0")
        return 0.0

    if union_area == 0:
        return 0.0

    return float(inter_area) / union_area


def is_inclusive_each_other(box1: np.ndarray, box2: np.ndarray) -> bool:
    """判断两个多边形框是否存在包含关系

    Args:
        box1 (np.ndarray): (4, 2)
        box2 (np.ndarray): (4, 2)

    Returns:
        bool: 是否存在包含关系
    """
    poly1 = Polygon(box1)
    poly2 = Polygon(box2)

    poly1_area = poly1.convex_hull.area
    poly2_area = poly2.convex_hull.area

    if poly1_area > poly2_area:
        box_max = box1
        box_min = box2
    else:
        box_max = box2
        box_min = box1

    x0, y0 = np.min(box_min[:, 0]), np.min(box_min[:, 1])
    x1, y1 = np.max(box_min[:, 0]), np.max(box_min[:, 1])

    edge_x0, edge_y0 = np.min(box_max[:, 0]), np.min(box_max[:, 1])
    edge_x1, edge_y1 = np.max(box_max[:, 0]), np.max(box_max[:, 1])

    if x0 >= edge_x0 and y0 >= edge_y0 and x1 <= edge_x1 and y1 <= edge_y1:
        return True
    return False


def float_range(mini, maxi):
    """Return function handle of an argument type function for
    ArgumentParser checking a float range: mini <= arg <= maxi
      mini - minimum acceptable argument
      maxi - maximum acceptable argument"""

    # Define the function with default arguments
    def float_range_checker(arg):
        """New Type function for argparse - a float within predefined range."""

        try:
            f = float(arg)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("must be a floating point number") from exc

        if f < mini or f > maxi:
            raise argparse.ArgumentTypeError(
                "must be in range [" + str(mini) + " .. " + str(maxi) + "]"
            )
        return f

    # Return function handle to checking function
    return float_range_checker
