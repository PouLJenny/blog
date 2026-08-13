from datetime import datetime

from minilog.parser import LogRecord
from minilog.stats import count_by_level, error_rate, slow_records


def rec(level="INFO", duration_ms=None):
    return LogRecord(
        timestamp=datetime(2026, 7, 1, 12, 0, 0),
        level=level,
        source="app",
        message="m",
        duration_ms=duration_ms,
    )


def test_count_by_level():
    records = [rec("INFO"), rec("INFO"), rec("ERROR")]
    assert count_by_level(records) == {"INFO": 2, "ERROR": 1}


def test_error_rate_empty_is_zero():
    assert error_rate([]) == 0.0


def test_error_rate_counts_error_and_above():
    records = [rec("INFO"), rec("ERROR"), rec("CRITICAL"), rec("WARNING")]
    assert error_rate(records) == 0.5


def test_slow_records_threshold_is_strict():
    records = [rec(duration_ms=499), rec(duration_ms=500), rec(duration_ms=501)]
    assert [r.duration_ms for r in slow_records(records)] == [501]


def test_slow_records_custom_threshold_and_missing_duration():
    records = [rec(duration_ms=None), rec(duration_ms=100), rec(duration_ms=200)]
    assert [r.duration_ms for r in slow_records(records, threshold_ms=150)] == [200]
