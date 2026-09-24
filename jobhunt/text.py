"""文本工具：HTML → 纯文本、关键词匹配。"""
from __future__ import annotations

import html
import re
from html.parser import HTMLParser

_BLOCK_TAGS = {
    "p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6",
    "tr", "table", "section", "article", "header", "footer",
}
_SKIP_TAGS = {"script", "style", "noscript"}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip += 1
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS and self._skip:
            self._skip -= 1
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_to_text(raw: str | None) -> str:
    """把 JD 的 HTML 转成干净的纯文本。

    Greenhouse 的 content 是「转义过的 HTML」（&lt;p&gt;），所以先反转义一次再解析。
    """
    if not raw:
        return ""
    s = html.unescape(raw) if "&lt;" in raw else raw
    parser = _TextExtractor()
    parser.feed(s)
    parser.close()
    text = "".join(parser.parts).replace("\xa0", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def compile_keyword(kw: str) -> re.Pattern:
    """关键词 → 正则。`re:` 开头的按原样当正则，其余按词边界匹配（不区分大小写）。"""
    if kw.startswith("re:"):
        return re.compile(kw[3:], re.I)
    escaped = re.escape(kw.lower())
    # 以非字母数字结尾的词（如 c++）不能用 \b 收尾
    left = r"\b" if kw[:1].isalnum() else ""
    right = r"\b" if kw[-1:].isalnum() else ""
    return re.compile(left + escaped + right, re.I)


def find_keywords(text: str, patterns: dict[str, re.Pattern]) -> list[str]:
    """返回在 text 里命中的关键词（按字典顺序去重）。"""
    return [kw for kw, pat in patterns.items() if pat.search(text)]
