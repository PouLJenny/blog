# Task 1 标准答案(判分依据)

## 1. 输出条件(4 条,每条 1 分)
- a. 行能被 `LINE_RE` 正则解析——`minilog/parser.py` 的 `parse_line`/`parse_lines`(解析失败且非 strict 时被静默丢弃,如 app.log 里的 corrupted 行)
- b. level 必须在 `LEVEL_ORDER` 中且 >= INFO——cli 默认 `--min-level=INFO`(`minilog/config.py` 的 `DEFAULT_MIN_LEVEL`),由 `minilog/filters.py` 的 `by_min_level` 实施(DEBUG 行被过滤)
- c. `duration_ms` 存在(行尾有 `(Nms)` 后缀)且**严格大于**阈值——`minilog/stats.py` 的 `slow_records`
- d. (可并入 c)`--slow-only` 分支在 `minilog/cli.py` 的 `main` 里调用 `stats.slow_records`

## 2. 阈值(2 分)
- `SLOW_THRESHOLD_MS = 500`,定义在 `minilog/config.py`(1 分)
- 还影响 `minilog/formatter.py` 的 `format_records`:慢记录行首加 `*` 标记(1 分)

## 3. 边界判断(2 分)
- order 1002(497ms)和 1003(500ms)都**不会**出现:比较是严格大于(`> 500`),500 不算慢(答对"都不出现"+理由是严格大于各 1 分)

## 判分
满分 8 分。>=6 分算成功;搞错"严格大于"或漏掉 formatter 的 `*` 标记是常见扣分点。
