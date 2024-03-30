#!/usr/bin/env python3

import sys
import argparse
import json

from written_book import Book, create_book_collection

parser = argparse.ArgumentParser(description="Generate written books in Minecraft")
parser.add_argument("txt_path", type=str)
parser.add_argument(
    "-e", "--encoding", help="Encoding method for txt", default="utf-8", type=str
)
parser.add_argument("-t", "--title", help="Title of the written book", type=str)
parser.add_argument("-a", "--author", help="Author of the written book", type=str)

args = parser.parse_args()
txtPath = args.txt_path
encoding = args.encoding
title = args.title
author = args.author

if title is None:
    title = input("title: ")
    if title == "":
        title = "writtenBook"

if author is None:
    author = input("author: ")
    if author == "":
        author = None

with open("extended_width.json", encoding="utf-8") as f:
    extended_width_dict = json.load(f)

with open(txtPath, "r", encoding=encoding) as f:
    string = f.read()

book_list = create_book_collection(string, title, author, extended_width_dict)
for i in range(len(book_list)):
    book = book_list[i]  # type:Book
    with open(f"output-{i+1}.txt", "w", encoding="utf-8") as f:
        f.write("/give @p written_book" + book.get_nbt().snbt())

print("done.")
