# LLM 工具调用核心概念解析

**Function Calling · Tools · MCP**

2026年版 | 基于 Anthropic Claude API 视角

---

## 1 先说结论

在 LLM 与外部世界交互的整个体系中，有三个核心概念需要明确区分：

> **Function Calling** — 模型侧的能力。指 LLM 能够输出结构化的工具调用请求，而不是纯文本。
>
> **Tools** — 外部侧的能力。指提供给模型的工具声明和对应的执行实现。
>
> **MCP** — 连接层的协议。标准化了 Client 与 Tool 之间的通信方式。

三者的关系可以类比为：Function Calling 是"大脑做决策"，Tools 是"手脚去执行"，MCP 是"大脑和手脚之间的神经网络协议"。

---

## 2 三个角色

在任何一次工具调用流程中，始终存在三个角色：

| 角色 | 身份 | 职责 |
|------|------|------|
| **LLM** | 模型（大脑） | 理解用户意图，决定是否调用工具、调用哪个、传什么参数。最后把工具返回的结果翻译成自然语言回答用户。它不执行任何外部操作，只做"决策"和"翻译"。 |
| **Client** | 编排层（你的代码） | 整个流程的控制者。负责把用户消息和工具定义发给模型，接收模型的调用请求，实际执行工具调用，再把结果传回模型。在 Agent 框架中这就是 Agentic Loop。 |
| **Tool** | 工具（手脚） | 被动执行。接收结构化输入，返回结构化输出。它不知道 LLM 的存在，就是一个普通的 API 或函数。天气接口、数据库查询、发邮件的 SMTP 服务都属于这个角色。 |

**核心分工：** LLM 是大脑但没有手，Tool 是手但没有大脑，Client 把它们连起来。

---

## 3 Function Calling 详解

### 3.1 是什么

Function Calling 是 LLM 的一种原生能力，指模型在生成过程中，不输出自然语言，而是输出一个结构化的函数调用请求（函数名 + 参数），交由外部系统执行，再把执行结果返回给模型继续推理。

### 3.2 解决什么问题

LLM 的本质是文本生成器，输出是非结构化的自然语言。但外部系统（API、数据库、工具）需要结构化输入。Function Calling 解决的核心矛盾是：如何让模型可靠地完成"自然语言 → 结构化动作"的转换。

### 3.3 模型具体做了什么

当模型支持 Function Calling 时，它在每次推理中需要做三个判断：

1. **意图识别：** 这个问题需要调用工具吗？还是直接用文本回答就行？
2. **工具选择：** 如果需要调用，应该调用哪个工具？
3. **参数提取：** 从用户的自然语言中提取出符合 schema 的结构化参数。

**关键点：** 模型自己不调 API。它只是输出一个"我要调 X 工具，参数是 Y"的结构化指令。真正执行调用的是 Client 的代码。

### 3.4 行业现状（2026）

截至 2026 年，Function Calling 已经是所有主流 LLM 的标配能力，不再是差异化功能：

- **OpenAI** — 最早商业化（2023.06），从 `functions` 参数演变为 `tools` 参数，支持并行调用（parallel function calling）和严格模式（`strict: true`，强制输出 100% 符合 schema）。
- **Anthropic** — 使用 `tools` 定义 + `tool_use` / `tool_result` 消息类型，与 MCP 协议深度集成。
- **Google** — Gemini API 同样支持 Function Calling，可与 Structured Output 结合使用。
- **开源模型** — Gorilla、ToolLLaMA 等专门针对工具调用微调的模型持续演进，开源社区也在 Berkeley Function-Calling Leaderboard (BFCL) 上持续评测各模型的工具调用能力。

**相关概念区分：** Function Calling 专注于"触发外部动作"。与之相关但不同的概念是 Structured Output（强制模型输出符合特定 JSON Schema 的数据，用于数据提取和分类，不涉及外部调用）和 JSON Mode（仅保证输出合法 JSON，不保证 schema 合规）。三者的选择标准：需要触发动作用 Function Calling，需要数据提取用 Structured Output，只需要合法 JSON 用 JSON Mode。

---

## 4 Tools 详解

### 4.1 是什么

Tools 是提供给模型的一组"工具声明"，每个 tool 包含名称、描述和参数 schema。它告诉模型"你有哪些能力可用"。

### 4.2 两个组成部分

Tools 的实现需要两部分配套：

1. **工具定义（Tool Definition）：** 传给模型的 JSON 声明，告诉模型这个工具叫什么、做什么、接受哪些参数。
2. **执行代码（Tool Implementation）：** Client 端提前写好的对应函数，负责拿着模型给的参数去实际执行。

**注册一个 tool 给模型，就必须在 Client 端有对应的实现。它们是成对出现的。**

### 4.3 Tool Definition 示例

