# CLuade code


## agent sdk


## 让你的claude使用chatgpt


1. 下载 [CLIProxyAPI](https://help.router-for.me/cn/agent-client/claude-code.html)
2. 生成最小配置文件 `config.yaml`
```yaml
# CLIProxyAPI minimal config
port: 8317

# OAuth/凭证存放目录
auth-dir: "~/.cli-proxy-api"

# Claude Code 连接代理时使用的访问 key（自己定义）
api-keys:
  - "sk-my-local-key"

debug: false
```
3. `./cli-proxy-api --config config.yaml -codex-login`
4. `./cli-proxy-api --config config.yaml` 启动服务
4. 执行命令，就可以愉快的使用了
```shell
ANTHROPIC_BASE_URL=http://127.0.0.1:8317 \
ANTHROPIC_AUTH_TOKEN=sk-my-local-key \
ANTHROPIC_DEFAULT_OPUS_MODEL=gpt-5.6-sol \
ANTHROPIC_DEFAULT_SONNET_MODEL=gpt-5.6-sol \
ANTHROPIC_DEFAULT_HAIKU_MODEL=gpt-5.6-sol \
CLAUDE_CODE_ALWAYS_ENABLE_EFFORT=1 \
CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY=3 \
ENABLE_TOOL_SEARCH=false \
claude
```




# EOF