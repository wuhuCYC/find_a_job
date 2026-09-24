#!/usr/bin/env python3
"""在已有网站的 HTTPS server 块里加 / 删一行 `include snippets/jobhunt.conf;`。

给 remote_setup.sh 用：求职台挂在同一台 VPS 已有站点（sell_csgo_monitor）的 /jobs/ 子路径下，
不新开域名、不动 SaaS 的其他配置。只用标准库，服务器自带的 python3 就能跑。

    python3 nginx_include.py add    --host 1.2.3.4 --snippet /etc/nginx/snippets/jobhunt.conf
    python3 nginx_include.py remove --snippet /etc/nginx/snippets/jobhunt.conf

输出一行给 shell 解析：
    ADDED <配置文件> <备份>  |  ALREADY <配置文件>  |  REMOVED <配置文件> <备份>  |  NOTHING
出错时写 stderr，退出码 2，不改任何文件。备份放在 --backup-dir（不能放 sites-enabled，
那里的每个文件都会被 nginx 加载，备份会变成重复的 server 块）。
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import sys
from datetime import datetime

DEFAULT_DIRS = ["/etc/nginx/sites-enabled", "/etc/nginx/conf.d"]
MARK = "# find_a_job 求职台（deploy/nginx_include.py 添加）"


class ConfError(Exception):
    pass


# ------------------------------------------------------------------ 解析
def tokenize(text: str):
    """按 nginx 的规则切词：(kind, value, start, end)，kind 是 word / { / } / ;。
    # 只在词首算注释；引号里的内容原样保留；${var} 不是块。"""
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
            continue
        if c == "#":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "{};":
            yield c, c, i, i + 1
            i += 1
            continue
        start = i
        if c in "\"'":
            i += 1
            while i < n and text[i] != c:
                i += 2 if text[i] == "\\" else 1
            if i >= n:
                raise ConfError(f"引号没有闭合（第 {text.count(chr(10), 0, start) + 1} 行）")
            i += 1
            yield "word", text[start + 1:i - 1], start, i
            continue
        while i < n:
            c = text[i]
            if c == "\\" and i + 1 < n:
                i += 2
                continue
            if c == "{" and i > start and text[i - 1] == "$":
                j = text.find("}", i)
                if j < 0:
                    raise ConfError("${ 没有闭合")
                i = j + 1
                continue
            if c.isspace() or c in ";{}":
                break
            i += 1
        yield "word", text[start:i], start, i


class Node:
    def __init__(self, words: list[str], start: int):
        self.words = words
        self.start = start
        self.close: int | None = None   # 块的 } 位置
        self.children: list[Node] | None = None

    @property
    def name(self) -> str:
        return self.words[0] if self.words else ""


def parse(text: str) -> list[Node]:
    root: list[Node] = []
    stack: list[list[Node]] = [root]
    blocks: list[Node] = []
    words: list[str] = []
    wstart = 0
    for kind, value, start, _end in tokenize(text):
        if kind == "word":
            if not words:
                wstart = start
            words.append(value)
        elif kind == ";":
            stack[-1].append(Node(words, wstart))
            words = []
        elif kind == "{":
            node = Node(words, wstart if words else start)
            node.children = []
            stack[-1].append(node)
            stack.append(node.children)
            blocks.append(node)
            words = []
        else:  # }
            if words or not blocks:
                raise ConfError("大括号不配对，或 } 前少了分号")
            blocks.pop().close = start
            stack.pop()
    if blocks or words:
        raise ConfError("大括号不配对，或文件末尾少了分号")
    return root


def server_blocks(nodes: list[Node]):
    for node in nodes:
        if node.children is None:
            continue
        if node.name == "server":
            yield node
        else:  # http { server { ... } } 这种嵌套
            yield from server_blocks(node.children)


def _listens(block: Node) -> list[list[str]]:
    return [n.words[1:] for n in block.children or [] if n.name == "listen"]


def is_https(block: Node) -> bool:
    for args in _listens(block):
        addr = args[0] if args else ""
        if "ssl" in args or addr == "443" or addr.endswith(":443"):
            return True
    return False


def server_names(block: Node) -> list[str]:
    return [w.lower() for n in block.children or [] if n.name == "server_name" for w in n.words[1:]]


