#!/usr/bin/env python3
"""Run one planned Aider cell and capture artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import threading
from datetime import UTC, datetime
from pathlib import Path

from stop_condition_alerts import is_stop_condition_alert


RUN_PLAN = Path("runs/run_plan.csv")


def run(command: list[str], cwd: Path, check: bool = True, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=check, input=stdin, text=True, capture_output=True)


def status(message: str) -> None:
    print(f"[run_aider] {message}", flush=True)


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
            if row["agent"] != "aider":
                continue
            run_dir = root / "runs" / "raw" / row["run_id"]
            if not is_completed_run(run_dir):
                return row["run_id"]
    raise SystemExit("all Aider primary runs are completed")


def run_agent(root: Path, run_id: str) -> str:
    with (root / RUN_PLAN).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["run_id"] == run_id:
                return row["agent"]
    raise SystemExit(f"unknown run_id: {run_id}")


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


def stream_pipe(pipe, transcript, label: str, stop_hits: list[str]) -> None:
    for line in pipe:
        transcript.write(line)
        transcript.flush()
        print(line, end="", flush=True)
        if is_stop_condition_alert(line):
            stop_hits.append(line.strip())
            print(f"\n[run_aider] STOP-CONDITION ALERT: {line.strip()}\n", file=sys.stderr, flush=True)


def update_metadata(run_dir: Path, transcript_path: Path, model: str | None) -> None:
    metadata_path = run_dir / "metadata.json"
    metadata = read_json(metadata_path)
    metadata["execution_mode"] = "aider-message-file"
    metadata["transcript"] = str(transcript_path.relative_to(run_dir))
    if model:
        metadata["aider_model"] = model
    write_json(metadata_path, metadata)


def execute_aider(run_dir: Path, worktree: Path, model: str | None, timeout: int | None) -> int:
    prompt_path = run_dir / "prompt.md"
    transcripts = run_dir / "transcripts"
    transcripts.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace(":", "")
    stdout_path = transcripts / f"aider-{timestamp}.stdout.txt"
    stderr_path = transcripts / f"aider-{timestamp}.stderr.txt"
    llm_history_path = transcripts / f"aider-{timestamp}.llm-history.txt"
    chat_history_path = transcripts / f"aider-{timestamp}.chat-history.md"
    result_path = transcripts / f"aider-{timestamp}.json"

    command = [
        "aider",
        "--message-file",
        str(prompt_path.resolve()),
        "--yes-always",
        "--no-pretty",
        "--no-stream",
        "--no-check-update",
        "--no-show-model-warnings",
        "--no-gitignore",
        "--llm-history-file",
        str(llm_history_path.resolve()),
        "--chat-history-file",
        str(chat_history_path.resolve()),
    ]
    if model:
        command.extend(["--model", model])

    env = os.environ.copy()
    env["AIDER_ANALYTICS_DISABLE"] = "true"

    status(f"waiting for Aider execution in {worktree}")
    process = subprocess.Popen(
        command,
        cwd=worktree,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=env,
    )
    stop_hits: list[str] = []
    with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open("w", encoding="utf-8") as stderr_file:
        stdout_thread = threading.Thread(target=stream_pipe, args=(process.stdout, stdout_file, "stdout", stop_hits))
        stderr_thread = threading.Thread(target=stream_pipe, args=(process.stderr, stderr_file, "stderr", stop_hits))
        stdout_thread.start()
        stderr_thread.start()
        try:
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            returncode = process.wait()
            stop_hits.append(f"aider timed out after {timeout} seconds")
        stdout_thread.join()
        stderr_thread.join()

    status(f"Aider finished with return code {returncode}")
    write_json(
        result_path,
        {
            "command": " ".join(command),
            "working_directory": str(worktree),
            "returncode": returncode,
            "stdout": str(stdout_path.relative_to(run_dir)),
            "stderr": str(stderr_path.relative_to(run_dir)),
            "llm_history": str(llm_history_path.relative_to(run_dir)),
            "chat_history": str(chat_history_path.relative_to(run_dir)),
            "stop_condition_alerted": bool(stop_hits),
            "stop_condition_matches": stop_hits,
        },
    )
    update_metadata(run_dir, result_path, model)
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
    parser.add_argument("--model", default=os.environ.get("AIDER_MODEL"))
    parser.add_argument("--timeout", type=int, default=None)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    run_id = next_run_id(root) if args.next else args.run_id
    agent = run_agent(root, run_id)
    if agent != "aider":
        raise SystemExit(f"refusing to run {run_id} with Aider runner because planned agent is {agent}")
    status(f"selected run: {run_id}")
    run_dir = ensure_prepared(root, run_id)
    metadata = read_json(run_dir / "metadata.json")
    worktree = root / metadata["worktree"]

    aider_returncode = execute_aider(run_dir, worktree, args.model, args.timeout)
    capture_returncode = capture(root, run_id)
    if args.commit:
        commit_and_push(root, run_id, args.push)
    if aider_returncode != 0:
        print(f"aider exited nonzero: {aider_returncode}")
    return capture_returncode if capture_returncode != 0 else aider_returncode


if __name__ == "__main__":
    raise SystemExit(main())
