from io import StringIO
from PyQt6.QtWidgets import QTextEdit  # pylint: disable=E0611


class Buffer(StringIO):
    def __init__(self, text_edit: QTextEdit) -> None:
        super().__init__()
        self.text_edit = text_edit

    def write(self, __s: str) -> int:
        result = super().write(__s)
        self.text_edit.setHtml(self.getvalue())
        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())  # type:ignore
        return result
