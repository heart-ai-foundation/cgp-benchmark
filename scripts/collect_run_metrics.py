#!/usr/bin/env python3
"""Collect basic benchmark run metrics from a git diff."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def changed_files(repo: Path, base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=repo,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
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
