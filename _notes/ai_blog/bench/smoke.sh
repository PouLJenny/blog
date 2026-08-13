#!/usr/bin/env bash
# 冒烟测试:每个端点各发一个最小请求,验证连通性和鉴权
set -uo pipefail
BENCH="$(cd "$(dirname "$0")" && pwd)"
source "$BENCH/keys.env"

smoke() {
  local model="$1"; shift
  echo "=== $model ==="
  timeout 120 env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL \
    -u ANTHROPIC_MODEL -u https_proxy -u http_proxy -u HTTPS_PROXY -u HTTP_PROXY \
    CLAUDE_CONFIG_DIR="$BENCH/claude-home" "$@" \
    claude -p '只回答一个词:你的模型名或家族名是什么?' --output-format json 2>&1 |
    tail -5
  echo
}

smoke claude ANTHROPIC_API_KEY="$ANTHROPIC_KEY_OFFICIAL" \
  ${CLAUDE_PROXY:+https_proxy="$CLAUDE_PROXY" http_proxy="$CLAUDE_PROXY"}
smoke glm ANTHROPIC_BASE_URL="$GLM_BASE_URL" ANTHROPIC_AUTH_TOKEN="$GLM_KEY" \
  ${GLM_MODEL:+ANTHROPIC_MODEL="$GLM_MODEL"}
smoke deepseek ANTHROPIC_BASE_URL="$DS_BASE_URL" ANTHROPIC_AUTH_TOKEN="$DS_KEY" \
  ${DS_MODEL:+ANTHROPIC_MODEL="$DS_MODEL"}
