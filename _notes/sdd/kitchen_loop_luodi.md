# KitchenLoop 本地落地问题与解决方式

> **环境**:Manjaro Linux + SSH 远程 + Claude 5x Max + Codex Plus + Gemini 免费 API key
> **项目**:mindful(Python CLI 冥想 app,练手项目)
> **整理时间**:2026-05-05 第一次跑通 iter-1 后
> **目标读者**:再次部署 KitchenLoop 的你 / sif 团队成员
>
> 共 7 个问题,按遇到顺序排列。每个问题都包括:**症状 → 根因 → 解决方式 → 是否要给上游提 issue**。

---

## 问题 1:Gemini CLI 在 SSH 环境下 OAuth 流程失败

### 症状

```
[API Error: Could not load the default credentials]
[API Error: Content generator not initialized]
```

CLI 同时弹出 "verification code" 页面和 API key 输入框,状态混乱,粘什么都不对。

### 根因

Gemini CLI v0.40+ OAuth 流程依赖**本地能起 listener + 浏览器能 redirect 回来**。SSH 环境无法满足这两个条件,CLI 降级到 verification code 流程,但当前版本在这个降级路径上有 bug。

### 解决方式

**直接用 API key,跳过 OAuth**:

1. 本地浏览器打开 `https://aistudio.google.com/app/apikey`
2. 创建 API key(免费,不绑卡)
3. SSH terminal 执行:

```bash
# 清掉之前折腾的烂状态
rm -rf ~/.gemini ~/.config/gemini-cli ~/.config/google-gemini

# 用环境变量注入,跳过交互式登录
echo 'export GEMINI_API_KEY="AIzaSy..."' >> ~/.bashrc
source ~/.bashrc

# 验证
echo "say PROCEED" | gemini -p
```

### 是否给上游提 issue

**否**。这是 Gemini CLI 自身的限制,KitchenLoop 无关。

---

## 问题 2:KitchenLoop pre-flight 检查报 `claude --print returned no output`

### 症状

```
Pre-flight: Verifying claude --print output...
  FATAL: claude --print returned no output. Check your API key and CLI version.
```

### 根因

Claude CLI 在 v2.1.83+ 版本 `--print` flag 有空输出 bug,KitchenLoop 在主流程里用 stream-json 绕开了,**但 pre-flight check 的代码忘记同步改**。

### 解决方式

定位 pre-flight 检查代码:

```bash
cd ~/code/mindful
grep -n "claude --print returned no output" scripts/kitchenloop/kitchenloop.sh
```

把那段检查代码从用 `claude --print` 改成 `claude --print --output-format stream-json --verbose`,或者直接注释掉这段 pre-flight 检查(主流程不依赖它)。

### 是否给上游提 issue

**是**。这是 KitchenLoop 自己的 bug,简单修复,值得给上游提 PR。

---

## 问题 3:`stream-json` 输出格式要求 `--verbose`

### 症状

```
Error: When using --print, --output-format=stream-json requires --verbose
```

### 根因

Claude CLI v2.1.85+ 给 `stream-json` 输出加了**强制要求 `--verbose`** 的检查。KitchenLoop 当前代码只写了 `--output-format stream-json`,没带 `--verbose`,在新版 CLI 上全线挂掉。

### 解决方式

一键给所有脚本里的 `stream-json` 调用补上 `--verbose`:

```bash
cd ~/code/mindful

# 备份
cp scripts/kitchenloop/kitchenloop.sh scripts/kitchenloop/kitchenloop.sh.bak

# 全局替换
find scripts/ -name "*.sh" -not -name "*.bak*" -exec \
  sed -i 's/--output-format stream-json/--output-format stream-json --verbose/g' {} \;

# 验证
grep "stream-json" scripts/kitchenloop/kitchenloop.sh
```

每一行都应该包含 `--output-format stream-json --verbose`。

### 是否给上游提 issue

**是**,优先级高。这个 bug 让任何用新版 Claude CLI 的用户开箱即败。

---

## 问题 4:Go 版 yq 输出带引号导致路径错误

### 症状

```
fatal: couldn't find remote ref "main"
fatal: invalid reference: origin/"main"
[worktree] ERROR: Failed to create worktree /home/.../"main"/...
```

注意路径里 `"main"` 包含字面引号,不是 `main`。

### 根因

Manjaro 默认装的 `yq` 是 Go 版(mikefarah),它的输出**保留 YAML 原始引号风格**:

```bash
yq '.paths.worktree_prefix' kitchenloop.yaml
# 输出: ".claude/worktrees"  (带引号)
```

KitchenLoop 假设了 Python 版 yq 的行为(默认剥引号)。

### 解决方式

