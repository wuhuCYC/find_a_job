"""本地网站服务（只监听 127.0.0.1）。用标准库 http.server，不引入额外依赖。

读：  GET  /                页面
      GET  /api/data        全量数据
      GET  /api/job?uid=    职位 JD 全文
      GET  /api/task?id=    后台任务状态
      GET  /files/<path>    output/ 下的 PDF / 报告（只允许这几种后缀）
写：  POST /api/status      {uid, status, note?}
      POST /api/tailor      {uid}      后台定制简历（调用 Claude）
      POST /api/apply       {uid}      后台打开浏览器预填（不点提交）
      POST /api/base        {}         后台生成基础简历
      POST /api/fetch       {}         后台抓取 + 打分
      POST /api/score       {}         重新打分

安全：写接口必须带 X-Jobhunt: 1 头且是 JSON（跨站页面发不出这种请求）；Host 必须是本机或 --allow-host
     指定的域名（防 DNS rebinding）。部署到服务器时仍只监听 127.0.0.1，由 nginx 反代并加密码（见 deploy/）。
"""
from __future__ import annotations

import json
import mimetypes
import threading
import traceback
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from .. import config
from ..store import STATUSES, Store
from .data import build_payload
from .export import STATIC, wrap_document

ALLOWED_FILE_SUFFIXES = {".pdf", ".md", ".yaml", ".txt"}
LOCAL_HOSTS = {"127.0.0.1", "localhost", "[::1]"}


