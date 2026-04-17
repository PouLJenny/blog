# Claude Managed Agents 完整参考手册

> 基于 2026 年 4 月最新公开文档整理。Managed Agents 于 2026-04-08 进入公开 Beta。
> Beta Header: `anthropic-beta: managed-agents-2026-04-01`

---

## 一、概览：四个核心概念

| 概念 | 说明 | 生命周期 |
|------|------|---------|
| **Agent** | 可复用的配置（model + system prompt + tools + MCP），带版本号 | 创建一次，跨 session 复用 |
| **Environment** | 云容器配置（预装包 + 网络策略 + 挂载文件） | 创建一次，跨 session 复用 |
| **Session** | Agent 在 Environment 中的一次运行实例 | 按任务创建，完成后归档 |
| **Events** | 双向消息流（用户 ↔ Agent） | Session 内实时流转 |

**架构分离（Brain / Hands / Session）**：
- **Brain**（LLM + Agent Harness）：无状态，可重启
- **Hands**（沙箱容器）：工具执行环境，独立故障隔离
- **Session**（事件日志）：append-only，服务端持久化，断线可续

---

## 二、完整 API 端点

### 2.1 Agent 管理

```
POST   /v1/agents                    # 创建 Agent
GET    /v1/agents                    # 列出所有 Agent
GET    /v1/agents/{agent_id}         # 获取 Agent 详情
```

**创建 Agent 示例**：
```python
agent = client.beta.agents.create(
    name="关键词调研助手",
    model="claude-sonnet-4-6",
    system="你是跨境电商 AI 助手...",
    tools=[
        {
            "type": "agent_toolset_20260401",
            "default_config": {"enabled": False},
            "configs": [
                {"name": "bash", "enabled": True},
                {"name": "read", "enabled": True},
                {"name": "edit", "enabled": True},
                {"name": "write", "enabled": True},
                {"name": "glob", "enabled": True},
            ]
        },
        {
            "type": "custom",
            "name": "filter_keywords",
            "description": "按条件筛选关键词数据...",
            "input_schema": { ... }
        }
    ],
)
```

### 2.2 Environment 管理

```
POST   /v1/environments                          # 创建 Environment
GET    /v1/environments                          # 列出
GET    /v1/environments/{env_id}                 # 获取详情
POST   /v1/environments/{env_id}/archive         # 归档
DELETE /v1/environments/{env_id}                 # 删除
```

**创建 Environment 示例**：
```python
environment = client.beta.environments.create(
    name="keyword-research-env",
    config={
        "type": "cloud",
        "packages": {
            "pip": ["pandas>=2.0", "numpy>=1.24", "openpyxl>=3.1"],
        },
        "networking": {
            "type": "limited",
            "allowed_hosts": ["new.sif.com"],
            "allow_mcp_servers": False,
            "allow_package_managers": True,
        },
    },
)
```

**网络策略**：
| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `unrestricted` | 除安全黑名单外全部放行 | 开发环境 |
| `limited` | 仅 `allowed_hosts` 白名单 | 生产环境（推荐） |

**预装包**：支持 apt / pip / npm / gem / cargo / go，按字母序安装，可锁定版本。

### 2.3 Session 管理

```
POST   /v1/sessions                              # 创建 Session
GET    /v1/sessions/{session_id}                 # 获取详情
POST   /v1/sessions/{session_id}/archive         # 归档
DELETE /v1/sessions/{session_id}                 # 删除
```

**创建 Session 示例**：
```python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="B07xxx 关键词调研",
    resources=[
        {
            "type": "file",
            "file_id": "file_abc123",
            "mount_path": "/workspace/report.html"
        }
    ],
)
```

### 2.4 事件收发（核心交互）

```
POST   /v1/sessions/{session_id}/events          # 发送事件给 Agent
GET    /v1/sessions/{session_id}/stream           # SSE 流接收 Agent 事件
```

**发送用户消息**：
```python
client.beta.sessions.events.send(
    session.id,
    events=[{
        "type": "user.message",
        "content": [{"type": "text", "text": "请筛选转化率>3%的关键词"}]
    }]
)
```

