"""Render LogRecord lists as text."""
from . import config, stats
from .parser import LogRecord


def format_records(records: list[LogRecord]) -> str:
    """One line per record; slow records get a ``*`` marker."""
    lines = []
    for r in records:
        is_slow = r.duration_ms is not None and r.duration_ms > config.SLOW_THRESHOLD_MS
        mark = "*" if is_slow else " "
        dur = f" ({r.duration_ms}ms)" if r.duration_ms is not None else ""
        lines.append(
            f"{mark} {r.timestamp:%Y-%m-%d %H:%M:%S} "
            f"[{r.level:<8}] {r.source}: {r.message}{dur}"
        )
    return "\n".join(lines)


def format_summary(records: list[LogRecord]) -> str:
    counts = stats.count_by_level(records)
    parts = [f"total={len(records)}"]
    for level in sorted(counts, key=lambda l: -config.LEVEL_ORDER.get(l, -1)):
        parts.append(f"{level.lower()}={counts[level]}")
    parts.append(f"error_rate={stats.error_rate(records):.1%}")
    parts.append(f"slow={len(stats.slow_records(records))}")
    return " ".join(parts)
