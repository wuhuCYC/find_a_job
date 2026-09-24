"""HTTP 客户端：统一超时、重试、礼貌间隔。抓公开招聘接口要温柔。"""
from __future__ import annotations

import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36 jobhunt/0.1 (personal job search)"
)


class HttpError(RuntimeError):
    """请求失败（带状态码，方便 check 命令报告哪个公司配置坏了）。"""

    def __init__(self, url: str, status: int | None, message: str):
        super().__init__(f"{status or 'ERR'} {url}: {message}")
        self.url = url
        self.status = status


class Http:
    def __init__(self, delay: float = 0.6, timeout: float = 20.0):
        self.delay = delay
        self.timeout = timeout
        self._last = 0.0
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST"}),
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, text/html;q=0.9"})

    def _throttle(self) -> None:
        wait = self.delay - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        self._throttle()
        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        except requests.RequestException as exc:
            raise HttpError(url, None, str(exc)) from exc
        if resp.status_code >= 400:
            raise HttpError(url, resp.status_code, resp.text[:200])
        return resp

    def get_json(self, url: str, params: dict | None = None) -> Any:
        return self._request("GET", url, params=params).json()

    def post_json(self, url: str, payload: dict) -> Any:
        return self._request("POST", url, json=payload, headers={"Content-Type": "application/json"}).json()

    def get_text(self, url: str, params: dict | None = None) -> str:
        return self._request("GET", url, params=params).text
