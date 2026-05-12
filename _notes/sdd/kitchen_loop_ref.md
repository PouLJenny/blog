# KitchenLoop 本地操作手册

> **目标读者**:已经安装好 Linux/macOS 开发环境的工程师
> **示例项目**:`mindful` —— 一个简单的命令行冥想 app
> **预计耗时**:首次跑通约 60–90 分钟,其中 30 分钟在等 Claude Code 跑

---

## 0. 心智模型(读完再开始)

KitchenLoop 不是一个"工具",是一套**让 Claude Code 反复跑你项目的脚手架**。它的核心是:

```
你写好 spec  →  Claude Code 模拟用户跑你的产品  →
发现 friction  →  自动开 ticket  →  自动写代码  →
多模型 review  →  自动 merge  →  跑回归  →  循环
```

**真正在干活的是 Claude Code(命令行版的 Claude)**。KitchenLoop 提供的是:

- 6 个 markdown 写的 skill(告诉 Claude 每个阶段干什么)
- 1 个 bash 编排器(`kitchenloop.sh`)负责把 6 阶段串起来,管 git worktree、PR 状态、stop 条件
- 1 个 Python 多模型辩论引擎(`discuss.py`)
- 一份 YAML 配置 + 一份你写的 spec 文档

**你 90% 的工作是写好 spec**,剩下 10% 是配置 + 监控。

---

## 1. 前置环境检查清单

按顺序检查,每一项都要 ✅ 才能进入下一节。

### 1.1 系统要求

- Linux(你有 Manjaro,完美)或 macOS
- 至少 8GB 可用磁盘(Claude Code 会缓存,worktree 会膨胀)
- 稳定的科学上网(Claude API + GitHub + 包管理器)

### 1.2 必需工具

```bash
# 一键自检
for cmd in claude git gh jq yq python3 node; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf "✅ %-8s %s\n" "$cmd" "$(command -v "$cmd")"
  else
    printf "❌ %-8s MISSING\n" "$cmd"
  fi
done
```

如果有缺失,在 Manjaro 上安装:

```bash
# 系统包
sudo pacman -S git jq nodejs npm python python-pip

# yq(YAML 处理器,Manjaro AUR 或 Go install)
sudo pacman -S yq
# 或: go install github.com/mikefarah/yq/v4@latest

# GitHub CLI
sudo pacman -S github-cli

# Claude Code(关键 —— 整个 KitchenLoop 都是它在跑)
npm install -g @anthropic-ai/claude-code
```

### 1.3 Claude Code 登录

```bash
claude --version           # 应该返回 v2.1.x 或更高
claude /login              # 打开浏览器走 OAuth
claude -p "say hello"      # 测试可以正常调用
```

如果 `-p` 返回空字符串(已知 bug),用 stream 模式测试:

```bash
echo "say hello" | claude --print --output-format stream-json | head -5
```

### 1.4 GitHub CLI 登录(必需,KitchenLoop 用 issues 做 ticket 系统)

```bash
gh auth login              # 选 HTTPS + browser 登录
gh auth status             # 应该显示 Logged in
```

### 1.5 可选但强烈建议:Codex / Gemini CLI(多模型 review)

KitchenLoop 在 polish 阶段做"多模型辩论",**只装 Claude 也能跑**,但启用 codex 后 review 质量明显提升。

```bash
# Codex CLI(OpenAI 出的)
npm install -g @openai/codex
codex auth login

# Gemini CLI(可选,Discussion Manager 用)
npm install -g @google/gemini-cli
gemini auth login
```

如果不装,在 `kitchenloop.yaml` 里把对应 reviewer 设成 `enabled: false` 即可。

---

## 2. 拉 KitchenLoop 源码

不要把 KitchenLoop 的源码塞进你的项目。它是**框架**,放独立目录,用环境变量引用。

```bash
mkdir -p ~/tools && cd ~/tools
git clone https://github.com/0xagentkitchen/kitchenloop.git
cd kitchenloop

# 设环境变量(加到 ~/.bashrc 或 ~/.zshrc 永久生效)
export KITCHENLOOP_HOME=~/tools/kitchenloop
echo 'export KITCHENLOOP_HOME=~/tools/kitchenloop' >> ~/.bashrc
```

验证:

