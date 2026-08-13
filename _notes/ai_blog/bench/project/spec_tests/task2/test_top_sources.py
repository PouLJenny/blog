"""Acceptance tests for Task 2: implement minilog.stats.top_sources."""
from datetime import datetime

from minilog.parser import LogRecord
from minilog.stats import top_sources


def rec(source):
    return LogRecord(
        timestamp=datetime(2026, 7, 1, 12, 0, 0),
        level="INFO",
        source=source,
        message="m",
    )


def make(counts):
    records = []
    for source, count in counts.items():
        records.extend(rec(source) for _ in range(count))
    return records


def test_orders_by_count_descending():
    records = make({"api.auth": 1, "db.pool": 3, "api.orders": 2})
    assert top_sources(records) == [
        ("db.pool", 3),
        ("api.orders", 2),
        ("api.auth", 1),
    ]


def test_ties_broken_by_source_name_ascending():
    records = make({"zeta": 2, "alpha": 2, "mid": 1})
    assert top_sources(records) == [("alpha", 2), ("zeta", 2), ("mid", 1)]


def test_n_limits_result_length():
    records = make({"a": 5, "b": 4, "c": 3, "d": 2})
    assert top_sources(records, n=2) == [("a", 5), ("b", 4)]


def test_n_larger_than_distinct_sources_returns_all():
    records = make({"a": 1, "b": 1})
    assert top_sources(records, n=10) == [("a", 1), ("b", 1)]


def test_empty_input():
    assert top_sources([]) == []