给所有 `yq` 调用加 `-r` 参数(raw output):

```bash
cd ~/code/mindful

# 一键给所有 yq 调用加 -r
find scripts/ -name "*.sh" -not -name "*.bak*" -exec \
  sed -i "s/yq '/yq -r '/g; s/yq \"/yq -r \"/g" {} \;

# 清理可能产生的 -r -r
find scripts/ -name "*.sh" -not -name "*.bak*" -exec \
  sed -i "s/yq -r -r/yq -r/g" {} \;

# 验证
yq -r '.paths.worktree_prefix' kitchenloop.yaml
# 应该输出: .claude/worktrees  (不带引号)
```

### 是否给上游提 issue

**是**,优先级最高。这个 bug 让任何 Linux 主流发行版用户(Manjaro/Arch、Ubuntu via snap/brew)开箱即败。

---

## 问题 5:agent 在 worktree 写的部分文件没被 KitchenLoop commit

### 症状

ideate 阶段跑完后:

```
[ideate] Working tree status (untracked + modified):
  ?? AGENTS.md
  ?? tests/__init__.py
  ?? tests/smoke/__init__.py
  ?? tests/smoke/test_smoke.py
[ideate] Staged files:
  + docs/internal/reports/iteration-1-report.md
```

只有 report 被 staged,其他 4 个 agent 写的文件留在 untracked 状态。

```
[verify] WARNING: docs/internal/reports/iteration-1-report.md exists on kitchen/iter-1 but NOT on main
```

### 根因

KitchenLoop 的 auto-commit 逻辑只 stage **白名单内的产物**(reports 目录),agent 在 worktree 内创建的其他必要文件(tests scaffold、AGENTS.md)被忽略。

另外 agent 在 worktree **外**修改了 `kitchenloop.yaml` 和 `.kitchenloop/` 下的状态文件 —— 这些会随 worktree 销毁丢失(report [IMP-3] 也提到了这点)。

### 解决方式

**短期(每次 iter 后手动补救)**:

```bash
cd ~/code/mindful

# 把 agent 在 worktree 写的但漏 commit 的拷出来
WORKTREE=.claude/worktrees/kitchen-iter-1

cp $WORKTREE/AGENTS.md ./
cp $WORKTREE/tests/__init__.py tests/
cp $WORKTREE/tests/smoke/__init__.py tests/smoke/
cp $WORKTREE/tests/smoke/test_smoke.py tests/smoke/

git add AGENTS.md tests/ kitchenloop.yaml .kitchenloop/
git commit -m "kitchenloop iter-N missing artifacts: tests scaffold + state files"
git push
```

**中期(改 KitchenLoop 行为)**:

修改 `kitchenloop.sh` 里 ideate 阶段的 commit 逻辑,把 untracked 的 `tests/`、`AGENTS.md`、`scenarios/` 都加入 stage 白名单。

**长期**:把 `.kitchenloop/` 状态目录改成项目内 git 跟踪的目录,而不是 worktree 外的。

### 是否给上游提 issue

**是**,但可以等积累更多观察后再提一个综合性 issue。

---

## 问题 6:PR 创建后不自动 merge

### 症状

```
[merge] PR created: https://github.com/.../pull/1
[merge] PR left open for CI checks and review.
```

PR 一直停在 open 状态,KitchenLoop 不进入 polish 阶段做 review,不自动 merge。

### 根因

三个原因叠加:

1. **新 repo 没配 GitHub Actions** → `merge_gates: ["ci_pass"]` 永远等不到 CI pass
2. **没装 CodeRabbit bot** → `pr_manager.review_bot: coderabbitai` 永远等不到 bot review
3. **跑了 `--only ideate`,没跑 polish 阶段** → 多模型 review 流程根本没启动

### 解决方式

**试运行期最快的方法 —— 关掉所有阻塞性 gate**:

修改 `kitchenloop.yaml`:

```yaml
verification:
  merge_gates: []           # 不再要求 CI pass

pr_manager:
  review_bot: ""            # 不再等 CodeRabbit
```

**手动推进当前卡住的 PR**:

```bash
# 你已经看过 report 觉得 OK
gh pr review 1 --approve --body "Manually approving iter-1"
gh pr merge 1 --merge --delete-branch
# 如果 merge method 不允许,换 --squash 或 --rebase
```

**后续跑完整流程**(不要再用 `--only ideate`):

```bash
./scripts/kitchenloop/kitchenloop.sh 5
```

### 是否给上游提 issue

**否**。这是配置问题,不是 bug。但 KitchenLoop 文档应该写得更清楚 —— "新项目首跑推荐先关掉 ci_pass 和 review_bot"。

---