```json
{
  "name": "get_weather",
  "description": "查询指定城市的实时天气",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名，如：北京、上海"
      }
    },
    "required": ["city"]
  }
}
```

模型会阅读 description 和参数的 description 来理解什么时候该用这个工具、怎么填参数。这也是为什么 description 的质量直接影响调用准确率。

---

## 5 MCP 详解

### 5.1 是什么

MCP（Model Context Protocol）是 Anthropic 于 2024 年 11 月发布的开放协议，基于 JSON-RPC 2.0 传输，标准化了 Client 与 Tool 之间的通信方式——包括工具发现、工具调用、结果返回这套完整交互。2025 年 1 月发布 v1.0 规范，2025 年 12 月 Anthropic 将 MCP 捐赠给 Linux 基金会下的 Agentic AI Foundation (AAIF)，成为行业共治的开放标准。

### 5.2 解决什么问题

没有 MCP 之前，每个工具的接入方式都是自定义的——你需要为每个 API 单独写对接逻辑。MCP 统一了这套协议，让所有工具用相同的方式接入，降低了集成成本。

### 5.3 MCP 的能力范围

MCP 不只是"调用工具"的协议，它覆盖了三大类能力：

1. **Tools（工具）：** AI 可以触发的动作，如发送 Slack 消息、查询数据库。这是 Function Calling 最直接对接的部分。
2. **Resources（资源）：** AI 可以读取的数据，如文件、数据库行。只读，不触发动作。
3. **Prompts（提示模板）：** 可复用的交互模板，服务端预定义好的提示词结构。

此外，MCP 规范还包含几个高级特性：

- **Sampling：** MCP Server 可以反向请求 Client 侧的 LLM 做推理，让工具端也能利用 AI 能力，而不需要自己接入模型。
- **Elicitation（2025.06 加入）：** Server 可以在执行过程中暂停，向用户请求结构化输入（如"请确认使用哪个邮箱"），实现 Human-in-the-Loop 交互。
- **Tool Output Schema（2025.06 加入）：** 工具可以预先声明输出的数据结构，让 Client 和 LLM 提前知道返回格式。

### 5.4 行业现状（2026）

截至 2026 年 3 月，MCP 月安装量已突破 9700 万，成为 AI 基础设施领域增长最快的协议。所有主流 AI 厂商——OpenAI、Google DeepMind、Cohere、Mistral——都已在其 Agent 框架中集成 MCP 支持。官方 GitHub 有 50+ 官方 Server 实现，社区贡献了 150+ 实现，覆盖数据库、开发工具、通信平台、云基础设施等场景。

最新规范版本为 2025-11-25，下一版预计 2026 年 6 月发布。

### 5.5 前提条件

> **重要：** 要使用 MCP，LLM 必须支持 Function Calling。
>
> MCP 解决的是 Client ↔ Tool 之间的通信问题，但整个流程的起点是模型要能输出结构化的调用请求。如果模型不支持 Function Calling，它只会输出纯文本，Client 无从知道该调什么工具。

### 5.6 三者关系图

```
LLM (Function Calling能力)  →  Client (编排层)  →  Tool (执行层)
       "调什么、传什么"         "拿着参数去执行"      "被动执行、返回结果"

其中 Client ↔ Tool 的通信可以用 MCP 协议标准化
但 Function Calling 不依赖 MCP——你自己写对接逻辑也行，只是不标准化。
```

---

## 6 完整 Case：查询天气

以下用一个实际的天气查询场景，基于 Anthropic Claude API，完整展示每一步的报文细节。

**场景：** 用户问"北京今天天气怎么样？"，模型调用天气 API 获取实时数据后回答。

### Step 1：Client → Anthropic API

Client 发送 HTTP 请求，包含用户消息和工具定义：

```json
POST /v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "tools": [
    {
      "name": "get_weather",
      "description": "查询指定城市的实时天气",
      "input_schema": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "城市名"
          }
        },
        "required": ["city"]
      }
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": "北京今天天气怎么样？"
    }
  ]
}
```

> **报文说明：**
>
> - **tools 数组：** 告诉模型"你有一个叫 get_weather 的工具可用"。模型通过阅读 description 和参数 schema 来理解如何使用。
> - **messages 数组：** 对话历史。当前只有用户的一条消息。
> - **input_schema：** 标准 JSON Schema 格式，定义了参数的类型、描述和是否必填。

