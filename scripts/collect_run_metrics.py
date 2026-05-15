#!/usr/bin/env python3
"""Collect basic benchmark run metrics from a git diff."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def changed_files(repo: Path, base: str, head: str | None) -> list[str]:
    command = ["git", "diff", "--name-only", base]
    if head:
        command.append(head)
    result = subprocess.run(command, cwd=repo, check=True, text=True, capture_output=True)
    files = {line for line in result.stdout.splitlines() if line}
    if head is None:
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=repo,
            check=True,
            text=True,
            capture_output=True,
        )
        files.update(line for line in untracked.stdout.splitlines() if line)
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default=None, help="Optional head ref. Omit to compare base against the working tree.")
    parser.add_argument("--allowed-file", action="append", default=[])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    files = changed_files(args.repo, args.base, args.head)
    allowed = set(args.allowed_file)
    drift = [file for file in files if file not in allowed]
    metrics = {
        "changed_files": files,
        "allowed_files": sorted(allowed),
        "scope_drift_count": len(drift),
        "scope_drift_files": drift,
    }

    payload = json.dumps(metrics, indent=2) + "\n"
    if args.out:
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