def includes_snippet(block: Node, snippet: str) -> bool:
    base = os.path.basename(snippet)
    for n in block.children or []:
        if n.name == "include" and len(n.words) > 1:
            target = n.words[1]
            if target == snippet or os.path.basename(target) == base:
                return True
    return False


# ------------------------------------------------------------------ 文件
def config_files(dirs: list[str]) -> list[str]:
    seen, files = set(), []
    for d in dirs:
        for path in sorted(glob.glob(os.path.join(d, "*"))):
            real = os.path.realpath(path)
            if not os.path.isfile(real) or real in seen:
                continue
            if d.rstrip("/").endswith("conf.d") and not path.endswith(".conf"):
                continue  # conf.d 只加载 *.conf
            seen.add(real)
            files.append(real)
    return files


def load(path: str) -> tuple[str, list[Node]]:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        return text, parse(text)
    except ConfError as exc:
        raise ConfError(f"{path}: {exc}") from None


def backup(path: str, backup_dir: str) -> str:
    os.makedirs(backup_dir, mode=0o700, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")   # 带微秒：同一秒内的两次备份不会互相覆盖
    dest = os.path.join(backup_dir, f"{os.path.basename(path)}.{stamp}.bak")
    shutil.copy2(path, dest)
    return dest


def insert_before_close(text: str, close: int, line: str) -> str:
    """在块的 } 前面插一行，缩进和块里的其他语句一致。"""
    line_start = text.rfind("\n", 0, close) + 1
    prefix = text[line_start:close]
    if prefix.strip() == "":   # } 独占一行
        return text[:line_start] + f"{prefix}    {line}\n" + text[line_start:]
    return text[:close] + f"\n    {line}\n" + text[close:]


# ------------------------------------------------------------------ 命令
def cmd_add(host: str, snippet: str, dirs: list[str], backup_dir: str, dry_run: bool = False) -> str:
    host = host.lower()
    parsed = {path: load(path) for path in config_files(dirs)}
    for path, (_text, nodes) in parsed.items():
        if any(includes_snippet(b, snippet) for b in server_blocks(nodes)):
            return f"ALREADY {path}"

    https = [(path, b) for path, (_t, nodes) in parsed.items() for b in server_blocks(nodes) if is_https(b)]
    matches = [(p, b) for p, b in https if host in server_names(b)]
    if not matches:
        matches = [(p, b) for p, b in https if any("default_server" in args for args in _listens(b))]
    if len(matches) != 1:
        found = "; ".join(f"{p}: server_name {' '.join(server_names(b)) or '(无)'}" for p, b in https) or "没有 HTTPS server 块"
        why = "没找到" if not matches else "找到多个"
        raise ConfError(f"{why} server_name 含 {host} 的 HTTPS server 块（{found}）。请手动在对应 server 块里加：include {snippet};")

    path, block = matches[0]
    text = parsed[path][0]
    new = insert_before_close(text, block.close, f"include {snippet};  {MARK}")
    parse(new)  # 插完还能解析
    if dry_run:
        return f"WOULD-ADD {path}"
    saved = backup(path, backup_dir)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return f"ADDED {path} {saved}"


def cmd_remove(snippet: str, dirs: list[str], backup_dir: str) -> str:
    for path in config_files(dirs):
        text, _ = load(path)
        lines = text.splitlines(keepends=True)
        keep = [ln for ln in lines if not ln.strip().startswith(f"include {snippet};")]
        if len(keep) != len(lines):
            new = "".join(keep)
            parse(new)
            saved = backup(path, backup_dir)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            return f"REMOVED {path} {saved}"
    return "NOTHING"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=["add", "remove"])
    ap.add_argument("--host", help="网站的 server_name（例如服务器 IP 或域名），add 时必填")
    ap.add_argument("--snippet", required=True)
    ap.add_argument("--dir", action="append", dest="dirs", help="nginx 站点配置目录（可重复），默认 sites-enabled + conf.d")
    ap.add_argument("--backup-dir", default="/var/backups/jobhunt-nginx")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    dirs = args.dirs or DEFAULT_DIRS
    try:
        if args.action == "add":
            if not args.host:
                raise ConfError("add 需要 --host")
            print(cmd_add(args.host, args.snippet, dirs, args.backup_dir, args.dry_run))
        else:
            print(cmd_remove(args.snippet, dirs, args.backup_dir))
    except (ConfError, OSError, UnicodeDecodeError) as exc:
        print(f"nginx_include: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
