import pytest

from conftest import make_job
from jobhunt.store import Store


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "jobs.db")
    yield s
    s.close()


def test_upsert_tracks_new_and_gone(store):
    a, b = make_job("Quant Developer"), make_job("Data Engineer")
    assert store.upsert_jobs("pimco", [a, b]) == (2, 0)
    assert store.upsert_jobs("pimco", [a]) == (0, 1)
    assert [j.title for j in store.active_jobs()] == ["Quant Developer"]
    assert store.upsert_jobs("pimco", [a, b]) == (0, 0)   # 重新上架不算新增
    assert len(store.active_jobs()) == 2


def test_scores_ranking_and_status(store, scorer):
    good = make_job("Quantitative Developer", "backtesting signal research in Python pandas")
    bad = make_job("Senior Staff Engineer", "Java")
    store.upsert_jobs("pimco", [good, bad])
    for j in (good, bad):
        store.save_score(j.uid, scorer.score(j))
    rows = store.ranked()
    assert [r["title"] for r in rows] == ["Quantitative Developer"]
    assert len(store.ranked(include_excluded=True)) == 2

    store.set_status(good.uid, "applied", notes="投了")
    store.set_status(good.uid, "interview", notes="一面")
    assert store.ranked(status="interview")[0]["uid"] == good.uid
    assert store.status_counts() == {"interview": 1}
    note = store.conn.execute("SELECT notes FROM applications").fetchone()["notes"]
    assert note == "投了\n一面"
    with pytest.raises(ValueError):
        store.set_status(good.uid, "ghosted")


def test_find_uid(store):
    job = make_job("Quant Developer")
    store.upsert_jobs("pimco", [job])
    assert store.find_uid(job.uid) == job.uid
    assert store.find_uid(job.source_id) == job.uid
    assert store.find_uid("nothing") is None
