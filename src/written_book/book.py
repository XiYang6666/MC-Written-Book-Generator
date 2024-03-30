from typing import Optional, Self
import nbtlib

from .exception.add_page_failed_exception import AddPageFailedException
from .page import Page

MAX_PAGE = 100


class Book:
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        author: Optional[str] = None,
        pages: Optional[list[Page]] = None,
    ):
        """
        创建一本成书

        如果string不是None则用输入的string创建书

        Args:
            - *
            - title(str): 成书标题
            - author(str): 成书作者
            - pages(list[Page]): 书页列表
            - string(str): 输入文本
            - extended_width_dict(dict): 扩展字符宽度字典

        Returns:
        """

        self.title = title or "writtenBook"
        self.author = author or "XiYang6666/writtenBookGenerator"
        self.pages = pages or []

    @classmethod
    def from_string(
        cls,
        string: str,
        *,
        title: Optional[str] = None,
        author: Optional[str] = None,
        extended_width_dict: Optional[dict] = None,
    ) -> Self:
        """
        用文本创建一本书

        Args:
            - string(str): 输入文本
            - *
            - extended_width_dict(dict): 扩展字符宽度字典

        Returns:
            - int: 创建书使用的字符数
        """

        instance = cls(title=title, author=author)
        length = 0  # 不使用instance.get_length()避免不必要的性能损耗

        for _ in range(MAX_PAGE):
            page = Page(string[length:], extended_width_dict=extended_width_dict)
            if not instance.add_page(page):
                raise AddPageFailedException()
            length += page.length
            if length >= len(string):
                break

        return instance

    def get_length(self) -> int:
        result = 0
        for page in self.pages:
            result += page.length
        return result

    def add_page(self, book_page: Page) -> bool:
        """
        添加书页

        返回是否成功

        Args:
            -bookPage(Page): 书页对象

        Returns:
            bool: 是否成功添加
        """

        if len(self.pages) >= MAX_PAGE:
            return False
        else:
            self.pages.append(book_page)
            return True

    def get_nbt(self, *, escapeWrap=True, json_text=True) -> nbtlib.Compound:
        """
        获取成书的nbt

        Args:
            - *
            - escapeWrap(bool): 是否转义换行符(json_text为True时该参数无效)
            - json_text(bool): 是否使用JSON字符(启用会占用更多空间,不启用无法换行)

        Returns:
            - nbtlib.Compound: 成书的nbt
        """
        nbt = nbtlib.Compound()
        nbt["title"] = nbtlib.String(self.title)
        nbt["author"] = nbtlib.String(self.author)
        nbt["pages"] = nbtlib.List(
            [
                page.get_nbt(
                    escape_wrap=escapeWrap,
                    json_text=json_text,
                )
                for page in self.pages
            ]
        )
        return nbt
