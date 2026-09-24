"""SQLite 本地追踪库：职位、打分、投递状态。库文件在 data/jobs.db（不进 git）。"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .config import DATA_DIR
from .models import Job, ScoreResult

STATUSES = ["new", "shortlisted", "tailored", "prefilled", "applied", "oa", "interview", "offer", "rejected", "skipped"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    uid TEXT PRIMARY KEY,
    company_key TEXT NOT NULL,
    company TEXT NOT NULL,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT,
    apply_url TEXT,
    locations TEXT,
    description TEXT,
    department TEXT,
    posted_at TEXT,
    remote INTEGER,
    salary TEXT,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS scores (
    uid TEXT PRIMARY KEY REFERENCES jobs(uid),
    score REAL NOT NULL,
    archetype TEXT,
    excluded INTEGER NOT NULL,
    detail TEXT NOT NULL,
    scored_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS applications (
    uid TEXT PRIMARY KEY REFERENCES jobs(uid),
    status TEXT NOT NULL,
    resume_path TEXT,
    notes TEXT,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fetch_log (
    company_key TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    ok INTEGER NOT NULL,
    n_jobs INTEGER,
    error TEXT
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, path: Path | None = None):
        self.path = path or DATA_DIR / "jobs.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    # ---------------------------------------------------------------- jobs
    def upsert_jobs(self, company_key: str, jobs: list[Job]) -> tuple[int, int]:
        """写入一次抓取结果。返回 (新增数, 下架数)。这次没出现的旧职位标记为 inactive。"""
        now = _now()
        new = 0
        seen = set()
        with self.conn:
            for j in jobs:
                seen.add(j.uid)
                exists = self.conn.execute("SELECT 1 FROM jobs WHERE uid=?", (j.uid,)).fetchone()
                if not exists:
                    new += 1
                self.conn.execute(
                    """INSERT INTO jobs (uid, company_key, company, source, source_id, title, url, apply_url,
                           locations, description, department, posted_at, remote, salary, first_seen, last_seen, active)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
                       ON CONFLICT(uid) DO UPDATE SET title=excluded.title, url=excluded.url,
                           apply_url=excluded.apply_url, locations=excluded.locations,
                           description=CASE WHEN excluded.description != '' THEN excluded.description ELSE jobs.description END,
                           department=excluded.department, posted_at=excluded.posted_at, remote=excluded.remote,
                           salary=excluded.salary, last_seen=excluded.last_seen, active=1""",
                    (
                        j.uid, j.company_key, j.company, j.source, j.source_id, j.title, j.url, j.apply_url,
                        json.dumps(j.locations, ensure_ascii=False), j.description, j.department, j.posted_at,
                        None if j.remote is None else int(j.remote), j.salary, now, now,
                    ),
                )
            gone = 0
            for row in self.conn.execute("SELECT uid FROM jobs WHERE company_key=? AND active=1", (company_key,)).fetchall():
                if row["uid"] not in seen:
                    self.conn.execute("UPDATE jobs SET active=0 WHERE uid=?", (row["uid"],))
                    gone += 1
        return new, gone

    def log_fetch(self, company_key: str, ok: bool, n_jobs: int | None = None, error: str | None = None) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO fetch_log (company_key, fetched_at, ok, n_jobs, error) VALUES (?,?,?,?,?)",
                (company_key, _now(), int(ok), n_jobs, error),
            )

    @staticmethod
    def row_to_job(row: sqlite3.Row) -> Job:
        return Job(
            company_key=row["company_key"], company=row["company"], source=row["source"], source_id=row["source_id"],
            title=row["title"], url=row["url"] or "", apply_url=row["apply_url"],
            locations=json.loads(row["locations"] or "[]"), description=row["description"] or "",
            department=row["department"], posted_at=row["posted_at"],
            remote=None if row["remote"] is None else bool(row["remote"]), salary=row["salary"],
        )

    def active_jobs(self) -> list[Job]:
        return [self.row_to_job(r) for r in self.conn.execute("SELECT * FROM jobs WHERE active=1")]

    def get_job(self, uid: str) -> Job | None:
        row = self.conn.execute("SELECT * FROM jobs WHERE uid=?", (uid,)).fetchone()
        return self.row_to_job(row) if row else None

    def find_uid(self, prefix: str) -> str | None:
        """支持用 uid 前缀 / 末尾 id 查职位，命令行里少打字。"""
        rows = self.conn.execute(
            "SELECT uid FROM jobs WHERE uid=? OR uid LIKE ? OR uid LIKE ?", (prefix, prefix + "%", "%:" + prefix)
        ).fetchall()
        return rows[0]["uid"] if len(rows) == 1 else None

    # -------------------------------------------------------------- scores
    def save_score(self, uid: str, result: ScoreResult) -> None:
        with self.conn:
            self.conn.execute(
                """INSERT INTO scores (uid, score, archetype, excluded, detail, scored_at) VALUES (?,?,?,?,?,?)
                   ON CONFLICT(uid) DO UPDATE SET score=excluded.score, archetype=excluded.archetype,
                   excluded=excluded.excluded, detail=excluded.detail, scored_at=excluded.scored_at""",
                (uid, result.score, result.archetype, int(result.excluded),
                 json.dumps(asdict(result), ensure_ascii=False), _now()),
            )

    def get_score(self, uid: str) -> dict | None:
        row = self.conn.execute("SELECT detail FROM scores WHERE uid=?", (uid,)).fetchone()
        return json.loads(row["detail"]) if row else None

    def ranked(self, min_score: float = 0, include_excluded: bool = False, status: str | None = None,
               only_new: bool = False) -> list[sqlite3.Row]:
        sql = """SELECT j.*, s.score, s.archetype, s.excluded, s.detail, COALESCE(a.status, 'new') AS status
                 FROM jobs j JOIN scores s ON s.uid = j.uid LEFT JOIN applications a ON a.uid = j.uid
                 WHERE j.active = 1 AND s.score >= ?"""
        args: list = [min_score]
        if not include_excluded:
            sql += " AND s.excluded = 0"
        if status:
            sql += " AND COALESCE(a.status, 'new') = ?"
            args.append(status)
        if only_new:
            sql += " AND COALESCE(a.status, 'new') = 'new'"
        sql += " ORDER BY s.score DESC, j.first_seen DESC"
        return self.conn.execute(sql, args).fetchall()

    # -------------------------------------------------------- applications
    def set_status(self, uid: str, status: str, notes: str | None = None, resume_path: str | None = None) -> None:
        if status not in STATUSES:
            raise ValueError(f"状态必须是 {STATUSES} 之一")
        with self.conn:
            self.conn.execute(
                """INSERT INTO applications (uid, status, resume_path, notes, updated_at) VALUES (?,?,?,?,?)
                   ON CONFLICT(uid) DO UPDATE SET status=excluded.status,
                   resume_path=COALESCE(excluded.resume_path, applications.resume_path),
                   notes=CASE WHEN excluded.notes IS NULL THEN applications.notes
                              WHEN applications.notes IS NULL THEN excluded.notes
                              ELSE applications.notes || char(10) || excluded.notes END,
                   updated_at=excluded.updated_at""",
                (uid, status, resume_path, notes, _now()),
            )

    def status_counts(self) -> dict[str, int]:
        rows = self.conn.execute("SELECT status, COUNT(*) AS n FROM applications GROUP BY status").fetchall()
        return {r["status"]: r["n"] for r in rows}
