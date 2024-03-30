from typing_extensions import override
from PyQt6 import QtCore
from PyQt6.QtGui import QCloseEvent  # pylint: disable=E0611
from PyQt6.QtWidgets import QMainWindow  # pylint: disable=E0611

from .ui_mainwindow import Ui_MainWindow
from .logger import appLogger


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(
            QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint  # pylint: disable=I1101
        )  # 固定大小,禁用全屏

    @override
    def closeEvent(self, a0: QCloseEvent | None) -> None:  # pylint: disable=C0103
        appLogger.info("程序已退出")
        return super().closeEvent(a0)
