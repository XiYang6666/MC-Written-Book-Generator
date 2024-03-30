from collections.abc import Mapping
from logging import Formatter, LogRecord
from typing import Any


class HtmlColoredFormatter(Formatter):
    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style="%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
        log_colors: dict,
    ) -> None:
        super().__init__(
            fmt, datefmt, style, validate, defaults=defaults  # type:ignore
        )
        self.log_colors = log_colors

    def formatMessage(self, record: LogRecord) -> str:
        result = super().formatMessage(record)
        color = self.log_colors[record.levelname]
        return f'<span style="color:{color}">{result}</span><br>'
