#!/usr/bin/env python3
"""Prepare one benchmark run from the preregistered run plan."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from pathlib import Path


BASELINE_TEMPLATE = Path("docs/prompt_templates/baseline.md")
CGP_TEMPLATE = Path("docs/prompt_templates/cgp.md")
RUN_PLAN = Path("runs/run_plan.csv")


def read_run(root: Path, run_id: str) -> dict[str, str]:
    with (root / RUN_PLAN).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["run_id"] == run_id:
                return row
    raise SystemExit(f"unknown run_id: {run_id}")


def task_spec_text(root: Path, row: dict[str, str]) -> str:
    return (root / row["task_spec"]).read_text(encoding="utf-8").strip()


def template_text(root: Path, condition: str) -> str:
    path = CGP_TEMPLATE if condition == "cgp" else BASELINE_TEMPLATE
    return (root / path).read_text(encoding="utf-8").strip()


def extract_section(markdown: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\s+([\s\S]*?)(\n## |$)"
    match = re.search(pattern, markdown)
    return match.group(1).strip() if match else ""


def active_protocol(root: Path) -> str:
    manifest = json.loads((root / "next-prompt-protocols" / "manifest.json").read_text(encoding="utf-8"))
    return manifest["active_protocol"]


def render_prompt(root: Path, row: dict[str, str]) -> str:
    spec = task_spec_text(root, row)
    template = template_text(root, row["condition"])
    task_description = extract_section(spec, "Description")
    replacements = {
        "{task_description}": task_description,
        "{allowed_files}": extract_section(spec, "Allowed Files"),
        "{verification_commands}": extract_section(spec, "Verification"),
        "{task_spec}": row["task_spec"],
        "{phase}": "phase-0",
        "{active_protocol}": active_protocol(root),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    return f"""# Benchmark Run Prompt

Run ID: `{row["run_id"]}`
Agent: `{row["agent"]}`
Condition: `{row["condition"]}`
Task: `{row["task_id"]}` / `{row["task_slug"]}`
Start tag: `{row["start_tag"]}`

## Task Specification

{spec}

## Condition Template

{template}
"""


def git_commit_for_ref(root: Path, ref: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", ref],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def create_worktree(root: Path, run_id: str, start_tag: str, worktree_root: Path) -> Path:
    worktree_path = worktree_root / run_id
    if worktree_path.exists():
        raise SystemExit(f"worktree already exists: {worktree_path}")
    subprocess.run(
        ["git", "worktree", "add", str(worktree_path), start_tag],
        cwd=root,
        check=True,
    )
    return worktree_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--out-root", type=Path, default=Path("runs/raw"))
    parser.add_argument("--worktree-root", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    row = read_run(root, args.run_id)
    prompt = render_prompt(root, row)
    start_commit = git_commit_for_ref(root, row["start_tag"])

    metadata = {
        "run_id": row["run_id"],
        "agent": row["agent"],
        "condition": row["condition"],
        "task_id": row["task_id"],
        "task_slug": row["task_slug"],
        "replication": int(row["replication"]),
        "run_order": int(row["run_order"]),
        "start_tag": row["start_tag"],
        "start_commit": start_commit,
        "task_spec": row["task_spec"],
        "status": "prepared",
    }

    if args.dry_run:
        print(prompt)
        print(json.dumps(metadata, indent=2))
        return 0

    run_dir = args.out_root / row["run_id"]
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    if args.worktree_root:
        worktree_path = create_worktree(root, row["run_id"], row["start_tag"], args.worktree_root)
        metadata["worktree"] = str(worktree_path)
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(f"prepared {row['run_id']} in {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