### Step 2：Anthropic API → Client（模型决定调用工具）

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "stop_reason": "tool_use",
  "content": [
    {
      "type": "text",
      "text": "让我查一下北京今天的天气。"
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": {
        "city": "北京"
      }
    }
  ]
}
```

> **报文说明：**
>
> - **stop_reason: "tool_use"：** 告诉 Client"我还没说完，先去执行这个工具"。如果是 `end_turn` 则表示回答完毕。
> - **content 是数组：** 可以同时包含文本和工具调用（模型先说句话再调工具）。
> - **tool_use.id：** 唯一标识符，后面返回结果时必须对应上。
> - **input.city: "北京"：** 模型从用户的自然语言"北京今天天气怎么样"中提取出来的结构化参数。

### Step 3：Client 自己执行工具

这步与 LLM API 无关，是 Client 端提前写好的代码。Client 解析模型返回的 tool_use，根据 name 路由到对应函数，把模型给的 input 透传过去：

```python
# Client 端提前写好的工具注册表
tool_registry = {
    "get_weather": call_weather_api,
    "send_email": call_email_api,
}

# 收到模型的 tool_use 后
tool_name = "get_weather"          # 来自模型输出
tool_input = {"city": "北京"}       # 来自模型输出

# 路由到对应函数，透传参数
func = tool_registry[tool_name]
result = func(**tool_input)
# result = {"temp": 18, "condition": "多云", "humidity": 45}
```

> **核心理解：**
>
> - **代码是提前写好的：** 注册一个 tool 给模型，就必须在 Client 端有对应的执行实现。
> - **参数是模型给的：** Client 不知道该传"北京"，是模型从用户自然语言中提取出来的。Client 拿着参数无脑透传。

### Step 4：Client → Anthropic API（把结果传回模型）

Client 把完整对话历史（包括模型的 tool_use 和工具的结果）发回去：

```json
POST /v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "tools": [ ...同 Step 1... ],
  "messages": [
    {
      "role": "user",
      "content": "北京今天天气怎么样？"
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "让我查一下北京今天的天气。"
        },
        {
          "type": "tool_use",
          "id": "toolu_01A09q90qw90lq917835lq9",
          "name": "get_weather",
          "input": { "city": "北京" }
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": "{\"temp\": 18, \"condition\": \"多云\", \"humidity\": 45}"
        }
      ]
    }
  ]
}
```

> **报文说明：**
>
> - **这是一个全新的 HTTP 请求：** LLM 无状态，必须带上完整对话历史。
> - **tool_use_id 必须匹配：** 对应 Step 2 中的 id，模型靠这个知道"这是哪次调用的结果"。
> - **tool_result 放在 role: user 里：** 从协议角度，工具结果是"外部世界给模型的输入"。

### Step 5：Anthropic API → Client（模型生成最终回答）

```json
{
  "id": "msg_02YGEUEZKhBBCavnqtvWpXRM",
  "type": "message",
  "role": "assistant",
  "stop_reason": "end_turn",
  "content": [
    {
      "type": "text",
      "text": "北京今天多云，气温18°C，湿度45%。体感比较舒适，出门带件薄外套就行。"
    }
  ]
}
```

> **报文说明：**
>
> - **stop_reason: "end_turn"：** 模型认为回答完毕，不需要再调用工具。Client 可以把文本展示给用户了。

---

## 7 交互时序总结

```
请求1:  Client → API     (用户消息 + tools 定义)
响应1:  API → Client     (stop_reason=tool_use, 含 tool_use 块)
         Client 自己执行工具
请求2:  Client → API     (完整历史 + tool_result)
响应2:  API → Client     (stop_reason=end_turn, 最终回答)
```

一次 Function Calling 至少是**两轮 HTTP 请求**。如果模型需要连续调用多个工具，就会是 3 轮、4 轮……Client 的 Agentic Loop 就是在循环处理这个过程：收到 `tool_use` 就执行再提交，收到 `end_turn` 就结束。

---

## 8 常见疑问

### Q: 模型怎么知道参数该填"北京"？

模型从用户的自然语言中提取的。用户说"北京今天天气怎么样"，模型理解语义后，按照 tool 的 input_schema 要求，把"北京"填到 city 字段里。Client 不做任何提取，它只是拿着模型给的参数透传。

### Q: Client 端的执行代码是提前写好的吗？

是的。你在 tools 数组里注册了哪些工具，Client 端就必须有对应的执行函数。它们是成对出现的。模型只输出"我要调 X"这个指令，不会帮你写执行代码。

### Q: 没有 MCP 能用 Function Calling 吗？

能。Function Calling 不依赖 MCP。你可以自己在 Client 端写每个工具的对接逻辑。MCP 只是让这个对接过程标准化，降低集成成本。

### Q: 没有 Function Calling 能用 MCP 吗？

不能。MCP 解决的是 Client ↔ Tool 之间的通信，但整个流程的起点是模型要能输出结构化的调用请求。模型不支持 Function Calling，它只会输出纯文本，后面的链路就断了。

### Q: 为什么是两轮 HTTP 请求，不是一轮？

LLM 无状态且不能主动调用外部 API。第一轮它告诉 Client"我需要这个工具的结果"，Client 执行完后，第二轮再把结果连同完整历史发回去，模型才能基于真实数据生成最终回答。