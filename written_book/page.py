import re
from typing import Optional
import unicodedata
import json

import nbtlib


from .config import EXTENDED_WIDTH_DICT


def is_chinese_or_japanese(char):
    name = unicodedata.name(char).split()
    return "CJK" in name or (
        ("HIRAGANA" in name or "KATAKANA" in name) and "HALFWIDTH" not in name
    )


def is_half_width_japanese(char):
    name = unicodedata.name(char).split()
    return "HALFWIDTH" in name and "KATAKANA" in name


def is_full_width(char):
    name = unicodedata.name(char).split()
    return "FULLWIDTH" in name


WIDTH_DICT = {
    2: lambda char: re.match(r"^['|!]$", char),
    4: lambda char: re.match(r"^[.·()\[\]:;,Ⅰ‘’]$", char),
    6: lambda char: re.match(r"^[1fijltI\-—{}\" <>]$", char),
    8: lambda char: re.match(
        r"^[023456789abcdeghkmnopqrsuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ~@#$&…*?=/\\+_ⅡⅢⅣⅤⅨⅩⅪⅫ“”]$",
        char,
    )
    or is_half_width_japanese(char),
    10: lambda char: re.match(r"^[ⅥⅦⅧ]$", char),
    18: lambda char: re.match(r"^[（）【】！￥……；：，。、？《》　﹝﹞〔〕]$", char)
    or is_chinese_or_japanese(char)
    or is_full_width(char),
}


def get_char_width(char: str, extended_width_dict: Optional[dict] = None) -> int:
    """
    获取字符宽度

    Args:
        - char(str): 输入字符

    Returns:
        - int: 字符宽度
    """

    width_dict = {
        **EXTENDED_WIDTH_DICT,
        **(extended_width_dict or {}),
    }

    if char == "\n":
        return 0

    for width, func in WIDTH_DICT.items():
        if func(char):
            return width

    if char in width_dict:
        return width_dict[char]

    raise ValueError(f"Width data without character “{char}”")


PAGE_WIDTH = 228
PAGE_HEIGHT = 14


class Page:
    def __init__(self, string: str, *, extended_width_dict: Optional[dict] = None):
        """
        生成一张书页

        Args:
            - string(str): 输入文本
            - *
            - extended_width_dict(dict): 扩展字符宽度字典
        """

        self.string = ""
        self.length = 0

        line_width = 0  # 本行长度
        line = 0  # 行数量
        for char in string:
            char_width = get_char_width(char, extended_width_dict=extended_width_dict)
            if (line_width + char_width) > PAGE_WIDTH or char == "\n":
                if char == "\n":
                    self.string += char
                line += 1
                line_width = 0

                if line >= PAGE_HEIGHT:
                    break

            if not char == "\n":
                self.string += char
            line_width += char_width
            self.length += 1

    def get_nbt(self, *, escape_wrap=True, json_text=True) -> nbtlib.String:
        """
        获取书页的nbt

        Args
            - *
            - escapeWrap(bool): 是否转义换行符(json_text为True时该参数无效)
            - json_text(bool): 是否使用JSON字符(启用会占用更多空间,不启用无法换行)

        Returns:
            - nbtlib.String: 书页的nbt
        """
        result_string = ""
        if json_text:
            result_string = json.dumps({"text": self.string}, ensure_ascii=False)
        elif escape_wrap:
            result_string = result_string.replace("\n", "\\n")
        else:
            result_string = self.string

        nbt = nbtlib.String(result_string)
        return nbt

    @classmethod
    def from_nbt(cls, nbt: nbtlib.Compound):
        string = nbt.get("text", "")  # type:nbtlib.String
        return cls(string.unpack())
