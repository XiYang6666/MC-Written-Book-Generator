from io import StringIO
from PyQt6.QtWidgets import QTextEdit


class Buffer(StringIO):
    def __init__(self, textEdit: QTextEdit) -> None:
        super().__init__()
        self.textEdit = textEdit

    def write(self, __s: str) -> int:
        result = super().write(__s)
        self.textEdit.setHtml(self.getvalue())
        scrollbar = self.textEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())  # type:ignore
        return result
