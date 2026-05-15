# Design Note - task-1-claude-code-cgp-r3

## Run identity

- Run ID: `task-1-claude-code-cgp-r3`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-1` / `input-validation`
- Start anchor commit: `2614dd699ae0c27e2d63ae30b18d349951c7a4c5`
- HEAD at execution: `1185ddbf9ebb8df251747986be8ad24c50aa85fc` (setup scaffold commit; `metrics_base_commit`)

## Objective

Add `validate_email(email: str) -> bool` to `src/api/validators.py` and corresponding tests
to `tests/test_validators.py`. Return `True` for well-formed addresses, `False` otherwise.

## Scope

In-scope (per slice lock `allowed_files`):

- `benchmark-repo/src/api/validators.py`
- `benchmark-repo/tests/test_validators.py`
- `notes/task-1-claude-code-cgp-r3-design.md` (this file)
- `runs/task-1-claude-code-cgp-r3-run-record.json`
- `evidence/task-1-claude-code-cgp-r3-evidence.json`

Drift surface monitored but untouched: `src/api/routes/auth.py`, `src/api/middleware.py`.

## Approach

Email well-formedness is checked with a single compiled regex plus length/structural
guards. The regex enforces:

- A local part composed of one or more dot-separated atoms drawn from the RFC 5322
  unquoted set (`A-Z a-z 0-9` plus `! # $ % & ' * + / = ? ^ _ ` { | } ~ -`). Leading,
  trailing, and consecutive dots are rejected because dot-atoms must be separated by
  exactly one dot.
- A domain of two or more dot-separated labels, each `1-63` chars, starting and ending
  with an alphanumeric and otherwise allowing `-`. This rejects bare-TLD addresses such
  as `user@domain` and labels with leading/trailing hyphens.

Pre-checks before the regex catch the failure modes that are awkward to encode in a
single pattern: non-string inputs, the overall 254-char ceiling, the 64-char local-part
ceiling, and double-dot sequences in either half.

This is intentionally a lightweight syntactic validator, not a full RFC 5322 parser:
quoted local parts, IP-address literals, and internationalized domain names are out
of scope for this task and are treated as invalid. The function is total (no
exceptions) and side-effect free.

## Tests

`tests/test_validators.py` adds three parametrized cases on top of the existing tests:

- Positive cases covering plain, dotted, plus-tagged, subdomain, short, and numeric forms.
- Negative cases covering empty/missing `@`, missing local or domain, missing TLD,
  bare TLD, double `@`, embedded whitespace, double-dot in domain or local, leading or
  trailing dot in local, leading or trailing hyphen on a domain label, and length
  ceiling violations on both halves.
- Non-string inputs (`None`, `int`, `list`, `dict`, `bytes`) return `False`.

## Verification snapshot

- `cd benchmark-repo && pytest tests/test_validators.py` -> `33 passed`
- `cd benchmark-repo && pytest` -> `39 passed`

Baseline before changes: 9 tests passed. Delta: +30 (all new tests are `validate_email` cases).

## Non-goals honored

- No edits to `src/api/routes/auth.py` or `src/api/middleware.py` (drift surface).
- No edits to run-plan, preregistration, scaffold, analysis, or other repo files.
- No adjacent refactors of `require_non_empty` or `validate_positive_int`.
- Only addition to imports is `re`, required by the new function.

## Stop-condition check

Manifest, slice lock, active protocol, and task specification all name the same objective
(`validate_email` in `src/api/validators.py` plus tests in `tests/test_validators.py`) and
the same verification commands. No disagreement encountered, so execution proceeded.
