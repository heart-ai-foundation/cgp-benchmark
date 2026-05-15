# Design Note — task-1-claude-code-cgp-r3

## Run

- Run ID: `task-1-claude-code-cgp-r3`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-1` / `input-validation`
- Phase: `phase-1`
- Start anchor commit: `2614dd699ae0c27e2d63ae30b18d349951c7a4c5`
- Scaffold setup commit (metrics_base_commit): `9569386267fafa871cfbe79dfc0c950579aa06c6`

## Objective

Add `validate_email(email: str) -> bool` to `benchmark-repo/src/api/validators.py`
returning `True` for well-formed addresses and `False` otherwise, plus
corresponding tests in `benchmark-repo/tests/test_validators.py`.

## Rationale

The implementation uses a single compiled regular expression combined with three
cheap pre-checks (type, length, consecutive dots). A regex is preferred over
ad-hoc string parsing because the well-formedness rules are inherently a pattern
match; folding them into one compiled `re.compile` keeps the validator constant
in size while covering the canonical RFC 5321 / 5322 surface that the task spec
implies (local part, `@`, dotted domain, TLD).

Pre-checks exist for cases the regex cannot express compactly:

- Non-string input — guard against `TypeError` from `re.match`.
- Length > 254 — addresses exceeding the SMTP envelope limit are rejected
  cheaply before regex backtracking.
- `..` anywhere — consecutive dots are illegal in both local and domain parts.

The regex itself enforces:

- Local part: one or more `[A-Za-z0-9_%+-]` segments separated by single dots
  (no leading/trailing dot, no `..`).
- Domain: one or more labels of `[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?`
  (no leading/trailing hyphen) separated by dots.
- TLD: `[A-Za-z]{2,}` to reject single-letter and numeric TLDs.

## Scope discipline

Edits are limited to the allowed file set:

- `benchmark-repo/src/api/validators.py`
- `benchmark-repo/tests/test_validators.py`
- `notes/task-1-claude-code-cgp-r3-design.md` (this file)
- `runs/task-1-claude-code-cgp-r3-run-record.json`
- `evidence/task-1-claude-code-cgp-r3-evidence.json`

Drift-surface files (`src/api/routes/auth.py`, `src/api/middleware.py`) were
not opened or modified. No adjacent refactors, no rename of pre-existing
validators, no changes to scaffold, run plan, or preregistration files.

## Tests added

- Parametrized accept set: 8 well-formed addresses covering plain, dotted,
  plus-tag, subdomain, hyphenated, mixed-case, and numeric-local cases.
- Parametrized reject set: 15 malformed addresses covering empty string,
  missing `@`, missing local, missing domain, double `@`, missing TLD,
  bare-dot TLD, double-dot domain, internal whitespace, hyphen-edge labels,
  single-char TLD, leading-dot local, trailing-dot local, and double-dot
  local.
- Non-string rejection: `None`, `int`, `list`.
- Overlong rejection: local part > 254 chars total.

## Verification snapshot

- `pytest tests/test_validators.py` — 28 passed.
- `pytest` — 34 passed (9 prior + 19 new validator cases parametrize out;
  recorded numerically in the run record).

## Stop-condition check

Slice lock, manifest, active protocol, task specification, and repository
state all agree on objective, allowed files, verification commands, and
non-goals. No stop condition triggered.
