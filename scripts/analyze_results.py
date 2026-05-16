#!/usr/bin/env python3
"""Build processed analysis tables from benchmark raw run records."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


PRIMARY_PLAN = Path("runs/run_plan.csv")
EXTENSION_PLAN = Path("runs/agent_extension_run_plan.csv")
RAW_ROOT = Path("runs/raw")
OUT_ROOT = Path("runs/processed")


@dataclass(frozen=True)
class PlannedRun:
    run_id: str
    dataset: str
    agent: str
    task_id: str
    task_slug: str
    task_complexity: str
    condition: str
    replication: int
    run_order: int


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_plan(path: Path, dataset: str) -> list[PlannedRun]:
    runs: list[PlannedRun] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            runs.append(
                PlannedRun(
                    run_id=row["run_id"],
                    dataset=dataset,
                    agent=row["agent"],
                    task_id=row["task_id"],
                    task_slug=row["task_slug"],
                    task_complexity=row["task_complexity"],
                    condition=row["condition"],
                    replication=int(row["replication"]),
                    run_order=int(row["run_order"]),
                )
            )
    return runs


def bool_int(value: object) -> int | None:
    if value is None:
        return None
    return 1 if bool(value) else 0


def load_run(plan: PlannedRun) -> dict:
    run_dir = RAW_ROOT / plan.run_id
    metadata_path = run_dir / "metadata.json"
    metrics_path = run_dir / "metrics.json"
    verification_path = run_dir / "verification.json"

    if not metadata_path.exists():
        return {
            **plan.__dict__,
            "record_status": "missing",
            "status": "",
            "run_validity": "",
            "completed": 0,
        }

    metadata = read_json(metadata_path)
    metrics = read_json(metrics_path) if metrics_path.exists() else {}
    verification = read_json(verification_path) if verification_path.exists() else {}
    changed_files = metrics.get("changed_files", verification.get("changed_files", []))
    drift_files = metadata.get("scope_drift_files", verification.get("scope_drift_files", metrics.get("scope_drift_files", [])))
    completed = (
        metadata.get("status") in {"completed_valid", "completed_invalid"}
        and metadata.get("run_validity") in {"valid", "invalid"}
    )

    return {
        **plan.__dict__,
        "record_status": "completed" if completed else "prepared",
        "status": metadata.get("status", ""),
        "run_validity": metadata.get("run_validity", ""),
        "completed": int(completed),
        "valid": 1 if metadata.get("run_validity") == "valid" else 0,
        "invalid": 1 if metadata.get("run_validity") == "invalid" else 0,
        "execution_mode": metadata.get("execution_mode", ""),
        "completed_at": metadata.get("completed_at", ""),
        "work_submitted": bool_int(metadata.get("work_submitted")),
        "task_success": bool_int(metadata.get("task_verification_success")),
        "verification_compliance": bool_int(metadata.get("verification_command_compliance")),
        "scope_drift_count": metadata.get("scope_drift_count", len(drift_files)),
        "scope_drift_any": 1 if metadata.get("scope_drift_count", len(drift_files)) > 0 else 0,
        "scope_drift_files": ";".join(drift_files),
        "changed_file_count": len(changed_files),
        "changed_files": ";".join(changed_files),
        "evidence_trio_completeness": metadata.get("evidence_trio_completeness"),
        "evidence_trio_complete": 1
        if plan.condition == "cgp" and metadata.get("evidence_trio_completeness") == 3
        else (None if plan.condition != "cgp" else 0),
        "transcript": metadata.get("transcript", ""),
    }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def rate(values: list[int | None]) -> float | None:
    usable = [value for value in values if value is not None]
    if not usable:
        return None
    return mean(usable)


def summarize(rows: list[dict], group_fields: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("completed") != 1:
            continue
        key = tuple(row[field] for field in group_fields)
        groups[key].append(row)

    summaries: list[dict] = []
    for key, items in sorted(groups.items()):
        out = {field: value for field, value in zip(group_fields, key, strict=True)}
        n = len(items)
        out.update(
            {
                "n": n,
                "valid_n": sum(int(item.get("valid") or 0) for item in items),
                "valid_rate": rate([item.get("valid") for item in items]),
                "invalid_n": sum(int(item.get("invalid") or 0) for item in items),
                "work_submitted_rate": rate([item.get("work_submitted") for item in items]),
                "task_success_rate": rate([item.get("task_success") for item in items]),
                "verification_compliance_rate": rate([item.get("verification_compliance") for item in items]),
                "scope_drift_any_rate": rate([item.get("scope_drift_any") for item in items]),
                "mean_scope_drift_count": mean([int(item.get("scope_drift_count") or 0) for item in items]),
                "mean_changed_file_count": mean([int(item.get("changed_file_count") or 0) for item in items]),
            }
        )
        evidence_values = [item.get("evidence_trio_complete") for item in items if item.get("condition") == "cgp"]
        if evidence_values:
            out["evidence_trio_complete_rate"] = rate(evidence_values)
        summaries.append(out)
    return summaries


def main() -> int:
    plans = read_plan(PRIMARY_PLAN, "primary") + read_plan(EXTENSION_PLAN, "extension")
    rows = [load_run(plan) for plan in plans]

    run_fields = [
        "dataset",
        "run_order",
        "run_id",
        "agent",
        "task_id",
        "task_slug",
        "task_complexity",
        "condition",
        "replication",
        "record_status",
        "status",
        "run_validity",
        "completed",
        "valid",
        "invalid",
        "execution_mode",
        "work_submitted",
        "task_success",
        "verification_compliance",
        "scope_drift_count",
        "scope_drift_any",
        "scope_drift_files",
        "changed_file_count",
        "changed_files",
        "evidence_trio_completeness",
        "evidence_trio_complete",
        "completed_at",
        "transcript",
    ]
    write_csv(OUT_ROOT / "run_level_metrics.csv", rows, run_fields)

    completed_rows = [row for row in rows if row.get("completed") == 1]
    summary_specs = {
        "summary_by_dataset_agent_condition.csv": ["dataset", "agent", "condition"],
        "summary_by_agent_condition.csv": ["agent", "condition"],
        "summary_by_task_agent_condition.csv": ["task_id", "task_slug", "agent", "condition"],
        "summary_by_dataset_condition.csv": ["dataset", "condition"],
        "summary_by_condition.csv": ["condition"],
    }
    for filename, fields in summary_specs.items():
        summary = summarize(completed_rows, fields)
        summary_fields = fields + [
            "n",
            "valid_n",
            "valid_rate",
            "invalid_n",
            "work_submitted_rate",
            "task_success_rate",
            "verification_compliance_rate",
            "scope_drift_any_rate",
            "mean_scope_drift_count",
            "mean_changed_file_count",
            "evidence_trio_complete_rate",
        ]
        write_csv(OUT_ROOT / filename, summary, summary_fields)

    manifest = {
        "planned_runs": len(plans),
        "completed_runs": len(completed_rows),
        "missing_or_prepared_runs": len(plans) - len(completed_rows),
        "primary_completed_runs": sum(1 for row in completed_rows if row["dataset"] == "primary"),
        "extension_completed_runs": sum(1 for row in completed_rows if row["dataset"] == "extension"),
        "archived_invalid_harness_records_excluded": len(list((RAW_ROOT / "invalid").glob("*/metadata.json"))),
        "outputs": sorted(path.name for path in OUT_ROOT.glob("*.csv")),
    }
    (OUT_ROOT / "analysis_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
