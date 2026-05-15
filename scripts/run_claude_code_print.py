#!/usr/bin/env python3
"""Run one planned Claude Code cell in print mode and capture artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import threading
from datetime import UTC, datetime
from pathlib import Path


RUN_PLAN = Path("runs/run_plan.csv")
STOP_CONDITION_RE = re.compile(
    r"(stop condition|stopping per|protocol conflict|load-bearing disagreement|manifest.*disagree|lock.*disagree|active protocol.*disagree)",
    re.IGNORECASE,
)


def run(command: list[str], cwd: Path, check: bool = True, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=check, input=stdin, text=True, capture_output=True)


def status(message: str) -> None:
    print(f"[run_claude_code_print] {message}", flush=True)


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


def is_blocking_invalid_run(run_dir: Path) -> bool:
    metadata_path = run_dir / "metadata.json"
    if not metadata_path.exists():
        return False
    metadata = read_json(metadata_path)
    if metadata.get("archive_status"):
        return False
    return metadata.get("run_validity") == "invalid" or metadata.get("status") == "completed_invalid"


def next_run_id(root: Path) -> str:
    with (root / RUN_PLAN).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            run_dir = root / "runs" / "raw" / row["run_id"]
            if is_blocking_invalid_run(run_dir):
                raise SystemExit(
                    f"blocking invalid run exists: {row['run_id']}. "
                    "Inspect/archive it before continuing with --next."
                )
            if not is_completed_production_run(run_dir):
                return row["run_id"]
    raise SystemExit("all planned runs are completed")


def ensure_prepared(root: Path, run_id: str) -> Path:
    run_dir = root / "runs" / "raw" / run_id
    if not run_dir.exists():
        status(f"preparing {run_id}")
        run(["python", "scripts/prepare_run.py", "--run-id", run_id], cwd=root)
    else:
        status(f"using existing prepared run {run_id}")
    metadata = read_json(run_dir / "metadata.json")
    worktree = root / metadata["worktree"]
    if not worktree.exists():
        raise SystemExit(f"missing worktree after preparation: {worktree}")
    status(f"worktree ready: {worktree}")
    return run_dir


def update_metadata_for_print_mode(run_dir: Path, transcript_path: Path) -> None:
    metadata_path = run_dir / "metadata.json"
    metadata = read_json(metadata_path)
    metadata["execution_mode"] = "claude-code-print"
    metadata["transcript"] = str(transcript_path.relative_to(run_dir))
    write_json(metadata_path, metadata)


def event_text_fragments(line: str) -> list[str]:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return [line]

    fragments: list[str] = []
    for key in ("text", "content", "message", "delta"):
        value = event.get(key)
        if isinstance(value, str):
            fragments.append(value)
        elif isinstance(value, dict):
            fragments.extend(_text_from_value(value))
        elif isinstance(value, list):
            for item in value:
                fragments.extend(_text_from_value(item))
    return fragments


def _text_from_value(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        fragments: list[str] = []
        for key in ("text", "content", "message", "delta"):
            item = value.get(key)
            if isinstance(item, str):
                fragments.append(item)
            elif isinstance(item, dict | list):
                fragments.extend(_text_from_value(item))
        return fragments
    if isinstance(value, list):
        fragments: list[str] = []
        for item in value:
            fragments.extend(_text_from_value(item))
        return fragments
    return []


def stream_pipe(
    pipe,
    transcript,
    label: str,
    stop_hits: list[str],
    echo_text: bool,
) -> None:
    for line in pipe:
        transcript.write(line)
        transcript.flush()
        fragments = event_text_fragments(line) if label == "stdout" else [line]
        for fragment in fragments:
            if not fragment:
                continue
            if echo_text:
                print(fragment, end="" if fragment.endswith("\n") else "\n", flush=True)
            if STOP_CONDITION_RE.search(fragment):
                stop_hits.append(fragment.strip())
                print(
                    f"\n[run_claude_code_print] STOP-CONDITION ALERT from Claude output: {fragment.strip()}\n",
                    file=sys.stderr,
                    flush=True,
                )


def execute_claude(run_dir: Path, worktree: Path, permission_mode: str) -> int:
    prompt = (run_dir / "prompt.md").read_text(encoding="utf-8")
    transcripts = run_dir / "transcripts"
    transcripts.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace(":", "")
    stdout_path = transcripts / f"claude-print-{timestamp}.stream.jsonl"
    stderr_path = transcripts / f"claude-print-{timestamp}.stderr.txt"
    result_path = transcripts / f"claude-print-{timestamp}.json"

    command = [
        "claude",
        "-p",
        "--permission-mode",
        permission_mode,
        "--dangerously-skip-permissions",
        "--verbose",
        "--output-format",
        "stream-json",
        "--include-partial-messages",
    ]
    status(f"waiting for Claude Code print-mode execution in {worktree}")
    process = subprocess.Popen(
        command,
        cwd=worktree,
        stdin=subprocess.PIPE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )
    if process.stdin is None:
        raise RuntimeError("failed to open Claude stdin")
    process.stdin.write(prompt)
    process.stdin.close()
    stop_hits: list[str] = []
    with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open("w", encoding="utf-8") as stderr_file:
        stdout_thread = threading.Thread(
            target=stream_pipe,
            args=(process.stdout, stdout_file, "stdout", stop_hits, True),
        )
        stderr_thread = threading.Thread(
            target=stream_pipe,
            args=(process.stderr, stderr_file, "stderr", stop_hits, True),
        )
        stdout_thread.start()
        stderr_thread.start()
        returncode = process.wait()
        stdout_thread.join()
        stderr_thread.join()

    status(f"Claude Code finished with return code {returncode}")
    write_json(
        result_path,
        {
            "command": " ".join(command),
            "working_directory": str(worktree),
            "returncode": returncode,
            "stdout": str(stdout_path.relative_to(run_dir)),
            "stderr": str(stderr_path.relative_to(run_dir)),
            "stop_condition_alerted": bool(stop_hits),
            "stop_condition_matches": stop_hits,
        },
    )
    update_metadata_for_print_mode(run_dir, result_path)
    return returncode


def capture(root: Path, run_id: str) -> int:
    status(f"capturing {run_id}")
    result = run(["python", "scripts/capture_run.py", "--run-id", run_id], cwd=root, check=False)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    status(f"capture finished with return code {result.returncode}")
    return result.returncode


def commit_and_push(root: Path, run_id: str, push: bool) -> None:
    status(f"staging raw artifacts for {run_id}")
    run(["git", "add", f"runs/raw/{run_id}"], cwd=root)
    working_tree_status = run(["git", "status", "--short"], cwd=root).stdout.strip()
    if not working_tree_status:
        print("no changes to commit")
        return
    status(f"committing {run_id}")
    run(["git", "commit", "-m", f"Capture {run_id}"], cwd=root)
    if push:
        status("pushing main")
        run(["git", "push", "origin", "main"], cwd=root)
        status("push finished")


def main() -> int:
    parser = argparse.ArgumentParser()
    run_selector = parser.add_mutually_exclusive_group(required=True)
    run_selector.add_argument("--run-id")
    run_selector.add_argument("--next", action="store_true")
    parser.add_argument("--permission-mode", default="bypassPermissions")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    run_id = next_run_id(root) if args.next else args.run_id
    status(f"selected run: {run_id}")
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
