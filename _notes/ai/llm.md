# LLMs

大语言模型

[wiki](https://en.wikipedia.org/wiki/Large_language_model )
[大语言模型历史-中国人民大学](http://ai.ruc.edu.cn/research/science/20230605100.html )
[大语言模型历史-中国人民大学-论文](https://arxiv.org/abs/2303.18223 )
[大语言模型历史-博客](https://juejin.cn/post/7226541360044556343 )
[Quick Start Guide to Large Language Models](https://archive.org/details/quick-start-guide-to-large-language-models-strategies-and-best-practices-for-usi_202407/page/n5/mode/2up?view=theater)
[quick start llms 作者主页](https://sinanozdemir.ai/#publications)

## 大模型公司列表

### 开源


以下是基于2026年3月初主流开源/开放权重（open-weight）大模型的综合排名表格。我综合了多个来源的数据，包括：
- **Hugging Face Open LLM Leaderboard**（客观基准，如MMLU-Pro、GPQA、MATH等）
- **LMArena / Chatbot Arena Elo**（人类偏好盲测）
- **OpenRouter 调用量 / 市占率**（实际生产使用）
- **SWE-bench / LiveCodeBench**（编程/工程能力）
- **其他专业榜单**（如GPQA Diamond、AIME数学等）
当前格局：中国开源模型在多数维度（尤其是性价比、推理、编程、社区采用）全面领先，Llama 4 等 Meta 模型在长上下文有优势但整体掉队。

| 排名 | 模型名称                  | 开发者/公司       | 主要参数规模（总/活跃） | 上下文长度    | 官方/下载 URL (Hugging Face 或官网)                          | 主要优势 & 依据                                                                 | 综合得分参考（Elo / 基准平均） |
|------|---------------------------|-------------------|--------------------------|---------------|-------------------------------------------------------------|---------------------------------------------------------------------------------|--------------------------------|
| 1    | GLM-5                     | 智谱AI (Zhipu)   | ~744B / MoE             | 200K+        | https://huggingface.co/THUDM/glm-5 (或 z.ai 官网)         | 推理/编程/SWE-bench 极强，常居开源トップ；Elo ~1450+，SWE 高分 | ~1450+ Elo, Top1-2 开源       |
| 2    | Kimi K2.5                 | 月之暗面 (Moonshot) | ~1T / MoE               | 262K         | https://huggingface.co/moonshotai/Kimi-K2.5 (kimi.ai)       | 综合最均衡，数学/编程/人类偏好强；OpenRouter 调用量常第1，GPQA/AIME 高 | ~1445-1447 Elo, Top1-3        |
| 3    | Qwen 3.5                  | 阿里通义千问      | 397B / ~170B active     | 262K         | https://huggingface.co/Qwen/Qwen-3.5-397B (qwen.ai)         | 下载量/社区衍生模型爆炸式增长；多模态+性价比王者，GPQA Diamond 88.4% | Top Hugging Face 下载，强基准  |
| 4    | DeepSeek V3.2             | DeepSeek AI      | 685B / MoE              | 长上下文     | https://huggingface.co/deepseek-ai/DeepSeek-V3.2            | 数学/硬核推理最强（AIME/GPQA/FrontierMath）；性价比高 | Top 数学/推理，Elo 高         |
| 5    | MiniMax M2.5              | MiniMax          | ~230B / MoE             | 长上下文     | https://huggingface.co/MiniMax/MiniMax-M2.5                 | 多模态/编程/Agent 强；OpenRouter 市占高 | Top5 常见，编程榜强           |
| 6    | MiMo-V2-Flash / Step-3.5-Flash | StepFun / 其他  | ~196-309B / MoE active 小 | 128K+        | Hugging Face 搜索对应模型                                   | 超高性价比/速度；AIME 94%+，成本仅顶级闭源1/10-1/50 | 性价比/速度 Top               |
| 7    | Llama 4 Maverick          | Meta             | ~400B / 17B active MoE  | 1M-10M       | https://huggingface.co/meta-llama/Llama-4-Maverick          | 超长上下文王者（10M tokens Scout 版更极致）；多模态原生 | 长上下文唯一强项，但 Elo/基准掉队 |
| 8    | Llama 4 Scout             | Meta             | ~109B / 17B active MoE  | 10M tokens   | https://huggingface.co/meta-llama/Llama-4-Scout             | 同上，部署友好（单 H100 可跑） | 长文档/RAG 专用               |


### 闭源

| 排名 | 模型系列 | 厂商 | 官方网站 / 在线对话 | API 开发者入口 |
| --- | --- | --- | --- | --- |
| **1** | **Claude 4.6** | Anthropic | [claude.ai](https://claude.ai) | [console.anthropic.com](https://console.anthropic.com) |
| **2** | **Gemini 3.1** | Google | [gemini.google.com](https://gemini.google.com) | [ai.google.dev](https://ai.google.dev) (AI Studio) |
| **3** | **GPT-5 / 5.1** | OpenAI | [chatgpt.com](https://chatgpt.com) | [platform.openai.com](https://platform.openai.com) |
| **4** | **Grok 4.20** | xAI | [grok.com](https://grok.com) | [console.x.ai](https://console.x.ai) |
| **5** | **豆包 (Doubao)** | 字节跳动 | [doubao.com](https://www.doubao.com) | [volcengine.com](https://www.volcengine.com/product/doubao) (火山引擎) |
| **6** | **文心一言 (ERNIE)** | 百度 | [yiyan.baidu.com](https://yiyan.baidu.com) | [qianfan.baidu.com](https://www.google.com/search?q=https://qianfan.baidu.com) (千帆平台) |
| **7** | **通义千问 (Qwen)** | 阿里巴巴 | [tongyi.aliyun.com](https://tongyi.aliyun.com) | [dashscope.aliyun.com](https://dashscope.aliyun.com) (灵积/百炼) |


## 定义

Large language models (LLMs) are AI models that are usually (but not necessarily) derived from the Transformer architecture and are designed to understand and generate human language, code, and much more


## 工具

### claude code
[官网](https://claude.ai )
[使用文档](https://code.claude.com/docs/en/overview )

cli版本需要添加下面的配置
```shell
cat >> ~/.zshrc << 'EOF'

# Proxy Configuration
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export ftp_proxy="http://127.0.0.1:7890"
export no_proxy="localhost,127.0.0.1,::1"
EOF

source ~/.zshrc
```

macos桌面版启动需要配置

```shell
launchctl setenv https_proxy http://127.0.0.1:7890
launchctl setenv http_proxy http://127.0.0.1:7890
launchctl setenv all_proxy socks5://127.0.0.1:7890
```

最精简、推荐的方式,直接小黑框里面执行下面的命令打开，让应用程序走代理：
```shell
https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 open -a Claude
```

### Gemini CLI (开源的agent)

[官网](https://geminicli.com/)
[github](https://github.com/google-gemini/gemini-cli)


### cursor
[官网](https://cursor.com/home)


### codex
[官网](https://openai.com/codex/ )

### opencode
[官网](https://opencode.ai/ )

### openclaw
[官网](https://openclaw.ai/ )
[clawhub](https://clawhub.ai/ )
[github](https://github.com/openclaw/openclaw)

```shell
npm install clawhub
npx clawhub install <hub-id>
```

#### 养龙虾



### openrouter
[官网](https://openrouter.ai/ )

### Cline
[官网](https://cline.bot/ )

#### Cli
[官网](https://cline.bot/ )

#### jetbrains
[官网](https://cline.bot/jetbrains )

#### vs code
[官网](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev )


## 概念

### Agent


普通的LLM只能根据输入生成文本，本质上是一个文本生成器，它不能访问实时信息、不能操作外部系统、不能执行计算。Agent通过接入工具，让LLM突破了这些限制

很多任务不是一句话能完成的。比如"帮我订一张明天去上海的机票"，这需要查航班、比价、确认时间、下单等一系列步骤。单次LLM调用做不到，但Agent可以把任务拆解并逐步执行。

没有Agent的情况下，用户需要手动把一个任务拆成多个prompt，自己串联中间结果，本质上人充当了"调度器"。Agent把这个调度过程自动化了，用户只需描述目标，Agent自己想办法完成。

很多场景需要LLM不只是给出建议，而是真正去执行——发邮件、写文件、查数据库、调API。Agent让LLM从"顾问"变成了"执行者"。

预设的固定流程无法应对所有场景，而Agent可以根据中间结果灵活调整策略。比如搜索第一次没找到答案，它会换个关键词再试，这种适应能力是传统自动化脚本做不到的。

传统程序的逻辑是开发者预先定义好的，if-else、循环、调用顺序都是确定的。而Agent的控制流是由LLM在运行时动态决定的。面对同一个任务，它可能因为中间结果不同而走完全不同的路径。这种灵活性是传统程序很难做到的


agentic loop：

一个典型的 Agent loop 大致是这样的：
```
while 任务未完成:
    1. 思考（Think）：LLM 根据当前上下文，决定下一步该做什么
    2. 行动（Act）：调用某个工具（读文件、执行命令、搜索等）
    3. 观察（Observe）：获取工具返回的结果
    4. 判断：任务完成了吗？
       - 没完成 → 回到第1步，带着新信息继续思考
       - 完成了 → 输出最终结果，退出循环
```

相关论文：

[ReAct: Synergizing Reasoning and Acting in Language Models（ICLR 2023）](https://arxiv.org/pdf/2210.03629)

[A Survey on Large Language Model based Autonomous Agents](https://arxiv.org/pdf/2308.11432)

[Large Language Model Agent: A Survey on Methodology, Applications and Challenges](arxiv.org/abs/2503.21460)

### Subagents

SubAgent（子智能体）是指在一个Agent系统中，由主Agent（也叫Orchestrator或Parent Agent）调度和管理的下级Agent。

核心思想很简单：把一个复杂任务拆分给多个专门的子Agent去完成，主Agent负责协调

打个比方，就像一个项目经理（主Agent）把任务分配给不同的专员（SubAgent）：一个负责搜索资料，一个负责写代码，一个负责数据分析，最后项目经理汇总结果。

和普通多Agent系统的区别在于层级关系。多Agent系统中的Agent可以是平等协作的，而SubAgent明确有上下级关系——它由主Agent创建、调用，完成后把结果返回给主Agent。SubAgent通常不会直接和用户交互，也不知道整体任务的全貌，只专注于自己被分配的子任务。

典型的工作流程是这样的：用户给主Agent一个复杂任务，主Agent分析任务并拆解成子任务，针对每个子任务调用对应的SubAgent，SubAgent完成后返回结果，主Agent整合所有SubAgent的结果并给出最终回答。

使用SubAgent的好处有几个方面。首先是专业化，每个SubAgent可以有不同的prompt、工具和能力，术业有专攻。其次是降低复杂度，主Agent不需要一次性处理所有细节，每个SubAgent只关注自己的小问题。另外还能并行执行，多个SubAgent可以同时工作，提高效率。

相关论文：

[MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework（2023）](https://arxiv.org/pdf/2308.00352)
[项目开源地址](https://github.com/FoundationAgents/MetaGPT)

[AgentOrchestra: A Hierarchical Multi-Agent Framework for General-Purpose Task Solving（2025）](https://arxiv.org/html/2506.12508v1)

[HLA: LLM-Powered Hierarchical Language Agent for Real-time Human-AI Coordination（AAMAS 2024）](https://dl.acm.org/doi/epdf/10.5555/3635637.3662979)

[Towards Effective GenAI Multi-Agent Collaboration（2024）](https://arxiv.org/html/2412.05449v1)

[LLM Augmented Hierarchical Agents（CoRL Workshop 2023）](https://eehpc.ece.jhu.edu/wp-content/uploads/2023/10/LangRob_CoRL.pdf)

[AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation（2023，微软）](https://arxiv.org/pdf/2308.08155)
[项目开源地址](https://github.com/microsoft/autogen)

[CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society（2023）](https://arxiv.org/pdf/2303.17760)
[官网](https://www.camel-ai.org/)

[Lilian Weng的博客："LLM Powered Autonomous Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/)

### MCP
[官方文档](https://modelcontextprotocol.io/docs/getting-started/intro )


#### 实现一个简单的本地MCP Server

1. 环境信息：
- OS：Manjaro Linux x86_64
- Python：3.10
- MCP 目录：/home/poul/workspace/software/llm_mcp

2. 第一步：创建项目
```shell
cd /home/poul/workspace/software/llm_mcp
uv init notes-server
cd notes-server
```

3. 第二步：安装依赖
```shell
uv add mcp -i https://pypi.tuna.tsinghua.edu.cn/simple
```

4. 第三步：写代码
把 `main.py` 内容替换为：
```python
import json
import os
import logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

mcp = FastMCP("笔记本")
NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.json")

log.info("MCP 笔记本服务启动中...")
log.info(f"笔记存储路径: {NOTES_FILE}")

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            log.info(f"加载笔记成功，共 {len(data)} 条")
            return data
    log.info("笔记文件不存在，返回空列表")
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    log.info(f"笔记保存成功，共 {len(notes)} 条")

@mcp.tool()
def add_note(title: str, content: str) -> str:
    """添加一条笔记"""
    log.info(f"调用 add_note: title={title}, content={content}")
    notes = load_notes()
    notes.append({"id": len(notes) + 1, "title": title, "content": content})
    save_notes(notes)
    result = f"✅ 笔记「{title}」添加成功，当前共 {len(notes)} 条笔记"
    log.info(f"add_note 完成: {result}")
    return result

@mcp.tool()
def list_notes() -> str:
    """列出所有笔记"""
    log.info("调用 list_notes")
    notes = load_notes()
    if not notes:
        log.info("list_notes: 暂无笔记")
        return "暂无笔记"
    lines = [f"[{n['id']}] {n['title']}: {n['content']}" for n in notes]
    result = "\n".join(lines)
    log.info(f"list_notes: 返回 {len(notes)} 条笔记")
    return result

@mcp.tool()
def delete_note(note_id: int) -> str:
    """根据 ID 删除一条笔记"""
    log.info(f"调用 delete_note: note_id={note_id}")
    notes = load_notes()
    original_len = len(notes)
    notes = [n for n in notes if n["id"] != note_id]
    if len(notes) == original_len:
        log.warning(f"delete_note: 未找到 ID={note_id} 的笔记")
        return f"❌ 未找到 ID 为 {note_id} 的笔记"
    save_notes(notes)
    result = f"✅ 笔记 {note_id} 已删除"
    log.info(f"delete_note 完成: {result}")
    return result

if __name__ == "__main__":
    log.info("MCP Server 开始监听 (stdio 模式)...")
    mcp.run()
    log.info("MCP Server 已退出")
```

5. 第四步：测试服务能跑起来
```shell
uv run main.py
```
看到日志输出、终端阻塞没有报错，`Ctrl+C` 退出。

6. 第五步：安装 Claude Code CLI
```shell
npm install -g @anthropic-ai/claude-code
```

7. 第六步：注册 MCP Server
注册mcp的方式
```
Examples:
  # Add HTTP server:
  claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

  # Add HTTP server with headers:
  claude mcp add --transport http corridor https://app.corridor.dev/api/mcp --header "Authorization: Bearer ..."

  # Add stdio server with environment variables:
  claude mcp add -e API_KEY=xxx my-server -- npx my-mcp-server

  # Add stdio server with subprocess flags:
  claude mcp add my-server -- my-command --some-flag arg1
```

```shell
claude mcp add notes-server \
  -- uv \
  --directory /home/poul/workspace/software/llm_mcp/notes-server \
  run main.py
```

验证注册成功：
```shell
claude mcp list
```

看到 `notes-server` 出现在列表里就OK。

8. 第七步：使用
```shell
claude
```

然后直接说：
```
> 帮我记一条笔记，标题是「学习计划」，内容是「每天学习 MCP 一小时」
> 列出我所有的笔记
> 删除第 1 条笔记
```

#### MCP的调用流程
```
你输入："帮我记一条笔记，标题是学习计划"
        ↓
Claude Code CLI（MCP Client）
        ↓ 把你的话 + 工具列表 一起发给 Claude
Anthropic API（Claude 大模型）
        ↓ 分析意图，决定调用哪个工具，返回结构化指令
Claude Code CLI（MCP Client）
        ↓ 解析指令，通过 stdio 发送 JSON-RPC 消息
你的 main.py（MCP Server 子进程）
        ↓ 执行 add_note() 函数
        ↓ 返回结果
Claude Code CLI
        ↓ 把结果喂回给 Claude
Claude 大模型
        ↓ 组织成自然语言回复
你看到："✅ 笔记「学习计划」添加成功"
```

#### 实现一个简单的远程MCP Server

1. 创建项目
```shell
cd /home/poul/workspace/software/llm_mcp
uv init weather-server-remote
cd weather-server-remote
uv add mcp httpx -i https://pypi.tuna.tsinghua.edu.cn/simple
```


2. 写代码
`main.py`
```python
import logging
import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

mcp = FastMCP(
    "天气查询",
    host="0.0.0.0",
    port=8000,
)

# 使用 wttr.in 免费天气API，无需注册申请key
WEATHER_API = "https://wttr.in/{city}?format=j1&lang=zh"

log.info("天气查询 MCP Server 启动中...")

@mcp.tool()
async def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    Call this tool when the user asks about weather, temperature, or climate of a place.
    city is the name of the city, e.g. Beijing, Shanghai, London.
    """
    log.info(f"调用 get_weather: city={city}")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(WEATHER_API.format(city=city))
            resp.raise_for_status()
            data = resp.json()

        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        desc = current["lang_zh"][0]["value"] if current.get("lang_zh") else current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]

        result = (
            f"🌤 {city} 当前天气\n"
            f"天气：{desc}\n"
            f"温度：{temp_c}°C（体感 {feels_like}°C）\n"
            f"湿度：{humidity}%\n"
            f"风速：{wind_speed} km/h"
        )
        log.info(f"get_weather 完成: {city} {temp_c}°C {desc}")
        return result

    except httpx.TimeoutException:
        log.error(f"get_weather 超时: city={city}")
        return f"❌ 查询 {city} 天气超时，请稍后再试"
    except Exception as e:
        log.error(f"get_weather 失败: {e}")
        return f"❌ 查询失败：{str(e)}"


@mcp.tool()
async def get_weather_forecast(city: str) -> str:
    """
    Get 3-day weather forecast for a city.
    Call this tool when the user asks about future weather or weather forecast.
    city is the name of the city, e.g. Beijing, Shanghai, London.
    """
    log.info(f"调用 get_weather_forecast: city={city}")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(WEATHER_API.format(city=city))
            resp.raise_for_status()
            data = resp.json()

        forecasts = data["weather"]
        lines = [f"📅 {city} 未来3天天气预报\n"]
        for day in forecasts:
            date = day["date"]
            max_c = day["maxtempC"]
            min_c = day["mintempC"]
            desc = day["hourly"][4]["lang_zh"][0]["value"] if day["hourly"][4].get("lang_zh") else day["hourly"][4]["weatherDesc"][0]["value"]
            lines.append(f"{date}：{desc}，{min_c}°C ~ {max_c}°C")

        result = "\n".join(lines)
        log.info(f"get_weather_forecast 完成: {city}")
        return result

    except httpx.TimeoutException:
        log.error(f"get_weather_forecast 超时: city={city}")
        return f"❌ 查询 {city} 天气预报超时，请稍后再试"
    except Exception as e:
        log.error(f"get_weather_forecast 失败: {e}")
        return f"❌ 查询失败：{str(e)}"


if __name__ == "__main__":
    log.info("MCP Server 启动，监听 http://0.0.0.0:8000 ...")
    mcp.run(transport="streamable-http")
```

3. 启动服务
```shell
uv run main.py
```

4. 注册到 Claude Code
```shell
claude mcp add weather-server \
  --transport http \
  http://localhost:8000/mcp
```

5. 使用，
> 北京今天天气怎么样
> Shanghai weather forecast
> 伦敦未来三天天气

> ⚠️ 不能在项目目录下使用


#### MCP(Model Context Protocol) 三种Transport方式
[MCP自身协议](https://modelcontextprotocol.io/docs/getting-started/intro)



##### stdio（标准输入输出）
```
Claude Code
    ↓ 写入 stdin
你的 main.py 子进程
    ↓ 写入 stdout
Claude Code
```

- Server 就是 Claude Code 启动的一个子进程
- 消息通过进程的标准输入输出传递
- Claude Code 退出，Server 也跟着退出
- 只能本地用，不能跨网络
- 适合：个人本地工具，开发调试

##### sse（Server-Sent Events）
```
Claude Code
    ↓ HTTP POST 发请求
远程 Server
    ↓ HTTP 长连接推送响应（SSE）
Claude Code
```

- 基于 HTTP，Server 独立运行
- 连接是单向推送：Server 主动往 Client 推消息
- 这是 MCP 早期的远程方案，现在已经是旧方案
- 适合：需要兼容老版本客户端的场景

##### http（Streamable HTTP）

```
Claude Code
    ↓ HTTP POST
远程 Server
    ↓ HTTP 响应（支持流式）
Claude Code
```

- 同样基于 HTTP，Server 独立运行
- 比 SSE 更现代，双向通信，支持流式返回
- 这是目前官方推荐的远程方案
- 适合：生产环境，部署到服务器，多人共用

#### MCP的作用域
Claude Code 的 MCP 配置有作用域的概念。

- local（默认）,只在当前目录下生效
- project, 整个项目目录下生效
- user, 任意目录都生效

注册mcp的时候指定一下scope就行了
```shell
claude mcp add notes-server \
  --scope user \
  -- uv --directory /home/poul/workspace/software/llm_mcp/notes-server run main.py
```

### Function Call


### Tools


### Skills

这个是Claude特有的功能，专门为Claude准备的操作手册，不是MCP，也不是给你用的功能。
当需要LLM做什么复杂任务("生成一个 PPT"、"创建 Word 文档")的时候,我会先去读对应的`skill.md`,里面记录了经过大量试错总结出来的最佳操作步骤--用哪个库、怎么排版、踩过哪些坑--让我能生成更高质量的输出

比如：
你说"帮我写个 Word 文档" → LLM先读 `/mnt/skills/public/docx/SKILL.md` → 按最佳实践生成

### Hooks

#### claude code支持的hook锚点：
##### 工具执行相关
| 事件 | 触发时机 | Matcher 过滤字段 | 示例值 |
|------|---------|----------------|--------|
| `PreToolUse` | 工具调用执行之前，可拦截阻止 | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `PostToolUse` | 工具调用成功之后 | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `PostToolUseFailure` | 工具调用失败之后 | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `PermissionRequest` | 权限确认框弹出时 | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |

##### 会话生命周期
| 事件 | 触发时机 | Matcher 过滤字段 | 示例值 |
|------|---------|----------------|--------|
| `SessionStart` | 会话开始或恢复时 | how the session started | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | 会话终止时 | why the session ended | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `UserPromptSubmit` | 你提交 prompt 后、Claude 处理之前 | 无 matcher | 每次触发 |
| `Stop` | Claude 完成一轮回复时 | 无 matcher | 每次触发 |
| `StopFailure` | 因 API 错误导致本轮结束时，输出和退出码均被忽略 | error type | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `CwdChanged` | 工作目录变更时，例如 Claude 执行了 `cd` 命令，可配合 direnv 做响应式环境管理 | 无 matcher | 每次触发 |

##### 子 Agent 相关
| 事件 | 触发时机 | Matcher 过滤字段 | 示例值 |
|------|---------|----------------|--------|
| `SubagentStart` | 子 agent 被启动时 | agent type | `Bash`, `Explore`, `Plan`，或自定义 agent 名 |
| `SubagentStop` | 子 agent 完成时 | agent type | 同 `SubagentStart` |
| `TeammateIdle` | agent team 中某个协作成员即将进入空闲时 | 无 matcher | 每次触发 |
| `TaskCreated` | 通过 `TaskCreate` 创建任务时 | 无 matcher | 每次触发 |
| `TaskCompleted` | 任务被标记为完成时 | 无 matcher | 每次触发 |

##### 通知与权限
| 事件 | 触发时机 | Matcher 过滤字段 | 示例值 |
|------|---------|----------------|--------|
| `Notification` | Claude Code 发出通知时 | notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `Elicitation` | MCP server 在工具调用过程中请求用户输入时 | MCP server name | 你配置的 MCP server 名称 |
| `ElicitationResult` | 用户响应 MCP elicitation 后、结果回传给 server 之前 | MCP server name | 同 `Elicitation` |

##### 上下文压缩
| 事件 | 触发时机 | Matcher 过滤字段 | 示例值 |
|------|---------|----------------|--------|
| `PreCompact` | 上下文压缩开始之前 | what triggered compaction | `manual`, `auto` |
| `PostCompact` | 上下文压缩完成之后 | what triggered compaction | `manual`, `auto` |

##### 配置与文件
| 事件 | 触发时机 | Matcher 过滤字段 | 示例值 |
|------|---------|----------------|--------|
| `ConfigChange` | 会话期间配置文件发生变更时 | configuration source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `InstructionsLoaded` | `CLAUDE.md` 或 `.claude/rules/*.md` 被加载进上下文时，包括会话启动和懒加载 | load reason | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |
| `FileChanged` | 被监听的文件在磁盘上发生变化时，由 matcher 指定监听哪些文件名 | filename (basename) | `.envrc`, `.env`，任意你想监听的文件名 |

##### Worktree
| 事件 | 触发时机 | Matcher 过滤字段 | 示例值 |
|------|---------|----------------|--------|
| `WorktreeCreate` | 通过 `--worktree` 或 `isolation: "worktree"` 创建 worktree 时，会替代默认 git 行为 | 无 matcher | 每次触发 |
| `WorktreeRemove` | Worktree 被移除时，包括会话退出或子 agent 完成时 | 无 matcher | 每次触发 |



#### Hook 执行类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `command` | 执行 shell 命令，通过 stdin 接收事件 JSON，通过退出码和 stdout 返回结果 | 最常用，发通知、格式化代码、日志记录等 |
| `http` | 将事件数据 POST 到 HTTP endpoint，返回格式与 command 相同 | 有独立服务处理 hook 逻辑时，如团队共享审计服务 |
| `prompt` | 将 hook 输入和你的 prompt 发给 Claude 模型（默认 Haiku）做单次判断，返回 `ok: true/false` + `reason` | 需要主观判断而非确定性规则时，如判断操作是否合规；`ok: false` 时 reason 会反馈给 Claude 让它调整 |
| `agent` | 启动一个子 agent，可读文件、搜索代码、执行命令，最多 50 次工具调用，默认超时 60 秒 | 需要检查代码库实际状态时，如验证测试是否通过再允许 Claude 停止 |


### Plugins



### System Prompt

### RAG/知识库

### Memory Harnesses

## 分类

## 提示词


如何写好大模型的提示词

[langchain](https://python.langchain.com/docs/introduction/)

## 微调

### SFT微调
Supervised Fine-Tuning，监督微调


## 论文

下面列出了一些**重要的 LLM（大型语言模型）相关论文及访问地址**，涵盖基础理论、能力研究、安全性、对齐等多个方面：

---

### 📘 基础与核心组件

* **“Attention Is All You Need”**：Transformer 架构的开创性论文，是 LLM 的技术基础。阅读维基百科可快速了解其核心思想与影响 ([blog.csdn.net][1])。
* **“Emergent Abilities of Large Language Models”** (Jason Wei 等, 2022)：首次分析规模扩展带来的“不可预测的新能力”。论文可在 arXiv 查阅 ([arxiv.org][2])。
* **“Understanding the Capabilities, Limitations, and Societal Impact of Large Language Models”** (Tamkin 等, 2021)：对 GPT‑3 的能力与社会影响进行了系统评估 ([arxiv.org][3])。

---

### 📚 综合性综述与调查

* **“A Survey of Large Language Models”** (Zhao et al., 2023)：涵盖预训练、微调、使用方式及评估方式，附资源列表 ([arxiv.org][4])。
* **“Large Language Models: A Survey”** (Minaee et al., 2024)：对 GPT、LLaMA、PaLM 等模型做横向比较，探讨挑战与未来方向，可在 arXiv 下载 PDF ([arxiv.org][5])。
* **“A Comprehensive Overview of Large Language Models”** (2023)：以长文 PDF 形式介绍体系结构、训练策略、推理效率等 ([arxiv.org][6])。
* **“Large Language Models: A Comprehensive Survey … Applications, Challenges …”** (Usman Hadi et al., 2023)：收录应用、局限与未来展望，并提供 GitHub 链接 ([researchgate.net][7])。

---

### 🔒 安全、隐私与对齐

* **“On Large Language Models’ Resilience to Coercive Interrogation”** (Purdue, 2023)：揭示当攻击者能获取 top‑k 概率时的安全漏洞 ([cs.purdue.edu][8])。
* **“Extracting Training Data from Large Language Models”** (Carlini 等, 2021)：展示从 LLM 中提取训练数据的安全风险 ([usenix.org][9])。
* **“DistillSeq: A Framework for Safety Alignment Testing in LLMs via Knowledge Distillation”** (ShanghaiTech, ISSTA 2024)：提出有效测试 LLM 安全对齐的新方法 ([sist.shanghaitech.edu.cn][10])。

---

### 🔍 上下文与长文理解

* **“Lost in the Middle: How Language Models Use Long Contexts”** (Liu et al., 2023)：研究 LLM 在超长上下文中的理解能力 ([cs.stanford.edu][11])。

---

### 🌐 最新模型与技术发展

* **DeepSeek-V3 / DeepSeek-R1**（2024–2025）：开源中文大模型，性能多项对标 GPT‑4，但训练成本低 ([zh.wikipedia.org][12])。
* **盘古‑Σ（Pangu‑Σ）**（2023）：华为研发的 1 T 参数稀疏模型，支持中英双语与代码任务 ([zh.wikipedia.org][13])。

---

### 🔗 资源入口汇总

* **CSDN博客**整合 RAG 等相关技术论文与资源链接 ([blog.csdn.net][1])；
* **GitHub “Awesome‑LLM”**：一个持续更新的大语言模型论文与工具资源合集 ([github.com][14])；
* **知乎专栏**：\[2025.03–04] 选出 10 篇最新 LLM 研究进展，可直接阅读全文 ([zhuanlan.zhihu.com][15])。

---

### 🗂 表格概览

| 方向          | 论文/资源                                          | 链接           |
| ----------- | ---------------------------------------------- | ------------ |
| 基础架构        | Attention Is All You Need                      | Wiki 页面      |
| Emergent 能力 | Emergent Abilities of LLMs (2022)              | arXiv        |
| 综合综述        | Surveys (Zhao et al. 2023; Minaee et al. 2024) | arXiv        |
| 安全对齐        | DistillSeq (ISSTA 2024)                        | ShanghaiTech |
| 长上下文        | Lost in the Middle (2023)                      | arXiv        |
| 最新 LLMs     | DeepSeek‑V3/R1, Pangu‑Σ                        | Wiki 算法模型概览  |

---

如你需要**具体论文的 PDF 下载地址™**，或某篇论文的**中文摘要、解析与应用案例**，欢迎告诉我，我可以继续帮你深入挖掘！

[1]: https://blog.csdn.net/weixin_44885180/article/details/140368817?utm_source=chatgpt.com "大模型论文、github地址汇总原创 - CSDN博客"
[2]: https://arxiv.org/abs/2206.07682?utm_source=chatgpt.com "Emergent Abilities of Large Language Models"
[3]: https://arxiv.org/abs/2102.02503?utm_source=chatgpt.com "Understanding the Capabilities, Limitations, and Societal Impact of Large Language Models"
[4]: https://arxiv.org/abs/2303.18223?utm_source=chatgpt.com "A Survey of Large Language Models"
[5]: https://arxiv.org/abs/2402.06196?utm_source=chatgpt.com "Large Language Models: A Survey"
[6]: https://arxiv.org/pdf/2307.06435?utm_source=chatgpt.com "[PDF] A Comprehensive Overview of Large Language Models - arXiv"
[7]: https://www.researchgate.net/publication/372258530_Large_Language_Models_A_Comprehensive_Survey_of_its_Applications_Challenges_Limitations_and_Future_Prospects?utm_source=chatgpt.com "(PDF) Large Language Models: A Comprehensive Survey of its ..."
[8]: https://www.cs.purdue.edu/homes/cheng535/static/papers/sp24_lint.pdf?utm_source=chatgpt.com "[PDF] On Large Language Models' Resilience to Coercive Interrogation"
[9]: https://www.usenix.org/system/files/sec21-carlini-extracting.pdf?utm_source=chatgpt.com "[PDF] Extracting Training Data from Large Language Models - USENIX"
[10]: https://sist.shanghaitech.edu.cn/2025/0320/c2858a1108422/page.htm?utm_source=chatgpt.com "科研进展| 信息学院系统与安全中心在大语言模型（LLMs）研究方面 ..."
[11]: https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf?utm_source=chatgpt.com "[PDF] Lost in the Middle: How Language Models Use Long Contexts"
[12]: https://zh.wikipedia.org/wiki/DeepSeek-V3?utm_source=chatgpt.com "DeepSeek-V3"
[13]: https://zh.wikipedia.org/wiki/%E7%9B%98%E5%8F%A4%E5%A4%A7%E6%A8%A1%E5%9E%8B?utm_source=chatgpt.com "盘古大模型"
[14]: https://github.com/Hannibal046/Awesome-LLM?utm_source=chatgpt.com "Awesome-LLM: a curated list of Large Language Model - GitHub"
[15]: https://zhuanlan.zhihu.com/p/1891444022985340495?utm_source=chatgpt.com "论文分享| 大语言模型最新进展 - 知乎专栏"


## 榜单

https://onyx.app/open-llm-leaderboard
https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/
https://artificialanalysis.ai/



# EOF