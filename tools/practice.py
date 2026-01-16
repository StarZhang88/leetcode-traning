#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create a new LeetCode problem folder with templates.

Output:
- review list: reviews/2026-01-16.md
- problem folder: problems/0001_two_sum/
- solution file: problems/0001_two_sum/solution.py
- notes file: problems/0001_two_sum/notes.md
- meta file: problems/0001_two_sum/meta.yaml

Usage:
  python tools/practice.py
  python tools/practice.py --new 2 --review 3
  python tools/practice.py --list leetcode_60
  python tools/practice.py --list-catalog  # List all available problem lists
  python tools/practice.py --problem 2  # Generate folder for problem ID 2
  python tools/practice.py --problem 2 --list leetcode_60  # Generate from specific list
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent
LISTS_DIR = REPO_ROOT / "lists"
PROBLEMS_DIR = REPO_ROOT / "problems"
REVIEW_DIR = REPO_ROOT / "reviews"
DEFAULT_LIST_NAME = "leetcode_60"




def get_list_path(list_name: str) -> Path:
    """Get problem list file path, supports with or without .json suffix"""
    if list_name.endswith(".json"):
        list_name = list_name[:-5]
    return LISTS_DIR / f"{list_name}.json"


def list_available_lists() -> List[str]:
    """List all available problem list files"""
    if not LISTS_DIR.exists():
        return []
    lists = []
    for f in LISTS_DIR.glob("*.json"):
        lists.append(f.stem)
    return sorted(lists)


def load_lists(list_name: str = DEFAULT_LIST_NAME) -> Dict[str, Any]:
    """Load specified problem list file"""
    list_path = get_list_path(list_name)
    if not list_path.exists():
        available = list_available_lists()
        if available:
            raise SystemExit(
                f"Problem list file does not exist: {list_path}\n"
                f"Available lists: {', '.join(available)}\n"
                f"Use --list <name> to select a list"
            )
        else:
            raise SystemExit(f"Problem list file does not exist: {list_path}\nNo problem list files found in lists/ directory")
    
    try:
        with open(list_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Problem list file format error: {list_path}\n{str(e)}")
    
    # Validate list structure
    validate_list_structure(data, list_name)
    return data


def validate_list_structure(data: Dict[str, Any], list_name: str) -> None:
    """Validate problem list JSON structure"""
    errors = []
    
    # Check required fields
    if "version" not in data:
        errors.append("Missing 'version' field")
    
    if "default_plan" not in data:
        errors.append("Missing 'default_plan' field")
    else:
        plan = data["default_plan"]
        required_plan_fields = ["new_per_day", "review_per_day", "review_days"]
        for field in required_plan_fields:
            if field not in plan:
                errors.append(f"default_plan missing '{field}' field")
    
    if "problems" not in data:
        errors.append("Missing 'problems' field")
    elif not isinstance(data["problems"], list):
        errors.append("'problems' must be an array")
    else:
        # Validate each problem structure
        for i, p in enumerate(data["problems"]):
            if not isinstance(p, dict):
                errors.append(f"problems[{i}] must be an object")
                continue
            if "id" not in p:
                errors.append(f"problems[{i}] missing 'id' field")
            if "title" not in p:
                errors.append(f"problems[{i}] missing 'title' field")
    
    if errors:
        raise SystemExit(
            f"Problem list structure validation failed ({list_name}):\n" + "\n".join(f"  - {e}" for e in errors)
        )
    
    
def slugify(title: str) -> str:
    s = title.strip().lower()
    # replace non-alnum with underscore
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "untitled"



def parse_meta(meta_path: Path) -> Dict[str, Any]:
    """
    Minimal parser for our meta.yml.
    Supports:
      key: value
      key: [a, b, c]
    """
    data: Dict[str, Any] = {}
    if not meta_path.exists():
        return data
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


def write_meta(meta_path: Path, meta: Dict[str, Any]) -> None:
    keys = ["id", "title", "difficulty", "tags", "first_done", "mistakes", "next_review", "status"]
    lines: List[str] = []
    for k in keys:
        if k not in meta:
            continue
        v = meta[k]
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(v)}]")
        else:
            if k in ("title", "difficulty", "next_review", "status"):
                lines.append(f'{k}: "{v}"')
            else:
                lines.append(f"{k}: {v}")
    meta_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


