"""Filters over lists of LogRecord."""
from datetime import datetime

from . import config
from .parser import LogRecord


def by_min_level(records: list[LogRecord], min_level: str) -> list[LogRecord]:
    """Keep records at ``min_level`` or above; unknown levels are dropped."""
    threshold = config.LEVEL_ORDER[min_level]
    return [r for r in records if config.LEVEL_ORDER.get(r.level, -1) >= threshold]


def by_source(records: list[LogRecord], source: str) -> list[LogRecord]:
    """Keep records whose source equals ``source`` or lives under it.

    ``by_source(rs, "api")`` matches ``api`` and ``api.auth``
    but not ``apix``.
    """
    return [
        r
        for r in records
        if r.source == source or r.source.startswith(source + ".")
    ]


def by_time_range(
    records: list[LogRecord],
    since: datetime | None = None,
    until: datetime | None = None,
) -> list[LogRecord]:
    out = []
    for r in records:
        if since is not None and r.timestamp < since:
            continue
        if until is not None and r.timestamp > until:
            continue
        out.append(r)
    return out
