# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QDialogButtonBox, QFileDialog, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QWidget)


class RapidVideOCRUI(QWidget):
    def __init__(self,):
        super(RapidVideOCRUI, self).__init__()

        self.main_name = 'RapidVideOCR'
        self.version = 'v0.0.1'

        self.setWindowTitle(self.main_name)
        self.resize(656, 188)

        self.label_img_dir = QLabel(self)
        self.label_img_dir.setGeometry(QtCore.QRect(20, 20, 71, 31))

        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_img_dir.setFont(font)
        self.label_img_dir.setObjectName("label_img_dir")
        self.label_img_dir.setText("图像目录：")

        self.le_display_img_dir = QLineEdit(self)
        self.le_display_img_dir.setGeometry(QtCore.QRect(100, 20, 421, 31))
        self.le_display_img_dir.setObjectName("le_display_img_dir")

        self.btn_select_img_dir = QPushButton(self)
        self.btn_select_img_dir.setGeometry(QtCore.QRect(540, 20, 81, 31))
        self.btn_select_img_dir.setObjectName("btn_select_img_dir")
        self.btn_select_img_dir.setText("点击选择")

        self.lable_save_name = QLabel(self)
        self.lable_save_name.setGeometry(QtCore.QRect(20, 90, 71, 21))

        font = QtGui.QFont()
        font.setPointSize(11)
        self.lable_save_name.setFont(font)
        self.lable_save_name.setObjectName("lable_save_name")
        self.lable_save_name.setText("保存路径：")

        self.le_save_path = QLineEdit(self)
        self.le_save_path.setGeometry(QtCore.QRect(100, 80, 421, 31))
        self.le_save_path.setObjectName("le_save_path")

        self.btn_save_result = QPushButton(self)
        self.btn_save_result.setGeometry(QtCore.QRect(540, 80, 81, 31))
        self.btn_save_result.setObjectName("btn_save_result")
        self.btn_save_result.setText("点击选择")

        self.btn_ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, self)
        self.btn_ok_cancel.setGeometry(QtCore.QRect(240, 140, 156, 23))
        self.btn_ok_cancel.setObjectName("btn_ok_cancel")
        self.btn_ok_cancel.accepted.connect(self.click_ok)
        self.btn_ok_cancel.rejected.connect(self.click_cancel)

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
        file_path, file_type = QFileDialog.getSaveFileName(None, '选择保存路径', './result.srt', 'srt(*.srt)')
        self.le_save_path.setText(file_path)

    def click_ok(self, ):
        img_dir = self.le_display_img_dir.text().strip()
        save_name = self.le_save_path.text().strip()

        if not img_dir:
            QMessageBox.information(self, '信息', '图像路径为空')
            return

        if not save_name:
            QMessageBox.information(self, '信息', '保存路径为空')
            return

        QMessageBox.information(self, '信息', '都有值')

    def click_cancel(self, ):
        self.close()
