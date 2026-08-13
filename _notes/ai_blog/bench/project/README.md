# minilog

A tiny log analysis library. Parses text logs, filters them, and prints
records or aggregate stats.

```
python -m minilog.cli sample_logs/app.log --summary
```

Layout:

- `minilog/parser.py` — parse raw lines into `LogRecord`
- `minilog/filters.py` — level / source / time-range filters
- `minilog/stats.py` — aggregate statistics
- `minilog/formatter.py` — text rendering
- `minilog/config.py` — project-wide defaults
- `minilog/cli.py` — command line entry point
- `tests/` — unit tests (`python -m pytest`)
- `spec_tests/` — acceptance tests for pending work, run explicitly,
  e.g. `python -m pytest spec_tests/task2 tests`