```bash
ls "$KITCHENLOOP_HOME/scripts/kitchenloop-init.sh"
# 应该返回路径,不是 No such file
```

---

## 3. 创建示例项目 `mindful`

我们要建一个**几乎空的 Python CLI 项目**,让 KitchenLoop 从零把它喂大。

### 3.1 初始化项目骨架

```bash
mkdir -p ~/code/mindful && cd ~/code/mindful
git init
git branch -M main

# 最小 Python 项目结构
mkdir -p src/mindful tests/smoke docs scenarios/incubating
touch src/mindful/__init__.py

# pyproject.toml(让 mindful 命令可以被安装)
cat > pyproject.toml <<'EOF'
[project]
name = "mindful"
version = "0.0.1"
description = "A mindful meditation companion CLI"
requires-python = ">=3.10"
dependencies = []

[project.scripts]
mindful = "mindful.cli:main"

[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 100
EOF

# 先写一个**会失败**的入口(让第一次 ideate 真的失败,这是设计)
cat > src/mindful/cli.py <<'EOF'
def main():
    raise NotImplementedError("mindful CLI not built yet — KitchenLoop will fill this in")
EOF

# 安装到当前 venv
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest ruff
mindful 2>&1 || true   # 应该报 NotImplementedError —— 这是预期
```

### 3.2 写 README(spec 的入口文档)

```bash
cat > README.md <<'EOF'
# mindful

A command-line meditation companion. Single-user, local-only, no network.
All data stored in `~/.mindful/` as JSON files.

## Commands (intended)

- `mindful start --duration N --mode M` — start a meditation session
- `mindful note "text"` — annotate the most recent session
- `mindful stats` — show streak, total minutes, completion rate
- `mindful history --last N` — list recent sessions
- `mindful config --bell-sound X` — adjust preferences

See `docs/spec.md` for full specification.
EOF
```

### 3.3 写 spec 主文档(这是你作为人最重要的产出)

```bash
cat > docs/spec.md <<'EOF'
# mindful — Product Specification

## What This Is

A command-line meditation companion. Single-user, local-only, no network.
Stores all data in `~/.mindful/` as JSON files.

## Core Entities

- **Session**: One sit. Has duration, mode, start_time, end_time, status, optional note.
- **Streak**: Consecutive days with at least one completed session.
- **Config**: User preferences (bell sound, default duration, voice gender).

## Commands

### `mindful start`

**User view**: `mindful start --duration 10 --mode breath_pacing` shows a
countdown, plays guidance, and on completion records the session.

**Preconditions**:
- `~/.mindful/` writable (auto-created on first run)
- duration is 1–120 minutes
- mode is one of: bell_only, voice_guide, breath_pacing

**Expected behavior**:
- Creates session record with status=in_progress
- Plays guidance per mode
- On completion, marks status=completed, updates streak
- Returns session_id (printed to stdout)

**Failure modes the product claims to handle**:
- Ctrl+C mid-session → save with status=interrupted, do NOT count toward streak
- duration > 120 → exit code 1, clear error message
- ~/.mindful/ not writable → exit code 3, name the directory and OS error
- Concurrent start (another in_progress exists) → reject, suggest resume/abort

**Ground truth (for unbeatable test)**:
- `~/.mindful/sessions.json` has +1 entry
- New entry has status="completed" or "interrupted"
- If completed: `~/.mindful/streak.json` updated correctly

---

### `mindful note`

**User view**: `mindful note "felt calm"` attaches text to the most recent
**completed** session.

**Preconditions**:
- At least one completed session exists
- Note is 1–500 chars

**Failure modes**:
- No prior session → error "no session to annotate"
- Note > 500 chars → reject with current count
- Note already exists → ask to overwrite, or `--force` to override
- Empty note → reject

**Ground truth**:
- `sessions.json` last completed entry has `note` field set

---

### `mindful stats`

**User view**: Prints current_streak, longest_streak, total_minutes,
avg_minutes, completion_rate_30d as a table.

**Preconditions**: None — works with zero sessions, returns zeros.

**Failure modes**:
- `sessions.json` corrupt → recover what's parseable, warn to stderr
- Timezone change between sessions → use UTC internally

**Ground truth**:
- stdout contains all 5 numeric metrics
- For corrupt data: warning to stderr, partial stats to stdout, exit 0

---

### `mindful history` (abbreviated — same pattern)

### `mindful config` (abbreviated — same pattern)

## Non-Goals (explicit)

- No cloud sync, accounts, social features
- No reminders/notifications
- mode/duration N/A to note/stats/config/history (see spec.blocked)

## Cross-cutting Constraints

- All times stored as UTC ISO8601
- All file writes are atomic (temp file + rename)
- Exit codes: 0=success, 1=user error, 2=data error, 3=system error
EOF
```