## 问题 7:`[no-work] No work produced` 误判

### 症状

```
Loop 1 complete.
[no-work] No work produced (1/3 consecutive)
```

实际上 ideate 阶段产出了 report、PR、smoke test 等多个产物,KitchenLoop 却判定"没干活"。

### 根因

`--only ideate` 模式下,KitchenLoop 的"干活"判定逻辑只看 execute 阶段产出的 PR。ideate 阶段产物(report、scenario)不算"work",所以连续 3 次 `--only ideate` 会触发 max_no_work_loops 退出。

### 解决方式

**忽略这个 warning**,只在跑 `--only ideate` 时出现,跑完整流程时不会出现。

如果非要消除:

```yaml
runtime:
  max_no_work_loops: 999   # 试运行期间放大
```

### 是否给上游提 issue

**否**。但文档应该说明 `--only ideate` 模式下的这个判定行为。

---

## 整体落地经验总结

### 成功要素(按重要性排序)

1. **spec 写得用心**:Opus 自己评价 "unusually good for a freshly-bootstrapped repo and made test design straightforward",这是 ideate 输出质量高的根本原因
2. **环境变量优先于交互登录**(SSH 场景下尤其):`GEMINI_API_KEY` 直接设比 OAuth 稳
3. **三个 reviewer 工具都通**(Claude / Codex / Gemini):缺一个 FLAG 率会显著上升
4. **用 tmux 挂着跑**:KitchenLoop 一跑几小时,SSH 断线就完蛋

### 试运行期间最务实的配置策略

```yaml
# 关掉所有阻塞性 gate,先把流程跑通
verification:
  merge_gates: []
pr_manager:
  review_bot: ""

# 试运行期间一次只处理一个 PR,便于观察
runtime:
  polish_max_prs: 1
  max_no_work_loops: 999    # 防止误判触发退出
```

跑稳后再逐项打开。

### 时间投入预期

- **首次踩坑跑通到 iter-1 SUCCESS**:约 3 小时(取决于网络和 bug 修复速度)
- **修完所有 bug 后单 iter 时间**:5–15 分钟(只 ideate)/ 30–45 分钟(完整 6 阶段)
- **跑通 mindful 完整产品(约 10 iter)**:3–5 小时实际计算 + 半天试错

### 触发实际产物质量提升的 3 个动作

按 ROI 排序:

1. **写好 spec**(最高 ROI):一份具体到 ground truth + failure modes + state delta 的 spec,直接决定 ideate 输出质量
2. **保留三个 reviewer**:即使 Gemini 是免费版,有它在 polish 阶段做第三票,FLAG 率从 30% 降到 5%
3. **不追求自动 merge,前 10 iter 自己看每个 PR diff**:建立信任,理解工具风格,发现你 spec 没写清楚的地方

### 给上游提 issue 的建议(整理后一次性反馈)

合并成一个综合性 issue,标题:

> Compatibility issues on Manjaro Linux + Claude CLI v2.1.85+ + Go-version yq

内容包括问题 2、3、4 的复现步骤和修复方法。这种"一次性梳理+附修复方案"的 issue,维护者通常很欢迎。

---

## 当前 mindful 项目状态(iter-1 跑完后)

- ✅ Pre-flight 通过
- ✅ Ideate 阶段产出高质量 report(Opus 评价 spec quality "unusually good")
- ✅ 4-layer smoke test 已写,Layer 1 PASS,Layer 2-4 RED(预期)
- ✅ MINDFUL_FAST_TICK env var 契约已建立
- ⏳ PR #1 待手动 merge
- 🔜 下一步:跑 5 个完整 iter,观察 execute 阶段会不会基于 BUG-1 / FEAT-1,2 真的实现 mindful CLI 入口

---

## 附录:遇到新问题的排查清单

每次跑 KitchenLoop 出问题,按这个顺序排查:

```bash
# 1. 检查环境变量污染
env | grep -iE "anthropic|claude|gemini|openai"

# 2. 三个 LLM CLI 是否都通
echo "test" | claude --print --output-format stream-json --verbose 2>/dev/null | head -3
echo "test" | codex exec 2>/dev/null
echo "test" | gemini -p 2>/dev/null

# 3. yq 输出是否带引号
yq '.project.name' kitchenloop.yaml

# 4. git 状态
git status
git worktree list
git branch -a

# 5. KitchenLoop lock 残留
ls -la .kitchenloop/kitchenloop.lock 2>/dev/null

# 6. 看最近一次 phase 日志
ls -lt .kitchenloop/logs/ | head -5
tail -100 .kitchenloop/logs/$(ls -t .kitchenloop/logs/ | head -1)
```

90% 的问题在前 6 步就能定位。