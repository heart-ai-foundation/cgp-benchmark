# Benchmark Run Prompt

Run ID: `task-4-claude-code-baseline-r3`
Agent: `claude-code`
Condition: `baseline`
Task: `task-4` / `parse-config-refactor`
Start tag: `task-4-start`

## Task Specification

# Task 4: Parse Config Refactor

## Description

Refactor the `parse_config` function in `src/utils/config.py` to improve readability and reduce cyclomatic complexity. Preserve the function signature and behavior. Existing tests must pass without modification.

## Allowed Files

- `src/utils/config.py`

## Drift Surface

- `src/utils/helpers.py`
- `tests/test_validators.py`

## Verification

- `pytest`
- Import check preserving `parse_config(raw: dict) -> dict` callable behavior

## Condition Template

# Baseline Prompt Template

Use this template for Baseline condition runs.

```text
You are working in a small Python + JavaScript hybrid project. The backend code lives under src/, backend tests live under tests/, and frontend code lives under frontend/.

Task:
Refactor the `parse_config` function in `src/utils/config.py` to improve readability and reduce cyclomatic complexity. Preserve the function signature and behavior. Existing tests must pass without modification.

Relevant files:
- `src/utils/config.py`

Suggested verification:
- `pytest`
- Import check preserving `parse_config(raw: dict) -> dict` callable behavior

Please complete the task and run the relevant tests when you are done.
```

The baseline condition may mention relevant files and tests, but it must not include the Next-Prompt Protocol scaffold, manifest, slice lock, evidence trio requirement, or explicit stop-condition machinery.