### 3.4 首次提交

```bash
git add .
git commit -m "Initial mindful project skeleton with spec"
```

### 3.5 推到 GitHub(KitchenLoop 用 GitHub issues 做 ticket 系统)

```bash
gh repo create mindful --public --source=. --remote=origin --push
# 如果已有 repo,改成: git remote add origin <url> && git push -u origin main
```

---

## 4. 在项目里安装 KitchenLoop

```bash
cd ~/code/mindful
"$KITCHENLOOP_HOME/scripts/kitchenloop-init.sh"
```

脚本会:

1. 检查前置工具(同 §1.2)
2. 交互式问你:project name、language、subject domain
3. 拷贝 `kitchenloop.example.yaml` → `kitchenloop.yaml`
4. 拷贝 6 个 skill 到 `.claude/skills/`(Claude Code 会自动发现)
5. 拷贝 orchestrator 脚本到 `scripts/kitchenloop/`
6. 创建空的状态文件(`.kitchenloop/`、`docs/internal/`)

完成后 `git status` 会看到一堆新增文件,先**不要 commit**,我们先调整配置。

---

## 5. 配置 `kitchenloop.yaml`(关键步骤)

打开 `~/code/mindful/kitchenloop.yaml`,修改以下字段。其他字段保留默认。

### 5.1 项目元信息

```yaml
project:
  name: "mindful"
  description: "A command-line meditation companion — sessions, journal, streaks"
  language: "python"
```

### 5.2 spec 块(这是核心)

```yaml
spec:
  docs:
    - "README.md"
    - "docs/spec.md"

  dimensions:
    subcommands:
      - "start"
      - "note"
      - "stats"
      - "history"
      - "config"

    duration:
      - "1min"
      - "10min"
      - "30min"
      - "custom"

    mode:
      - "bell_only"
      - "voice_guide"
      - "breath_pacing"

    state_condition:
      - "first_ever_session"
      - "active_streak"
      - "broken_streak"
      - "interrupted_session"
      - "data_corrupt"

  blocked:
    - subcommands: "note"
      mode: "*"
    - subcommands: "config"
      duration: "*"
    - subcommands: "stats"
      mode: "*"
    - subcommands: "history"
      mode: "*"
```

**矩阵规模**:5 × 4 × 3 × 5 = 300 个原始组合,减去 blocked 后约 180 个有效场景。这就是论文说的 spec surface coverage matrix。

### 5.3 verification 块(unbeatable test 的接入点)

```yaml
verification:
  oracle:
    type: "deterministic"
    full_command: "pytest"
    quick_command: "pytest tests/smoke/ -x"
    smoke_command: ""    # 第一次跑先留空,让 KitchenLoop 自己生成
    lint_command: "ruff check ."
    security_command: ""
    build_command: ""

  stop_conditions:
    pass_rate_floor: 0.80         # 试运行可以宽松些,跑稳后改 0.95
    max_consecutive_failures: 3
```

**重要**:`smoke_command` 第一次先留空。KitchenLoop 看到空会主动在第一个 iteration 把"创建一个真正的端到端 smoke test"作为最高优先级任务。这是它**自举**自己的验证基础设施。

### 5.4 reviewers 块(按你装了什么调整)

```yaml
reviewers:
  codex:
    enabled: true       # 装了就开
    timeout: 30
  gemini:
    enabled: false      # 没装就关
    timeout: 60
```

### 5.5 runtime 块(本地试跑用,降低成本)

```yaml
runtime:
  timeouts:
    ideate: 1800        # 30 min(默认 45 min)
    triage: 600         # 10 min
    execute: 2400       # 40 min
    polish: 3600        # 60 min
    regress: 3600
    backlog: 600
  backlog_interval: 3
  review_interval: 5
  polish_max_prs: 1     # 试跑期间一次只处理 1 个 PR,容易观察
```

---

