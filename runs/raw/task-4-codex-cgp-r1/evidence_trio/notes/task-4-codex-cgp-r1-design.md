# Task 4 Design Note

Run ID: `task-4-codex-cgp-r1`

## Scope

Refactored `parse_config` in `benchmark-repo/src/utils/config.py` only. No drift-surface files were edited.

## Rationale

The original function mixed top-level configuration flow with field-specific parsing and validation. I extracted page-size and features parsing into small private helpers and moved default values into `DEFAULT_CONFIG`. The public `parse_config(raw: dict) -> dict` signature is unchanged, and the function now reads as:

1. validate the raw input type,
2. copy defaults,
3. apply optional parsed fields,
4. return the parsed config.

Behavior intentionally preserved:

- non-dict input raises `TypeError("config must be a dictionary")`;
- `debug` is converted with `bool`;
- `page_size` is converted with `int` before range validation;
- page-size bounds remain inclusive from 1 through 100;
- string `features` becomes a one-item list;
- list `features` entries are converted with `str`;
- other `features` values raise `ValueError("features must be a string or list")`.

## Verification Snapshot

- `cd benchmark-repo && pytest` passed with 9 tests.
- `cd benchmark-repo && python - <<'PY' ...` import/signature/behavior check passed, confirming `parse_config(raw: dict) -> dict` remains callable.
