from datetime import datetime

from minilog.filters import by_min_level, by_source, by_time_range
from minilog.parser import LogRecord


def rec(level="INFO", source="app", ts=None):
    return LogRecord(
        timestamp=ts or datetime(2026, 7, 1, 12, 0, 0),
        level=level,
        source=source,
        message="m",
    )


def test_by_min_level():
    records = [rec("DEBUG"), rec("INFO"), rec("WARNING"), rec("ERROR")]
    assert [r.level for r in by_min_level(records, "WARNING")] == ["WARNING", "ERROR"]


def test_by_min_level_drops_unknown_levels():
    records = [rec("TRACE"), rec("INFO")]
    assert [r.level for r in by_min_level(records, "DEBUG")] == ["INFO"]


def test_by_source_matches_exact_and_children():
    records = [rec(source="api"), rec(source="api.auth"), rec(source="apix")]
    assert [r.source for r in by_source(records, "api")] == ["api", "api.auth"]


def test_by_time_range():
    records = [
        rec(ts=datetime(2026, 7, 1, 12, 0, 0)),
        rec(ts=datetime(2026, 7, 1, 13, 0, 0)),
        rec(ts=datetime(2026, 7, 1, 14, 0, 0)),
    ]
    out = by_time_range(
        records,
        since=datetime(2026, 7, 1, 12, 30, 0),
        until=datetime(2026, 7, 1, 13, 30, 0),
    )
    assert [r.timestamp.hour for r in out] == [13]