SOLUTION_TMPL = """\"\"\"
LC {pid:04d} {title}
Difficulty: {difficulty}
Tags: {tags_csv}

Key:
- (write 1-2 key observations)

Pitfalls:
- (edge cases / common mistakes)

Complexity: O(?) time, O(?) space
\"\"\"

from typing import List, Optional, Tuple, Dict


class Solution:
    # TODO: rename method signature to LeetCode's required one.
    pass
"""

NOTES_TMPL = """## Mistakes / Stuck Points
- 

## Key Insights (1-2 sentences)
- 

## Edge Cases Checklist
- 
- 

## Related / Similar Problems
- 
"""


def create_problem_folder(pid: int, title: str, difficulty: str, tags: List[str], review_days: List[int]) -> Path:
    PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
    folder = PROBLEMS_DIR / f"{pid:04d}_{slugify(title)}"
    folder.mkdir(parents=True, exist_ok=False)

    (folder / "solution.py").write_text(
        SOLUTION_TMPL.format(
            pid=pid,
            title=title,
            difficulty=difficulty or "unknown",
            tags_csv=", ".join(tags) if tags else "-",
        ),
        encoding="utf-8",
    )
    (folder / "notes.md").write_text(NOTES_TMPL, encoding="utf-8")

    today = dt.date.today()
    meta = {
        "id": str(pid),
        "title": title,
        "difficulty": difficulty or "unknown",
        "tags": tags,
        "first_done": "",
        "mistakes": [],
        "next_review": (today + dt.timedelta(days=int(review_days[0]) if review_days else 2)).isoformat(),
        "status": "new",
    }
    write_meta(folder / "meta.yml", meta)
    return folder


def existing_problem_dir(pid: int) -> Optional[Path]:
    """Check if problem directory exists, return path or None"""
    if not PROBLEMS_DIR.exists():
        return None
    pat = re.compile(rf"^{pid:04d}_")
    for d in PROBLEMS_DIR.iterdir():
        if d.is_dir() and pat.match(d.name):
            return d
    return None


def get_all_metas() -> List[Tuple[int, Path, Dict[str, Any]]]:
    metas: List[Tuple[int, Path, Dict[str, Any]]] = []
    if not PROBLEMS_DIR.exists():
        return metas
    for d in PROBLEMS_DIR.iterdir():
        if not d.is_dir():
            continue
        meta_path = d / "meta.yml"
        if not meta_path.exists():
            continue
        meta = parse_meta(meta_path)
        try:
            pid = int(str(meta.get("id") or d.name.split("_", 1)[0]))
        except Exception:
            continue
        metas.append((pid, d, meta))
    return metas


def pick_today(db: Dict[str, Any], new_n: int, review_n: int) -> Dict[str, List[Dict[str, Any]]]:
    today = dt.date.today().isoformat()

    # Due reviews: meta.next_review <= today AND first_done exists
    due: List[Dict[str, Any]] = []
    for pid, _, meta in get_all_metas():
        if not meta.get("first_done"):
            continue
        if meta.get("next_review", "9999-12-31") <= today:
            due.append(
                {
                    "id": pid,
                    "title": meta.get("title", ""),
                    "difficulty": meta.get("difficulty", ""),
                    "tags": meta.get("tags", []),
                    "reason": f"due({meta.get('next_review')})",
                }
            )

    # New candidates: in list but folder not created
    created = {pid for pid, _, _ in get_all_metas()}
    candidates: List[Dict[str, Any]] = []
    for p in db.get("problems", []):
        pid = int(p["id"])
        if pid in created or existing_problem_dir(pid):
            continue
        candidates.append(p)

    # Prioritize starred, then random
    starred = [p for p in candidates if p.get("star")]
    unstarred = [p for p in candidates if not p.get("star")]
    random.shuffle(starred)
    random.shuffle(unstarred)
    new_pick = (starred + unstarred)[:new_n]

    random.shuffle(due)
    review_pick = due[:review_n]

    return {"new": new_pick, "review": review_pick}


