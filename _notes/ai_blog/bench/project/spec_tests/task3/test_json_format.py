"""Acceptance tests for Task 3: JSON Lines log format support.

Spec:
- Each JSON line looks like:
  {"time": "2026-07-01 12:00:03", "level": "ERROR", "source": "api.auth",
   "message": "token expired", "duration_ms": 123}
  ``duration_ms`` is optional (missing -> None).
- ``minilog.parser.parse_json_line(line)`` parses one such line.
- ``minilog.parser.parse_lines(lines, fmt=...)`` accepts fmt in
  {"auto", "text", "json"}; "auto" means: JSON if the first non-blank
  line starts with "{", text otherwise. Default comes from
  ``minilog.config.DEFAULT_FORMAT``.
- The CLI gains ``--format {auto,text,json}`` defaulting to
  ``config.DEFAULT_FORMAT``.
"""
from datetime import datetime

from minilog import config
from minilog.cli import main
from minilog.parser import parse_json_line, parse_lines

JSON_LOG = """\
{"time": "2026-07-01 12:00:02", "level": "INFO", "source": "api.orders", "message": "created order", "duration_ms": 642}
{"time": "2026-07-01 12:00:03", "level": "ERROR", "source": "api.auth", "message": "token expired"}
"""

TEXT_LOG = "2026-07-01 12:00:04 [INFO] db.pool: query ok (30ms)\n"


def test_default_format_config():
    assert config.DEFAULT_FORMAT == "auto"


def test_parse_json_line_full():
    r = parse_json_line(
        '{"time": "2026-07-01 12:00:03", "level": "ERROR",'
        ' "source": "api.auth", "message": "token expired", "duration_ms": 123}'
    )
    assert r.timestamp == datetime(2026, 7, 1, 12, 0, 3)
    assert r.level == "ERROR"
    assert r.source == "api.auth"
    assert r.message == "token expired"
    assert r.duration_ms == 123


def test_parse_json_line_duration_optional():
    r = parse_json_line(
        '{"time": "2026-07-01 12:00:03", "level": "INFO",'
        ' "source": "app", "message": "hi"}'
    )
    assert r.duration_ms is None


def test_parse_lines_auto_detects_json():
    records = parse_lines(JSON_LOG.splitlines())
    assert [r.source for r in records] == ["api.orders", "api.auth"]


def test_parse_lines_auto_still_parses_text():
    records = parse_lines(TEXT_LOG.splitlines())
    assert [r.source for r in records] == ["db.pool"]


def test_parse_lines_explicit_json():
    records = parse_lines(JSON_LOG.splitlines(), fmt="json")
    assert len(records) == 2


def test_cli_format_flag_and_auto(tmp_path, capsys):
    f = tmp_path / "app.jsonl"
    f.write_text(JSON_LOG, encoding="utf-8")

    main([str(f), "--format", "json", "--summary"])
    assert "total=2" in capsys.readouterr().out

    main([str(f), "--summary"])  # auto detection
    assert "total=2" in capsys.readouterr().out
