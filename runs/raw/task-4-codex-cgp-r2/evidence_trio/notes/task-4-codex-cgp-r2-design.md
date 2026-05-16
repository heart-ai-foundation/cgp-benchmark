# Task 4 Design Note

Run ID: `task-4-codex-cgp-r2`

## Scope

Refactored `parse_config(raw: dict) -> dict` in `benchmark-repo/src/utils/config.py` only. Evidence artifacts were written to the run-specific allowed paths.

## Design

The original function combined default construction, type coercion, range validation, and feature normalization in one branching body. The refactor extracts field-specific parsing into private helpers and uses a parser registry to apply those helpers to present keys.

Behavior preserved:

- Non-dict input raises `TypeError("config must be a dictionary")`.
- Missing keys use `debug=False`, `page_size=25`, and `features=[]`.
- `debug` is coerced with `bool`.
- `page_size` is coerced with `int` and must remain in `[1, 100]`.
- `features` accepts a string as a one-item list or a list converted with `str(...)`; other types raise `ValueError("features must be a string or list")`.

## Verification Snapshot

- `cd benchmark-repo && pytest` passed: 9 tests passed.
- `cd benchmark-repo && python - <<'PY' ... PY` import/signature/behavior check passed.
