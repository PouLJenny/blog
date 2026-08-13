import pytest
from datetime import datetime

from minilog.parser import ParseError, parse_line, parse_lines


def test_parse_basic_line():
    r = parse_line("2026-07-01 12:00:03 [ERROR] api.auth: token expired")
    assert r.timestamp == datetime(2026, 7, 1, 12, 0, 3)
    assert r.level == "ERROR"
    assert r.source == "api.auth"
    assert r.message == "token expired"
    assert r.duration_ms is None


def test_parse_line_with_duration():
    r = parse_line("2026-07-01 12:00:03 [INFO] api.orders: created order (642ms)")
    assert r.duration_ms == 642
    assert r.message == "created order"


def test_parse_bad_line_raises():
    with pytest.raises(ParseError):
        parse_line("not a log line at all")


def test_parse_lines_skips_blank_and_bad_lines():
    lines = [
        "",
        "2026-07-01 12:00:03 [INFO] db.pool: connected",
        "garbage",
        "   ",
    ]
    records = parse_lines(lines)
    assert len(records) == 1
    assert records[0].source == "db.pool"


def test_parse_lines_strict_raises_on_bad_line():
    with pytest.raises(ParseError):
        parse_lines(["garbage"], strict=True)
