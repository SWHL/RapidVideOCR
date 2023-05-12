# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys

from PyQt5.QtWidgets import QApplication
from RapidVideOCR_ui import RapidVideOCRUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = RapidVideOCRUI()
    ui.show()
    sys.exit(app.exec_())
