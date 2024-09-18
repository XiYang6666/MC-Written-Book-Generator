from typing import Optional
from .book import Book
from .page import Page


def create_book_collection(
    string: str,
    *,
    title: Optional[str] = None,
    author: Optional[str] = None,
    extended_width_dict: Optional[dict] = None,
) -> list[Book]:
    """
    创建书集

    title中的"{volume}"将被格式化为卷的序号

    Args:
        - string(str): 输入字符串
        - title(str): 书的标题
        - author(str): 书的作者
        - extended_width_dict(dict): 扩展宽度字典

    Returns:
        - list[Book]: 书集列表
    """

    title = title or "writtenBook"
    length = 0  # 字符长度
    volume = 0  # 卷序号
    book_list = []  # 书集列表
    while True:
        volume += 1
        book = Book.from_string(
            string[length:],
            title=title.format(volume=volume),
            author=author,
            extended_width_dict=extended_width_dict,
        )
        book_list.append(book)

        length += book.get_length()
        if length >= len(string):
            break
    return book_list


__all__ = ["Page", "Book", "create_book_collection"]
