#!/usr/bin/env bash
# 单次运行:./run.sh <claude|glm|deepseek> <1|2|3>
# 结果落在 results/<model>_task<N>_<时间戳>.{json,stderr,meta,diff,pytest}
set -uo pipefail

BENCH="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$BENCH/project"
RESULTS="$BENCH/results"
source "$BENCH/keys.env"

MODEL="${1:?usage: run.sh <claude|glm|deepseek> <1|2|3>}"
TASK="${2:?usage: run.sh <claude|glm|deepseek> <1|2|3>}"
mkdir -p "$RESULTS"
OUT="$RESULTS/${MODEL}_task${TASK}_$(date +%Y%m%d_%H%M%S)"

# 恢复干净现场
git -C "$PROJECT" reset --hard -q
git -C "$PROJECT" clean -fdq

PROMPT="$(cat "$BENCH/tasks/task${TASK}.prompt.txt")"

# 隔离环境:清空所有可能干扰的变量,用独立 CLAUDE_CONFIG_DIR
# 避开本机 hooks/全局 CLAUDE.md,保证三个模型条件一致
ENVV=(env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL
      -u ANTHROPIC_MODEL -u ANTHROPIC_SMALL_FAST_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL
      -u https_proxy -u http_proxy -u HTTPS_PROXY -u HTTP_PROXY -u all_proxy -u ALL_PROXY
      CLAUDE_CONFIG_DIR="$BENCH/claude-home"
      PATH="$BENCH/venv/bin:$PATH")

case "$MODEL" in
  claude)
    ENVV+=(ANTHROPIC_API_KEY="$ANTHROPIC_KEY_OFFICIAL")
    if [ -n "${CLAUDE_PROXY:-}" ]; then
      ENVV+=(https_proxy="$CLAUDE_PROXY" http_proxy="$CLAUDE_PROXY")
    fi
    ;;
  glm)
    ENVV+=(ANTHROPIC_BASE_URL="$GLM_BASE_URL" ANTHROPIC_AUTH_TOKEN="$GLM_KEY")
    [ -n "${GLM_MODEL:-}" ] && ENVV+=(ANTHROPIC_MODEL="$GLM_MODEL")
    ;;
  deepseek)
    ENVV+=(ANTHROPIC_BASE_URL="$DS_BASE_URL" ANTHROPIC_AUTH_TOKEN="$DS_KEY")
    [ -n "${DS_MODEL:-}" ] && ENVV+=(ANTHROPIC_MODEL="$DS_MODEL")
    ;;
  *) echo "unknown model: $MODEL" >&2; exit 2 ;;
esac

echo ">>> [$MODEL][task$TASK] start $(date +%H:%M:%S)"
START=$(date +%s)
(
  cd "$PROJECT" &&
  timeout 1200 "${ENVV[@]}" claude -p "$PROMPT" \
    --output-format json --dangerously-skip-permissions \
    > "$OUT.json" 2> "$OUT.stderr"
)
RC=$?
WALL=$(( $(date +%s) - START ))
{
  echo "model=$MODEL task=$TASK"
  echo "exit_code=$RC"
  echo "wall_seconds=$WALL"
} > "$OUT.meta"

# 客观判分:task2/3 跑对应验收测试;task1 留待人工比对 answer key
case "$TASK" in
  2|3)
    ( cd "$PROJECT" &&
      "$BENCH/venv/bin/python" -m pytest "spec_tests/task${TASK}" tests -q \
        > "$OUT.pytest" 2>&1 )
    echo "pytest_rc=$?" >> "$OUT.meta"
    ;;
esac

# 留存改动供分析,然后恢复现场
git -C "$PROJECT" diff > "$OUT.diff"
git -C "$PROJECT" status --porcelain > "$OUT.gitstatus"
git -C "$PROJECT" reset --hard -q
git -C "$PROJECT" clean -fdq

echo ">>> [$MODEL][task$TASK] done: exit=$RC wall=${WALL}s -> $(basename "$OUT")"
