#!/usr/bin/env python3

import argparse
import json
from typing import Optional

from src.written_book import create_book_collection

parser = argparse.ArgumentParser(description="Generate written books in Minecraft")
parser.add_argument("txt_path", type=str)
parser.add_argument(
    "-e", "--encoding", help="Encoding method for txt", default="utf-8", type=str
)
parser.add_argument("-t", "--title", help="Title of the written book", type=str)
parser.add_argument("-a", "--author", help="Author of the written book", type=str)

args = parser.parse_args()
txtPath: str = args.txt_path
encoding: str = args.encoding
title: Optional[str] = args.title
author: Optional[str] = args.author

if title is None:
    title = input("title: ") or None

if author is None:
    author = input("author: ") or None

with open("extended_width.json", encoding="utf-8") as f:
    extended_width_dict = json.load(f)

with open(txtPath, "r", encoding=encoding) as f:
    string = f.read()

book_list = create_book_collection(
    string, title=title, author=author, extended_width_dict=extended_width_dict
)
for i, book in enumerate(book_list):
    with open(f"output-{i+1}.txt", "w", encoding="utf-8") as f:
        f.write(f"/give @p written_book {book.get_nbt().snbt()}")

print("done.")