**发送自定义工具结果**：
```python
client.beta.sessions.events.send(
    session.id,
    events=[{
        "type": "user.custom_tool_result",
        "custom_tool_use_id": event.id,
        "content": [{"type": "text", "text": json.dumps(result)}],
        "is_error": False
    }]
)
```

**流式接收事件**：
```python
with client.beta.sessions.events.stream(session.id) as stream:
    for event in stream:
        match event.type:
            case "agent.message":       ...  # 文本输出
            case "agent.tool_use":      ...  # 内置工具调用
            case "agent.custom_tool_use": ... # 自定义工具调用
            case "session.status_idle":  ...  # Agent 空闲
```

### 2.5 Files API

```
POST   /v1/files                                 # 上传文件（multipart, purpose="agent"）
GET    /v1/files?session_id={id}                 # 列出 Session 输出文件
GET    /v1/files/{file_id}/content               # 下载文件内容
```

**文件行为**：
- 上传文件挂载为**只读**
- Agent 写入 `/mnt/session/outputs/` 的文件自动可下载
- 每 Session 最多 100 个文件

---

## 三、事件类型完整清单

### 3.1 用户 → Agent 事件

| 事件类型 | 用途 | 关键字段 |
|---------|------|---------|
| `user.message` | 发送文本消息 | `content: [{type:"text", text:"..."}]` |
| `user.custom_tool_result` | 返回自定义工具结果 | `custom_tool_use_id`, `content`, `is_error` |
| `user.tool_confirmation` | 批准/拒绝工具调用 | 当权限策略要求确认时 |
| `user.interrupt` | 中断 Agent 执行 | — |
| `user.define_outcome` | 定义目标 | 可选的目标描述 |

### 3.2 Agent → 用户事件

| 事件类型 | 用途 | 关键字段 |
|---------|------|---------|
| `agent.message` | Agent 文本回复 | `content: [{type:"text", text:"..."}]` |
| `agent.thinking` | Agent 思考内容（extended thinking） | `content` |
| `agent.tool_use` | 调用内置工具 | `id`, `name`, `input` |
| `agent.tool_result` | 内置工具执行结果 | `tool_use_id`, 结果内容 |
| `agent.custom_tool_use` | 调用自定义工具 | `id`, `name`, `input` → 需回 `user.custom_tool_result` |
| `agent.mcp_tool_use` | 调用 MCP 工具 | `name`, `input` |
| `agent.mcp_tool_result` | MCP 工具结果 | 结果内容 |

### 3.3 Session 状态事件

| 事件类型 | 用途 | 说明 |
|---------|------|------|
| `session.status_idle` | Agent 完成，等待输入 | `stop_reason.type`: `end_turn` / `requires_action` |
| `session.status_busy` | Agent 正在工作 | 计费中 |
| `session.created` | Session 初始化完成 | — |
| `session.error` | 执行错误 | `error` 字段包含详情 |
| `span.start` / `span.end` | 工具执行或推理跨度 | 可用于性能追踪 |
| `span.model_request_end` | LLM 调用完成 | `model_usage`: input/output/cache_read/cache_create tokens |

### 3.4 stop_reason 详解

| stop_reason | 含义 | 后续操作 |
|-------------|------|---------|
| `end_turn` | Agent 一轮结束，等待用户下一条消息 | 可发新 `user.message` |
| `requires_action` | Agent 等待自定义工具结果 | 必须发 `user.custom_tool_result` |

---

## 四、内置工具详解

### 4.1 工具集 `agent_toolset_20260401`

| 工具 | 功能 | 说明 |
|------|------|------|
| `bash` | 执行 shell 命令 | 完整 Linux 环境 |
| `read` | 读取文件 | 支持文本和二进制 |
| `write` | 创建/覆盖文件 | 写入沙箱文件系统 |
| `edit` | 文本替换编辑 | 精确字符串匹配替换 |
| `glob` | 文件模式匹配 | 如 `**/*.py` |
| `grep` | 正则搜索文件内容 | ripgrep 语法 |
| `web_fetch` | 获取 URL 内容 | 可禁用（安全考虑） |
| `web_search` | 网页搜索 | $10/1000 次，可禁用 |

