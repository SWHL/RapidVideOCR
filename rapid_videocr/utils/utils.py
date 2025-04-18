# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from typing import List, Tuple, Union

import cv2
import numpy as np
import shapely
from shapely.geometry import MultiPoint, Polygon


def compute_centroid(points: np.ndarray) -> List:
    """计算所给框的质心坐标

    :param points ([type]): (4, 2)
    :return: [description]
    """
    x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
    return [(x_min + x_max) / 2, (y_min + y_max) / 2]


def write_txt(
    save_path: Union[str, Path], contents: Union[List[str], str], mode: str = "w"
) -> None:
    if not isinstance(contents, list):
        contents = [contents]

    with open(save_path, mode, encoding="utf-8") as f:
        for value in contents:
            f.write(f"{value}\n")


def read_img(img_path: Union[str, Path]) -> np.ndarray:
    img = cv2.imdecode(np.fromfile(str(img_path), dtype=np.uint8), 1)
    return img


def padding_img(
    img: np.ndarray,
    padding_value: Tuple[int, int, int, int],
    padding_color: Tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    padded_img = cv2.copyMakeBorder(
        img,
        padding_value[0],
        padding_value[1],
        padding_value[2],
        padding_value[3],
        cv2.BORDER_CONSTANT,
        value=padding_color,
    )
    return padded_img


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