def render_daily_md(picked: Dict[str, List[Dict[str, Any]]]) -> str:
    today = dt.date.today().isoformat()
    lines: List[str] = []
    lines.append(f"# {today}")
    lines.append("")
    lines.append("## Today")
    lines.append("")
    lines.append("### Review (due)")
    if not picked["review"]:
        lines.append("- (none)")
    else:
        for r in picked["review"]:
            pid = int(r["id"])
            lines.append(f"- LC {pid:04d} {r.get('title','')}  ({r.get('reason','')})")
    lines.append("")
    lines.append("### New")
    if not picked["new"]:
        lines.append("- (none)")
    else:
        for p in picked["new"]:
            pid = int(p["id"])
            tags = ",".join(p.get("tags", []))
            lines.append(f"- LC {pid:04d} {p['title']}  [{p.get('difficulty','')}]  tags={tags}")
    lines.append("")
    lines.append("## Checklist")
    lines.append("- New: implement `solution.py` + fill `notes.md` (mistakes/key insights/edge cases/related problems)")
    lines.append("- Optional: generate AI explanation to `ai.md`: `python tools/ai_solve.py <id>`")
    lines.append("")
    return "\n".join(lines)


def find_problem_in_list(pid: int, db: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find problem by ID in the problem list"""
    for p in db.get("problems", []):
        if int(p.get("id", 0)) == pid:
            return p
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate daily LeetCode practice plan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--list",
        type=str,
        default=DEFAULT_LIST_NAME,   
        help=f"Select problem list file (default: {DEFAULT_LIST_NAME})",
    )
    parser.add_argument(
        "--list-catalog",
        action="store_true",
        help="List all available problem list files",
    )
    parser.add_argument(
        "--problem",
        type=int,
        default=None,
        help="Generate folder for specific problem ID",
    )
    parser.add_argument(
        "--new",
        type=int,
        default=None,
        help="Override default_plan.new_per_day",
    )
    parser.add_argument(
        "--review",
        type=int,
        default=None,
        help="Override default_plan.review_per_day",
    )
    args = parser.parse_args()

    # If just listing catalogs, display and exit
    if args.list_catalog:
        available = list_available_lists()
        if not available:
            print("No problem list files found in lists/ directory")
            return
        print("Available problem lists:")
        for name in available:
            marker = " (default)" if name == DEFAULT_LIST_NAME else ""
            print(f"  - {name}{marker}")
        return

    # Load problem list
    db = load_lists(args.list)
    plan = db.get("default_plan", {})
    review_days = plan.get("review_days", [2, 7, 21])

    # If --problem is specified, generate folder for that specific problem
    if args.problem is not None:
        pid = args.problem
        problem = find_problem_in_list(pid, db)
        
        if not problem:
            raise SystemExit(
                f"Problem ID {pid} not found in list '{args.list}'.\n"
                f"Use --list <name> to search in a different list."
            )
        
        if existing_problem_dir(pid):
            print(f"Problem folder already exists: {existing_problem_dir(pid)}")
            return
        
        folder = create_problem_folder(
            pid=pid,
            title=problem["title"],
            difficulty=problem.get("difficulty", "unknown"),
            tags=problem.get("tags", []),
            review_days=review_days,
        )
        print(f"Created problem folder: {folder}")
        return

    # Normal daily plan generation
    new_n = args.new if args.new is not None else int(plan.get("new_per_day", 2))
    review_n = args.review if args.review is not None else int(plan.get("review_per_day", 3))

    picked = pick_today(db, new_n=new_n, review_n=review_n)

    # Ensure folders for today's NEW problems
    for p in picked["new"]:
        pid = int(p["id"])
        if existing_problem_dir(pid):
            continue
        create_problem_folder(
            pid=pid,
            title=p["title"],
            difficulty=p.get("difficulty", "unknown"),
            tags=p.get("tags", []),
            review_days=review_days,
        )

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REVIEW_DIR / f"{dt.date.today().isoformat()}.md"
    out_path.write_text(render_daily_md(picked), encoding="utf-8")
    print(f"Using problem list: {args.list}")
    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()
