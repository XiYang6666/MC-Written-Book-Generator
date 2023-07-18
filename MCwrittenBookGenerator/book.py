import nbtlib

from .page import Page


class Book:
    MAX_PAGE = 100

    def __init__(
        self,
        *,
        title: str = "writtenBook",
        author: str = "XiYang6666/writtenBookGenerator",
        pages: list[Page] = [],
        string: str | None = None,
        extended_width_dict={},
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
        self.title = title  # 标题
        self.author = author  # 作者
        self.length = 0  # 成书的字符数
        if string is None:
            self.pages = pages  # 书页列表
        else:
            self.pages = []
            self.length = self.createBook(
                string,
                extended_width_dict=extended_width_dict,
            )

    def createBook(
        self,
        string,
        *,
        extended_width_dict={},
    ) -> int:
        """
        用文本创建一本书

        Args:
            - string(str): 输入文本
            - *
            - extended_width_dict(dict): 扩展字符宽度字典
        Returns:
            - int: 创建书使用的字符数
        """
        length = 0
        for i in range(self.MAX_PAGE):
            bookPage = self.createPage(
                string[length:],
                extended_width_dict=extended_width_dict,
            )
            # print(bookPage.string)
            length += bookPage.length
            # print(f"--------------->翻页了 {i}")
            if length >= len(string):
                break
        return length

    def createPage(
        self,
        string: str,
        *,
        extended_width_dict={},
    ) -> Page | bool:
        """
        创建书页并添加到书中

        成功返回书页对象,失败返回False

        Args:
            - string(str): 输入文本
            - *
            - extended_width_dict(dict): 扩展字符宽度字典
        Returns:
            - Page|bool: 成功返回书页对象,失败返回False
        """
        result = self.addPage(
            page := Page(
                string,
                extended_width_dict=extended_width_dict,
            )
        )
        return page if result else result

    def addPage(self, bookPage: Page = Page("")) -> bool:
        """
        添加书页

        返回是否成功

        Args:
            -bookPage(Page): 书页
        Returns:
            bool: 是否成功添加
        """
        if len(self.pages) >= 100:
            return False
        else:
            self.pages.append(bookPage)
            return True

    def getNbt(self, *, escapeWrap=True, json_text=True) -> nbtlib.Compound:
        """
        获取成书的nbt

        Returns:
            - nbtlib.Compound: 成书的nbt
            - *
            - escapeWrap(bool): 是否转义换行符(json_text为True时该参数无效)
            - json_text(bool): 是否使用JSON字符(会占用更多空间)
        """
        nbt = nbtlib.Compound()
        nbt["title"] = nbtlib.String(self.title)
        nbt["author"] = nbtlib.String(self.author)
        nbt["pages"] = nbtlib.List(
            [
                page.getNbt(
                    escapeWrap=escapeWrap,
                    json_text=json_text,
                )
                for page in self.pages
            ]
        )
        return nbt


# if __name__ == "__main__":
#     with open("刘慈欣 - 三体.txt", "r", encoding="GBK") as f:
#         string = f.read()
#     book = Book()
#     length = 0
#     for i in range(2):
#         length += (bookPage := Page(string[length:]))
#         book.addPage(bookPage)

#     print(book.getNbt())
