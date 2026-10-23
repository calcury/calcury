#!/usr/bin/env python3
"""把 README 里 QUOTE 区块替换成「今日一句」。

按日期序号取模选句子，同一天重复执行结果一致（幂等），
所以 Actions 重跑不会产生无意义的提交。
"""
from __future__ import annotations

import datetime
import pathlib
import re
import sys

START = "<!-- QUOTE:START -->"
END = "<!-- QUOTE:END -->"

QUOTES: list[tuple[str, str]] = [
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away.", "Antoine de Saint-Exupéry"),
    ("The most dangerous phrase in the language is, we have always done it this way.", "Grace Hopper"),
    ("The purpose of computing is insight, not numbers.", "Richard Hamming"),
    ("Measuring programming progress by lines of code is like measuring aircraft building progress by weight.", "Bill Gates"),
    ("There are only two hard things in computer science: cache invalidation and naming things.", "Phil Karlton"),
    ("Code is like humor. When you have to explain it, it is bad.", "Cory House"),
    ("A ship in port is safe, but that is not what ships are built for.", "Grace Hopper"),
    ("You cannot connect the dots looking forward; you can only connect them looking backwards.", "Steve Jobs"),
    ("The only way to learn a new programming language is by writing programs in it.", "Dennis Ritchie"),
    ("Controlling complexity is the essence of computer programming.", "Brian Kernighan"),
    ("Deleted code is debugged code.", "Jeff Sickel"),
    ("Science is what we understand well enough to explain to a computer. Art is everything else we do.", "Donald Knuth"),
    ("Everything should be made as simple as possible, but not simpler.", "Albert Einstein"),
    ("Imagination is more important than knowledge.", "Albert Einstein"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("One machine can do the work of fifty ordinary men. No machine can do the work of one extraordinary man.", "Elbert Hubbard"),
    ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
    ("It is not that I am so smart, it is just that I stay with problems longer.", "Albert Einstein"),
]


def build(day: datetime.date) -> str:
    text, author = QUOTES[day.toordinal() % len(QUOTES)]
    return f'{START}\n<div align="center"><i>\u201c{text}\u201d</i> \u2014 {author}</div>\n{END}'


def main() -> int:
    readme = pathlib.Path("README.md")
    source = readme.read_text(encoding="utf-8")
    pattern = re.escape(START) + r".*?" + re.escape(END)
    if not re.search(pattern, source, flags=re.S):
        print("README 里找不到 QUOTE 标记，跳过", file=sys.stderr)
        return 1

    updated = re.sub(pattern, build(datetime.date.today()), source, flags=re.S)
    if updated == source:
        print("今日一句无变化")
        return 0

    readme.write_text(updated, encoding="utf-8")
    print("已更新今日一句")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
