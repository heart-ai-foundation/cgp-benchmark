#!/usr/bin/env python3
"""Generate and validate the CGP benchmark run plan."""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path


SEED = 20260515
AGENTS = ["claude-code", "aider"]
CONDITIONS = ["baseline", "cgp"]
REPLICATIONS = [1, 2, 3]


@dataclass(frozen=True)
class Task:
    task_id: str
    slug: str
    complexity: str
    start_tag: str
    spec_path: str


TASKS = [
    Task("task-1", "input-validation", "simple", "task-1-start", "docs/task_specs/task-1-input-validation.md"),
    Task("task-2", "user-docstring", "simple", "task-2-start", "docs/task_specs/task-2-user-docstring.md"),
    Task("task-3", "user-items-endpoint", "medium", "task-3-start", "docs/task_specs/task-3-user-items-endpoint.md"),
    Task("task-4", "parse-config-refactor", "medium", "task-4-start", "docs/task_specs/task-4-parse-config-refactor.md"),
    Task("task-5", "favorite-items", "complex", "task-5-start", "docs/task_specs/task-5-favorite-items.md"),
    Task("task-6", "login-empty-password", "complex", "task-6-start", "docs/task_specs/task-6-login-empty-password.md"),
]


FIELDNAMES = [
    "run_order",
    "run_id",
    "agent",
    "task_id",
    "task_slug",
    "task_complexity",
    "condition",
    "replication",
    "condition_order_within_pair",
    "start_tag",
    "task_spec",
]


def generate_rows() -> list[dict[str, str | int]]:
    rng = random.Random(SEED)
    rows: list[dict[str, str | int]] = []
    run_order = 1

    for agent in AGENTS:
        agent_tasks = list(TASKS)
        rng.shuffle(agent_tasks)
        for task in agent_tasks:
            condition_order = list(CONDITIONS)
            rng.shuffle(condition_order)
            condition_order_label = "-then-".join(condition_order)
            for replication in REPLICATIONS:
                for condition in condition_order:
                    rows.append(
                        {
                            "run_order": run_order,
                            "run_id": f"{task.task_id}-{agent}-{condition}-r{replication}",
                            "agent": agent,
                            "task_id": task.task_id,
                            "task_slug": task.slug,
                            "task_complexity": task.complexity,
                            "condition": condition,
                            "replication": replication,
                            "condition_order_within_pair": condition_order_label,
                            "start_tag": task.start_tag,
                            "task_spec": task.spec_path,
                        }
                    )
                    run_order += 1

    return rows


def write_outputs(root: Path) -> None:
    rows = generate_rows()
    run_plan_path = root / "runs" / "run_plan.csv"
    metadata_path = root / "runs" / "run_plan_metadata.json"

    with run_plan_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "seed": SEED,
        "agents": AGENTS,
        "conditions": CONDITIONS,
        "replications": REPLICATIONS,
        "tasks": [task.__dict__ for task in TASKS],
        "run_count": len(rows),
        "randomization": {
            "task_order": "shuffled within each agent platform",
            "condition_order": "shuffled within each task-agent pair",
            "replication_order": "replications executed in ascending order within task-agent pair",
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def validate(root: Path) -> list[str]:
    expected = generate_rows()
    run_plan_path = root / "runs" / "run_plan.csv"
    metadata_path = root / "runs" / "run_plan_metadata.json"
    problems: list[str] = []

    if not run_plan_path.exists():
        problems.append("runs/run_plan.csv is missing")
        return problems
    if not metadata_path.exists():
        problems.append("runs/run_plan_metadata.json is missing")
        return problems

    with run_plan_path.open(newline="", encoding="utf-8") as handle:
        actual = list(csv.DictReader(handle))

    normalized_expected = [
        {key: str(value) for key, value in row.items()}
        for row in expected
    ]
    if actual != normalized_expected:
        problems.append("runs/run_plan.csv does not match deterministic generation")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("seed") != SEED:
        problems.append("run_plan_metadata.json has the wrong seed")
    if metadata.get("run_count") != 72:
        problems.append("run_plan_metadata.json does not record 72 runs")
    if len(actual) != 72:
        problems.append(f"run_plan.csv has {len(actual)} rows, expected 72")

    run_ids = [row["run_id"] for row in actual]
    if len(set(run_ids)) != len(run_ids):
        problems.append("run_plan.csv contains duplicate run_id values")

    required_cells = {
        (task.task_id, agent, condition, str(replication))
        for task in TASKS
        for agent in AGENTS
        for condition in CONDITIONS
        for replication in REPLICATIONS
    }
    actual_cells = {
        (row["task_id"], row["agent"], row["condition"], row["replication"])
        for row in actual
    }
    if actual_cells != required_cells:
        problems.append("run_plan.csv does not cover the full task-agent-condition-replication grid")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()

    if args.check:
        problems = validate(root)
        if problems:
            for problem in problems:
                print(problem, file=sys.stderr)
            return 1
        print("run plan is valid")
        return 0

    write_outputs(root)
    print("wrote runs/run_plan.csv and runs/run_plan_metadata.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