### 4.2 配置策略

**全部启用**（默认）：
```python
{"type": "agent_toolset_20260401"}
```

**仅启用指定工具**：
```python
{
    "type": "agent_toolset_20260401",
    "default_config": {"enabled": False},
    "configs": [
        {"name": "bash", "enabled": True},
        {"name": "read", "enabled": True},
        {"name": "edit", "enabled": True},
        {"name": "write", "enabled": True},
        {"name": "glob", "enabled": True},
    ]
}
```

### 4.3 自定义工具定义

```python
{
    "type": "custom",
    "name": "filter_keywords",
    "description": "按条件筛选关键词数据。当用户要求筛选、过滤关键词时使用。"
                   "支持的操作符：>=, <=, >, <, ==, !=, contains, not_contains。"
                   "返回筛选后的关键词数量和预览。",
    "input_schema": {
        "type": "object",
        "properties": {
            "intent": {"type": "string", "description": "筛选目的"},
            "column": {"type": "string", "description": "字段名"},
            "operator": {"type": "string", "enum": [">=","<=",">","<","==","!=","contains","not_contains"]},
            "value": {"description": "筛选值"},
            "keep": {"type": "boolean", "default": True}
        },
        "required": ["intent", "column", "operator", "value"]
    }
}
```

**自定义工具交互协议**：
```
1. Agent 决定调用 → agent.custom_tool_use {id, name, input}
2. Session → session.status_idle + stop_reason: requires_action
3. 你的应用执行工具逻辑
4. 发送 user.custom_tool_result {custom_tool_use_id, content, is_error}
5. Agent 恢复推理，stream 继续
```

**最佳实践**：
- 描述写 3-4 句话，说明何时使用、输入输出格式
- 合并相关操作为一个工具 + `action` 参数
- 返回精简结果，大数据不进 LLM 上下文

---

## 五、沙箱环境能力与边界

### 5.1 容器能力

| 能力 | 详情 |
|------|------|
| **预装运行时** | Python 3.11+, Node.js, Ruby, Go, Rust |
| **Agent 工作目录** | `/workspace` |
| **可写输出路径** | `/mnt/session/outputs/`（自动可下载） |
| **挂载文件路径** | 创建 Session 时指定 `mount_path`（只读） |
| **网络** | 受 Environment 网络策略控制 |
| **包安装** | Environment 预装 或 运行时 pip/npm |

### 5.2 限制

| 限制 | 说明 |
|------|------|
| 无 localStorage | 容器无浏览器环境 |
| 文件数上限 | 每 Session 最多 100 个文件 |
| 网络受限 | limited 模式下仅白名单域名 |
| 无跨 Session 共享 | 每个 Session 独立文件系统 |
| 凭证隔离 | OAuth token 存 vault，代理层注入，沙箱看不到真实凭证 |
| 仅云端 | 不支持 Bedrock / Vertex AI |
| 单 Agent | 多 Agent 编排需自建 |

### 5.3 Session 生命周期

| 状态 | 计费 | 说明 |
|------|------|------|
| `running` | 按毫秒计 | Agent 推理或执行工具中 |
| `idle` | **不计费** | 等待用户输入 |
| `archived` | 不计费 | 已归档，不可恢复 |

- 容器崩溃后可 `wake(sessionId)` 恢复（重放事件日志）
- 事件服务端缓存，断线重连可续接

---

## 六、定价

| 计费项 | 费率 | 说明 |
|--------|------|------|
| **Token 费用** | 与标准 Claude API 相同 | input/output/cache_read/cache_create |
| **运行时费用** | $0.08 / Session 小时 | 仅 `running` 状态，精确到毫秒 |
| **Web Search** | $10 / 1000 次 | 可禁用 |

---

## 七、Rate Limits

| 端点类型 | 限制 | 级别 |
|---------|------|------|
| 创建端点（agents/environments/sessions） | 60 RPM | 组织级 |
| 读取端点（retrieve/list/stream） | 600 RPM | 组织级 |
| 事件发送（POST events） | 600 RPM | 组织级 |

---

## 八、支持的模型

