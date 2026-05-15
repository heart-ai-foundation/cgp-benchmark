#!/usr/bin/env python3
"""Run one planned Codex extension cell and capture artifacts."""

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


RUN_PLAN = Path("runs/agent_extension_run_plan.csv")
STOP_CONDITION_RE = re.compile(
    r"(stop condition|stopping per|protocol conflict|load-bearing disagreement|manifest.*disagree|lock.*disagree|active protocol.*disagree)",
    re.IGNORECASE,
)


def run(command: list[str], cwd: Path, check: bool = True, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=check, input=stdin, text=True, capture_output=True)


def status(message: str) -> None:
    print(f"[run_codex_exec] {message}", flush=True)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def is_completed_run(run_dir: Path) -> bool:
    metadata_path = run_dir / "metadata.json"
    if not metadata_path.exists():
        return False
    metadata = read_json(metadata_path)
    if metadata.get("archive_status"):
        return False
    return metadata.get("status") in {"completed_valid", "completed_invalid"} and metadata.get("run_validity") in {"valid", "invalid"}


def next_run_id(root: Path) -> str:
    with (root / RUN_PLAN).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["agent"] != "codex":
                continue
            run_dir = root / "runs" / "raw" / row["run_id"]
            if not is_completed_run(run_dir):
                return row["run_id"]
    raise SystemExit("all Codex extension runs are completed")


def ensure_prepared(root: Path, run_id: str) -> Path:
    run_dir = root / "runs" / "raw" / run_id
    if not run_dir.exists():
        status(f"preparing {run_id}")
        run(["python", "scripts/prepare_run.py", "--run-id", run_id, "--run-plan", str(RUN_PLAN)], cwd=root)
    else:
        status(f"using existing prepared run {run_id}")
    metadata = read_json(run_dir / "metadata.json")
    worktree = root / metadata["worktree"]
    if not worktree.exists():
        raise SystemExit(f"missing worktree after preparation: {worktree}")
    status(f"worktree ready: {worktree}")
    return run_dir


def text_fragments(line: str) -> list[str]:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return [line]
    fragments: list[str] = []
    for value in event.values():
        fragments.extend(text_from_value(value))
    return fragments


def text_from_value(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        fragments: list[str] = []
        for item in value:
            fragments.extend(text_from_value(item))
        return fragments
    if isinstance(value, dict):
        fragments: list[str] = []
        for item in value.values():
            fragments.extend(text_from_value(item))
        return fragments
    return []


def stream_pipe(pipe, transcript, label: str, stop_hits: list[str]) -> None:
    for line in pipe:
        transcript.write(line)
        transcript.flush()
        fragments = text_fragments(line) if label == "stdout" else [line]
        for fragment in fragments:
            if not fragment:
                continue
            print(fragment, end="" if fragment.endswith("\n") else "\n", flush=True)
            if STOP_CONDITION_RE.search(fragment):
                stop_hits.append(fragment.strip())
                print(f"\n[run_codex_exec] STOP-CONDITION ALERT: {fragment.strip()}\n", file=sys.stderr, flush=True)


def update_metadata(run_dir: Path, transcript_path: Path) -> None:
    metadata_path = run_dir / "metadata.json"
    metadata = read_json(metadata_path)
    metadata["execution_mode"] = "codex-exec"
    metadata["transcript"] = str(transcript_path.relative_to(run_dir))
    write_json(metadata_path, metadata)


def execute_codex(run_dir: Path, worktree: Path, sandbox: str, approval: str) -> int:
    prompt = (run_dir / "prompt.md").read_text(encoding="utf-8")
    transcripts = run_dir / "transcripts"
    transcripts.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace(":", "")
    stdout_path = transcripts / f"codex-{timestamp}.stdout.jsonl"
    stderr_path = transcripts / f"codex-{timestamp}.stderr.txt"
    last_message_path = transcripts / f"codex-{timestamp}.last-message.txt"
    result_path = transcripts / f"codex-{timestamp}.json"
    command = [
        "codex",
        "exec",
        "--cd",
        str(worktree),
        "--sandbox",
        sandbox,
        "--ask-for-approval",
        approval,
        "--json",
        "--output-last-message",
        str(last_message_path),
        "-",
    ]

    status(f"waiting for Codex exec in {worktree}")
    process = subprocess.Popen(
        command,
        cwd=worktree,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    if process.stdin is None:
        raise RuntimeError("failed to open Codex stdin")
    process.stdin.write(prompt)
    process.stdin.close()
    stop_hits: list[str] = []
    with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open("w", encoding="utf-8") as stderr_file:
        stdout_thread = threading.Thread(target=stream_pipe, args=(process.stdout, stdout_file, "stdout", stop_hits))
        stderr_thread = threading.Thread(target=stream_pipe, args=(process.stderr, stderr_file, "stderr", stop_hits))
        stdout_thread.start()
        stderr_thread.start()
        returncode = process.wait()
        stdout_thread.join()
        stderr_thread.join()

    status(f"Codex exec finished with return code {returncode}")
    write_json(
        result_path,
        {
            "command": " ".join(command),
            "working_directory": str(worktree),
            "returncode": returncode,
            "stdout": str(stdout_path.relative_to(run_dir)),
            "stderr": str(stderr_path.relative_to(run_dir)),
            "last_message": str(last_message_path.relative_to(run_dir)),
            "stop_condition_alerted": bool(stop_hits),
            "stop_condition_matches": stop_hits,
        },
    )
    update_metadata(run_dir, result_path)
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
    if not run(["git", "status", "--short"], cwd=root).stdout.strip():
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
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--run-id")
    selector.add_argument("--next", action="store_true")
    parser.add_argument("--sandbox", default="workspace-write", choices=["read-only", "workspace-write", "danger-full-access"])
    parser.add_argument("--ask-for-approval", default="never", choices=["untrusted", "on-failure", "on-request", "never"])
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    run_id = next_run_id(root) if args.next else args.run_id
    status(f"selected run: {run_id}")
    run_dir = ensure_prepared(root, run_id)
    metadata = read_json(run_dir / "metadata.json")
    worktree = root / metadata["worktree"]

    codex_returncode = execute_codex(run_dir, worktree, args.sandbox, args.ask_for_approval)
    capture_returncode = capture(root, run_id)
    if args.commit:
        commit_and_push(root, run_id, args.push)
    if codex_returncode != 0:
        print(f"codex exited nonzero: {codex_returncode}")
    return capture_returncode if capture_returncode != 0 else codex_returncode


if __name__ == "__main__":
    raise SystemExit(main())
