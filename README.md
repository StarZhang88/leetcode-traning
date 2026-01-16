# LeetCode Training

<div align="right">

[🇺🇸 English](#english) | [🇨🇳 中文](#chinese)

</div>

---

<a name="english"></a>
## 🇺🇸 English

A structured LeetCode practice system with spaced repetition and AI-powered explanations.

### Features

- **Problem Lists**: Organize problems into custom lists (e.g., `leetcode_60.json`)
- **Daily Practice Plan**: Automatically generate daily practice schedules with new problems and reviews
- **Spaced Repetition**: Built-in review scheduling (2, 7, 21 days)
- **AI Solutions**: Generate detailed explanations using LLM APIs
- **Progress Tracking**: Track problem status, mistakes, and review dates

### Quick Start

#### 1. Install Dependencies

```bash
pip install openai python-dotenv
```

#### 2. Configure AI (Optional)

Create a `.env` file in the project root:

```env
LLM_API_KEY=sk-your-api-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.2
```

#### 3. Generate Daily Practice Plan

```bash
python tools/practice.py
```

This will:
- Create problem folders for new problems
- Generate a daily review list in `reviews/YYYY-MM-DD.md`
- Use the default problem list (`leetcode_60`) or specify with `--list`

#### 4. Generate AI Solution

```bash
python tools/ai_solve.py 76
python tools/ai_solve.py 76 --user "Focus on explaining the sliding window approach"
```

### Project Structure

```
leetcode-training/
├── lists/              # Problem list files (JSON)
│   └── leetcode_60.json
├── problems/           # Problem folders
│   └── 0001_two_sum/
│       ├── meta.yml    # Problem metadata
│       ├── solution.py # Your solution
│       ├── notes.md    # Your notes
│       └── ai.md       # AI-generated explanation
├── reviews/            # Daily review lists
│   └── 2026-01-16.md
└── tools/
    ├── practice.py     # Generate daily practice plan
    └── ai_solve.py     # Generate AI solutions
```

### Usage

#### Practice Tool

```bash
# Use default list
python tools/practice.py

# Specify problem list
python tools/practice.py --list leetcode_60

# List available problem lists
python tools/practice.py --list-catalog

# Override daily plan
python tools/practice.py --new 3 --review 5
```

#### AI Solve Tool

```bash
# Basic usage
python tools/ai_solve.py <problem_id>

# With user input
python tools/ai_solve.py 76 --user "Explain the time complexity"
```

### Problem List Format

See `lists/README.md` for detailed format specification.

### License

MIT

---

<a name="chinese"></a>
## 🇨🇳 中文

一个结构化的 LeetCode 练习系统，支持间隔重复和 AI 驱动的解答生成。

### 功能特性

- **题库管理**: 将题目组织到自定义题库中（如 `leetcode_60.json`）
- **每日练习计划**: 自动生成包含新题和复习的每日练习计划
- **间隔重复**: 内置复习调度（2、7、21 天）
- **AI 解答**: 使用 LLM API 生成详细解答
- **进度跟踪**: 跟踪题目状态、错误和复习日期

### 快速开始

#### 1. 安装依赖

```bash
pip install openai python-dotenv
```

#### 2. 配置 AI（可选）

在项目根目录创建 `.env` 文件：

```env
LLM_API_KEY=sk-your-api-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.2
```

#### 3. 生成每日练习计划

```bash
python tools/practice.py
```

这将：
- 为新题目创建题目文件夹
- 在 `reviews/YYYY-MM-DD.md` 生成每日复习列表
- 使用默认题库（`leetcode_60`）或通过 `--list` 指定

#### 4. 生成 AI 解答

```bash
python tools/ai_solve.py 76
python tools/ai_solve.py 76 --user "请重点解释滑动窗口的思路"
```

### 项目结构

```
leetcode-training/
├── lists/              # 题库文件（JSON）
│   └── leetcode_60.json
├── problems/           # 题目文件夹
│   └── 0001_two_sum/
│       ├── meta.yml    # 题目元数据
│       ├── solution.py # 你的解答
│       ├── notes.md    # 你的笔记
│       └── ai.md       # AI 生成的解答
├── reviews/            # 每日复习列表
│   └── 2026-01-16.md
└── tools/
    ├── practice.py     # 生成每日练习计划
    └── ai_solve.py     # 生成 AI 解答
```

### 使用方法

#### 练习工具

```bash
# 使用默认题库
python tools/practice.py

# 指定题库
python tools/practice.py --list leetcode_60

# 列出可用题库
python tools/practice.py --list-catalog

# 覆盖每日计划
python tools/practice.py --new 3 --review 5
```

#### AI 解答工具

```bash
# 基本使用
python tools/ai_solve.py <题目ID>

# 带用户输入
python tools/ai_solve.py 76 --user "请解释时间复杂度"
```

### 题库格式

详细格式说明请参见 `lists/README.md`。

### 许可证

MIT
