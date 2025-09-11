# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


class VideoFormat(Enum):
    MP4 = ".mp4"
    AVI = ".avi"
    MOV = ".mov"
    MKV = ".mkv"


class OutputFormat(Enum):
    TXT = "txt"
    SRT = "srt"
    ASS = "ass"
    ALL = "all"


@dataclass
class RapidVideOCRInput:
    is_batch_rec: bool = False
    batch_size: int = 10
    out_format: str = OutputFormat.ALL.value
    ocr_params: Optional[Dict[str, Any]] = None
    log_level: str = "info"  # debug / info / warning / error / critical


LOG_LEVEL_MAP = {
    50: "CRITICAL",
    40: "ERROR",
    30: "WARNING",
    20: "INFO",
    10: "DEBUG",
    0: "NOTSET",
}
