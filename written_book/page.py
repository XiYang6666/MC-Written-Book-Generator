import re
import unicodedata
import nbtlib
import json

from .config import EXTENDED_WIDTH_DICT


def isChineseOrJapanese(char):
    name = unicodedata.name(char).split()
    return "CJK" in name or (
        ("HIRAGANA" in name or "KATAKANA" in name) and not "HALFWIDTH" in name
    )


def isHalfWidthJapanese(char):
    name = unicodedata.name(char).split()
    return "HALFWIDTH" in name and "KATAKANA" in name


def isFullWidth(char):
    name = unicodedata.name(char).split()
    return "FULLWIDTH" in name


WIDTH_DICT = {
    2: lambda char: re.match(r"^['|!]$", char),
    4: lambda char: re.match(r"^[..·()\[\];,Ⅰ‘’]$", char),
    6: lambda char: re.match(r"^[1fijltI-—-{}\" <>]$", char),
    8: lambda char: re.match(
        r"^[023456789abcdeghkmnopqrsuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ~@#$&……&*?=/\\+_℃ⅡⅢⅣⅤⅨⅩⅪⅫ“”]$",
        char,
    )
    or isHalfWidthJapanese(char),
    10: lambda char: re.match(r"^[ⅥⅦⅧ]$", char),
    18: lambda char: re.match(r"^[（）【】！￥……；：，。、？《》　﹝﹞〔〕]$", char)
    or isChineseOrJapanese(char)
    or isFullWidth(char),
}

PAGE_WIDTH = 228
PAGE_HEIGHT = 14


class Page:
    def __init__(
        self,
        string: str,
        *,
        extended_width_dict={},
    ):
        """
        生成一张书页

        Args:
            - string(str): 输入文本
            - *
            - extended_width_dict(dict): 扩展字符宽度字典
        """
        self.string = ""  # 书页的字符
        self.extended_width_dict = extended_width_dict  # 扩展字符长度字典
        self.length = self.create(string)  # 书页字符数

    def create(self, string: str) -> int:
        """
        创建一张书页

        Args:
            - string(str): 输入文本
            - escapeWrap(bool): 是否转义换行符
            - extended_width_dict(dict): 扩展字符宽度字典
            
        Returns:
            - int: 创建书页使用的字符数
        """
        dbg_line = ""  # 调试输出单行字符

        lineWidth = 0  # 本行长度
        line = 0  # 行数量
        length = 0  # 字符数
        for char in string:
            charWidth = self.getCharWidth(char)
            if (lineWidth + charWidth) > PAGE_WIDTH or char == "\n":
                # 单行字符过多，换行

                if char == "\n":
                    self.string += char
                    dbg_line += char
                line += 1
                lineWidth = 0
                # print(f"-> 换行了 {line} {len(dbg_line)} {dbg_line}")
                dbg_line = ""

                if line >= PAGE_HEIGHT:
                    # 翻页
                    break
                # 未翻页
                ...
            if not char == "\n":
                self.string += char
                dbg_line += char
            lineWidth += charWidth
            length += 1
        return length

    def getCharWidth(self, char: str) -> int:
        """
        获取字符宽度

        Args:
            - char(str): 输入字符

        Returns:
            - int: 字符宽度
        """
        if char == "\n":
            return 0
        for width in WIDTH_DICT:
            if WIDTH_DICT[width](char):
                return width
            extended_width_dict = {**EXTENDED_WIDTH_DICT, **self.extended_width_dict} #type:dict
        if char in extended_width_dict: # type: ignore
            return extended_width_dict[char] # type: ignore
        raise ValueError(f"Width data without character “{char}”")

    def getNbt(self, *, escapeWrap=True, json_text=True) -> nbtlib.String:
        """
        获取书页的nbt

        Args
            - *
            - escapeWrap(bool): 是否转义换行符(json_text为True时该参数无效)
            - json_text(bool): 是否使用JSON字符(启用会占用更多空间,不启用无法换行)

        Returns:
            - nbtlib.String: 书页的nbt
        """
        resultString = ""
        if json_text:
            resultString = json.dumps({"text": self.string}, ensure_ascii=False)
        else:
            resultString = self.string
            if escapeWrap:
                resultString = resultString.replace("\n", "\\n")

        nbt = nbtlib.String(resultString)
        return nbt

    @classmethod
    def fromNbt(cls, nbt: nbtlib.Compound):
        string = nbt.get("text", "").unpack()  # type: ignore
        return cls(string)
