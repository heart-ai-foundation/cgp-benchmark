#!/usr/bin/env python3
"""Prepare one benchmark run from the preregistered run plan."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from hashlib import sha256
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


def markdown_list_items(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- `") and stripped.endswith("`"):
            items.append(stripped[3:-1])
        elif stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def benchmark_path(path: str) -> str:
    return path if path.startswith("benchmark-repo/") else f"benchmark-repo/{path}"


def render_prompt(root: Path, row: dict[str, str]) -> str:
    spec = task_spec_text(root, row)
    template = template_text(root, row["condition"])
    task_description = extract_section(spec, "Description")
    replacements = {
        "{task_description}": task_description,
        "{allowed_files}": extract_section(spec, "Allowed Files"),
        "{verification_commands}": extract_section(spec, "Verification"),
        "{task_spec}": row["task_spec"],
        "{phase}": "phase-1" if row["condition"] == "cgp" else "phase-0",
        "{active_protocol}": f"active/{row['run_id']}.md" if row["condition"] == "cgp" else "",
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


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
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


def write_run_scaffold(worktree: Path, row: dict[str, str], spec: str, current_commit: str) -> None:
    protocol_root = worktree / "next-prompt-protocols"
    active_dir = protocol_root / "active"
    completed_dir = protocol_root / "completed"
    phase_dir = protocol_root / "phases" / "phase-1"
    active_dir.mkdir(parents=True, exist_ok=True)
    completed_dir.mkdir(parents=True, exist_ok=True)
    phase_dir.mkdir(parents=True, exist_ok=True)

    for old_active in active_dir.glob("*.md"):
        old_active.unlink()

    allowed_files = [benchmark_path(item) for item in markdown_list_items(extract_section(spec, "Allowed Files"))]
    verification = [
        f"cd benchmark-repo && {item}"
        for item in markdown_list_items(extract_section(spec, "Verification"))
    ]
    design_note = f"notes/{row['run_id']}-design.md"
    run_record = f"runs/{row['run_id']}-run-record.json"
    evidence_json = f"evidence/{row['run_id']}-evidence.json"
    evidence_files = [design_note, run_record, evidence_json]
    allowed_files_with_evidence = allowed_files + evidence_files
    active_rel = f"active/{row['run_id']}.md"
    active_path = protocol_root / active_rel
    objective = extract_section(spec, "Description")
    active_text = f"""# Benchmark Run {row['run_id']}

## Why this exists

This active protocol governs one preregistered CGP benchmark cell. The OSF preregistration is complete, and this run is authorized by `runs/run_plan.csv`.

## Next objective

{objective}

## Files in play

{chr(10).join(f"- `{path}`" for path in allowed_files)}
- `{design_note}` - design note for rationale, scope, and verification snapshot.
- `{run_record}` - operational run record.
- `{evidence_json}` - machine-readable evidence artifact.

## Non-goals

- Do not edit files outside the allowed-files set.
- Do not perform adjacent refactors.
- Do not alter run-plan, preregistration, scaffold, or analysis files.
- Do not change task requirements beyond the task specification.

## Acceptance

{chr(10).join(f"- `{command}` passes." for command in verification)}
- Scope remains limited to allowed files.
- Evidence trio is written:
  - `{design_note}`
  - `{run_record}`
  - `{evidence_json}`
