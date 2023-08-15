import sys
import json
import logging
import zipfile
from logging import StreamHandler
from pathlib import Path

import chardet
import nbtlib
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from .logger import appLogger, log_colors
from .logger.htmlColoredFormatter import HtmlColoredFormatter
from .output_buffer import Buffer
from .mainwindow import MainWindow
from written_book import CreateBookCollection


class App(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.setup()

    def setup(self):
        appLogger.info("初始化")
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        # 绑定选择文件按钮事件
        self.mainWindow.pb_selectFile.clicked.connect(self.selectFile)
        # 绑定生成按钮事件
        self.mainWindow.pb_create.clicked.connect(self.create)
        # 输出缓冲区
        self.output_buffer = Buffer(self.mainWindow.te_output)
        log_colors_new = log_colors.copy()
        log_colors_new["WARNING"] = "orange"  # 黄色在白色背景下看不清
        formatter = HtmlColoredFormatter(
            "[%(levelname)s] %(message)s", log_colors=log_colors_new
        )
        handler = StreamHandler(stream=self.output_buffer)
        handler.setFormatter(formatter)
        appLogger.addHandler(handler)
        appLogger.info("初始化完成")

    def selectFile(self):
        # 获取文件
        appLogger.info("正在选择文件")
        filePath, FileType = QFileDialog.getOpenFileName(
            self.mainWindow,
            "选择文件",
            str(Path.home() / "Desktop"),
            "Text Files (*.txt);;All Files (*)",
        )
        # 设置显示文件路径
        self.mainWindow.le_filePath.setText(filePath)
        appLogger.info("文件选择完毕")

    def create(self):
        # 打开文件
        filePath = self.mainWindow.le_filePath.text()
        # 判断是否为空
        if self.mainWindow.le_filePath.text() == "":
            # 为空 弹出警告
            appLogger.warn("未选择文件")
            QMessageBox.warning(self.mainWindow, "警告", "请先选择文件")
            return
        # 判断文件是否存在
        filePath = Path(filePath)
        if not filePath.is_file():
            # 不存在 弹出警告
            appLogger.warn("文件不存在,请选择正确的文件")
            QMessageBox.warning(self.mainWindow, "警告", "文件不存在")
            return
        # 获取编码格式
        appLogger.info("正在获取编码格式")
        if self.mainWindow.cb_encoding.currentText() == "自动识别(可能不准确)":
            appLogger.info("正在自动识别编码格式")
            with open(filePath, "rb") as f:
                fileEncoding = chardet.detect(f.read())["encoding"]
            if fileEncoding is None:
                appLogger.warn("自动识别失败,错误的编码格式,请选择编码格式正确的文件")
                QMessageBox.warning(self.mainWindow, "警告", "错误的编码格式")
                return
            appLogger.info(f"自动识别编码格式: {fileEncoding}")
        else:
            fileEncoding = self.mainWindow.cb_encoding.currentText()
        # 打开文件
        appLogger.info("正在打开文件")
        try:
            with open(filePath, "r", encoding=fileEncoding) as f:
                bookContent = f.read()
        except UnicodeDecodeError:
            appLogger.error("文件打开失败,编码格式错误")
            return
        else:
            appLogger.info("文件打开成功")

        # 获取成书信息
        appLogger.info("正在获取配置")
        bookTitle = self.mainWindow.le_title.text()  # 成书标题
        bookAuthor = self.mainWindow.le_author.text()  # 成书作者
        # 获取生成配置
        outputType = self.mainWindow.cb_outputType.currentText()
        exportFormat = self.mainWindow.cb_exportFormat.currentText()
        # 生成成书
        self.createWrittenBook(
            bookContent, bookTitle, bookAuthor, outputType, exportFormat
        )

    def createWrittenBook(
        self, content: str, title: str, author: str, outputType: str, exportFormat: str
    ):
        # 读取扩展宽度数据
        appLogger.info("正在读取扩展宽度数据")
        with open("extended_width.json", encoding="utf-8") as f:
            extendWidthDict = json.load(f)
        appLogger.info("开始生成")
        try:
            bookList = CreateBookCollection(
                content,
                title,
                author,
                extended_width_dict=extendWidthDict,
            )
        except ValueError as e:
            appLogger.error(str(e))
            appLogger.warn("生成失败,请在extended_width.json中添加对应字符的宽度")
            return
        appLogger.info("生成完毕")
        appLogger.info("开始导出")
        appLogger.info("开始处理导出类型")
        resultNbtList = []
        match outputType:
            case "成书":
                resultNbtList = [book.getNbt() for book in bookList]
            case "潜影盒":
                resultNbtList = []
                temp_list = [bookList[i : i + 27] for i in range(0, len(bookList), 27)]
                for shulkerBoxBooks in temp_list:
                    shulkerBoxNbt = nbtlib.Compound()
                    shulkerBoxItemsNbt = nbtlib.List()
                    for i in range(len(shulkerBoxBooks)):
                        book = shulkerBoxBooks[i]
                        bookNbt = book.getNbt()
                        itemNbt = nbtlib.Compound()
                        itemNbt["Solt"] = nbtlib.Byte(i)
                        itemNbt["id"] = nbtlib.String("minecraft:written_book")
                        itemNbt["Count"] = nbtlib.Byte(16)
                        itemNbt["tag"] = book
                        shulkerBoxItemsNbt.append(itemNbt)
                    shulkerBoxNbt["Items"] = shulkerBoxItemsNbt
                    resultNbtList.append(shulkerBoxNbt)

        appLogger.info("开始处理导出格式")
        # 判断输出路径是否合法
        outputPath = Path("output")
        if outputPath.is_file():
            outputPath.unlink()
        if not outputPath.is_dir():
            outputPath.mkdir()
        # 清空输出路径
        for file in outputPath.iterdir():
            file.unlink()

        match exportFormat:
            case "TXT 指令":
                for i in range(len(resultNbtList)):
                    nbt = resultNbtList[i]
                    with open(
                        f"output/command_volume{i}.txt", "w", encoding="utf-8"
                    ) as f:
                        f.write("/give @p written_book" + nbt.snbt())
            case "函数文件":
                result = ""
                for nbt in resultNbtList:
                    result += f"give @p written_book" + nbt.snbt() + "\n"
                with open(
                    f"output/get_written_book.mcfunction", "w", encoding="utf-8"
                ) as f:
                    f.write(result)
            case "数据包":
                result = ""
                for nbt in resultNbtList:
                    result += f"give @p written_book" + nbt.snbt() + "\n"
                # 写入函数
                with open(
                    "gui/datapack_template/data/written_book_generator/functions/get_written_books.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(result)
                # 压缩文件
                zipObj = zipfile.ZipFile(
                    "output/written_book_datapack.zip",
                    "w",
                    compression=zipfile.ZIP_DEFLATED,
                )
                datapackTemplatePath = Path("gui/datapack_template")
                for file in datapackTemplatePath.rglob("*"):
                    zipObj.write(file, file.relative_to(datapackTemplatePath))
        appLogger.info("导出完毕,请在output目录查看输出")


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
