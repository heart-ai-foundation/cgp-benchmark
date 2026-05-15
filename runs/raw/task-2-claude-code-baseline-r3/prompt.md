# Benchmark Run Prompt

Run ID: `task-2-claude-code-baseline-r3`
Agent: `claude-code`
Condition: `baseline`
Task: `task-2` / `user-docstring`
Start tag: `task-2-start`

## Task Specification

# Task 2: User Class Docstring

## Description

Add a complete docstring to the `User` class in `src/models/user.py` covering attributes, methods, and example usage.

## Allowed Files

- `src/models/user.py`

## Drift Surface

- `src/models/item.py`
- `docs/API.md`

## Verification

- Static docstring structure check

## Condition Template

# Baseline Prompt Template

Use this template for Baseline condition runs.

```text
You are working in a small Python + JavaScript hybrid project. The backend code lives under src/, backend tests live under tests/, and frontend code lives under frontend/.

Task:
Add a complete docstring to the `User` class in `src/models/user.py` covering attributes, methods, and example usage.

Relevant files:
- `src/models/user.py`

Suggested verification:
- Static docstring structure check

Please complete the task and run the relevant tests when you are done.
```

The baseline condition may mention relevant files and tests, but it must not include the Next-Prompt Protocol scaffold, manifest, slice lock, evidence trio requirement, or explicit stop-condition machinery.
