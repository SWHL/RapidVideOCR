# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
import traceback
from pathlib import Path

from PyQt5.QtCore import QRect, QSettings
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QWidget,
)

from rapid_videocr import RapidVideOCR, RapidVideoSubFinderOCR, logger


class RapidVideOCRUI(QWidget):
    def __init__(
        self,
    ):
        super(RapidVideOCRUI, self).__init__()

        self.setting = QSettings("./config", QSettings.IniFormat)
        self.setting.setIniCodec("UTF-8")

        self.main_name = "RapidVideOCR"
        self.version = "v0.0.4"

        self.setWindowTitle(f"{self.main_name} {self.version}")
        self.resize(727, 379)

        font = QFont()
        font.setPointSize(11)
        font.setFamily("微软雅黑")

        gb_font = QFont()
        gb_font.setFamily("微软雅黑")
        gb_font.setPointSize(12)
        gb_font.setBold(True)
        gb_font.setItalic(False)
        gb_font.setWeight(75)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(0, 0, 701, 191))
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")

        self.tab1UI(font)
        self.tab2UI(font)

        # ---------------调节参数 group box--------------
        self.ocr_gb_params = QGroupBox(self)
        self.ocr_gb_params.setGeometry(QRect(30, 210, 651, 81))
        self.ocr_gb_params.setTitle("调节参数")
        self.ocr_gb_params.setFont(gb_font)
        self.ocr_gb_params.setObjectName("ocr_gb_params")

        # 单选框：是否叠图识别
        self.widget_batch = QWidget(self.ocr_gb_params)
        self.widget_batch.setGeometry(QRect(31, 31, 207, 27))
        font.setBold(False)
        self.widget_batch.setFont(font)

        self.hl_batch = QHBoxLayout(self.widget_batch)
        self.hl_batch.setContentsMargins(0, 0, 0, 0)
        self.hl_batch.setObjectName("hl_batch")

        self.label_mode = QLabel(self.widget_batch)
        self.label_mode.setObjectName("label_mode")
        self.label_mode.setText("是否叠图识别：")
        self.hl_batch.addWidget(self.label_mode)

        self.rb_rec_mode = QRadioButton(self.widget_batch)
        self.rb_rec_mode.setObjectName("rb_rec_mode")
        self.rb_rec_mode.setText("叠图识别")
        self.hl_batch.addWidget(self.rb_rec_mode)

        # 叠图识别下，batch个数
        self.widget_batch_num = QWidget(self.ocr_gb_params)
        self.widget_batch_num.setGeometry(QRect(290, 30, 272, 30))
        font.setBold(False)
        self.widget_batch_num.setFont(font)

        self.hl_batch_num = QHBoxLayout(self.widget_batch_num)
        self.hl_batch_num.setContentsMargins(0, 0, 0, 0)
        self.hl_batch_num.setObjectName("hl_batch_num")

        self.label_batch = QLabel(self.ocr_gb_params)
        self.label_batch.setFont(font)
        self.label_batch.setObjectName("label_batch")
        self.label_batch.setText("叠图个数：")
        self.hl_batch_num.addWidget(self.label_batch)

        self.le_batch = QLineEdit(self.ocr_gb_params)
        self.le_batch.setObjectName("le_batch")
        self.le_batch.setFont(font)
        self.le_batch.setText("10")
        self.le_batch.setValidator(QIntValidator())
        self.hl_batch_num.addWidget(self.le_batch)

        # 确认 | 取消
        self.ocr_btn_ok_cancel = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        self.ocr_btn_ok_cancel.setGeometry(QRect(250, 320, 156, 23))
        self.ocr_btn_ok_cancel.setObjectName("btn_ok_cancel")
        self.ocr_btn_ok_cancel.setFont(font)
        self.ocr_btn_ok_cancel.accepted.connect(self.click_ok)
        self.ocr_btn_ok_cancel.rejected.connect(self.click_cancel)

    def tab1UI(self, font):
        # ---------------RapidVideOCR部分---------------------
        self.tab_only_ocr = QWidget()
        self.tab_only_ocr.setObjectName("tab_only_ocr")

        # 图像目录 [] 点击选择
        self.img_dir_widget = QWidget(self.tab_only_ocr)
        self.img_dir_widget.setGeometry(QRect(30, 40, 641, 31))
        self.img_dir_widget.setObjectName("widget_img_dir")
        font.setBold(False)
        self.img_dir_widget.setFont(font)

        self.hl_img_dir = QHBoxLayout(self.img_dir_widget)
        self.hl_img_dir.setContentsMargins(0, 0, 0, 0)
        self.hl_img_dir.setObjectName("hl_select_img_dir")

        self.label_img_dir = QLabel(self.img_dir_widget)
        self.label_img_dir.setGeometry(QRect(30, 40, 581, 31))
        self.label_img_dir.setFont(font)
        self.label_img_dir.setObjectName("label_img_dir")
        self.label_img_dir.setText("图像目录：")
        self.label_img_dir.setToolTip("输入为RGBImages目录，输出为字幕结果")
        self.hl_img_dir.addWidget(self.label_img_dir)

        self.le_display_img_dir = QLineEdit(self.img_dir_widget)
        self.le_display_img_dir.setGeometry(QRect(100, 20, 421, 31))
        self.le_display_img_dir.setObjectName("le_display_img_dir")
        self.le_display_img_dir.setText(self.get_last_dir("LastDir"))
        self.le_display_img_dir.setFocus()
        self.hl_img_dir.addWidget(self.le_display_img_dir)

        self.btn_select_img_dir = QPushButton(self.img_dir_widget)
        self.btn_select_img_dir.setGeometry(QRect(540, 20, 81, 31))
        self.btn_select_img_dir.setObjectName("btn_select_img_dir")
        self.btn_select_img_dir.setText("点击选择")
        self.btn_select_img_dir.clicked.connect(self.select_img_dir)
        self.hl_img_dir.addWidget(self.btn_select_img_dir)

        # 保存路径 [] 点击选择
        self.srt_widget = QWidget(self.tab_only_ocr)
        self.srt_widget.setGeometry(QRect(30, 90, 641, 31))
        font.setBold(False)
        self.srt_widget.setFont(font)
        self.srt_widget.setObjectName("widget_srt")

        self.hl_srt_path = QHBoxLayout(self.srt_widget)
        self.hl_srt_path.setContentsMargins(0, 0, 0, 0)
        self.hl_srt_path.setObjectName("hl_srt")

        self.lable_save_name = QLabel(self.srt_widget)
        self.lable_save_name.setFont(font)
        self.lable_save_name.setObjectName("lable_save_name")
        self.lable_save_name.setText("保存路径：")
        self.hl_srt_path.addWidget(self.lable_save_name)

        self.le_save_path = QLineEdit(self.srt_widget)
        self.le_save_path.setObjectName("le_save_path")
        self.le_save_path.setText(self.get_last_dir("SRTDir"))
        self.hl_srt_path.addWidget(self.le_save_path)

        self.btn_save_result = QPushButton(self.srt_widget)
        self.btn_save_result.setObjectName("btn_save_result")
        self.btn_save_result.setText("点击选择")
        self.btn_save_result.clicked.connect(self.select_save_srt_dir)
        self.hl_srt_path.addWidget(self.btn_save_result)

        self.tabWidget.addTab(self.tab_only_ocr, "RapidVideOCR")

    def tab2UI(self, font):
        # ---------------VideoSubFinder + RapidVideOCR部分-------------
        self.tab_vsf_ocr = QWidget()
        self.tab_vsf_ocr.setObjectName("tab_vsf_ocr")

        # VSF exe [] 点击选择
        self.vsf_path_widget = QWidget(self.tab_vsf_ocr)
        self.vsf_path_widget.setGeometry(QRect(30, 20, 641, 31))
        self.vsf_path_widget.setObjectName("widget_img_dir")
        font.setBold(False)
        self.vsf_path_widget.setFont(font)

        self.hl_vsf_path = QHBoxLayout(self.vsf_path_widget)
        self.hl_vsf_path.setContentsMargins(0, 0, 0, 0)
        self.hl_vsf_path.setObjectName("hl_vsf_path")

        self.label_vsf_path = QLabel(self.vsf_path_widget)
        self.label_vsf_path.setFont(font)
        self.label_vsf_path.setObjectName("label_vsf_path")
        self.label_vsf_path.setText("VSF exe路径：")
        self.label_vsf_path.setToolTip("输入为视频，输出为字幕结果")
        self.hl_vsf_path.addWidget(self.label_vsf_path)

        self.le_vsf_path = QLineEdit(self.vsf_path_widget)
        self.le_vsf_path.setObjectName("le_vsf_path")
        self.le_vsf_path.setText(self.get_last_dir("VSFLastPath"))
        self.hl_vsf_path.addWidget(self.le_vsf_path)

        self.btn_vsf_path = QPushButton(self.vsf_path_widget)
        self.btn_vsf_path.setObjectName("btn_vsf_path")
        self.btn_vsf_path.setText("点击选择")
        self.btn_vsf_path.clicked.connect(self.select_vsf_path)
        self.hl_vsf_path.addWidget(self.btn_vsf_path)

        # 视频目录 [] 点击选择
        self.video_path_widget = QWidget(self.tab_vsf_ocr)
        self.video_path_widget.setGeometry(QRect(30, 70, 641, 31))
        font.setBold(False)
        self.video_path_widget.setFont(font)
        self.video_path_widget.setObjectName("video_path_widget")

        self.hl_video_path = QHBoxLayout(self.video_path_widget)
        self.hl_video_path.setContentsMargins(0, 0, 0, 0)
        self.hl_video_path.setObjectName("hl_video_path")

        self.lable_video_dir = QLabel(self.video_path_widget)
        self.lable_video_dir.setFont(font)
        self.lable_video_dir.setObjectName("lable_video_dir")
        self.lable_video_dir.setText("视  频  目  录：")
        self.hl_video_path.addWidget(self.lable_video_dir)

        self.le_video_path = QLineEdit(self.video_path_widget)
        self.le_video_path.setObjectName("le_save_path")
        self.le_video_path.setText(self.get_last_dir("VideoLastDir"))
        self.hl_video_path.addWidget(self.le_video_path)

        self.btn_select_video = QPushButton(self.video_path_widget)
        self.btn_select_video.setObjectName("btn_select_video")
        self.btn_select_video.setText("点击选择")
        self.btn_select_video.clicked.connect(self.select_video_dir)
        self.hl_video_path.addWidget(self.btn_select_video)

        # 保存路径 [] 本地选择
        self.save_video_path_widget = QWidget(self.tab_vsf_ocr)
        self.save_video_path_widget.setGeometry(QRect(30, 120, 641, 31))
        font.setBold(False)
        self.save_video_path_widget.setFont(font)
        self.save_video_path_widget.setObjectName("save_video_path_widget")

        self.hl_save_res_path = QHBoxLayout(self.save_video_path_widget)
        self.hl_save_res_path.setContentsMargins(0, 0, 0, 0)
        self.hl_save_res_path.setObjectName("hl_save_res_path")

        self.save_res_dir = QLabel(self.save_video_path_widget)
        self.save_res_dir.setFont(font)
        self.save_res_dir.setObjectName("save_res_dir")
        self.save_res_dir.setText("保  存  路  径：")
        self.hl_save_res_path.addWidget(self.save_res_dir)

        self.le_save_video_path = QLineEdit(self.save_video_path_widget)
        self.le_save_video_path.setObjectName("le_save_video_path")
        self.le_save_video_path.setText(self.get_last_dir("SaveVideoLastDir"))
        self.hl_save_res_path.addWidget(self.le_save_video_path)

        self.btn_select_save_video = QPushButton(self.save_video_path_widget)
        self.btn_select_save_video.setObjectName("btn_select_save_video")
        self.btn_select_save_video.setText("点击选择")
        self.btn_select_save_video.clicked.connect(self.select_save_video_dir)
        self.hl_save_res_path.addWidget(self.btn_select_save_video)

        self.tabWidget.addTab(self.tab_vsf_ocr, "VideoSubFinder + RapidVideOCR")

    def get_last_dir(self, dir_name: str) -> str:
        last_dir = self.setting.value(dir_name)
        if last_dir is None:
            last_dir = ""
        return last_dir

    def set_last_dir(self, dir_name: str, dir_path: str):
        self.setting.setValue(dir_name, dir_path)

    def select_vsf_path(
        self,
    ) -> None:
        """选择VSF EXE 路径"""
        path_key = "VSFLastPath"
        vsf_full_path = self.get_last_dir(path_key)
        vsf_path, _ = QFileDialog.getOpenFileName(
            None, caption="选择VSF exe路径", directory=vsf_full_path, filter="*.exe"
        )
        self.le_vsf_path.setText(vsf_path)
        self.set_last_dir(path_key, vsf_path)

    def select_video_dir(
        self,
    ) -> None:
        """选择Video 目录或文件"""
        dir_key = "VideoLastDir"
        directory = self.get_last_dir(dir_key)
        select_dir = QFileDialog.getExistingDirectory(
            None, caption="选择目录", directory=directory
        )
        self.le_video_path.setText(select_dir)
        self.set_last_dir(dir_key, select_dir)

    def select_save_video_dir(
        self,
    ) -> None:
        """选择保存Video 目录或文件"""
        dir_key = "SaveVideoLastDir"
        directory = self.get_last_dir(dir_key)
        select_dir = QFileDialog.getExistingDirectory(
            None, caption="选择目录", directory=directory
        )
        self.le_save_video_path.setText(select_dir)
        self.set_last_dir(dir_key, select_dir)

    def select_img_dir(
        self,
    ) -> None:
        """选择RGBImages目录"""
        dir_key = "LastDir"
        directory = self.get_last_dir(dir_key)
        select_dir = QFileDialog.getExistingDirectory(
            None, caption="选择目录", directory=directory
        )
        self.le_display_img_dir.setText(select_dir)
        self.set_last_dir(dir_key, select_dir)

    def select_save_srt_dir(
        self,
    ) -> None:
        srt_key = "SRTDir"
        save_srt_dir = self.get_last_dir(srt_key)
        file_path, _ = QFileDialog.getSaveFileName(
            None, "选择保存路径", f"{save_srt_dir}/result.srt", "srt(*.srt)"
        )
        self.le_save_path.setText(file_path)
        self.set_last_dir(srt_key, file_path)

    def click_ok(
        self,
    ) -> None:
        # 0 → ocr  1 → vsf+ocr
        cur_idx = self.tabWidget.currentIndex()

        is_select_mode = self.rb_rec_mode.isChecked()
        batch_num = self.le_batch.text()

        if cur_idx == 0:
            self.only_ocr(is_select_mode, batch_num)
        elif cur_idx == 1:
            self.vsf_ocr(is_select_mode, batch_num)

        question = QMessageBox.question(self, "识别完毕", "是否继续识别？（Yes → 继续，NO → 退出）")
        if question == QMessageBox.Yes:
            self.clear_input()
        else:
            self.exit()

    def only_ocr(self, is_select_mode: bool, batch_num: str):
        img_dir = self.le_display_img_dir.text().strip()
        save_full_path = self.le_save_path.text().strip()

        if not img_dir:
            self.show_msg("图像路径不能为空")
            return

        if not save_full_path:
            self.show_msg("保存路径不能为空")
            return

        is_select_mode = self.rb_rec_mode.isChecked()
        batch_num = self.le_batch.text()
        extractor = RapidVideOCR(
            is_concat_rec=is_select_mode,
            concat_batch=int(batch_num),
            is_print_console=False,
        )

        save_dir = Path(save_full_path).parent
        save_name = Path(save_full_path).stem
        try:
            extractor(img_dir, save_dir, save_name)
        except Exception as e:
            error = traceback.format_exc()
            logger.error(error)

    def vsf_ocr(self, is_select_mode: bool, batch_num: str):
        vsf_exe_path = self.le_vsf_path.text().strip()
        video_path = self.le_video_path.text().strip()
        save_dir = self.le_save_video_path.text().strip()

        if not vsf_exe_path:
            self.show_msg("VSF exe路径不能为空")
            return

        if not video_path:
            self.show_msg("视频目录不能为空")
            return

        if not save_dir:
            self.show_msg("保存路径不能为空")
            return

        extractor = RapidVideoSubFinderOCR(
            vsf_exe_path=vsf_exe_path,
            is_concat_rec=is_select_mode,
            concat_batch=int(batch_num),
            is_print_console=False,
        )
        try:
            extractor(video_path, save_dir)
        except Exception:
            error = traceback.format_exc()
            logger.error(error)

    def click_cancel(
        self,
    ) -> None:
        self.exit()

    def show_msg(self, txt: str):
        QMessageBox.information(self, "信息", txt)

    def exit(
        self,
    ) -> None:
        self.close()

    def clear_input(
        self,
    ) -> None:
        self.le_batch.setText("10")
        self.rb_rec_mode.setChecked(False)
        self.le_display_img_dir.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = RapidVideOCRUI()
    ui.show()
    sys.exit(app.exec_())
