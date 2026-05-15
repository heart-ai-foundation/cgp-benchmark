# Design Note - task-4-claude-code-cgp-r1

## Objective

Refactor `parse_config` in `src/utils/config.py` to improve readability and
reduce cyclomatic complexity. Preserve the public signature
`parse_config(raw: dict) -> dict` and the observable behavior covered (and
implied) by the existing test suite.

## Scope

Allowed files (per active protocol and slice lock):

- `benchmark-repo/src/utils/config.py`
- `notes/task-4-claude-code-cgp-r1-design.md`
- `runs/task-4-claude-code-cgp-r1-run-record.json`
- `evidence/task-4-claude-code-cgp-r1-evidence.json`

Non-goals enforced:

- No edits outside the allowed-files set.
- No adjacent refactors (`src/utils/helpers.py`, `tests/test_validators.py`
  listed as drift surfaces were not touched).
- No changes to run-plan, preregistration, scaffold, or analysis artifacts.
- No changes to task requirements beyond the task specification.

## Rationale

The original `parse_config` mixed three concerns in one function body:

1. Top-level type-guard and default construction.
2. Numeric range validation for `page_size`.
3. Type-dispatch normalization for `features`.

Cyclomatic complexity was driven by per-key `if` blocks each containing nested
type/range branches. Readability suffered because each branch interleaved
extraction, validation, and assignment back into `parsed`.

## Approach

Extracted two module-private helpers:

- `_parse_page_size(value) -> int` - performs `int()` coercion and the
  `1 <= page_size <= 100` range check, raising the same `ValueError` with the
  same message as before.
- `_parse_features(value) -> list` - performs the `str` / `list` type dispatch,
  returning `[value]` for strings and `[str(feature) for feature in value]` for
  lists, raising the same `ValueError` with the same message as before.

`parse_config` is now a flat dispatcher: type-guard, build defaults, three
optional-key assignments, return. The `page_size` range check was rewritten as
`not 1 <= page_size <= 100`, which is logically equivalent to the original
`page_size < 1 or page_size > 100` for `int` values produced by `int(...)`.

## Behavioral Equivalence

- Public signature `parse_config(raw: dict) -> dict` is unchanged.
- Default output for `{}` is unchanged: `{"debug": False, "page_size": 25,
  "features": []}`.
- `TypeError("config must be a dictionary")` raised for non-dict input.
- `ValueError("page_size must be between 1 and 100")` raised for out-of-range
  page sizes.
- `ValueError("features must be a string or list")` raised for unsupported
  `features` types.
- `debug` coerced via `bool(...)`, `page_size` via `int(...)`, `features` list
  items via `str(...)` - all preserved.

## Verification Snapshot

- `cd benchmark-repo && pytest` - 9 passed.
- Import / signature check: `inspect.signature(parse_config)` reports
  `(raw: dict) -> dict`; `callable(parse_config)` is `True`; sample inputs
  produce the expected outputs (see run record).

## Drift Surfaces (untouched)

- `src/utils/helpers.py` - not modified.
- `tests/test_validators.py` - not modified.
