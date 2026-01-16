# LeetCode Training

<div align="right">

[🇺🇸 English](#) | [🇨🇳 中文](README.zh.md)

</div>

---

A structured LeetCode practice system with spaced repetition and AI-powered explanations.

## Features

- **Problem Lists**: Organize problems into custom lists (e.g., `leetcode_60.json`)
- **Daily Practice Plan**: Automatically generate daily practice schedules with new problems and reviews
- **Spaced Repetition**: Built-in review scheduling (2, 7, 21 days)
- **AI Solutions**: Generate detailed explanations using LLM APIs
- **Progress Tracking**: Track problem status, mistakes, and review dates

## Quick Start

### 1. Install Dependencies

```bash
pip install openai python-dotenv
```

### 2. Configure AI (Optional)

Create a `.env` file in the project root:

```env
LLM_API_KEY=sk-your-api-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.2
```

### 3. Generate Daily Practice Plan

```bash
python tools/practice.py
```

This will:
- Create problem folders for new problems
- Generate a daily review list in `reviews/YYYY-MM-DD.md`
- Use the default problem list (`leetcode_60`) or specify with `--list`

### 4. Generate AI Solution

```bash
python tools/ai_solve.py 76
python tools/ai_solve.py 76 --user "Focus on explaining the sliding window approach"
```

## Project Structure

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

## Usage

### Practice Tool

```bash
# Use default list
python tools/practice.py

# Specify problem list
python tools/practice.py --list leetcode_60

# List available problem lists
python tools/practice.py --list-catalog

# Override daily plan
python tools/practice.py --new 3 --review 5

# Generate specific problem folder
python tools/practice.py --problem 2
```

### AI Solve Tool

```bash
# Basic usage
python tools/ai_solve.py <problem_id>

# With user input
python tools/ai_solve.py 76 --user "Explain the time complexity"
```

## Problem List Format

See `lists/README.md` for detailed format specification.

## License

MIT