- If the task specification, manifest, lock, or repository state disagree, stop and report.
"""
    active_path.write_text(active_text, encoding="utf-8")
    active_hash = "sha256:" + sha256(active_text.encode("utf-8")).hexdigest()

    manifest = {
        "project": "CGP Drift Reduction Benchmark",
        "current_commit": current_commit,
        "current_commit_role": "task start anchor before run-specific scaffold setup; final setup commit is recorded in run metadata as metrics_base_commit",
        "current_phase": "phase-1",
        "active_protocol": active_rel,
        "completed_protocols": [],
        "allowed_files": allowed_files_with_evidence,
        "non_goals": [
            "do not edit files outside the allowed-files set",
            "do not perform adjacent refactors",
            "do not alter run-plan, preregistration, scaffold, or analysis files except the assigned evidence trio paths",
            "do not change task requirements beyond the task specification",
        ],
        "verification": {f"check_{index + 1}": command for index, command in enumerate(verification)},
        "stop_condition": "If the active protocol, manifest, lock, task specification, or repository state disagree on the active task, stop and report.",
    }
    (protocol_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    lock = {
        "lock_version": 1,
        "project": manifest["project"],
        "current_commit": manifest["current_commit"],
        "current_commit_role": manifest["current_commit_role"],
        "current_phase": manifest["current_phase"],
        "active_protocol": active_rel,
        "active_protocol_sha256": active_hash,
        "active_objective": objective,
        "allowed_files": allowed_files_with_evidence,
        "verification": manifest["verification"],
        "stop_condition": manifest["stop_condition"],
    }
    (protocol_root / ".slice-lock.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    (protocol_root / "README.md").write_text(
        f"""# Next-Prompt Protocol Scaffold

Project: CGP Drift Reduction Benchmark

Current phase: `phase-1`

Active protocol:

`{active_rel}`

This scaffold is run-specific and governs `{row['run_id']}`. The manifest `current_commit` is the task-start anchor before scaffold setup. The run metadata records the setup commit used as the metrics base.
""",
        encoding="utf-8",
    )
    (phase_dir / "README.md").write_text(
        f"""# Phase 1 - Benchmark Run Execution

Current run: `{row['run_id']}`

Condition: `{row['condition']}`

Task: `{row['task_id']}` / `{row['task_slug']}`
""",
        encoding="utf-8",
    )
    (protocol_root / "role-context.md").write_text(
        """# Role Context - CGP Benchmark Run

Read in this order:

1. `.slice-lock.json`
2. `manifest.json`
3. `role-context.md`
4. `phases/phase-1/README.md`
5. The active protocol
6. The assigned task specification

Stay inside `allowed_files`. Preserve non-goals. Run the named verification commands before declaring completion. Stop and report if protocol state and task state disagree.

Commit anchor note: `current_commit` is the task-start anchor before run-specific scaffold setup. The setup commit is recorded externally in run metadata as `metrics_base_commit`; do not reject the run solely because HEAD includes the setup scaffold commit.
""",
        encoding="utf-8",
    )

def commit_setup(worktree: Path, row: dict[str, str], spec: str) -> str:
    write_run_scaffold(worktree, row, spec, git(worktree, "rev-parse", "HEAD"))
    git(worktree, "add", "next-prompt-protocols")
    git(worktree, "commit", "-m", f"Prepare scaffold for {row['run_id']}")
    return git(worktree, "rev-parse", "HEAD")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--out-root", type=Path, default=Path("runs/raw"))
    parser.add_argument("--worktree-root", type=Path, default=Path("worktrees"))
    parser.add_argument("--no-worktree", action="store_true")
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
        "metrics_base_commit": start_commit,
        "task_spec": row["task_spec"],
        "status": "prepared",
    }

    if args.dry_run:
        print(prompt)
        print(json.dumps(metadata, indent=2))
        return 0

    run_dir = args.out_root / row["run_id"]
    worktree_path = None if args.no_worktree else args.worktree_root / row["run_id"]
    if run_dir.exists():
        raise SystemExit(f"run directory already exists: {run_dir}")
    if worktree_path and worktree_path.exists():
        raise SystemExit(f"worktree already exists: {worktree_path}")

    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    if worktree_path:
        worktree_path = create_worktree(root, row["run_id"], row["start_tag"], args.worktree_root)
        if row["condition"] == "cgp":
            metadata["setup_commit"] = commit_setup(worktree_path, row, task_spec_text(root, row))
            metadata["metrics_base_commit"] = metadata["setup_commit"]
        metadata["worktree"] = str(worktree_path)
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(f"prepared {row['run_id']}")
    print(f"run_dir: {run_dir}")
    print(f"prompt: {run_dir / 'prompt.md'}")
    if worktree_path:
        print(f"worktree: {worktree_path}")
    print(f"capture: python scripts/capture_run.py --run-id {row['run_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
