from .book import Book
from .page import Page

__all__ = ["Page", "Book"]


def CreateBookCollection(
    string: str,
    title: str = "writtenBook",
    author: str = None,
    extended_width_dict={},
) -> list[Book]:
    """
    创建书集

    title中的"{volume}"将被格式化为卷的序号

    Args:
        - string(str): 输入字符串
        - title(str): 书的标题
        - author(str): 书的作者
    Returns:
        - list[Book]: 书集列表
    """
    length = 0  # 字符长度
    volume = 0  # 卷序号
    bookList = []  # 书集列表
    while True:
        volume += 1
        book = Book(
            title=title.format(volume=volume),
            author=author,
            string=string[length:],
            extended_width_dict=extended_width_dict,
        )
        bookList.append(book)

        length += book.length
        if length >= len(string):
            break
    return bookList
