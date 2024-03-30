import sys
import json
import zipfile
from logging import StreamHandler
from pathlib import Path

import chardet
import nbtlib
from PyQt6.QtWidgets import QApplication  # pylint: disable=E0611
from PyQt6.QtWidgets import QFileDialog, QMessageBox  # pylint: disable=E0611

from written_book import create_book_collection
from .logger import appLogger, logColors
from .logger.html_colored_formatter import HtmlColoredFormatter
from .output_buffer import Buffer
from .mainwindow import MainWindow


class App(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.setup()

    def setup(self):
        appLogger.info("初始化")
        self.main_window = MainWindow()
        self.main_window.show()
        # 绑定选择文件按钮事件
        self.main_window.pb_selectFile.clicked.connect(self.select_file)
        # 绑定生成按钮事件
        self.main_window.pb_create.clicked.connect(self.create)
        # 输出缓冲区
        self.output_buffer = Buffer(self.main_window.te_output)
        log_colors_new = logColors.copy()
        log_colors_new["WARNING"] = "orange"  # 黄色在白色背景下看不清
        formatter = HtmlColoredFormatter(
            "[%(levelname)s] %(message)s", log_colors=log_colors_new
        )
        handler = StreamHandler(stream=self.output_buffer)
        handler.setFormatter(formatter)
        appLogger.addHandler(handler)
        appLogger.info("初始化完成")

    def select_file(self):
        # 获取文件
        appLogger.info("正在选择文件")
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "选择文件",
            str(Path.home() / "Desktop"),
            "Text Files (*.txt);;All Files (*)",
        )
        # 设置显示文件路径
        self.main_window.le_filePath.setText(file_path)
        appLogger.info("文件选择完毕")

    def create(self):
        # 打开文件
        file_path = self.main_window.le_filePath.text()
        # 判断是否为空
        if self.main_window.le_filePath.text() == "":
            # 为空 弹出警告
            appLogger.warning("未选择文件")
            QMessageBox.warning(self.main_window, "警告", "请先选择文件")
            return
        # 判断文件是否存在
        file_path = Path(file_path)
        if not file_path.is_file():
            # 不存在 弹出警告
            appLogger.warning("文件不存在,请选择正确的文件")
            QMessageBox.warning(self.main_window, "警告", "文件不存在")
            return
        # 获取编码格式
        appLogger.info("正在获取编码格式")
        if self.main_window.cb_encoding.currentText() == "自动识别(可能不准确)":
            appLogger.info("正在自动识别编码格式")
            with open(file_path, "rb") as f:
                file_encoding = chardet.detect(f.read())["encoding"]
            if file_encoding is None:
                appLogger.warning(
                    "自动识别失败,错误的编码格式,请选择编码格式正确的文件"
                )
                QMessageBox.warning(self.main_window, "警告", "错误的编码格式")
                return
            appLogger.info(  # pylint: disable=W1203
                f"自动识别编码格式: {file_encoding}"
            )
        else:
            file_encoding = self.main_window.cb_encoding.currentText()
        # 打开文件
        appLogger.info("正在打开文件")
        try:
            with open(file_path, "r", encoding=file_encoding) as f:
                book_content = f.read()
        except UnicodeDecodeError:
            appLogger.error("文件打开失败,编码格式错误")
            return
        else:
            appLogger.info("文件打开成功")

        # 获取成书信息
        appLogger.info("正在获取配置")
        book_title = self.main_window.le_title.text()  # 成书标题
        book_author = self.main_window.le_author.text()  # 成书作者
        # 获取生成配置
        output_type = self.main_window.cb_outputType.currentText()
        export_format = self.main_window.cb_exportFormat.currentText()
        # 生成成书
        self.create_written_book(
            book_content, book_title, book_author, output_type, export_format
        )

    def create_written_book(
        self, content: str, title: str, author: str, outputType: str, exportFormat: str
    ):
        # 读取扩展宽度数据
        appLogger.info("正在读取扩展宽度数据")
        with open("extended_width.json", encoding="utf-8") as f:
            extend_width_dict = json.load(f)
        appLogger.info("开始生成")
        try:
            book_list = create_book_collection(
                content,
                title=title,
                author=author,
                extended_width_dict=extend_width_dict,
            )
        except ValueError as e:
            appLogger.error(str(e))
            appLogger.warning("生成失败,请在extended_width.json中添加对应字符的宽度")
            return
        appLogger.info("生成完毕")
        appLogger.info("开始导出")
        appLogger.info("开始处理导出类型")
        result_nbt_list = []
        item_name = "written_book"
        match outputType:
            case "成书":
                item_name = "written_book"
                result_nbt_list = [book.get_nbt() for book in book_list]
            case "潜影盒":
                item_name = "white_shulker_box"
                result_nbt_list = []
                temp_list = [
                    book_list[i : i + 27] for i in range(0, len(book_list), 27)
                ]
                for shulker_box_books in temp_list:
                    shulker_box_block_nbt = nbtlib.Compound()
                    items_nbt_list = []
                    for i, book in enumerate(shulker_box_books):
                        item_nbt = nbtlib.Compound()
                        item_nbt["Slot"] = nbtlib.Byte(i)
                        item_nbt["id"] = nbtlib.String("minecraft:written_book")
                        item_nbt["Count"] = nbtlib.Byte(16)
                        item_nbt["tag"] = book.get_nbt()
                        items_nbt_list.append(item_nbt)
                    shulker_box_items_nbt = nbtlib.List(items_nbt_list)
                    shulker_box_block_nbt["Items"] = shulker_box_items_nbt
                    shulker_box_nbt = nbtlib.Compound()
                    shulker_box_nbt["BlockEntityTag"] = shulker_box_block_nbt
                    result_nbt_list.append(shulker_box_nbt)

        appLogger.info("开始处理导出格式")
        # 判断输出路径是否合法
        output_path = Path("output")
        if output_path.is_file():
            output_path.unlink()
        if not output_path.is_dir():
            output_path.mkdir()
        # 清空输出路径
        for file in output_path.iterdir():
            file.unlink()

        match exportFormat:
            case "TXT 指令":
                for i, nbt in enumerate(result_nbt_list):
                    with open(
                        f"output/command_volume{i}.txt",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(f"/give @p {item_name}" + nbt.snbt())
            case "函数文件":
                result = ""
                for nbt in result_nbt_list:
                    result += f"give @p {item_name}" + nbt.snbt() + "\n"
                with open(
                    "output/get_written_book.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(result)
            case "数据包":
                result = ""
                for nbt in result_nbt_list:
                    result += f"give @p {item_name}" + nbt.snbt() + "\n"
                # 处理路径
                func_path = Path(
                    "gui/datapack_template/data/written_book_generator/functions"
                )
                func_path.mkdir(parents=True, exist_ok=True)
                # 写入函数
                with open(
                    func_path / "get_written_books.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(result)
                # 压缩文件
                zip_obj = zipfile.ZipFile(
                    "output/written_book_datapack.zip",
                    "w",
                    compression=zipfile.ZIP_DEFLATED,
                )
                datapack_template_path = Path("gui/datapack_template")
                for file in datapack_template_path.rglob("*"):
                    zip_obj.write(file, file.relative_to(datapack_template_path))
        appLogger.info("导出完毕,请在output目录查看输出")


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
