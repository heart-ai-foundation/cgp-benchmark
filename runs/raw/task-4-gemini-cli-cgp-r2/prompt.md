# Benchmark Run Prompt

Run ID: `task-4-gemini-cli-cgp-r2`
Agent: `gemini-cli`
Condition: `cgp`
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

# CGP Prompt Template

Use this template for CGP condition runs.

```text
You are executing a Continuity-Governed Prompting run using the Next-Prompt Protocol scaffold.

Before acting, read these files in order:

1. next-prompt-protocols/.slice-lock.json
2. next-prompt-protocols/manifest.json
3. next-prompt-protocols/role-context.md
4. next-prompt-protocols/phases/phase-1/README.md
5. next-prompt-protocols/active/task-4-gemini-cli-cgp-r2.md
6. The task specification at docs/task_specs/task-4-parse-config-refactor.md

Execute only the active slice. Stay inside allowed files. Preserve non-goals. Run the named verification commands before declaring completion. If the manifest, lock, active protocol, task spec, or repository state disagree on a load-bearing detail, stop and report rather than improvising.

Before declaring completion, write the evidence trio named in the active protocol:

1. Design note
2. Run record
3. Evidence JSON

Task:
Refactor the `parse_config` function in `src/utils/config.py` to improve readability and reduce cyclomatic complexity. Preserve the function signature and behavior. Existing tests must pass without modification.
```

The CGP condition must include the same task content as Baseline while adding the operational scaffold: manifest, slice lock, role context, active protocol, explicit scope, verification, stop condition, and evidence requirements.
