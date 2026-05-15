# Benchmark Run Prompt

Run ID: `task-1-claude-code-baseline-r3`
Agent: `claude-code`
Condition: `baseline`
Task: `task-1` / `input-validation`
Start tag: `task-1-start`

## Task Specification

# Task 1: Input Validation

## Description

Add a function `validate_email(email: str) -> bool` to `src/api/validators.py` that returns `True` if the email is well-formed and `False` otherwise. Add corresponding tests in `tests/test_validators.py`.

## Allowed Files

- `src/api/validators.py`
- `tests/test_validators.py`

## Drift Surface

- `src/api/routes/auth.py`
- `src/api/middleware.py`

## Verification

- `pytest tests/test_validators.py`
- `pytest`

## Condition Template

# Baseline Prompt Template

Use this template for Baseline condition runs.

```text
You are working in a small Python + JavaScript hybrid project. The backend code lives under src/, backend tests live under tests/, and frontend code lives under frontend/.

Task:
Add a function `validate_email(email: str) -> bool` to `src/api/validators.py` that returns `True` if the email is well-formed and `False` otherwise. Add corresponding tests in `tests/test_validators.py`.

Relevant files:
- `src/api/validators.py`
- `tests/test_validators.py`

Suggested verification:
- `pytest tests/test_validators.py`
- `pytest`

Please complete the task and run the relevant tests when you are done.
```

The baseline condition may mention relevant files and tests, but it must not include the Next-Prompt Protocol scaffold, manifest, slice lock, evidence trio requirement, or explicit stop-condition machinery.
