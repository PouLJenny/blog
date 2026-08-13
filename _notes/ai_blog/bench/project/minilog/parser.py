"""Parse text log lines into LogRecord objects.

Expected line format::

    2026-07-01 12:00:03 [ERROR] api.auth: token expired (123ms)

The trailing ``(<n>ms)`` duration suffix is optional.
"""
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

LINE_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"\[(?P<level>[A-Z]+)\] "
    r"(?P<source>[\w.]+): "
    r"(?P<message>.*)$"
)
DURATION_RE = re.compile(r"\s*\((?P<ms>\d+)ms\)$")


class ParseError(ValueError):
    pass


@dataclass
class LogRecord:
    timestamp: datetime
    level: str
    source: str
    message: str
    duration_ms: int | None = None


def parse_line(line: str) -> LogRecord:
    m = LINE_RE.match(line.strip())
    if not m:
        raise ParseError(f"unrecognized log line: {line!r}")
    message = m.group("message")
    duration_ms = None
    dm = DURATION_RE.search(message)
    if dm:
        duration_ms = int(dm.group("ms"))
        message = message[: dm.start()].rstrip()
    return LogRecord(
        timestamp=datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S"),
        level=m.group("level"),
        source=m.group("source"),
        message=message,
        duration_ms=duration_ms,
    )


def parse_lines(lines: Iterable[str], strict: bool = False) -> list[LogRecord]:
    """Parse many lines; blank lines are skipped.

    Unparseable lines raise ParseError when ``strict`` is true, otherwise
    they are silently dropped.
    """
    records = []
    for line in lines:
        if not line.strip():
            continue
        try:
            records.append(parse_line(line))
        except ParseError:
            if strict:
                raise
    return records