## 6. 第一次"干跑"(只 ideate,不写代码)

跑全流程之前,先用最便宜的方式验证配置正确。**只跑 ideate 阶段,不进 execute**。

```bash
cd ~/code/mindful
./scripts/kitchenloop/kitchenloop.sh 1 --only ideate
```

预期看到:

```
[KitchenLoop v1.0.0] Starting iteration 1
[Phase: ideate] Reading spec from docs/spec.md...
[Phase: ideate] Enumerating dimensions: 300 combos, 180 unblocked
[Phase: ideate] Selected: subcommand=start, duration=1min, mode=breath_pacing
                Tier: T1 (foundation, single feature happy path)
[Phase: ideate] Codex feasibility check: PROCEED
[Phase: ideate] Implementing scenario in scenarios/incubating/...
[Phase: ideate] Running lint... PASS
[Phase: ideate] Running quick tests... FAIL (mindful command raises NotImplementedError)
[Phase: ideate] Writing experience report to docs/internal/reports/experience-report-iter-1.md
[Phase: ideate] DONE
```

**第一次 ideate "失败"是预期行为** —— 因为 mindful 没实现。但 friction log 被写出来了,这就是产物。

去看一眼:

```bash
cat docs/internal/reports/experience-report-iter-1.md
```

你会看到一个完整的 markdown 报告,列出了 5–10 个 friction items(类似"mindful 命令不可用"、"~/.mindful/ 没创建"、"session 模式未定义"...)

如果这一步成功了,**你的配置就对了**,可以进下一节。

如果失败,常见问题在 §10 排查清单。

---

## 7. 跑第一个完整 iteration

```bash
cd ~/code/mindful
./scripts/kitchenloop/kitchenloop.sh 1
```

这会跑完六个阶段。预计耗时:

| 阶段 | 耗时 | 干什么 |
|---|---|---|
| backlog | ~3 min | (首次跑会先做一次 backlog grooming) |
| ideate | ~10 min | 模拟用户,写 scenario,跑测试 |
| triage | ~3 min | friction → GitHub issues |
| execute | ~15 min | 选 1–3 个 ticket,写代码,开 PR |
| polish | ~10 min | 多模型 review,自动 merge |
| regress | ~5 min | 跑回归,更新 drift |

**全程不要插手**。如果你的 terminal 看起来卡住了,Claude Code 在思考。

跑完后检查:

```bash
# 看创建了哪些 ticket
gh issue list --label "kitchenloop:done"

# 看 merge 了哪些 PR
gh pr list --state merged

# 看 loop state
cat docs/internal/loop-state.md

# 看代码长出了什么
git log --oneline -20
```

**iter 1 通常会**:

1. 创建 5–10 个 issue(对应 friction items)
2. merge 1–3 个 PR(实现最优先的 ticket,通常是 CLI 入口和 ~/.mindful/ bootstrap)
3. 你的 `mindful --help` 应该开始能跑了

---

## 8. 跑 5–10 个 iteration 看产品长出来

```bash
./scripts/kitchenloop/kitchenloop.sh 10
```

挂着不管,泡杯茶。预计 2–3 小时。

**前 3 个 iteration**:实现核心 CLI 框架和文件存储。
**iter 4–6**:实现 start 命令(模拟时长、写 session 记录)。
**iter 7–10**:实现 note/stats/history,开始进入 T2 组合场景,会发现真正的 bug(比如 streak 跨夜计算、并发 session 检测)。

**第 10 个 iteration 后,你应该有一个真的能用的 mindful CLI**:

```bash
mindful start --duration 1 --mode breath_pacing
mindful note "first test session"
mindful stats
```

---

## 9. 监控与调试

### 9.1 日常查看

```bash
# 当前迭代状态
cat .kitchenloop/state/current-iteration.txt

# drift 指标趋势
cat .kitchenloop/metrics.json | jq '.iterations[-5:]'

# 实时日志
tail -f .kitchenloop/logs/iter-$(cat .kitchenloop/state/current-iteration.txt).log
```

### 9.2 暂停 / 恢复

```bash
# 优雅暂停(等当前阶段跑完)
touch .kitchenloop/PAUSE

# 强制中断
pkill -f "kitchenloop.sh"
rm -rf .kitchenloop/kitchenloop.lock

# 恢复
rm .kitchenloop/PAUSE
./scripts/kitchenloop/kitchenloop.sh 5    # 接着跑 5 轮
```

