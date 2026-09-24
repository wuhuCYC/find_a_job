"""把网站导出成一个自包含的 HTML 文件（CSS / JS / 数据全部内联）。

--artifact 版本不带 <html>/<head>/<body> 外壳：Claude Artifact 发布时会自动套上。
"""
from __future__ import annotations

import json
from pathlib import Path

STATIC = Path(__file__).resolve().parent / "static"
CSS_TAG = '<link rel="stylesheet" href="app.css">'
JS_TAG = '<script src="app.js"></script>'


def wrap_document(page: str) -> str:
    return (
        '<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"</head>\n<body>\n{page}\n</body>\n</html>\n"
    )


def inline_page(payload: dict) -> str:
    page = (STATIC / "page.html").read_text(encoding="utf-8")
    css = (STATIC / "app.css").read_text(encoding="utf-8")
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    if CSS_TAG not in page or JS_TAG not in page:
        raise RuntimeError("page.html 里找不到 app.css / app.js 的引用")
    if "</script" in js.lower():
        raise RuntimeError("app.js 里不能出现 </script，否则内联会断")
    # JSON 放进 <script type="application/json">，转义 "</" 防止提前闭合
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = page.replace(CSS_TAG, f"<style>\n{css}\n</style>")
    page = page.replace(JS_TAG, f'<script id="snapshot" type="application/json">{data}</script>\n<script>\n{js}\n</script>')
    return page


def export_site(path: Path, standalone: bool = True, include_jobs: bool = True) -> Path:
    from .data import build_payload

    payload = build_payload(mode="snapshot", include_jobs=include_jobs, include_descriptions=True,
                            examples_if_empty=True)
    page = inline_page(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(wrap_document(page) if standalone else page, encoding="utf-8")
    return path
