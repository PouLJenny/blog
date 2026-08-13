#!/usr/bin/env bash
# 全量:3 模型 x 3 任务 = 9 次,串行跑(避免限流互相干扰计时)
set -uo pipefail
BENCH="$(cd "$(dirname "$0")" && pwd)"
for model in claude glm deepseek; do
  for task in 1 2 3; do
    bash "$BENCH/run.sh" "$model" "$task"
  done
done
echo "ALL DONE"
