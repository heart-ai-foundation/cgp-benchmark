#!/usr/bin/env python3
"""Capture one completed benchmark run into runs/raw."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=check, text=True, capture_output=True)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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


def task_allowed_files(root: Path, metadata: dict) -> list[str]:
    spec = (root / metadata["task_spec"]).read_text(encoding="utf-8")
    return [benchmark_path(item) for item in markdown_list_items(extract_section(spec, "Allowed Files"))]


def verification_commands(root: Path, metadata: dict) -> list[dict[str, str]]:
    spec = (root / metadata["task_spec"]).read_text(encoding="utf-8")
    return [
        {"working_directory": "benchmark-repo", "command": item}
        for item in markdown_list_items(extract_section(spec, "Verification"))
    ]


def cgp_evidence_files(run_id: str) -> list[str]:
    return [
        f"notes/{run_id}-design.md",
        f"runs/{run_id}-run-record.json",
        f"evidence/{run_id}-evidence.json",
    ]


def changed_files(worktree: Path, base: str) -> list[str]:
    tracked = run(["git", "diff", "--name-only", base], cwd=worktree).stdout.splitlines()
    untracked = run(["git", "ls-files", "--others", "--exclude-standard"], cwd=worktree).stdout.splitlines()
    return sorted({item for item in tracked + untracked if item})


def diff_patch(worktree: Path, base: str, files: list[str]) -> str:
    parts = [run(["git", "diff", base], cwd=worktree).stdout]
    tracked = set(run(["git", "ls-files"], cwd=worktree).stdout.splitlines())
    for file in files:
        if file in tracked:
            continue
        result = run(["git", "diff", "--no-index", "--", "/dev/null", file], cwd=worktree, check=False)
        if result.stdout:
            parts.append(result.stdout)
    return "\n".join(part for part in parts if part)


def run_verification(worktree: Path, commands: list[dict[str, str]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for item in commands:
        cwd = worktree / item["working_directory"]
        completed = run(item["command"].split(), cwd=cwd, check=False)
        results.append(
            {
                "working_directory": item["working_directory"],
                "command": item["command"],
                "result": "passed" if completed.returncode == 0 else "failed",
                "returncode": completed.returncode,
                "stdout_tail": completed.stdout[-4000:],
                "stderr_tail": completed.stderr[-4000:],
            }
        )
    return results


def copy_evidence_trio(worktree: Path, run_dir: Path, run_id: str) -> int:
    copied = 0
    targets = {
        f"notes/{run_id}-design.md": run_dir / "evidence_trio" / "notes" / f"{run_id}-design.md",
        f"runs/{run_id}-run-record.json": run_dir / "evidence_trio" / "runs" / f"{run_id}-run-record.json",
        f"evidence/{run_id}-evidence.json": run_dir / "evidence_trio" / "evidence" / f"{run_id}-evidence.json",
    }
    for source_rel, target in targets.items():
        source = worktree / source_rel
        if not source.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied += 1
    return copied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-root", type=Path, default=Path("runs/raw"))
    args = parser.parse_args()

    root = Path.cwd()
    run_dir = args.run_root / args.run_id
    metadata_path = run_dir / "metadata.json"
    if not metadata_path.exists():
        raise SystemExit(f"missing metadata: {metadata_path}")

    metadata = read_json(metadata_path)
    worktree = root / metadata.get("worktree", "")
    if not worktree.exists():
        raise SystemExit(f"missing worktree: {worktree}")

    base = metadata["metrics_base_commit"]
    allowed = task_allowed_files(root, metadata)
    if metadata["condition"] == "cgp":
        allowed += cgp_evidence_files(args.run_id)

    files = changed_files(worktree, base)
    drift = [file for file in files if file not in set(allowed)]
    verification = run_verification(worktree, verification_commands(root, metadata))
    verification_success = all(item["result"] == "passed" for item in verification)
    work_submitted = len(files) > 0
    evidence_count = copy_evidence_trio(worktree, run_dir, args.run_id) if metadata["condition"] == "cgp" else 0
    evidence_complete = evidence_count == 3 if metadata["condition"] == "cgp" else None

    metrics = {
        "changed_files": files,
        "allowed_files": sorted(set(allowed)),
        "scope_drift_count": len(drift),
        "scope_drift_files": drift,
    }
    write_json(run_dir / "metrics.json", metrics)
    (run_dir / "diff.patch").write_text(diff_patch(worktree, base, files), encoding="utf-8")

    verification_payload = {
        "run_id": args.run_id,
        "metrics_base_commit": base,
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "post_run_verification": verification,
        "changed_files": files,
        "scope_drift_count": len(drift),
        "scope_drift_files": drift,
        "work_submitted": work_submitted,
        "verification_command_compliance": verification_success,
        "task_verification_success": verification_success,
        "evidence_trio_completeness": evidence_count if metadata["condition"] == "cgp" else None,
        "run_validity": "valid"
        if work_submitted and len(drift) == 0 and verification_success and (evidence_complete is not False)
        else "invalid",
    }
    write_json(run_dir / "verification.json", verification_payload)

    metadata.update(
        {
            "status": f"completed_{verification_payload['run_validity']}",
            "completed_at": verification_payload["verified_at"],
            "scope_drift_count": len(drift),
            "scope_drift_files": drift,
            "work_submitted": work_submitted,
            "verification_command_compliance": verification_success,
            "task_verification_success": verification_success,
            "evidence_trio_completeness": evidence_count if metadata["condition"] == "cgp" else None,
            "run_validity": verification_payload["run_validity"],
        }
    )
    write_json(metadata_path, metadata)

    print(f"captured {args.run_id}: {verification_payload['run_validity']}")
    print(f"changed_files={len(files)} scope_drift_count={len(drift)} verification_passed={verification_success}")
    if metadata["condition"] == "cgp":
        print(f"evidence_trio_completeness={evidence_count}/3")
    return 0 if verification_payload["run_validity"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
