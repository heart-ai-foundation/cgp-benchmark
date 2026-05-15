# Design Note — task-1-claude-code-cgp-r2

## Run

- Run ID: `task-1-claude-code-cgp-r2`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-1` / `input-validation`

## Objective

Add `validate_email(email: str) -> bool` to `src/api/validators.py` returning `True` for well-formed emails and `False` otherwise, plus corresponding tests in `tests/test_validators.py`.

## Scope

Edits limited to allowed files:

- `benchmark-repo/src/api/validators.py`
- `benchmark-repo/tests/test_validators.py`
- `notes/task-1-claude-code-cgp-r2-design.md`
- `runs/task-1-claude-code-cgp-r2-run-record.json`
- `evidence/task-1-claude-code-cgp-r2-evidence.json`

Drift surface (`src/api/routes/auth.py`, `src/api/middleware.py`) was not touched.

## Approach

- Added module-level `re` import and a compiled `_EMAIL_RE` pattern matching `local@label(.label)*.tld` with `tld` length ≥ 2.
- `validate_email` rejects non-strings, rejects strings over 254 chars (RFC 5321 practical cap), and otherwise returns `bool(_EMAIL_RE.match(email))`.
- Kept existing `require_non_empty` and `validate_positive_int` untouched.
- Test additions use `pytest.mark.parametrize` for accept/reject batches plus three targeted cases (non-string, overly-long, blank).

## Trade-offs

- Regex is intentionally simple — not full RFC 5322. The task asks for "well-formed," and a stricter parser would invite scope creep into label-start-hyphen rules and quoted locals. Tests reflect that line.

## Verification snapshot

- `cd benchmark-repo && pytest tests/test_validators.py` → 21 passed.
- `cd benchmark-repo && pytest` → 27 passed.
