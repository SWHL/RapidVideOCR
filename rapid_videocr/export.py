# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import List

from .utils.utils import write_txt


class OutputFormat(Enum):
    TXT = "txt"
    SRT = "srt"
    ALL = "all"


class ExportStrategy(ABC):
    @abstractmethod
    def export(
        self,
        save_dir: Path,
        save_name: str,
        srt_result: List[str],
        txt_result: List[str],
    ):
        pass


class TxtExportStrategy(ExportStrategy):
    def export(
        self,
        save_dir: Path,
        save_name: str,
        srt_result: List[str],
        txt_result: List[str],
    ):
        file_path = save_dir / f"{save_name}.txt"
        write_txt(file_path, txt_result)


class SrtExportStrategy(ExportStrategy):
    def export(
        self,
        save_dir: Path,
        save_name: str,
        srt_result: List[str],
        txt_result: List[str],
    ):
        file_path = save_dir / f"{save_name}.srt"
        write_txt(file_path, srt_result)


class AllExportStrategy(ExportStrategy):
    def export(
        self,
        save_dir: Path,
        save_name: str,
        srt_result: List[str],
        txt_result: List[str],
    ):
        txt_export = TxtExportStrategy()
        srt_export = SrtExportStrategy()

        txt_export.export(save_dir, save_name, srt_result, txt_result)
        srt_export.export(save_dir, save_name, srt_result, txt_result)


class ExportStrategyFactory:
    @staticmethod
    def create_strategy(out_format: str = OutputFormat.ALL.value) -> ExportStrategy:
        strategies = {
            OutputFormat.TXT.value: TxtExportStrategy(),
            OutputFormat.SRT.value: SrtExportStrategy(),
            OutputFormat.ALL.value: AllExportStrategy(),
        }

        if strategy := strategies.get(out_format):
            return strategy
        raise ValueError(f"Unsupported output format: {out_format}")
