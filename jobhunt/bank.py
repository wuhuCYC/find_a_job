"""经历素材库（profile/experience_bank.yaml）的加载与校验。"""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from .config import bank_path, load_yaml
from .guard import check_claims, check_skills, compile_vocabulary


class Fact(BaseModel):
    id: str
    text: str
    source: str = ""


class Bullet(BaseModel):
    id: str
    text: str
    label: str = ""                    # 网站上显示的中文短标签，不进简历
    facts: list[str] = Field(default_factory=list)
    weights: dict[str, int] = Field(default_factory=dict)


class Entry(BaseModel):
    id: str
    kind: str = "project"              # project / experience / research
    title: str
    role: str = ""
    org: str = ""
    location: str = ""
    start: str | int | None = None
    end: str | int | None = None
    url: str = ""
    stack: list[str] = Field(default_factory=list)
    facts: list[Fact] = Field(default_factory=list)
    bullets: list[Bullet] = Field(default_factory=list)

    def fact(self, fact_id: str) -> Fact | None:
        return next((f for f in self.facts if f.id == fact_id), None)

    def bullet(self, bullet_id: str) -> Bullet | None:
        return next((b for b in self.bullets if b.id == bullet_id), None)

    def evidence_for(self, bullet: Bullet) -> list[str]:
        """一条 bullet 的「证据」：它本身 + 它引用的事实。"""
        return [bullet.text] + [f.text for f in self.facts if f.id in bullet.facts]


class Skill(BaseModel):
    name: str
    level: str = "working"
    group: str = "Other"


class Education(BaseModel):
    id: str
    institution: str
    degree: str = ""
    area: str = ""
    location: str = ""
    start: str | int | None = None
    end: str | int | None = None
    gpa: str | float | None = None
    coursework: list[str] = Field(default_factory=list)


class Bank(BaseModel):
    version: int = 1
    summaries: dict[str, str] = Field(default_factory=dict)
    skills: list[Skill] = Field(default_factory=list)
    spoken_languages: list[dict] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    entries: list[Entry] = Field(default_factory=list)

    def entry(self, entry_id: str) -> Entry | None:
        return next((e for e in self.entries if e.id == entry_id), None)

    def find_bullet(self, bullet_id: str) -> tuple[Entry, Bullet] | None:
        for e in self.entries:
            b = e.bullet(bullet_id)
            if b:
                return e, b
        return None

    def all_fact_texts(self) -> list[str]:
        return [f.text for e in self.entries for f in e.facts]

    def skill_level(self, name: str) -> str:
        s = next((s for s in self.skills if s.name.lower() == name.lower()), None)
        return s.level if s else "none"


def load_bank(path: Path | None = None) -> Bank:
    return Bank.model_validate(load_yaml(path or bank_path()))


def validate_bank(bank: Bank, vocabulary_raw: dict[str, list[str]] | None = None) -> list[str]:
    """检查素材库自身：id 唯一、引用存在、bullet 的数字/技术都有事实支撑。"""
    problems: list[str] = []
    vocab = compile_vocabulary(vocabulary_raw or {})
    seen_entry, seen_bullet = set(), set()
    for e in bank.entries:
        if e.id in seen_entry:
            problems.append(f"entry id 重复：{e.id}")
        seen_entry.add(e.id)
        fact_ids = [f.id for f in e.facts]
        if len(fact_ids) != len(set(fact_ids)):
            problems.append(f"{e.id}: fact id 重复")
        for b in e.bullets:
            if b.id in seen_bullet:
                problems.append(f"bullet id 重复：{b.id}")
            seen_bullet.add(b.id)
            for fid in b.facts:
                if fid not in fact_ids:
                    problems.append(f"{b.id}: 引用了不存在的 fact {fid}")
            evidence = [f.text for f in e.facts if f.id in b.facts]
            for p in check_claims(b.text, evidence):
                problems.append(f"{b.id}: {p}")
            if vocab:
                for p in check_skills(b.text, evidence, e.stack, vocab):
                    problems.append(f"{b.id}: {p}")
    return problems
