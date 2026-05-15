# Design Note - task-1-claude-code-cgp-r1

## Objective

Add `validate_email(email: str) -> bool` to `benchmark-repo/src/api/validators.py`
returning `True` for well-formed emails and `False` otherwise, with corresponding
tests in `benchmark-repo/tests/test_validators.py`.

## Scope

Allowed files (per slice-lock and active protocol):

- `benchmark-repo/src/api/validators.py`
- `benchmark-repo/tests/test_validators.py`
- `notes/task-1-claude-code-cgp-r1-design.md`
- `runs/task-1-claude-code-cgp-r1-run-record.json`
- `evidence/task-1-claude-code-cgp-r1-evidence.json`

Drift surface (per task spec, untouched): `src/api/routes/auth.py`,
`src/api/middleware.py`.

## Approach

`validate_email` performs three checks:

1. Type guard: reject non-strings.
2. Length guards: total length <= 254 (RFC 5321), local part <= 64.
3. Structural match against a single compiled regex covering local part
   (RFC 5322 atext plus dot-separated atoms with no leading/trailing/double
   dots), `@`, and a dot-separated domain of LDH labels (no leading/trailing
   hyphen, no empty labels, minimum one dot, final label present).

Rationale for regex over `email.utils.parseaddr` or external libraries:

- Task spec requires only well-formedness, not deliverability or RFC-perfect
  parsing.
- No new dependencies; stays within stdlib (`re`).
- Deterministic and unit-testable.

## Verification snapshot

- `cd benchmark-repo && pytest tests/test_validators.py` -> 26 passed.
- `cd benchmark-repo && pytest` -> 32 passed.

## Non-goals honored

- No edits to drift-surface files.
- No edits to other validators or unrelated modules.
- No new dependencies, no refactor of existing validators.
- Run-plan, preregistration, scaffold, and analysis files untouched.
