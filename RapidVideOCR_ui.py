# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import (QDialogButtonBox, QFileDialog, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QRadioButton, QWidget)

from rapid_videocr import RapidVideOCR


class RapidVideOCRUI(QWidget):
    def __init__(self,):
        super(RapidVideOCRUI, self).__init__()

        self.main_name = 'RapidVideOCR'
        self.version = 'v0.0.1'

        self.setWindowTitle(f'{self.main_name} {self.version}')
        self.resize(694, 237)

        self.label_img_dir = QLabel(self)
        self.label_img_dir.setGeometry(QRect(20, 20, 71, 31))

        font = QFont()
        font.setPointSize(11)

        # 选择RGBImages目录
        self.label_img_dir.setFont(font)
        self.label_img_dir.setObjectName("label_img_dir")
        self.label_img_dir.setText("图像目录：")

        self.le_display_img_dir = QLineEdit(self)
        self.le_display_img_dir.setGeometry(QRect(100, 20, 421, 31))
        self.le_display_img_dir.setObjectName("le_display_img_dir")

        self.btn_select_img_dir = QPushButton(self)
        self.btn_select_img_dir.setGeometry(QRect(540, 20, 81, 31))
        self.btn_select_img_dir.setObjectName("btn_select_img_dir")
        self.btn_select_img_dir.setText("点击选择")

        # 选择保存srt路径
        self.lable_save_name = QLabel(self)
        self.lable_save_name.setGeometry(QRect(20, 90, 71, 21))

        self.lable_save_name.setFont(font)
        self.lable_save_name.setObjectName("lable_save_name")
        self.lable_save_name.setText("保存路径：")

        self.le_save_path = QLineEdit(self)
        self.le_save_path.setGeometry(QRect(100, 80, 421, 31))
        self.le_save_path.setObjectName("le_save_path")

        self.btn_save_result = QPushButton(self)
        self.btn_save_result.setGeometry(QRect(540, 80, 81, 31))
        self.btn_save_result.setObjectName("btn_save_result")
        self.btn_save_result.setText("点击选择")

        # 确认 | 取消
        self.btn_ok_cancel = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.btn_ok_cancel.setGeometry(QRect(410, 170, 156, 23))
        self.btn_ok_cancel.setObjectName("btn_ok_cancel")
        self.btn_ok_cancel.accepted.connect(self.click_ok)
        self.btn_ok_cancel.rejected.connect(self.click_cancel)

        # 单选框：是否叠图识别
        self.label_mode = QLabel(self)
        self.label_mode.setGeometry(QRect(20, 140, 111, 31))
        self.label_mode.setFont(font)
        self.label_mode.setObjectName("label_mode")
        self.label_mode.setText('是否叠图识别：')

        self.rb_rec_mode = QRadioButton(self)
        self.rb_rec_mode.setGeometry(QRect(130, 150, 89, 16))
        self.rb_rec_mode.setFont(font)
        self.rb_rec_mode.setObjectName("rb_rec_mode")
        self.rb_rec_mode.setText('叠图识别')

        # 叠图识别下，batch个数
        self.label_batch = QLabel(self)
        self.label_batch.setGeometry(QRect(20, 180, 71, 21))
        self.label_batch.setFont(font)
        self.label_batch.setObjectName("label_batch")
        self.label_batch.setText('叠图个数：')

        self.le_batch = QLineEdit(self)
        self.le_batch.setGeometry(QRect(100, 180, 113, 20))
        self.le_batch.setObjectName("le_batch")
        self.le_batch.setText('10')
        self.le_batch.setValidator(QIntValidator())

        # 选择图像目录
        self.btn_select_img_dir.clicked.connect(self.select_directory)

        # 选择保存srt路径
        self.btn_save_result.clicked.connect(self.select_save_name)

    def select_directory(self, ):
        """选择RGBImages目录
        """
        file_name = QFileDialog.getExistingDirectory(None, '选择目录', "./")
        self.le_display_img_dir.setText(file_name)

    def select_save_name(self, ):
        file_path, _ = QFileDialog.getSaveFileName(None,
                                                   '选择保存路径',
                                                   './result.srt',
                                                   'srt(*.srt)')
        self.le_save_path.setText(file_path)

    def click_ok(self, ):
        img_dir = self.le_display_img_dir.text().strip()
        save_name = self.le_save_path.text().strip()
        is_select_mode = self.rb_rec_mode.isChecked()
        batch_num = self.le_batch.text()

        # 初始化实例
        extractor = RapidVideOCR(is_concat_rec=is_select_mode,
                                 concat_batch=int(batch_num),
                                 is_print_console=False)

        if not img_dir:
            self.show_msg('图像路径不能为空')
            return

        if not save_name:
            self.show_msg('保存路径不能为空')
            return

        extractor(img_dir, save_name)

    def click_cancel(self, ):
        self.close()

    def show_msg(self, txt: str):
        QMessageBox.information(self, '信息', txt)
