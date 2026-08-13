"""Aggregate statistics over lists of LogRecord."""
from collections import Counter

from . import config
from .parser import LogRecord


def count_by_level(records: list[LogRecord]) -> dict[str, int]:
    return dict(Counter(r.level for r in records))


def error_rate(records: list[LogRecord]) -> float:
    """Fraction of records at ERROR level or above; 0.0 for empty input."""
    if not records:
        return 0.0
    error_threshold = config.LEVEL_ORDER["ERROR"]
    errors = [
        r for r in records if config.LEVEL_ORDER.get(r.level, -1) >= error_threshold
    ]
    return len(errors) / len(records)


def slow_records(
    records: list[LogRecord], threshold_ms: int = config.SLOW_THRESHOLD_MS
) -> list[LogRecord]:
    """Records with a duration strictly greater than ``threshold_ms``."""
    return [
        r for r in records if r.duration_ms is not None and r.duration_ms > threshold_ms
    ]


def top_sources(records: list[LogRecord], n: int = 3) -> list[tuple[str, int]]:
    """Return the ``n`` most frequent sources as ``(source, count)`` tuples.

    Sorted by count descending; ties broken by source name ascending.
    Fewer than ``n`` distinct sources returns them all; empty input
    returns an empty list.
    """
    raise NotImplementedError("top_sources is not implemented yet")