### 9.3 单阶段重跑(调试用)

```bash
./scripts/kitchenloop/kitchenloop.sh 1 --only ideate     # 只跑 ideate
./scripts/kitchenloop/kitchenloop.sh 1 --only execute    # 只 execute(用现有 ticket)
./scripts/kitchenloop/kitchenloop.sh 1 --skip ideate,triage  # 跳过前两阶段
```

### 9.4 模式切换

```bash
# 只刷 ideate,把 backlog 喂胖(不写代码)
./scripts/kitchenloop/kitchenloop.sh 20 --mode user-only

# 只消化 backlog,不再 ideate(适合 backlog 已经多到吓人时)
./scripts/kitchenloop/kitchenloop.sh 10 --mode dev-only
```

---

## 10. 排查清单

| 症状 | 原因 | 修复 |
|---|---|---|
| `claude: command not found` | Claude Code 未安装 | `npm install -g @anthropic-ai/claude-code` |
| `claude` 调用返回空 | CLI v2.1.83+ `--print` 已知 bug | KitchenLoop 已经用 stream-json 绕开,确保用脚本调用而非手测 |
| `gh: not authenticated` | 没登录 | `gh auth login` |
| ideate 阶段 timeout | 30min 不够 | 调高 `runtime.timeouts.ideate` 到 3600 |
| Codex feasibility 总是 REJECT | spec 不清楚 | 回去补 docs/spec.md,把每个 capability 的 user view 写细 |
| execute 创建的 PR CI 一直挂 | smoke_command 配置错误 | 看 PR 的 Actions 日志,通常是路径问题 |
| `kitchenloop.lock` 已存在但没进程 | 上次崩了没清锁 | `rm -rf .kitchenloop/kitchenloop.lock` |
| 同一个 ticket 反复被 triage 创建 | 去重失效 | 检查 GitHub issue title 是否一致;改 ticketing.github.labels |
| 跑出来的代码完全偏离你的设计 | spec 不够具体 | 这是最常见问题 —— 回到 docs/spec.md,加更多"Failure modes"和"Ground truth" |

---

## 11. 成本预估(本地试跑)

KitchenLoop 跑一轮的 token 消耗主要在 Claude Code:

| 阶段 | 单轮 input tokens | 单轮 output tokens |
|---|---|---|
| ideate | ~15K | ~8K |
| triage | ~5K | ~3K |
| execute | ~30K | ~15K |
| polish | ~20K | ~5K |
| regress | ~10K | ~3K |
| **合计** | **~80K** | **~34K** |

按 Claude Sonnet 价格,**1 个 iteration 大约 $0.5–1.5**。
跑 10 个 iter 把 mindful 拉起来,**总成本约 $5–15**。

如果你用 Claude Pro/Max 订阅(包含 Claude Code 用量),没有额外费用,但有 5 小时窗口的 token 上限,跑 10 iter 可能跨多个窗口。

---

## 12. 跑完之后:迁移到 sif skill 平台

mindful 这个练手项目跑通后,迁移到你的 sif skill 平台只要改三件事:

1. **`spec.dimensions`**:替换为 sif 真实维度
   ```yaml
   features: [skill_install, skill_invoke, skill_uninstall, skill_version_switch, quota_management, translation_fallback, session_resume, sse_reconnect]
   actor_type: [end_user, skill_developer, workspace_admin]
   invocation_mode: [rest_sync, sse_stream]
   quota_state: [normal, near_limit, exhausted]
   ```

2. **`spec.docs`**:换成 sif skill 平台的 spec 文档(我之前对话给过完整模板)

3. **`smoke_command`**:这是最关键的改动。mindful 用 `pytest` 已经够了,sif 需要真的起 PG/Redis/OSS 容器跑端到端:
   ```yaml
   smoke_command: "docker compose -f docker-compose.test.yml run --rm smoke ./tests/integration/skill-e2e.sh"
   ```

   这个 smoke test 必须能验证 sessions/usage_records/quotas 三张表的真实状态变化(state delta),才是真正的 unbeatable test。

---

## 13. 每天的工作流(稳态后)

跑稳之后,你的日常长这样:

