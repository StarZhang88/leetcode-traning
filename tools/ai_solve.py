#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ai_solve.py
Generate a detailed teaching-style explanation + reference solution into ai.md
under problems/<id_*>/.

Usage:
  python tools/ai_solve.py 76
  python tools/ai_solve.py 76 --user "Focus on explaining the sliding window approach"

Configuration (.env file in project root):
  LLM_API_KEY=sk-xxx
  LLM_BASE_URL=https://api.openai.com/v1
  LLM_MODEL=gpt-4o-mini
  LLM_TEMPERATURE=0.2
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

REPO_ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_DIR = REPO_ROOT / "problems"
ENV_FILE = REPO_ROOT / ".env"


def find_problem_dir(pid: int) -> Path:
    """Find problem directory by problem ID"""
    if not PROBLEMS_DIR.exists():
        raise SystemExit(f"problems/ directory does not exist. Run practice.py first to create problem folders")
    
    pat = re.compile(rf"^{pid:04d}_")
    for d in PROBLEMS_DIR.iterdir():
        if d.is_dir() and pat.match(d.name):
            return d
    
    raise SystemExit(f"Problem folder for ID {pid} does not exist. Run practice.py first to create problem folders")


def parse_meta(meta_path: Path) -> Dict[str, Any]:
    """Parse meta.yml file"""
    data: Dict[str, Any] = {}
    if not meta_path.exists():
        raise SystemExit(f"meta.yml file does not exist: {meta_path}")
    
    for line in meta_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"')
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            if inner:
                data[k] = [x.strip().strip('"') for x in inner.split(",") if x.strip()]
            else:
                data[k] = []
        else:
            data[k] = v
    return data


def load_env_config() -> Dict[str, Any]:
    """Load configuration from .env file"""
    # Load .env file
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
    else:
        # If .env doesn't exist, try loading from environment variables
        load_dotenv()
    
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing LLM_API_KEY. Please create a .env file in the project root with:\n"
            "LLM_API_KEY=sk-your-api-key-here\n"
            "LLM_BASE_URL=https://api.openai.com/v1\n"
            "LLM_MODEL=gpt-4o-mini\n"
            "LLM_TEMPERATURE=0.2"
        )
    
    return {
        "api_key": api_key,
        "base_url": os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.2")),
        "timeout": int(os.getenv("LLM_TIMEOUT", "180")),
    }


def call_llm(messages: List[Dict[str, str]], config: Dict[str, Any]) -> str:
    """Call LLM API"""
    if not HAS_OPENAI:
        raise SystemExit("Dependencies not installed. Please run: pip install openai python-dotenv")
    
    try:
        client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"],
            timeout=config["timeout"],
        )
        
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,  # type: ignore
            temperature=config["temperature"],
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise SystemExit("API returned empty response")
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg:
            raise SystemExit(f"API Key is invalid or expired")
        elif "404" in error_msg or "Not Found" in error_msg:
            raise SystemExit(f"Model not found or API endpoint error")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            raise SystemExit(f"API rate limit exceeded, please try again later")
        else:
            raise SystemExit(f"API call failed: {error_msg}")


def build_messages(
    pid: int,
    problem: Dict[str, Any],
    notes: str,
    solution: str,
    user_input: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Build messages to send to AI"""
    title = problem.get("title", f"LC {pid:04d}")
    difficulty = problem.get("difficulty", "unknown")
    tags = problem.get("tags", [])

    system = (
        "You are a LeetCode tutor. "
        "Write a detailed teaching-style explanation that helps me understand and review later. "
        "Be structured and practical. "
        "Always include: key insight, step-by-step approach, pitfalls/edge cases checklist, complexity, "
        "and a clean Python reference solution ready to submit."
    )

    user_parts = [
        f"Solve the LeetCode problem in a detailed teaching style.",
        "",
        "Problem:",
        f"- ID: {pid:04d}",
        f"- Title: {title}",
        f"- Difficulty: {difficulty}",
        f"- Tags: {tags}",
    ]
    
    if notes:
        user_parts.extend([
            "",
            "My current notes:",
            notes,
        ])
    
    if solution:
        user_parts.extend([
            "",
            "My current code:",
            solution,
        ])
    
    if user_input:
        user_parts.extend([
            "",
            "Additional requirements from user:",
            user_input,
        ])
    
    user_parts.extend([
        "",
        "Output Markdown sections (keep headings exactly):",
        "",
        "1) Restatement",
        "2) Key Insight",
        "3) Step-by-step Approach",
        "4) Pitfalls & Edge Cases Checklist",
        "5) Complexity",
        "6) Reference Python Solution",
        "7) Short Alternatives (optional)",
        "",
        "Extra constraints:",
        "",
        "Do NOT hide critical details behind vague phrases.",
        "",
        "If method signature is uncertain, choose the most standard LeetCode signature for this problem and keep it reasonable.",
        "",
        "Keep code clean and readable (no unnecessary micro-optimizations).",
    ])

    user = "\n".join(user_parts)
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AI solution for LeetCode problem")
    parser.add_argument("id", type=int, help="LeetCode problem ID")
    parser.add_argument(
        "--user",
        type=str,
        default=None,
        help="Additional user input to pass to AI",
    )
    args = parser.parse_args()

    # Load configuration
    config = load_env_config()
    
    # Find problem directory
    pid = args.id
    pdir = find_problem_dir(pid)
    
    # Get problem info from meta.yml
    meta = parse_meta(pdir / "meta.yml")
    
    # Read notes and solution if they exist
    notes = ""
    solution = ""
    if (pdir / "notes.md").exists():
        notes = (pdir / "notes.md").read_text(encoding="utf-8")
    if (pdir / "solution.py").exists():
        solution = (pdir / "solution.py").read_text(encoding="utf-8")
    
    # Determine output path
    out_path = pdir / "ai.md"
    if out_path.exists():
        raise SystemExit(f"{out_path} already exists, please delete or rename it first")

    # Call LLM
    print(f"Generating solution (model: {config['model']})...")
    messages = build_messages(pid, meta, notes, solution, args.user)
    content = call_llm(messages, config)

    # Save result
    title = meta.get("title", "")
    header = f"# AI Solution — LC {pid:04d} {title}".strip()
    out_path.write_text(
        header + "\n\n" + content.strip() + "\n\n> Generated by tools/ai_solve.py\n",
        encoding="utf-8",
    )
    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()