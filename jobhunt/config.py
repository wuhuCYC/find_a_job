"""配置加载：公司列表、岗位方向、搜索规则、个人档案。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(os.environ.get("JOBHUNT_HOME", Path(__file__).resolve().parent.parent))
CONFIG_DIR = ROOT / "config"
PROFILE_DIR = ROOT / "profile"
PRIVATE_DIR = ROOT / "private"
OUTPUT_DIR = ROOT / "output"
DATA_DIR = ROOT / "data"

ATS_TYPES = {"greenhouse", "lever", "ashby", "workday", "smartrecruiters", "icims", "jobvite", "manual"}


@dataclass
class CompanyConfig:
    key: str
    name: str
    tier: int = 2
    category: str = ""
    hq: str = ""
    ats: dict[str, Any] = field(default_factory=lambda: {"type": "manual"})
    enabled: bool = True
    verified: bool = False
    careers_url: str | None = None
    notes: str | None = None
    search_terms: list[str] = field(default_factory=list)
    map_city: str | None = None    # 网站地图上的落点城市（默认从 hq 推断）
    group: str | None = None       # 网站分组：buy_side / fintech / market（默认按 category 推断）

    @property
    def ats_type(self) -> str:
        return str(self.ats.get("type", "manual")).lower()


def load_yaml(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_companies(path: Path | None = None) -> list[CompanyConfig]:
    data = load_yaml(path or CONFIG_DIR / "companies.yaml") or {}
    companies = []
    for key, raw in (data.get("companies") or {}).items():
        raw = dict(raw or {})
        ats = raw.pop("ats", None) or {"type": "manual"}
        if ats.get("type") not in ATS_TYPES:
            raise ValueError(f"companies.yaml: {key} 的 ats.type={ats.get('type')!r} 不支持，可选 {sorted(ATS_TYPES)}")
        companies.append(CompanyConfig(key=key, ats=ats, **raw))
    return companies


def load_archetypes(path: Path | None = None) -> dict[str, dict]:
    return load_yaml(path or CONFIG_DIR / "archetypes.yaml") or {}


def load_search(path: Path | None = None) -> dict:
    return load_yaml(path or CONFIG_DIR / "search.yaml") or {}


def profile_path() -> Path:
    """优先读 private/profile.yaml（真实信息，不进 git），没有就用模板。"""
    private = PRIVATE_DIR / "profile.yaml"
    return private if private.exists() else PROFILE_DIR / "profile.example.yaml"


def load_profile(path: Path | None = None) -> dict:
    return load_yaml(path or profile_path()) or {}


def bank_path() -> Path:
    private = PRIVATE_DIR / "experience_bank.yaml"
    return private if private.exists() else PROFILE_DIR / "experience_bank.yaml"
