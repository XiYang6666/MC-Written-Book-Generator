import logging
from logging import FileHandler, StreamHandler
from datetime import datetime
from pathlib import Path

from colorlog import ColoredFormatter

appLogger = logging.getLogger("app")
appLogger.setLevel(logging.INFO)

# 设置控制台输出
consoleHandler = StreamHandler()
logColors = {
    "DEBUG": "white",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "purple",
}
consoleFormatter = ColoredFormatter(
    "%(log_color)s%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s",
    log_colors=logColors,
)
consoleHandler.setFormatter(consoleFormatter)
appLogger.addHandler(consoleHandler)

# 设置文件输出
logDir = Path("logs")
if not logDir.is_dir():
    logDir.mkdir()
logPath = Path(f"logs/app_{datetime.now().date()}.log")
logPath.touch()
fileHandler = FileHandler(logPath, encoding="utf-8")
fileFormatter = logging.Formatter(
    "%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s"
)
fileHandler.setFormatter(fileFormatter)
appLogger.addHandler(fileHandler)