| 模型 | Model ID | 推荐场景 |
|------|---------|---------|
| **Claude Sonnet 4.6** | `claude-sonnet-4-6` | 大多数 Agent 任务（性价比最优，5x cheaper than Opus） |
| **Claude Opus 4.6** | `claude-opus-4-6` | 复杂编排、长上下文推理（1M context） |
| **Claude Haiku 4.5** | `claude-haiku-4-5-20251001` | 轻量辅助任务（不推荐主 Agent） |

---

## 九、完整 Python SDK 示例

```python
import asyncio, json
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key="...")

# ── 1. 创建 Agent（一次性） ──
agent = await client.beta.agents.create(
    name="Keyword Research Assistant",
    model="claude-sonnet-4-6",
    system=SYSTEM_PROMPT,
    tools=[
        {
            "type": "agent_toolset_20260401",
            "default_config": {"enabled": False},
            "configs": [
                {"name": "bash", "enabled": True},
                {"name": "read", "enabled": True},
                {"name": "edit", "enabled": True},
                {"name": "write", "enabled": True},
                {"name": "glob", "enabled": True},
            ]
        },
        {"type": "custom", "name": "filter_keywords", ...},
        {"type": "custom", "name": "sort_keywords", ...},
    ],
)

# ── 2. 创建 Environment（一次性） ──
environment = await client.beta.environments.create(
    name="keyword-env",
    config={
        "type": "cloud",
        "packages": {"pip": ["pandas", "numpy", "openpyxl"]},
        "networking": {"type": "unrestricted"},
    },
)

# ── 3. 创建 Session ──
session = await client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
)

# ── 4. 发送消息 + 流式接收 ──
await client.beta.sessions.events.send(session.id, events=[{
    "type": "user.message",
    "content": [{"type": "text", "text": "请帮我筛选搜索量>1000的关键词"}]
}])

async with client.beta.sessions.events.stream(session.id) as stream:
    async for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    print(block.text, end="")
            
            case "agent.custom_tool_use":
                result = await dispatch_tool(event.name, event.input)
                await client.beta.sessions.events.send(session.id, events=[{
                    "type": "user.custom_tool_result",
                    "custom_tool_use_id": event.id,
                    "content": [{"type": "text", "text": json.dumps(result)}],
                    "is_error": False,
                }])
            
            case "session.status_idle":
                if event.stop_reason.type == "end_turn":
                    break

# ── 5. 清理 ──
await client.beta.sessions.archive(session.id)
```

---

## 十、Managed Agents vs Claude Code vs Agent SDK

| 维度 | Managed Agents | Claude Code | Agent SDK |
|------|---------------|-------------|-----------|
| **部署** | Anthropic 云端 | 本地终端/IDE/CI | 开发者自托管 |
| **基础设施** | 全托管 | 用户环境 | 开发者管理 |
| **Agent 循环** | 内置自动 | 内置自动 | 开发者实现 |
| **沙箱** | 托管容器 | 用户本地 | 开发者管理 |
| **状态持久化** | 内置事件日志 | Claude Code SDK | 开发者管理 |
| **Session 时长** | 分钟~小时，idle 不计费 | 交互式或 headless | 取决于实现 |
| **扩展** | Anthropic 自动 | 用户管理 | 开发者管理 |
| **数据驻留** | Anthropic 基础设施 | 本地 | 开发者控制 |
| **定制性** | API 表面 | 完全控制 | 完全控制 |
| **适用场景** | 长时自主任务 | 开发者协作 | 深度定制 |

---

## 十一、关键最佳实践

1. **Agent + Environment 只创建一次**，通过 ID 跨 Session 复用
2. **生产用 `limited` 网络**，显式白名单 `allowed_hosts`
3. **利用 idle 不计费**，长会话中 Agent 等待输入零成本
4. **事件可先发后连**，发消息后再连 stream，事件服务端缓存不丢
5. **断线可续接**，重新连接 stream 从上次断点继续
6. **容器崩溃可恢复**，`wake(sessionId)` 重放事件日志
7. **Prompt cache 自动生效**，system prompt 和长上下文享受缓存折扣
8. **工具结果精简**，大数据存 Session 内存，LLM 只看摘要
