"""Command line interface: ``python -m minilog.cli <logfile> [options]``."""
import argparse
import sys

from . import config, filters, stats
from .formatter import format_records, format_summary
from .parser import parse_lines


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="minilog", description="Analyze log files.")
    p.add_argument("logfile")
    p.add_argument(
        "--min-level",
        default=config.DEFAULT_MIN_LEVEL,
        choices=list(config.LEVEL_ORDER),
        help="hide records below this level (default: %(default)s)",
    )
    p.add_argument("--source", help="only records from this dotted source path")
    p.add_argument(
        "--slow-only",
        action="store_true",
        help="only records slower than the slow threshold",
    )
    p.add_argument(
        "--summary",
        action="store_true",
        help="print aggregate stats instead of records",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    with open(args.logfile, encoding="utf-8") as f:
        records = parse_lines(f)
    records = filters.by_min_level(records, args.min_level)
    if args.source:
        records = filters.by_source(records, args.source)
    if args.slow_only:
        records = stats.slow_records(records)
    if args.summary:
        print(format_summary(records))
    else:
        print(format_records(records))
    return 0


if __name__ == "__main__":
    sys.exit(main())
