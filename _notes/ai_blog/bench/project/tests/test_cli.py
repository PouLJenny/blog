from minilog.cli import main

LOG = """\
2026-07-01 12:00:01 [DEBUG] db.pool: acquiring connection
2026-07-01 12:00:02 [INFO] api.orders: created order (642ms)
2026-07-01 12:00:03 [ERROR] api.auth: token expired (120ms)
2026-07-01 12:00:04 [INFO] db.pool: query ok (30ms)
"""


def write_log(tmp_path):
    f = tmp_path / "app.log"
    f.write_text(LOG, encoding="utf-8")
    return str(f)


def test_default_hides_debug(tmp_path, capsys):
    main([write_log(tmp_path)])
    out = capsys.readouterr().out
    assert "acquiring connection" not in out
    assert "created order" in out


def test_slow_only(tmp_path, capsys):
    main([write_log(tmp_path), "--slow-only"])
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1
    assert "created order" in out[0]
    assert out[0].startswith("*")


def test_summary(tmp_path, capsys):
    main([write_log(tmp_path), "--summary"])
    out = capsys.readouterr().out
    assert "total=3" in out
    assert "error_rate=33.3%" in out
    assert "slow=1" in out


def test_source_filter(tmp_path, capsys):
    main([write_log(tmp_path), "--source", "api"])
    out = capsys.readouterr().out
    assert "created order" in out
    assert "token expired" in out
    assert "query ok" not in out
