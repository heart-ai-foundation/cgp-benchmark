#!/usr/bin/env python3
"""Generate a deterministic multi-agent extension run plan."""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

from generate_run_plan import CONDITIONS, FIELDNAMES, REPLICATIONS, SEED, TASKS


EXTENSION_AGENTS = ["codex", "gemini-cli"]
PLAN_PATH = Path("runs/agent_extension_run_plan.csv")
METADATA_PATH = Path("runs/agent_extension_run_plan_metadata.json")


def generate_rows() -> list[dict[str, str | int]]:
    rng = random.Random(SEED)
    rows: list[dict[str, str | int]] = []
    run_order = 1

    for agent in EXTENSION_AGENTS:
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
    with (root / PLAN_PATH).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "seed": SEED,
        "extension_type": "multi-agent companion benchmark",
        "agents": EXTENSION_AGENTS,
        "conditions": CONDITIONS,
        "replications": REPLICATIONS,
        "tasks": [task.__dict__ for task in TASKS],
        "run_count": len(rows),
        "relationship_to_primary_plan": "Extension plan; do not pool with primary preregistered 72-run analysis unless reported as an amended or companion analysis.",
        "randomization": {
            "task_order": "shuffled within each agent platform",
            "condition_order": "shuffled within each task-agent pair",
            "replication_order": "replications executed in ascending order within task-agent pair",
        },
    }
    (root / METADATA_PATH).write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def validate(root: Path) -> list[str]:
    expected = [{key: str(value) for key, value in row.items()} for row in generate_rows()]
    problems: list[str] = []
    plan_path = root / PLAN_PATH
    metadata_path = root / METADATA_PATH
    if not plan_path.exists():
        problems.append(f"{PLAN_PATH} is missing")
        return problems
    if not metadata_path.exists():
        problems.append(f"{METADATA_PATH} is missing")
        return problems
    with plan_path.open(newline="", encoding="utf-8") as handle:
        actual = list(csv.DictReader(handle))
    if actual != expected:
        problems.append(f"{PLAN_PATH} does not match deterministic generation")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("agents") != EXTENSION_AGENTS:
        problems.append(f"{METADATA_PATH} has the wrong agents")
    if metadata.get("run_count") != len(expected):
        problems.append(f"{METADATA_PATH} has the wrong run count")
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
        print("extension run plan is valid")
        return 0

    write_outputs(root)
    print(f"wrote {PLAN_PATH} and {METADATA_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
