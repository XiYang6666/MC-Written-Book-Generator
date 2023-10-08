from PyQt6 import QtCore
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow

from .Ui_mainwindow import Ui_MainWindow
from .logger import appLogger


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(
            QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint
        )  # 固定大小,禁用全屏

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        appLogger.info("程序已退出")
        return super().closeEvent(a0)