class Tasks:
    """后台任务：定制简历、抓取这类慢操作放到线程里跑，前端轮询状态。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._tasks: dict[str, dict] = {}

    def start(self, kind: str, label: str, fn) -> str:
        task_id = uuid.uuid4().hex[:12]
        with self._lock:
            self._tasks[task_id] = {"id": task_id, "kind": kind, "label": label, "status": "running",
                                    "result": None, "error": None}

        def run():
            try:
                result = fn()
                self._update(task_id, status="done", result=result)
            except Exception as exc:  # noqa: BLE001 —— 错误原样回给前端
                traceback.print_exc()
                self._update(task_id, status="error", error=f"{exc.__class__.__name__}: {exc}")

        threading.Thread(target=run, daemon=True).start()
        return task_id

    def _update(self, task_id: str, **kw) -> None:
        with self._lock:
            self._tasks[task_id].update(kw)

    def get(self, task_id: str) -> dict | None:
        with self._lock:
            task = self._tasks.get(task_id)
            return dict(task) if task else None


def _jsonable(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


def safe_output_path(rel: str) -> Path | None:
    """把 /files/<rel> 映射到 output/ 下的文件；越界或后缀不允许就返回 None。"""
    base = config.OUTPUT_DIR.resolve()
    target = (base / unquote(rel)).resolve()
    if base not in target.parents or target.suffix.lower() not in ALLOWED_FILE_SUFFIXES or not target.is_file():
        return None
    return target


def make_handler(tasks: Tasks, allowed_hosts: set[str] | None = None, server_mode: bool = False):
    """server_mode：部署在服务器上时关闭「打开浏览器预填」（服务器上没有你的浏览器）。"""
    page_cache: dict[str, str] = {}
    hosts = LOCAL_HOSTS | {h.lower() for h in (allowed_hosts or set())}

    class Handler(BaseHTTPRequestHandler):
        server_version = "jobhunt"

        def log_message(self, fmt, *args):  # 安静一点，只打印错误
            if args and str(args[1]).startswith(("4", "5")):
                super().log_message(fmt, *args)

        # ------------------------------------------------------------ 工具
        def _host_ok(self) -> bool:
            host = (self.headers.get("Host") or "").rsplit(":", 1)[0].lower()
            return host in hosts

        def _send(self, status: int, body: bytes, ctype: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, data, status: int = 200) -> None:
            self._send(status, json.dumps(_jsonable(data), ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8")

        def _error(self, status: int, message: str) -> None:
            self._json({"error": message}, status)

        # ------------------------------------------------------------ GET
        def do_GET(self):
            if not self._host_ok():
                return self._error(403, "只接受本机访问")
            url = urlparse(self.path)
            query = parse_qs(url.query)
            path = url.path
            if path in ("/", "/index.html"):
                if "page" not in page_cache:
                    page_cache["page"] = wrap_document((STATIC / "page.html").read_text(encoding="utf-8"))
                return self._send(200, page_cache["page"].encode("utf-8"), "text/html; charset=utf-8")
            if path in ("/app.css", "/app.js"):
                ctype = "text/css" if path.endswith(".css") else "text/javascript"
                return self._send(200, (STATIC / path[1:]).read_bytes(), f"{ctype}; charset=utf-8")
            if path == "/api/data":
                payload = build_payload(mode="live")
                payload["can_apply"] = not server_mode
                return self._json(payload)
            if path == "/api/job":
                uid = (query.get("uid") or [""])[0]
                store = Store()
                try:
                    job = store.get_job(uid)
                finally:
                    store.close()
                if not job:
                    return self._error(404, "找不到这个职位")
                return self._json({"uid": uid, "description": job.description, "url": job.url})
            if path == "/api/task":
                task = tasks.get((query.get("id") or [""])[0])
                return self._json(task) if task else self._error(404, "任务不存在")
            if path.startswith("/files/"):
                target = safe_output_path(path[len("/files/"):])
                if not target:
                    return self._error(404, "文件不存在或不允许访问")
                ctype = mimetypes.guess_type(target.name)[0] or "text/plain"
                if ctype.startswith("text/") or target.suffix in (".md", ".yaml"):
                    ctype = "text/plain; charset=utf-8"
                return self._send(200, target.read_bytes(), ctype)
            return self._error(404, "没有这个地址")

        # ------------------------------------------------------------ POST
        def do_POST(self):
            if not self._host_ok():
                return self._error(403, "只接受本机访问")
            if self.headers.get("X-Jobhunt") != "1" or "application/json" not in (self.headers.get("Content-Type") or ""):
                return self._error(403, "缺少 X-Jobhunt 头或不是 JSON 请求")
            try:
                length = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(length) or b"{}") if length else {}
            except (ValueError, json.JSONDecodeError):
                return self._error(400, "请求体不是合法 JSON")
            route = urlparse(self.path).path
            handler = {
                "/api/status": self._post_status,
                "/api/tailor": self._post_tailor,
                "/api/apply": self._post_apply,
                "/api/base": self._post_base,
                "/api/fetch": self._post_fetch,
                "/api/score": self._post_score,
            }.get(route)
            if not handler:
                return self._error(404, "没有这个接口")
            return handler(body)

        def _job_or_error(self, uid: str):
            store = Store()
            try:
                job = store.get_job(uid)
            finally:
                store.close()
            if not job:
                self._error(404, "找不到这个职位")
            return job

        def _post_status(self, body):
            uid, status, note = body.get("uid"), body.get("status"), body.get("note") or None
            if status not in STATUSES:
                return self._error(400, f"状态必须是 {STATUSES} 之一")
            if not self._job_or_error(uid):
                return None
            store = Store()
            try:
                store.set_status(uid, status, notes=note)
            finally:
                store.close()
            return self._json({"ok": True, "uid": uid, "status": status})

        def _post_tailor(self, body):
            from ..actions import tailor_job

            job = self._job_or_error(body.get("uid"))
            if not job:
                return None

            def run():
                store = Store()
                try:
                    result = tailor_job(job, store=store)
                finally:
                    store.close()
                out = config.OUTPUT_DIR.resolve()
                rel = lambda p: str(Path(p).resolve().relative_to(out)) if p else None  # noqa: E731
                return {"pdf": rel(result.get("pdf")), "report": rel(result["report"]), "pages": result.get("pages"),
                        "warnings": result["warnings"]}

            return self._json({"task": tasks.start("tailor", f"定制简历：{job.company} — {job.title}", run)})

        def _post_apply(self, body):
            from ..actions import resume_for
            from ..apply import apply_url_for, open_and_prefill

            if server_mode:
                return self._error(400, "服务器上不能打开浏览器预填，请在自己电脑上运行 python -m jobhunt apply")
            job = self._job_or_error(body.get("uid"))
            if not job:
                return None

            def run():
                store = Store()
                try:
                    resume = resume_for(store, job.uid)
                finally:
                    store.close()
                result = open_and_prefill(apply_url_for(job.url, job.apply_url), config.load_profile(), resume)
                store = Store()
                try:
                    store.set_status(job.uid, "prefilled")
                finally:
                    store.close()
                return {"filled": result["filled"], "uploaded": result["uploaded"],
                        "manual": [m.get("label") for m in result["manual"] if m.get("label")][:40]}

            return self._json({"task": tasks.start("apply", f"预填申请：{job.company} — {job.title}", run)})

        def _post_base(self, body):
            from ..actions import render_base

            def run():
                out = config.OUTPUT_DIR.resolve()
                return [{"archetype": r["archetype"], "pages": r["pages"],
                         "pdf": str(Path(r["pdf"]).resolve().relative_to(out)) if r["pdf"] else None}
                        for r in render_base()]

            return self._json({"task": tasks.start("base", "生成基础简历", run)})

        def _post_fetch(self, body):
            from ..actions import fetch_all, score_all

            def run():
                lines: list[str] = []
                new = fetch_all(log=lines.append)
                total, kept = score_all()
                return {"new": new, "total": total, "kept": kept, "log": lines}

            return self._json({"task": tasks.start("fetch", "抓取职位并打分", run)})

        def _post_score(self, body):
            from ..actions import score_all

            total, kept = score_all()
            return self._json({"total": total, "kept": kept})

    return Handler


def make_server(port: int = 8765, host: str = "127.0.0.1", allowed_hosts: set[str] | None = None,
                server_mode: bool = False) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), make_handler(Tasks(), allowed_hosts, server_mode))


def serve(port: int = 8765, open_browser: bool = True, allowed_hosts: set[str] | None = None,
          server_mode: bool = False) -> None:
    server = make_server(port, allowed_hosts=allowed_hosts, server_mode=server_mode)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"钱途求职台已启动：{url}（Ctrl+C 退出）" + ("  [服务器模式]" if server_mode else ""))
    if open_browser and not server_mode:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已退出")
    finally:
        server.server_close()
