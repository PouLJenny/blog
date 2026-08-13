#!/usr/bin/env python3
"""汇总 results/ 下的运行记录成 markdown 表格。

用法: python summarize.py [--prices prices.json]

prices.json 格式(单位:每百万 token 的价格,币种自带):
{
  "claude":   {"currency": "USD", "input": 3.0, "output": 15.0,
               "cache_read": 0.3, "cache_write": 3.75},
  "glm":      {"currency": "CNY", "input": 4.0, "output": 16.0,
               "cache_read": 0.8, "cache_write": 0},
  "deepseek": {"currency": "CNY", "input": 4.0, "output": 12.0,
               "cache_read": 0.8, "cache_write": 0}
}
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
RESULTS = HERE / "results"


def load_meta(path: Path) -> dict:
    meta = {}
    for line in path.read_text().splitlines():
        for kv in line.split():
            if "=" in kv:
                k, v = kv.split("=", 1)
                meta[k] = v
    return meta


def cost(usage: dict, price: dict | None) -> str:
    if not price:
        return "-"
    m = 1_000_000
    total = (
        usage.get("input_tokens", 0) / m * price.get("input", 0)
        + usage.get("output_tokens", 0) / m * price.get("output", 0)
        + usage.get("cache_read_input_tokens", 0) / m * price.get("cache_read", 0)
        + usage.get("cache_creation_input_tokens", 0) / m * price.get("cache_write", 0)
    )
    return f"{total:.4f} {price.get('currency', '')}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices", type=Path, default=HERE / "prices.json")
    args = ap.parse_args()
    prices = json.loads(args.prices.read_text()) if args.prices.exists() else {}

    rows = []
    for meta_path in sorted(RESULTS.glob("*.meta")):
        stem = meta_path.stem
        m = re.match(r"(?P<model>\w+?)_task(?P<task>\d)_", stem)
        if not m:
            continue
        meta = load_meta(meta_path)
        json_path = meta_path.with_suffix(".json")
        data = {}
        if json_path.exists():
            try:
                data = json.loads(json_path.read_text())
            except json.JSONDecodeError:
                pass
        usage = data.get("usage", {})
        if meta["task"] in ("2", "3"):
            ok = "✅" if meta.get("pytest_rc") == "0" else "❌"
        else:
            ok = "人工判分"
        rows.append({
            "model": m.group("model"),
            "task": meta["task"],
            "ok": ok,
            "wall_s": meta.get("wall_seconds", "?"),
            "turns": data.get("num_turns", "?"),
            "in": usage.get("input_tokens", "?"),
            "out": usage.get("output_tokens", "?"),
            "cache_r": usage.get("cache_read_input_tokens", 0),
            "cache_w": usage.get("cache_creation_input_tokens", 0),
            "cost": cost(usage, prices.get(m.group("model"))),
            "cli_cost": data.get("total_cost_usd", "?"),
            "file": stem,
        })

    hdr = ("| 模型 | 任务 | 结果 | 耗时(s) | 轮数 | 输入tok | 输出tok "
           "| cache读 | cache写 | 牌价成本 |")
    print(hdr)
    print("|" + "---|" * 10)
    for r in sorted(rows, key=lambda r: (r["task"], r["model"])):
        print(
            f"| {r['model']} | {r['task']} | {r['ok']} | {r['wall_s']} "
            f"| {r['turns']} | {r['in']} | {r['out']} "
            f"| {r['cache_r']} | {r['cache_w']} | {r['cost']} |"
        )
    print()
    for r in rows:
        print(f"  {r['file']}: cli_cost_usd={r['cli_cost']}")


if __name__ == "__main__":
    main()