**早上(10 分钟)**:
```bash
cd ~/code/mindful
gh pr list                         # 看昨晚 KitchenLoop 自动 merge 了什么
cat .kitchenloop/metrics.json | jq '.iterations[-5:]'   # drift 看下
git log --oneline --since=yesterday
```

**有空时(20 分钟)**:挑 1–2 个 friction items 自己审一下,看 KitchenLoop 创建的 issue 描述是否准确,如果不准确说明 spec 要改。

**周一上午(60 分钟)**:**spec review meeting**(纯人,不带 KitchenLoop)。决定下周要新增/修改哪些 capability claim,改 docs/spec.md,push。

**晚上 / 周末**:
```bash
./scripts/kitchenloop/kitchenloop.sh 10    # 让它挂着跑
```

---

## 附录 A:文件结构对照

跑通之后你的项目长这样:

```
mindful/
├── README.md                           ← 你写的
├── docs/
│   ├── spec.md                         ← 你写的(核心)
│   └── internal/
│       ├── loop-state.md               ← KitchenLoop 维护
│       └── reports/
│           └── experience-report-iter-N.md   ← 每轮一份
├── kitchenloop.yaml                    ← 你配置的
├── pyproject.toml                      ← 你写的
├── scenarios/
│   └── incubating/
│       └── start-1min-breath-first/    ← agent 写的 scenario
├── scripts/
│   ├── kitchenloop/                    ← init 脚本拷进来的
│   ├── pr-manager/                     ← 同上
│   └── ai-discussion/                  ← 同上
├── src/
│   └── mindful/                        ← 这里的代码 95% 是 KitchenLoop 写的
├── tests/
│   ├── smoke/                          ← KitchenLoop 自举出来的
│   └── integration/
│       └── cli-smoke.sh                ← unbeatable test
├── .claude/
│   └── skills/                         ← 6 个 KitchenLoop skill
└── .kitchenloop/
    ├── metrics.json                    ← drift 指标
    ├── coverage-matrix.yaml            ← spec 覆盖矩阵
    ├── logs/                           ← 每次迭代的日志
    └── state/                          ← 状态机
```

---

## 附录 B:关键命令速查

```bash
# 初始化(一次性)
"$KITCHENLOOP_HOME/scripts/kitchenloop-init.sh"

# 跑 N 轮
./scripts/kitchenloop/kitchenloop.sh N

# 只跑某阶段
./scripts/kitchenloop/kitchenloop.sh 1 --only ideate

# 跳过某阶段
./scripts/kitchenloop/kitchenloop.sh 5 --skip polish

# 模式切换
./scripts/kitchenloop/kitchenloop.sh 10 --mode user-only   # 只灌 backlog
./scripts/kitchenloop/kitchenloop.sh 10 --mode dev-only    # 只消化 backlog

# 暂停 / 恢复
touch .kitchenloop/PAUSE
rm .kitchenloop/PAUSE

# 看状态
cat .kitchenloop/state/current-iteration.txt
cat docs/internal/loop-state.md
gh issue list --label "kitchenloop:todo"
gh pr list

# 启动 Discussion Manager(架构辩论)
python scripts/ai-discussion/discuss.py "Should we use SQLite or PostgreSQL?" --max-rounds 3
```

---

## 附录 C:什么时候应该停下来 / 介入

**停下来检查的信号**:

- 连续 3 个 iter 的 friction log 都是同一类问题 → spec 太抽象,需要重写
- pass_rate 跌破 0.8 → 通常是 spec 和实现已经矛盾了
- 同一个 ticket 反复被创建 → triage 去重逻辑挂了或 issue title 不稳定
- 连续 3 个 iter 都没有新 ticket(starvation) → spec 覆盖率到顶了,需要扩 spec

**人介入的时机**(按优先级):

1. **每周改一次 spec**(高杠杆) —— 你作为产品负责人最重要的活
2. **看 Discussion Manager 输出的 ratification report**(中杠杆) —— 不要参与辩论,只看结论和分歧点
3. **看 drift metrics 报警**(中杠杆) —— 通常意味着 spec 演化了但 oracle 没跟上
4. **review 自动 merge 的 PR**(低杠杆) —— 抽样,别每个都看,否则你被它榨干

记住核心原则:**人在 spec 层面用力,不在代码层面用力**。这就是 KitchenLoop 的全部意义。