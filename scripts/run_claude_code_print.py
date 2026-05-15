#!/usr/bin/env python3
"""Run one planned Claude Code cell in print mode and capture artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


RUN_PLAN = Path("runs/run_plan.csv")


def run(command: list[str], cwd: Path, check: bool = True, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=check, input=stdin, text=True, capture_output=True)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def is_completed_production_run(run_dir: Path) -> bool:
    metadata_path = run_dir / "metadata.json"
    if not metadata_path.exists():
        return False
    metadata = read_json(metadata_path)
    if metadata.get("archive_status"):
        return False
    return metadata.get("status") == "completed_valid" and metadata.get("run_validity") == "valid"


def next_run_id(root: Path) -> str:
    with (root / RUN_PLAN).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            run_dir = root / "runs" / "raw" / row["run_id"]
            if not is_completed_production_run(run_dir):
                return row["run_id"]
    raise SystemExit("all planned runs are completed")


def ensure_prepared(root: Path, run_id: str) -> Path:
    run_dir = root / "runs" / "raw" / run_id
    if not run_dir.exists():
        run(["python", "scripts/prepare_run.py", "--run-id", run_id], cwd=root)
    metadata = read_json(run_dir / "metadata.json")
    worktree = root / metadata["worktree"]
    if not worktree.exists():
        raise SystemExit(f"missing worktree after preparation: {worktree}")
    return run_dir


def update_metadata_for_print_mode(run_dir: Path, transcript_path: Path) -> None:
    metadata_path = run_dir / "metadata.json"
    metadata = read_json(metadata_path)
    metadata["execution_mode"] = "claude-code-print"
    metadata["transcript"] = str(transcript_path.relative_to(run_dir))
    write_json(metadata_path, metadata)


def execute_claude(run_dir: Path, worktree: Path, permission_mode: str) -> int:
    prompt = (run_dir / "prompt.md").read_text(encoding="utf-8")
    transcripts = run_dir / "transcripts"
    transcripts.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace(":", "")
    stdout_path = transcripts / f"claude-print-{timestamp}.stdout.txt"
    stderr_path = transcripts / f"claude-print-{timestamp}.stderr.txt"
    result_path = transcripts / f"claude-print-{timestamp}.json"

    result = run(
        ["claude", "-p", "--permission-mode", permission_mode],
        cwd=worktree,
        check=False,
        stdin=prompt,
    )
    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    write_json(
        result_path,
        {
            "command": f"claude -p --permission-mode {permission_mode}",
            "working_directory": str(worktree),
            "returncode": result.returncode,
            "stdout": str(stdout_path.relative_to(run_dir)),
            "stderr": str(stderr_path.relative_to(run_dir)),
        },
    )
    update_metadata_for_print_mode(run_dir, result_path)
    return result.returncode


def capture(root: Path, run_id: str) -> int:
    result = run(["python", "scripts/capture_run.py", "--run-id", run_id], cwd=root, check=False)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    return result.returncode


def commit_and_push(root: Path, run_id: str, push: bool) -> None:
    run(["git", "add", f"runs/raw/{run_id}"], cwd=root)
    status = run(["git", "status", "--short"], cwd=root).stdout.strip()
    if not status:
        print("no changes to commit")
        return
    run(["git", "commit", "-m", f"Capture {run_id}"], cwd=root)
    if push:
        run(["git", "push", "origin", "main"], cwd=root)


def main() -> int:
    parser = argparse.ArgumentParser()
    run_selector = parser.add_mutually_exclusive_group(required=True)
    run_selector.add_argument("--run-id")
    run_selector.add_argument("--next", action="store_true")
    parser.add_argument("--permission-mode", default="auto")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    run_id = next_run_id(root) if args.next else args.run_id
    print(f"selected run: {run_id}")
    run_dir = ensure_prepared(root, run_id)
    metadata = read_json(run_dir / "metadata.json")
    worktree = root / metadata["worktree"]

    claude_returncode = execute_claude(run_dir, worktree, args.permission_mode)
    capture_returncode = capture(root, run_id)
    if args.commit:
        commit_and_push(root, run_id, args.push)

    if claude_returncode != 0:
        print(f"claude exited nonzero: {claude_returncode}")
    return capture_returncode if capture_returncode != 0 else claude_returncode


if __name__ == "__main__":
    raise SystemExit(main())
