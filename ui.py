#!/usr/bin/env python3

import sys

from src.written_book_gui import App

app = App(sys.argv)
sys.exit(app.exec())
